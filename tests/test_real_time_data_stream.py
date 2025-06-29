import pytest
import yaml
import time
from unittest.mock import Mock, patch
from agentic_ai_system.real_time_data_stream import AlpacaDataStream

@pytest.fixture
def mock_config():
    """Mock configuration for testing"""
    return {
        'alpaca': {
            'api_key': 'test_api_key',
            'secret_key': 'test_secret_key',
            'base_url': 'wss://stream.data.sandbox.alpaca.markets',
            'paper_trading': True
        },
        'trading': {
            'symbols': ['AAPL', 'META', 'AMZN', 'GOOG', 'NFLX']
        }
    }

class TestAlpacaDataStream:
    """Test cases for AlpacaDataStream class"""
    
    def test_initialization(self, mock_config):
        """Test AlpacaDataStream initialization"""
        with patch('alpaca.trading.client.TradingClient'), \
             patch('alpaca.data.StockHistoricalDataClient'):
            
            stream = AlpacaDataStream(mock_config)
            
            assert stream.api_key == 'test_api_key'
            assert stream.secret_key == 'test_secret_key'
            assert stream.base_url == 'wss://stream.data.sandbox.alpaca.markets'
            assert stream.symbols == ['AAPL', 'META', 'AMZN', 'GOOG', 'NFLX']
            assert len(stream.data_buffer) == 5
            assert 'AAPL' in stream.data_buffer
            assert 'META' in stream.data_buffer
    
    def test_data_buffer_initialization(self, mock_config):
        """Test data buffer initialization for all symbols"""
        with patch('alpaca.trading.client.TradingClient'), \
             patch('alpaca.data.StockHistoricalDataClient'):
            
            stream = AlpacaDataStream(mock_config)
            
            for symbol in mock_config['trading']['symbols']:
                assert symbol in stream.data_buffer
                assert 'trades' in stream.data_buffer[symbol]
                assert 'quotes' in stream.data_buffer[symbol]
                assert 'bars' in stream.data_buffer[symbol]
                assert 'latest_bar' in stream.data_buffer[symbol]
                assert stream.data_buffer[symbol]['latest_bar'] is None
    
    def test_process_trade_data(self, mock_config):
        """Test processing trade data"""
        with patch('alpaca.trading.client.TradingClient'), \
             patch('alpaca.data.StockHistoricalDataClient'):
            
            stream = AlpacaDataStream(mock_config)
            
            # Mock trade data
            trade_data = {
                'T': 't',
                'S': 'AAPL',
                'i': 12345,
                'x': 'NASDAQ',
                'p': 150.25,
                's': 100,
                't': '2024-01-01T10:30:00Z',
                'c': ['@', 'I'],
                'z': 'C'
            }
            
            stream._process_market_data(trade_data)
            
            assert len(stream.data_buffer['AAPL']['trades']) == 1
            trade = stream.data_buffer['AAPL']['trades'][0]
            assert trade['symbol'] == 'AAPL'
            assert trade['price'] == 150.25
            assert trade['size'] == 100
            assert trade['exchange'] == 'NASDAQ'
    
    def test_process_quote_data(self, mock_config):
        """Test processing quote data"""
        with patch('alpaca.trading.client.TradingClient'), \
             patch('alpaca.data.StockHistoricalDataClient'):
            
            stream = AlpacaDataStream(mock_config)
            
            # Mock quote data
            quote_data = {
                'T': 'q',
                'S': 'META',
                'bx': 'NASDAQ',
                'bp': 350.20,
                'bs': 500,
                'ax': 'NASDAQ',
                'ap': 350.30,
                'as': 300,
                't': '2024-01-01T10:30:00Z',
                'c': ['R'],
                'z': 'C'
            }
            
            stream._process_market_data(quote_data)
            
            assert len(stream.data_buffer['META']['quotes']) == 1
            quote = stream.data_buffer['META']['quotes'][0]
            assert quote['symbol'] == 'META'
            assert quote['bid_price'] == 350.20
            assert quote['ask_price'] == 350.30
            assert quote['bid_size'] == 500
            assert quote['ask_size'] == 300
    
    def test_process_bar_data(self, mock_config):
        """Test processing bar data"""
        with patch('alpaca.trading.client.TradingClient'), \
             patch('alpaca.data.StockHistoricalDataClient'):
            
            stream = AlpacaDataStream(mock_config)
            
            # Mock bar data
            bar_data = {
                'T': 'b',
                'S': 'AMZN',
                'o': 150.00,
                'h': 150.50,
                'l': 149.80,
                'c': 150.25,
                'v': 1000000,
                'vw': 150.15,
                't': '2024-01-01T10:30:00Z',
                'z': 'C'
            }
            
            stream._process_market_data(bar_data)
            
            assert len(stream.data_buffer['AMZN']['bars']) == 1
            bar = stream.data_buffer['AMZN']['bars'][0]
            assert bar['symbol'] == 'AMZN'
            assert bar['open'] == 150.00
            assert bar['high'] == 150.50
            assert bar['low'] == 149.80
            assert bar['close'] == 150.25
            assert bar['volume'] == 1000000
            
            # Check latest_bar is updated
            assert stream.data_buffer['AMZN']['latest_bar'] == bar
    
    def test_data_buffer_limits(self, mock_config):
        """Test data buffer size limits"""
        with patch('alpaca.trading.client.TradingClient'), \
             patch('alpaca.data.StockHistoricalDataClient'):
            
            stream = AlpacaDataStream(mock_config)
            
            # Add more than 100 trades
            for i in range(110):
                trade_data = {
                    'T': 't',
                    'S': 'AAPL',
                    'i': i,
                    'x': 'NASDAQ',
                    'p': 150.0 + i * 0.01,
                    's': 100,
                    't': '2024-01-01T10:30:00Z',
                    'c': ['@'],
                    'z': 'C'
                }
                stream._process_market_data(trade_data)
            
            # Should only keep last 100 trades
            assert len(stream.data_buffer['AAPL']['trades']) == 100
            assert stream.data_buffer['AAPL']['trades'][-1]['price'] == 151.09  # 150.0 + 109 * 0.01
    
    def test_get_latest_data(self, mock_config):
        """Test getting latest data for a symbol"""
        with patch('alpaca.trading.client.TradingClient'), \
             patch('alpaca.data.StockHistoricalDataClient'):
            
            stream = AlpacaDataStream(mock_config)
            
            # Add some test data
            trade_data = {
                'T': 't',
                'S': 'GOOG',
                'i': 12345,
                'x': 'NASDAQ',
                'p': 2500.00,
                's': 50,
                't': '2024-01-01T10:30:00Z',
                'c': ['@'],
                'z': 'C'
            }
            stream._process_market_data(trade_data)
            
            latest_data = stream.get_latest_data('GOOG')
            
            assert 'latest_trade' in latest_data
            assert 'latest_quote' in latest_data
            assert 'latest_bar' in latest_data
            assert 'recent_trades' in latest_data
            assert 'recent_quotes' in latest_data
            
            assert latest_data['latest_trade']['price'] == 2500.00
            assert len(latest_data['recent_trades']) == 1
    
    def test_get_latest_data_empty_buffer(self, mock_config):
        """Test getting latest data when buffer is empty"""
        with patch('alpaca.trading.client.TradingClient'), \
             patch('alpaca.data.StockHistoricalDataClient'):
            
            stream = AlpacaDataStream(mock_config)
            
            latest_data = stream.get_latest_data('NFLX')
            
            assert latest_data['latest_trade'] is None
            assert latest_data['latest_quote'] is None
            assert latest_data['latest_bar'] is None
            assert latest_data['recent_trades'] == []
            assert latest_data['recent_quotes'] == []
    
    def test_add_data_callback(self, mock_config):
        """Test adding data callback"""
        with patch('alpaca.trading.client.TradingClient'), \
             patch('alpaca.data.StockHistoricalDataClient'):
            
            stream = AlpacaDataStream(mock_config)
            
            # Mock callback function
            callback_called = False
            callback_data = None
            
            def test_callback(data_type, data):
                nonlocal callback_called, callback_data
                callback_called = True
                callback_data = (data_type, data)
            
            stream.add_data_callback(test_callback)
            
            # Process some data
            trade_data = {
                'T': 't',
                'S': 'AAPL',
                'i': 12345,
                'x': 'NASDAQ',
                'p': 150.25,
                's': 100,
                't': '2024-01-01T10:30:00Z',
                'c': ['@'],
                'z': 'C'
            }
            
            stream._process_market_data(trade_data)
            
            # Check if callback was called
            assert callback_called
            assert callback_data[0] == 'trade'
            assert callback_data[1]['symbol'] == 'AAPL'
            assert callback_data[1]['price'] == 150.25
    
    def test_ignore_unknown_symbol(self, mock_config):
        """Test that unknown symbols are ignored"""
        with patch('alpaca.trading.client.TradingClient'), \
             patch('alpaca.data.StockHistoricalDataClient'):
            
            stream = AlpacaDataStream(mock_config)
            
            # Try to process data for unknown symbol
            trade_data = {
                'T': 't',
                'S': 'UNKNOWN',
                'i': 12345,
                'x': 'NASDAQ',
                'p': 150.25,
                's': 100,
                't': '2024-01-01T10:30:00Z',
                'c': ['@'],
                'z': 'C'
            }
            
            stream._process_market_data(trade_data)
            
            # Should not be added to any buffer
            for symbol in mock_config['trading']['symbols']:
                assert len(stream.data_buffer[symbol]['trades']) == 0
    
    def test_ignore_unknown_message_type(self, mock_config):
        """Test that unknown message types are ignored"""
        with patch('alpaca.trading.client.TradingClient'), \
             patch('alpaca.data.StockHistoricalDataClient'):
            
            stream = AlpacaDataStream(mock_config)
            
            # Try to process unknown message type
            unknown_data = {
                'T': 'x',  # Unknown type
                'S': 'AAPL',
                'data': 'some data'
            }
            
            stream._process_market_data(unknown_data)
            
            # Should not be added to any buffer
            assert len(stream.data_buffer['AAPL']['trades']) == 0
            assert len(stream.data_buffer['AAPL']['quotes']) == 0
            assert len(stream.data_buffer['AAPL']['bars']) == 0 