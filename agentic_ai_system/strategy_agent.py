import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, Optional, List
from .agent_base import Agent

class StrategyAgent(Agent):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.symbols = config['trading']['symbols']
        self.primary_symbol = config['trading']['primary_symbol']
        self.capital = config['trading']['capital']
        self.max_position = config['risk']['max_position']
        self.max_drawdown = config['risk']['max_drawdown']
        self.data_buffers = {symbol: [] for symbol in self.symbols}
        self.logger.info(f"Strategy agent initialized for symbols {self.symbols} with capital {self.capital}")
    
    def act(self, data: pd.DataFrame, symbol: str = None) -> Dict[str, Any]:
        """
        Analyze market data and generate trading signals.
        
        Args:
            data: DataFrame with OHLCV market data
            symbol: Symbol to analyze (if None, uses primary symbol)
            
        Returns:
            Dictionary containing trading signal
        """
        try:
            if symbol is None:
                symbol = self.primary_symbol
            
            self.logger.info(f"Analyzing {len(data)} data points for {symbol}")
            
            # Validate data
            if data.empty:
                self.logger.warning(f"Empty data received for {symbol}")
                return self._generate_no_action_signal(symbol)
            
            # Calculate technical indicators
            indicators = self._calculate_indicators(data)
            
            # Generate trading signal
            signal = self._generate_signal(data, indicators, symbol)
            
            # Log the signal
            self.log_action(signal)
            
            return signal
            
        except Exception as e:
            self.log_error(e, f"Error in strategy analysis for {symbol}")
            return self._generate_no_action_signal(symbol)
    
    def process_realtime_data(self, data_type: str, data: Dict):
        """
        Process real-time data updates
        
        Args:
            data_type: Type of data ('trade', 'quote', 'bar')
            data: Data dictionary
        """
        try:
            symbol = data.get('symbol')
            if symbol not in self.symbols:
                return
            
            # Store data in buffer
            self.data_buffers[symbol].append({
                'type': data_type,
                'data': data,
                'timestamp': data.get('timestamp')
            })
            
            # Keep only recent data
            max_buffer_size = 100
            if len(self.data_buffers[symbol]) > max_buffer_size:
                self.data_buffers[symbol] = self.data_buffers[symbol][-max_buffer_size:]
            
            # If we have enough bar data, analyze it
            if data_type == 'bar' and len(self.data_buffers[symbol]) >= 20:
                self._analyze_realtime_data(symbol)
                
        except Exception as e:
            self.log_error(e, f"Error processing real-time data for {symbol}")
    
    def _analyze_realtime_data(self, symbol: str):
        """Analyze real-time data and generate signals"""
        try:
            # Convert buffer data to DataFrame format
            bar_data = [item['data'] for item in self.data_buffers[symbol] 
                       if item['type'] == 'bar']
            
            if len(bar_data) < 20:
                return
            
            # Create DataFrame from bar data
            df = pd.DataFrame(bar_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
            
            # Generate signal
            signal = self.act(df, symbol)
            
            if signal['action'] != 'hold':
                self.logger.info(f"Real-time signal for {symbol}: {signal['action']} {signal['quantity']} @ {signal['price']}")
                
        except Exception as e:
            self.log_error(e, f"Error analyzing real-time data for {symbol}")
    
    def _calculate_indicators(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate technical indicators from market data"""
        try:
            close_prices = data['close'].values
            
            # Simple Moving Averages
            sma_20 = self._calculate_sma(close_prices, 20)
            sma_50 = self._calculate_sma(close_prices, 50)
            
            # RSI
            rsi = self._calculate_rsi(close_prices, 14)
            
            # Bollinger Bands
            bb_upper, bb_lower = self._calculate_bollinger_bands(close_prices, 20, 2)
            
            # MACD
            macd, signal_line = self._calculate_macd(close_prices)
            
            indicators = {
                'sma_20': sma_20,
                'sma_50': sma_50,
                'rsi': rsi,
                'bb_upper': bb_upper,
                'bb_lower': bb_lower,
                'macd': macd,
                'macd_signal': signal_line
            }
            
            self.logger.debug(f"Calculated indicators: {list(indicators.keys())}")
            return indicators
            
        except Exception as e:
            self.log_error(e, "Error calculating indicators")
            return {}
    
    def _generate_signal(self, data: pd.DataFrame, indicators: Dict[str, Any], symbol: str) -> Dict[str, Any]:
        """Generate trading signal based on indicators"""
        try:
            if not indicators:
                return self._generate_no_action_signal(symbol)
            
            current_price = data['close'].iloc[-1]
            current_volume = data['volume'].iloc[-1]
            
            # Get latest indicator values
            sma_20 = indicators['sma_20'][-1] if len(indicators['sma_20']) > 0 else current_price
            sma_50 = indicators['sma_50'][-1] if len(indicators['sma_50']) > 0 else current_price
            rsi = indicators['rsi'][-1] if len(indicators['rsi']) > 0 else 50
            bb_upper = indicators['bb_upper'][-1] if len(indicators['bb_upper']) > 0 else current_price * 1.02
            bb_lower = indicators['bb_lower'][-1] if len(indicators['bb_lower']) > 0 else current_price * 0.98
            
            # Simple strategy: Buy when price is above SMA20 and RSI < 70
            # Sell when price is below SMA20 or RSI > 80
            action = 'hold'
            quantity = 0
            confidence = 0.5
            
            if current_price > sma_20 and rsi < 70:
                action = 'buy'
                quantity = self._calculate_position_size(current_price)
                confidence = 0.7
                self.logger.info(f"BUY signal for {symbol}: Price {current_price} > SMA20 {sma_20}, RSI {rsi}")
                
            elif current_price < sma_20 or rsi > 80:
                action = 'sell'
                quantity = self._calculate_position_size(current_price)
                confidence = 0.6
                self.logger.info(f"SELL signal for {symbol}: Price {current_price} < SMA20 {sma_20}, RSI {rsi}")
            
            return {
                'action': action,
                'symbol': symbol,
                'quantity': quantity,
                'price': current_price,
                'confidence': confidence,
                'timestamp': data.index[-1] if hasattr(data.index[-1], 'timestamp') else None,
                'indicators': {
                    'sma_20': sma_20,
                    'sma_50': sma_50,
                    'rsi': rsi,
                    'bb_upper': bb_upper,
                    'bb_lower': bb_lower
                }
            }
            
        except Exception as e:
            self.log_error(e, f"Error generating signal for {symbol}")
            return self._generate_no_action_signal(symbol)
    
    def _calculate_position_size(self, price: float) -> int:
        """Calculate position size based on risk management rules"""
        try:
            # Simple position sizing: use 10% of capital per trade
            position_value = self.capital * 0.1
            quantity = int(position_value / price)
            
            # Apply max position limit
            quantity = min(quantity, self.max_position)
            
            # Ensure minimum quantity
            if quantity < 1:
                quantity = 1
                
            return quantity
            
        except Exception as e:
            self.log_error(e, "Error calculating position size")
            return 1
    
    def _generate_no_action_signal(self, symbol: str) -> Dict[str, Any]:
        """Generate a no-action signal"""
        return {
            'action': 'hold',
            'symbol': symbol,
            'quantity': 0,
            'price': 0,
            'confidence': 0.0,
            'timestamp': None,
            'indicators': {}
        }
    
    # Technical indicator calculations
    def _calculate_sma(self, prices: np.ndarray, window: int) -> np.ndarray:
        """Calculate Simple Moving Average"""
        if len(prices) < window:
            return np.array([])
        return np.convolve(prices, np.ones(window)/window, mode='valid')
    
    def _calculate_rsi(self, prices: np.ndarray, window: int = 14) -> np.ndarray:
        """Calculate Relative Strength Index"""
        if len(prices) < window + 1:
            return np.array([])
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gains = np.convolve(gains, np.ones(window)/window, mode='valid')
        avg_losses = np.convolve(losses, np.ones(window)/window, mode='valid')
        
        rs = avg_gains / (avg_losses + 1e-10)  # Avoid division by zero
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def _calculate_bollinger_bands(self, prices: np.ndarray, window: int = 20, std_dev: float = 2) -> tuple:
        """Calculate Bollinger Bands"""
        if len(prices) < window:
            return np.array([]), np.array([])
        
        sma = self._calculate_sma(prices, window)
        if len(sma) == 0:
            return np.array([]), np.array([])
        
        # Calculate rolling standard deviation
        std = np.array([np.std(prices[i:i+window]) for i in range(len(prices) - window + 1)])
        
        upper_band = sma + (std_dev * std)
        lower_band = sma - (std_dev * std)
        
        return upper_band, lower_band
    
    def _calculate_macd(self, prices: np.ndarray, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        if len(prices) < slow:
            return np.array([]), np.array([])
        
        ema_fast = self._calculate_ema(prices, fast)
        ema_slow = self._calculate_ema(prices, slow)
        
        if len(ema_fast) == 0 or len(ema_slow) == 0:
            return np.array([]), np.array([])
        
        # Align lengths
        min_len = min(len(ema_fast), len(ema_slow))
        ema_fast = ema_fast[-min_len:]
        ema_slow = ema_slow[-min_len:]
        
        macd_line = ema_fast - ema_slow
        signal_line = self._calculate_ema(macd_line, signal)
        
        return macd_line, signal_line
    
    def _calculate_ema(self, prices: np.ndarray, window: int) -> np.ndarray:
        """Calculate Exponential Moving Average"""
        if len(prices) < window:
            return np.array([])
        
        alpha = 2 / (window + 1)
        ema = np.zeros(len(prices))
        ema[0] = prices[0]
        
        for i in range(1, len(prices)):
            ema[i] = alpha * prices[i] + (1 - alpha) * ema[i-1]
        
        return ema[window-1:]  # Return only the valid EMA values
