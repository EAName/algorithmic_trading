import json
import logging
import threading
import time
from datetime import datetime
from typing import Dict, List, Callable, Optional
import websocket
import pandas as pd
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

logger = logging.getLogger(__name__)

class AlpacaDataStream:
    """
    Real-time data streaming from Alpaca Markets WebSocket API
    """
    
    def __init__(self, config: Dict):
        """
        Initialize the Alpaca data stream
        
        Args:
            config: Configuration dictionary with Alpaca credentials
        """
        self.config = config
        self.api_key = config['alpaca']['api_key']
        self.secret_key = config['alpaca']['secret_key']
        self.base_url = config['alpaca']['base_url']
        self.symbols = config['trading']['symbols']
        self.data_callbacks = []
        self.ws = None
        self.is_connected = False
        self.data_buffer = {}
        
        # Initialize Alpaca clients
        self.trading_client = TradingClient(
            api_key=self.api_key,
            secret_key=self.secret_key,
            paper=config['alpaca'].get('paper_trading', True)
        )
        
        self.data_client = StockHistoricalDataClient(
            api_key=self.api_key,
            secret_key=self.secret_key
        )
        
        # Initialize data buffers for each symbol
        for symbol in self.symbols:
            self.data_buffer[symbol] = {
                'trades': [],
                'quotes': [],
                'bars': [],
                'latest_bar': None
            }
    
    def connect(self):
        """Connect to Alpaca WebSocket stream"""
        try:
            # Create WebSocket connection
            self.ws = websocket.WebSocketApp(
                f"{self.base_url}/v2/iex",
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            
            # Start WebSocket connection in a separate thread
            self.ws_thread = threading.Thread(target=self.ws.run_forever)
            self.ws_thread.daemon = True
            self.ws_thread.start()
            
            logger.info("WebSocket connection initiated")
            
        except Exception as e:
            logger.error(f"Error connecting to WebSocket: {e}")
            raise
    
    def _on_open(self, ws):
        """Handle WebSocket connection open"""
        logger.info("WebSocket connection opened")
        
        # Authenticate
        auth_message = {
            "action": "auth",
            "key": self.api_key,
            "secret": self.secret_key
        }
        ws.send(json.dumps(auth_message))
        
        # Subscribe to data channels
        subscribe_message = {
            "action": "subscribe",
            "trades": self.symbols,
            "quotes": self.symbols,
            "bars": self.symbols
        }
        ws.send(json.dumps(subscribe_message))
        
        logger.info(f"Subscribed to data for symbols: {self.symbols}")
    
    def _on_message(self, ws, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            
            # Handle authentication response
            if isinstance(data, list) and len(data) > 0:
                if data[0].get('T') == 'success':
                    if data[0].get('msg') == 'authenticated':
                        logger.info("Successfully authenticated with Alpaca")
                        self.is_connected = True
                    elif data[0].get('msg') == 'connected':
                        logger.info("Connected to Alpaca WebSocket")
                    elif data[0].get('msg') == 'subscription':
                        logger.info("Successfully subscribed to data feeds")
                    return
            
            # Handle market data messages
            if isinstance(data, list):
                for item in data:
                    self._process_market_data(item)
            
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON message: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def _process_market_data(self, data: Dict):
        """Process individual market data messages"""
        try:
            msg_type = data.get('T')
            symbol = data.get('S')
            
            if not symbol or symbol not in self.symbols:
                return
            
            if msg_type == 't':  # Trade
                self._process_trade(data, symbol)
            elif msg_type == 'q':  # Quote
                self._process_quote(data, symbol)
            elif msg_type == 'b':  # Bar
                self._process_bar(data, symbol)
                
        except Exception as e:
            logger.error(f"Error processing market data: {e}")
    
    def _process_trade(self, data: Dict, symbol: str):
        """Process trade data"""
        trade = {
            'symbol': symbol,
            'price': data.get('p'),
            'size': data.get('s'),
            'timestamp': data.get('t'),
            'exchange': data.get('x'),
            'conditions': data.get('c', [])
        }
        
        self.data_buffer[symbol]['trades'].append(trade)
        
        # Keep only recent trades (last 100)
        if len(self.data_buffer[symbol]['trades']) > 100:
            self.data_buffer[symbol]['trades'] = self.data_buffer[symbol]['trades'][-100:]
        
        # Notify callbacks
        self._notify_callbacks('trade', trade)
    
    def _process_quote(self, data: Dict, symbol: str):
        """Process quote data"""
        quote = {
            'symbol': symbol,
            'bid_price': data.get('bp'),
            'bid_size': data.get('bs'),
            'ask_price': data.get('ap'),
            'ask_size': data.get('as'),
            'timestamp': data.get('t'),
            'bid_exchange': data.get('bx'),
            'ask_exchange': data.get('ax')
        }
        
        self.data_buffer[symbol]['quotes'].append(quote)
        
        # Keep only recent quotes (last 100)
        if len(self.data_buffer[symbol]['quotes']) > 100:
            self.data_buffer[symbol]['quotes'] = self.data_buffer[symbol]['quotes'][-100:]
        
        # Notify callbacks
        self._notify_callbacks('quote', quote)
    
    def _process_bar(self, data: Dict, symbol: str):
        """Process bar data"""
        bar = {
            'symbol': symbol,
            'open': data.get('o'),
            'high': data.get('h'),
            'low': data.get('l'),
            'close': data.get('c'),
            'volume': data.get('v'),
            'vwap': data.get('vw'),
            'timestamp': data.get('t')
        }
        
        self.data_buffer[symbol]['bars'].append(bar)
        self.data_buffer[symbol]['latest_bar'] = bar
        
        # Keep only recent bars (last 50)
        if len(self.data_buffer[symbol]['bars']) > 50:
            self.data_buffer[symbol]['bars'] = self.data_buffer[symbol]['bars'][-50:]
        
        # Notify callbacks
        self._notify_callbacks('bar', bar)
    
    def _notify_callbacks(self, data_type: str, data: Dict):
        """Notify registered callbacks with new data"""
        for callback in self.data_callbacks:
            try:
                callback(data_type, data)
            except Exception as e:
                logger.error(f"Error in data callback: {e}")
    
    def _on_error(self, ws, error):
        """Handle WebSocket errors"""
        logger.error(f"WebSocket error: {error}")
        self.is_connected = False
    
    def _on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket connection close"""
        logger.info("WebSocket connection closed")
        self.is_connected = False
    
    def add_data_callback(self, callback: Callable):
        """Add a callback function to be called when new data arrives"""
        self.data_callbacks.append(callback)
    
    def get_latest_data(self, symbol: str) -> Dict:
        """Get the latest data for a specific symbol"""
        if symbol not in self.data_buffer:
            return {}
        
        buffer = self.data_buffer[symbol]
        return {
            'latest_trade': buffer['trades'][-1] if buffer['trades'] else None,
            'latest_quote': buffer['quotes'][-1] if buffer['quotes'] else None,
            'latest_bar': buffer['latest_bar'],
            'recent_trades': buffer['trades'][-10:] if buffer['trades'] else [],
            'recent_quotes': buffer['quotes'][-10:] if buffer['quotes'] else []
        }
    
    def get_historical_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Get historical data for a symbol"""
        try:
            request_params = StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=TimeFrame.Minute,
                start=start_date,
                end=end_date
            )
            
            bars = self.data_client.get_stock_bars(request_params)
            
            if bars and symbol in bars:
                df = bars[symbol].df
                df.reset_index(inplace=True)
                df.rename(columns={'timestamp': 'timestamp'}, inplace=True)
                return df
            else:
                logger.warning(f"No historical data found for {symbol}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            return pd.DataFrame()
    
    def disconnect(self):
        """Disconnect from WebSocket"""
        if self.ws:
            self.ws.close()
        self.is_connected = False
        logger.info("Disconnected from Alpaca WebSocket")
    
    def is_streaming(self) -> bool:
        """Check if the stream is currently active"""
        return self.is_connected and self.ws and self.ws.sock 