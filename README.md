# Algorithmic Trading System

A comprehensive, production-ready algorithmic trading system with real-time market data streaming, multi-symbol trading, advanced technical analysis, and robust risk management capabilities.

## 🚀 Features

### Core Trading System
- **Agent-based Architecture**: Modular design with separate strategy and execution agents
- **Real-time Data Streaming**: Live market data from Alpaca Markets WebSocket API
- **Multi-Symbol Trading**: Support for multiple symbols (AAPL, META, AMZN, GOOG, NFLX)
- **Advanced Technical Analysis**: Built-in technical indicators (SMA, RSI, Bollinger Bands, MACD, EMA)
- **Risk Management**: Position sizing, drawdown limits, and portfolio management
- **Order Execution**: Real Alpaca trading API integration with paper trading support
- **Performance Monitoring**: Real-time performance tracking and analytics

### Real-time Market Data
- **Alpaca Markets Integration**: Live WebSocket streaming for real-time data
- **Multiple Data Types**: Trades, quotes, and bars (OHLCV) data
- **Historical Data**: Access to historical market data for backtesting
- **Paper Trading**: Safe testing environment with paper trading accounts
- **Live Trading**: Production-ready live trading capabilities
- **Auto-reconnection**: Robust connection handling with automatic reconnection

### Synthetic Data Generation
- **Realistic Market Data**: Generate OHLCV data using geometric Brownian motion
- **Multiple Frequencies**: Support for 1min, 5min, 1H, and 1D data
- **Market Scenarios**: Normal, volatile, trending, and crash market conditions
- **Tick Data**: High-frequency tick data generation for testing
- **Configurable Parameters**: Volatility, trend, noise levels, and base prices
- **Data Validation**: Comprehensive data quality checks and validation

### Comprehensive Logging & Monitoring
- **Multi-level Logging**: Console and file-based logging with rotation
- **Specialized Loggers**: Separate loggers for trading, performance, and errors
- **Structured Logging**: Detailed log messages with timestamps and context
- **Performance Metrics**: Real-time performance tracking and reporting
- **Error Handling**: Robust error handling and recovery mechanisms

### Testing Framework
- **Unit Tests**: Comprehensive tests for all components (84 total tests)
- **Integration Tests**: End-to-end workflow testing
- **Test Coverage**: Code coverage reporting with HTML and XML outputs
- **Mock Testing**: Isolated testing with mocked dependencies
- **Data Validation Tests**: Extensive data quality and validation testing

## 📁 Directory Structure

