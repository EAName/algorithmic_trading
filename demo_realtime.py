#!/usr/bin/env python3
"""
Real-time Trading Demo with Alpaca Markets

This script demonstrates the real-time trading capabilities of the agentic AI system
using live market data from Alpaca Markets for AAPL, META, AMZN, GOOG, and NFLX.

Before running:
1. Sign up for an Alpaca Markets account at https://alpaca.markets/
2. Get your API key and secret from the Alpaca dashboard
3. Update the config.yaml file with your credentials
4. Install required dependencies: pip install -r requirements.txt
"""

import yaml
import logging
import time
from datetime import datetime
from agentic_ai_system.orchestrator import run_realtime_trading, run_backtest
from agentic_ai_system.logger_config import setup_logging

def load_config():
    """Load configuration from YAML file"""
    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

def check_alpaca_credentials(config):
    """Check if Alpaca credentials are properly configured"""
    if not config:
        return False
    
    api_key = config.get('alpaca', {}).get('api_key')
    secret_key = config.get('alpaca', {}).get('secret_key')
    
    if api_key == 'YOUR_ALPACA_API_KEY' or secret_key == 'YOUR_ALPACA_SECRET_KEY':
        print("⚠️  Please update your Alpaca API credentials in config.yaml")
        print("   Get your credentials from: https://alpaca.markets/")
        return False
    
    return True

def demo_realtime_trading():
    """Demonstrate real-time trading"""
    print("🚀 Starting Real-time Trading Demo")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    if not config:
        print("❌ Failed to load configuration")
        return
    
    # Check Alpaca credentials
    if not check_alpaca_credentials(config):
        print("❌ Alpaca credentials not configured")
        return
    
    # Setup logging
    setup_logging(config)
    logger = logging.getLogger(__name__)
    
    print(f"📊 Trading symbols: {config['trading']['symbols']}")
    print(f"💰 Initial capital: ${config['trading']['capital']:,}")
    print(f"📈 Timeframe: {config['trading']['timeframe']}")
    print(f"🔧 Broker: {config['execution']['broker_api']}")
    print(f"🧪 Paper trading: {config['alpaca']['paper_trading']}")
    print()
    
    try:
        # Run real-time trading for 5 minutes
        print("⏱️  Starting real-time trading for 5 minutes...")
        print("   Press Ctrl+C to stop early")
        print()
        
        results = run_realtime_trading(config, duration_minutes=5)
        
        if results['success']:
            print("✅ Real-time trading completed successfully!")
            print(f"📈 Total trades: {results['total_trades']}")
            print(f"⏱️  Duration: {results['duration_minutes']} minutes")
        else:
            print(f"❌ Real-time trading failed: {results.get('error', 'Unknown error')}")
            
    except KeyboardInterrupt:
        print("\n⏹️  Trading stopped by user")
    except Exception as e:
        print(f"❌ Error during real-time trading: {e}")
        logger.error(f"Real-time trading error: {e}", exc_info=True)

def demo_backtest():
    """Demonstrate backtesting with historical data"""
    print("📈 Starting Backtest Demo")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    if not config:
        print("❌ Failed to load configuration")
        return
    
    # Setup logging
    setup_logging(config)
    logger = logging.getLogger(__name__)
    
    try:
        print("🔄 Running backtest with historical data...")
        
        # Run backtest for the last 30 days
        from datetime import datetime, timedelta
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        results = run_backtest(config, start_date=start_date, end_date=end_date)
        
        if results['success']:
            print("✅ Backtest completed successfully!")
            print(f"📊 Period: {start_date} to {end_date}")
            print(f"💰 Initial capital: ${results['initial_capital']:,}")
            print(f"💰 Final value: ${results['final_value']:,.2f}")
            print(f"📈 Total return: {results['total_return']:.2%}")
            print(f"🔄 Total trades: {results['total_trades']}")
        else:
            print(f"❌ Backtest failed: {results.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error during backtest: {e}")
        logger.error(f"Backtest error: {e}", exc_info=True)

def main():
    """Main demo function"""
    print("🤖 Agentic AI Trading System - Real-time Demo")
    print("=" * 60)
    print()
    
    while True:
        print("Choose a demo option:")
        print("1. Real-time Trading (requires Alpaca credentials)")
        print("2. Backtest with Historical Data")
        print("3. Exit")
        print()
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            print()
            demo_realtime_trading()
        elif choice == '2':
            print()
            demo_backtest()
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
        
        print()
        input("Press Enter to continue...")
        print()

if __name__ == "__main__":
    main() 