```
algorithmic_trading/
├── agentic_ai_system/           # Core trading system modules
│   ├── __init__.py
│   ├── agent_base.py           # Base agent class with common functionality
│   ├── data_ingestion.py       # Data loading and validation
│   ├── execution_agent.py      # Order execution and management
│   ├── logger_config.py        # Logging configuration and setup
│   ├── main.py                 # Main application entry point
│   ├── orchestrator.py         # System orchestration and workflow
│   ├── real_time_data_stream.py # Alpaca WebSocket data streaming
│   ├── strategy_agent.py       # Trading strategy and signal generation
│   └── synthetic_data_generator.py # Synthetic market data generation
├── data/                       # Data storage directory
│   └── synthetic_market_data.csv # Generated synthetic data
├── logs/                       # Log files directory
│   ├── errors.log             # Error logs
│   ├── performance.log        # Performance metrics
│   ├── trading_system.log     # Main system logs
│   └── trading.log            # Trading activity logs
├── tests/                      # Comprehensive test suite
│   ├── __init__.py
│   ├── test_data_ingestion.py # Data ingestion and validation tests
│   ├── test_execution_agent.py # Execution agent tests
│   ├── test_integration.py    # Integration and workflow tests
│   ├── test_real_time_data_stream.py # Real-time data tests
│   ├── test_strategy_agent.py # Strategy agent tests
│   └── test_synthetic_data_generator.py # Synthetic data tests
├── config.yaml                 # Main configuration file
├── demo.py                     # Standard trading demo
├── demo_realtime.py            # Real-time trading demo
├── LICENSE                     # Dual-license file
├── pytest.ini                 # Pytest configuration
├── README.md                   # This file
└── requirements.txt            # Python dependencies
```

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/ParallelLLC/algorithmic_trading
cd algorithmic_trading
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up Alpaca Markets account (for real-time trading):**
   - Sign up at [Alpaca Markets](https://alpaca.markets/)
   - Get your API key and secret from the dashboard
   - Update `config.yaml` with your credentials

## ⚙️ Configuration

The system is configured via `config.yaml`:

```yaml
# Data source configuration
data_source:
  type: 'realtime'  # Options: 'csv', 'synthetic', 'realtime'
  path: 'data/market_data.csv'

# Alpaca Markets configuration
alpaca:
  api_key: 'YOUR_ALPACA_API_KEY'
  secret_key: 'YOUR_ALPACA_SECRET_KEY'
  base_url: 'wss://stream.data.alpaca.markets'
  paper_trading: true  # Set to false for live trading

# Trading parameters
trading:
  symbols: ['AAPL', 'META', 'AMZN', 'GOOG', 'NFLX']
  primary_symbol: 'AAPL'
  timeframe: '1min'
  capital: 100000

# Real-time data configuration
realtime_data:
  start_date: '2024-01-01'
  end_date: '2024-12-31'
  buffer_size: 100
  auto_reconnect: true
  reconnect_delay: 5

# Risk management
risk:
  max_position: 100
  max_drawdown: 0.05

# Order execution
execution:
  broker_api: 'alpaca'  # Options: 'alpaca', 'simulation'
  order_size: 10
  delay_ms: 10
  success_rate: 1.0

# Synthetic data generation (fallback)
synthetic_data:
  base_price: 150.0
  volatility: 0.02
  trend: 0.001
  noise_level: 0.005
  generate_data: true
  data_path: 'data/synthetic_market_data.csv'

# Logging configuration
logging:
  log_level: 'INFO'
  log_dir: 'logs'
  enable_console: true
  enable_file: true
  max_file_size_mb: 10
  backup_count: 5
```

## 🚀 Usage

### Real-time Trading Demo
```bash
python demo_realtime.py
```

### Standard Trading Mode
```bash
python -m agentic_ai_system.main
```

### Backtest Mode
```bash
python -m agentic_ai_system.main --mode backtest --start-date 2024-01-01 --end-date 2024-12-31
```

### Real-time Trading Mode
```bash
python -m agentic_ai_system.main --mode realtime --duration 60
```

### Custom Configuration
```bash
python -m agentic_ai_system.main --config custom_config.yaml
```

## 📊 Real-time Trading Setup

### 1. Alpaca Markets Account
- Sign up for a free account at [Alpaca Markets](https://alpaca.markets/)
- Complete account verification
- Get your API key and secret from the dashboard

### 2. Update Configuration
Edit `config.yaml` and replace the placeholder credentials:
```yaml
alpaca:
  api_key: 'your_actual_api_key_here'
  secret_key: 'your_actual_secret_key_here'
  paper_trading: true  # Start with paper trading
```

### 3. Test Connection
Run the demo to test your setup:
```bash
python demo_realtime.py
```

### 4. Paper Trading vs Live Trading
- **Paper Trading** (`paper_trading: true`): Safe testing environment with virtual money
- **Live Trading** (`paper_trading: false`): Real money trading (use with caution!)

## 🧪 Running Tests

### All Tests
```bash
pytest
```

### Unit Tests Only
```bash
pytest -m unit
```

### Integration Tests Only
```bash
pytest -m integration
```

### With Coverage Report
```bash
pytest --cov=agentic_ai_system --cov-report=html --cov-report=xml
```

### Specific Test Categories
```bash
# Data ingestion tests
pytest tests/test_data_ingestion.py

# Strategy agent tests
pytest tests/test_strategy_agent.py

# Execution agent tests
pytest tests/test_execution_agent.py

# Integration tests
pytest tests/test_integration.py
```

## 🔧 System Architecture

### Agent-based Design
- **Strategy Agent**: Analyzes market data and generates trading signals
- **Execution Agent**: Executes orders and manages positions
- **Data Ingestion**: Handles data loading and validation
- **Orchestrator**: Coordinates system workflow and manages state

### Real-time Data Flow
1. **Data Streaming**: Alpaca WebSocket API provides real-time market data
2. **Data Processing**: Real-time data is processed and stored in buffers
3. **Signal Generation**: Strategy agent analyzes data and generates signals
4. **Order Execution**: Execution agent processes signals and places orders
5. **Performance Tracking**: System monitors performance and logs activities

### Risk Management
- **Position Sizing**: Dynamic position sizing based on capital and risk parameters
- **Drawdown Limits**: Maximum drawdown protection
- **Order Validation**: Comprehensive order validation before execution
- **Error Handling**: Robust error handling and recovery mechanisms

## 📈 Performance Features

### Technical Indicators
- **Simple Moving Average (SMA)**: 20 and 50-period SMAs
- **Relative Strength Index (RSI)**: 14-period RSI with overbought/oversold levels
- **Bollinger Bands**: 20-period with 2 standard deviations
- **MACD**: 12/26/9 MACD with signal line
- **Exponential Moving Average (EMA)**: Configurable periods

### Trading Strategies
- **Trend Following**: Buy when price > SMA20 and RSI < 70
- **Mean Reversion**: Sell when price < SMA20 or RSI > 80
- **Risk Management**: Position sizing based on capital and volatility
- **Multi-timeframe Analysis**: Support for different timeframes

## 🔒 Security & Safety

### Paper Trading First
- Always start with paper trading to test strategies
- Validate system behavior before live trading
- Monitor performance and adjust parameters

### Risk Controls
- Maximum position limits
- Drawdown protection
- Order size validation
- Error handling and recovery

### Data Validation
- Comprehensive data quality checks
- OHLCV relationship validation
- Null value detection
- Price and volume validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is dual-licensed.

### • NON-COMMERCIAL USE → PolyForm Noncommercial License 1.0.0

**PolyForm Noncommercial License 1.0.0**

https://polyformproject.org/licenses/noncommercial/1.0.0

**Acceptance**

In order to get any license under these terms, you must agree to them as both strict obligations and conditions to all your licenses.

**Copyright License**

The licensor grants you a copyright license for the software to do everything you might do with the software that would otherwise infringe the licensor's copyright in it for any permitted purpose. However, you may only distribute the software according to Distribution License and make changes or new works based on the software according to Changes and New Works License.

**Distribution License**

The licensor grants you an additional copyright license to distribute copies of the software. Your license to distribute covers distributing the software with changes and new works permitted by Changes and New Works License.

**Notices**

You must ensure that anyone who gets a copy of any part of the software from you also gets a copy of these terms or the URL for them above, as well as copies of any plain-text lines beginning with Required Notice: that the licensor provided with the software. For example:

Required Notice: Copyright Yoyodyne, Inc.

**Changes and New Works License**

The licensor grants you an additional copyright license to make changes and new works based on the software for any permitted purpose.

**Patent License**

The licensor grants you a patent license for the software that covers patent claims the licensor can license, or becomes able to license, that you would infringe by using the software.

**Noncommercial Purposes**

Any noncommercial purpose is a permitted purpose.

**Personal Uses**

Personal use for research, experiment, and testing for the benefit of public knowledge, personal study, private entertainment, hobby projects, amateur pursuits, or religious observance, without any anticipated commercial application, is use for a permitted purpose.

**Noncommercial Organizations**

Use by any charitable organization, educational institution, public research organization, public safety or health organization, environmental protection organization, or government institution is use for a permitted purpose regardless of the source of funding or obligations resulting from the funding.

**Fair Use**

You may have "fair use" rights for the software under the law. These terms do not limit them.

**No Other Rights**

These terms do not allow you to sublicense or transfer any of your licenses to anyone else, or prevent the licensor from granting licenses to anyone else. These terms do not imply any other licenses.

**Patent Defense**

If you make any written claim that the software infringes or contributes to infringement of any patent, your patent license for the software granted under these terms ends immediately. If your company makes such a claim, your patent license ends immediately for work on behalf of your company.

**Violations**

The first time you are notified in writing that you have violated any of these terms, or done anything with the software not covered by your licenses, your licenses can nonetheless continue if you come into full compliance with these terms, and take practical steps to correct past violations, within 32 days of receiving notice. Otherwise, all your licenses end immediately.

**No Liability**

As far as the law allows, the software comes as-is, without any warranty or condition, and the licensor will not be liable to you for any damages arising out of these terms or the use or nature of the software, under any kind of legal claim.

**Definitions**

The licensor is the individual or entity offering these terms, and the software is the software the licensor makes available under these terms. You refers to the individual or entity agreeing to these terms. Your company is any legal entity, sole proprietorship, or other kind of organization that you work for, plus all organizations that have control over, are under the control of, or are under common control with that organization. Control means ownership of substantially all the assets of an entity, or the power to direct its management and policies by vote, contract, or otherwise. Control can be direct or indirect. Your licenses are all the licenses granted to you for the software under these terms. Use means anything you do with the software requiring one of your licenses.

### • COMMERCIAL USE → Parallel LLC Commercial License v1.0

**Parallel LLC Commercial License v1.0**

IMPORTANT—READ CAREFULLY. This Commercial License ("Agreement") is a legal contract between Parallel LLC ("Licensor") and the licensee identified in the Order Form or invoice ("Licensee"). By installing, copying, accessing, or otherwise using the Software, Licensee agrees to be bound by this Agreement.

**Definitions**

1.1 "Software" means the source code, object code, scripts, models, and all accompanying documentation found in this repository.

1.2 "Authorized Users" means Licensee's employees or contractors who are bound by written agreement to terms no less protective of Licensor's rights than this Agreement.

1.3 "Derivative Work" has the meaning set forth in 17 U.S.C. § 101.

**Grant of License**

2.1 Production Use. Subject to payment of all applicable fees, Licensor grants Licensee a worldwide, non-exclusive, non-transferable license to (a) use, reproduce, and modify the Software, and (b) distribute the Software and Derivative Works as part of Licensee's products or services, including software-as-a-service (SaaS).

2.2 Sublicensing. Licensee may sublicense distribution rights under Section 2.1(b) to its end customers solely in executable form and only pursuant to terms at least as protective of Licensor as this Agreement.

2.3 Reservation of Rights. All rights not expressly granted are reserved by Licensor.

**Fees & Payment**

3.1 License fees are specified in the Order Form and are due within thirty (30) days of invoice. Late payments accrue interest at 1.5% per month or the maximum allowed by law, whichever is less.

**Support & Updates**

4.1 Licensor will provide commercially reasonable support during the term purchased. Updates are provided at Licensor's discretion and are governed by this Agreement unless accompanied by a new license.

**Confidentiality**

5.1 The Software and any non-public documentation are "Confidential Information." Licensee will not disclose Confidential Information except to Authorized Users and will protect it with at least the same care used for its own secrets.

**Intellectual-Property Protection**

6.1 Licensee shall not remove or alter any copyright, trademark, or proprietary notices.

6.2 Licensee shall defend, indemnify, and hold harmless Licensor from any claim arising out of Licensee's use or distribution of the Software.

**Warranty Disclaimer**

7.1 THE SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

**Limitation of Liability**

8.1 LICENSOR WILL NOT BE LIABLE FOR ANY INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, OR LOST PROFITS, ARISING OUT OF OR RELATED TO THIS AGREEMENT, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. LICENSOR'S TOTAL LIABILITY SHALL NOT EXCEED THE FEES PAID BY LICENSEE IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM.

**Term & Termination**

9.1 This Agreement begins on the Effective Date and continues for the term stated in the Order Form unless terminated earlier.

9.2 Either party may terminate for material breach after thirty (30) days' written notice if the breach is not cured.

9.3 Upon termination, all rights granted to Licensee cease, and Licensee must destroy all copies of the Software in its possession.

**Governing Law & Dispute Resolution**

10.1 This Agreement is governed by the laws of the Commonwealth of Virginia, U.S.A., without regard to conflict-of-law rules.

10.2 Any dispute shall be resolved by binding arbitration in Fairfax County, Virginia, under the Commercial Arbitration Rules of the American Arbitration Association.

**Entire Agreement; Amendments**

11.1 This Agreement, together with any Order Form, constitutes the complete and exclusive understanding between the parties and supersedes all prior proposals and agreements. Any amendment must be in writing and signed by both parties.

**© 2025 Parallel LLC. All rights reserved.**

To obtain a paid commercial license, e-mail edwinsalguero@parallelLLC.com.

---

**© 2025 Parallel LLC**
