---
tags:
- finance
- code
---
# Algorithmic Trading System

A comprehensive algorithmic trading system with synthetic data generation, comprehensive logging, and extensive testing capabilities.

## Features

### Core Trading System
- **Agent-based Architecture**: Modular design with separate strategy and execution agents
- **Technical Analysis**: Built-in technical indicators (SMA, RSI, Bollinger Bands, MACD)
- **Risk Management**: Position sizing and drawdown limits
- **Order Execution**: Simulated broker integration with realistic execution delays

### Synthetic Data Generation
- **Realistic Market Data**: Generate OHLCV data using geometric Brownian motion
- **Multiple Frequencies**: Support for 1min, 5min, 1H, and 1D data
- **Market Scenarios**: Normal, volatile, trending, and crash market conditions
- **Tick Data**: High-frequency tick data generation for testing
- **Configurable Parameters**: Volatility, trend, noise levels, and base prices

### Comprehensive Logging
- **Multi-level Logging**: Console and file-based logging
- **Rotating Log Files**: Automatic log rotation with size limits
- **Specialized Loggers**: Separate loggers for trading, performance, and errors
- **Structured Logging**: Detailed log messages with timestamps and context

### Testing Framework
- **Unit Tests**: Comprehensive tests for all components
- **Integration Tests**: End-to-end workflow testing
- **Test Coverage**: Code coverage reporting with HTML and XML outputs
- **Mock Testing**: Isolated testing with mocked dependencies

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd algorithmic_trading
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The system is configured via `config.yaml`:

```yaml
# Data source configuration
data_source:
  type: 'synthetic'  # or 'csv'
  path: 'data/market_data.csv'

# Trading parameters
trading:
  symbol: 'AAPL'
  timeframe: '1min'
  capital: 100000

# Risk management
risk:
  max_position: 100
  max_drawdown: 0.05

# Order execution
execution:
  broker_api: 'paper'
  order_size: 10
  delay_ms: 100
  success_rate: 0.95

# Synthetic data generation
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

## Usage

### Standard Trading Mode
```bash
python -m agentic_ai_system.main
```

### Backtest Mode
```bash
python -m agentic_ai_system.main --mode backtest --start-date 2024-01-01 --end-date 2024-12-31
```

### Live Trading Mode
```bash
python -m agentic_ai_system.main --mode live --duration 60
```

### Custom Configuration
```bash
python -m agentic_ai_system.main --config custom_config.yaml
```

## Running Tests

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
pytest --cov=agentic_ai_system --cov-report=html
```

### Specific Test File
```bash
pytest tests/test_synthetic_data_generator.py
```

## System Architecture

### Components

1. **SyntheticDataGenerator**: Generates realistic market data for testing
2. **DataIngestion**: Loads and validates market data from various sources
3. **StrategyAgent**: Analyzes market data and generates trading signals
4. **ExecutionAgent**: Executes trading orders with broker simulation
5. **Orchestrator**: Coordinates the entire trading workflow
6. **LoggerConfig**: Manages comprehensive logging throughout the system

### Data Flow

```
Synthetic Data Generator → Data Ingestion → Strategy Agent → Execution Agent
                              ↓
                         Logging System
```

## Synthetic Data Generation

### Features
- **Geometric Brownian Motion**: Realistic price movement simulation
- **OHLCV Data**: Complete market data with open, high, low, close, and volume
- **Market Scenarios**: Different market conditions for testing
- **Configurable Parameters**: Adjustable volatility, trend, and noise levels

### Usage Examples

```python
from agentic_ai_system.synthetic_data_generator import SyntheticDataGenerator

# Initialize generator
generator = SyntheticDataGenerator(config)

# Generate OHLCV data
data = generator.generate_ohlcv_data(
    symbol='AAPL',
    start_date='2024-01-01',
    end_date='2024-12-31',
    frequency='1min'
)

# Generate tick data
tick_data = generator.generate_tick_data(
    symbol='AAPL',
    duration_minutes=60,
    tick_interval_ms=1000
)

# Generate market scenarios
crash_data = generator.generate_market_scenarios('crash')
volatile_data = generator.generate_market_scenarios('volatile')
```

## Logging System

### Log Files
- `logs/trading_system.log`: General system logs
- `logs/trading.log`: Trading-specific logs
- `logs/performance.log`: Performance metrics
- `logs/errors.log`: Error logs

### Log Levels
- **DEBUG**: Detailed debugging information
- **INFO**: General information about system operation
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failed operations
- **CRITICAL**: Critical system failures

### Usage Examples

```python
import logging
from agentic_ai_system.logger_config import setup_logging, get_logger

# Setup logging
setup_logging(config)

# Get logger for specific module
logger = get_logger(__name__)

# Log messages
logger.info("Trading signal generated")
logger.warning("High volatility detected")
logger.error("Order execution failed", exc_info=True)
```

## Testing

### Test Structure
```
tests/
├── __init__.py
├── test_synthetic_data_generator.py
├── test_strategy_agent.py
├── test_execution_agent.py
├── test_data_ingestion.py
└── test_integration.py
```

### Test Categories
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test complete workflows
- **Performance Tests**: Test system performance and scalability
- **Error Handling Tests**: Test error conditions and edge cases

### Running Specific Tests

```bash
# Run tests with specific markers
pytest -m unit
pytest -m integration
pytest -m slow

# Run tests with coverage
pytest --cov=agentic_ai_system --cov-report=html

# Run tests in parallel
pytest -n auto

# Run tests with verbose output
pytest -v
```

## Performance Monitoring

The system includes comprehensive performance monitoring:

- **Execution Time Tracking**: Monitor workflow execution times
- **Trade Statistics**: Track successful vs failed trades
- **Performance Metrics**: Calculate returns and drawdowns
- **Resource Usage**: Monitor memory and CPU usage

## Error Handling

The system includes robust error handling:

- **Graceful Degradation**: System continues operation despite component failures
- **Error Logging**: Comprehensive error logging with stack traces
- **Fallback Mechanisms**: Automatic fallback to synthetic data when CSV files are missing
- **Validation**: Data validation at multiple levels

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

### License
This project is dual-licensed.

• NON-COMMERCIAL USE → PolyForm Noncommercial License 1.0.0  
  # PolyForm Noncommercial License 1.0.0
<https://polyformproject.org/licenses/noncommercial/1.0.0>

## Acceptance
In order to get any license under these terms, you must agree to them as
both strict obligations and conditions to all your licenses.

## Copyright License
The licensor grants you a copyright license for the software to do
everything you might do with the software that would otherwise infringe
the licensor's copyright in it for any permitted purpose. However, you
may only distribute the software according to **Distribution License**
and make changes or new works based on the software according to
**Changes and New Works License**.

## Distribution License
The licensor grants you an additional copyright license to distribute
copies of the software. Your license to distribute covers distributing
the software with changes and new works permitted by **Changes and New
Works License**.

## Notices
You must ensure that anyone who gets a copy of any part of the software
from you also gets a copy of these terms or the URL for them above, as
well as copies of any plain-text lines beginning with `Required Notice:`
that the licensor provided with the software. For example:

> Required Notice: Copyright Yoyodyne, Inc.

## Changes and New Works License
The licensor grants you an additional copyright license to make changes
and new works based on the software for any permitted purpose.

## Patent License
The licensor grants you a patent license for the software that covers
patent claims the licensor can license, or becomes able to license, that
you would infringe by using the software.

## Noncommercial Purposes
Any noncommercial purpose is a permitted purpose.

## Personal Uses
Personal use for research, experiment, and testing for the benefit of
public knowledge, personal study, private entertainment, hobby projects,
amateur pursuits, or religious observance, without any anticipated
commercial application, is use for a permitted purpose.

## Noncommercial Organizations
Use by any charitable organization, educational institution, public
research organization, public safety or health organization,
environmental protection organization, or government institution is use
for a permitted purpose regardless of the source of funding or
obligations resulting from the funding.

## Fair Use
You may have “fair use” rights for the software under the law. These
terms do not limit them.

## No Other Rights
These terms do not allow you to sublicense or transfer any of your
licenses to anyone else, or prevent the licensor from granting licenses
to anyone else. These terms do not imply any other licenses.

## Patent Defense
If you make any written claim that the software infringes or contributes
to infringement of any patent, your patent license for the software
granted under these terms ends immediately. If your company makes such a
claim, your patent license ends immediately for work on behalf of your
company.

## Violations
The first time you are notified in writing that you have violated any of
these terms, or done anything with the software not covered by your
licenses, your licenses can nonetheless continue if you come into full
compliance with these terms, and take practical steps to correct past
violations, within 32 days of receiving notice. Otherwise, all your
licenses end immediately.

## No Liability
**As far as the law allows, the software comes as-is, without any
warranty or condition, and the licensor will not be liable to you for
any damages arising out of these terms or the use or nature of the
software, under any kind of legal claim.**

## Definitions
The **licensor** is the individual or entity offering these terms, and
the **software** is the software the licensor makes available under
these terms. **You** refers to the individual or entity agreeing to
these terms. **Your company** is any legal entity, sole proprietorship,
or other kind of organization that you work for, plus all organizations
that have control over, are under the control of, or are under common
control with that organization. **Control** means ownership of
substantially all the assets of an entity, or the power to direct its
management and policies by vote, contract, or otherwise. Control can be
direct or indirect. **Your licenses** are all the licenses granted to
you for the software under these terms. **Use** means anything you do
with the software requiring one of your licenses.

• COMMERCIAL USE → Parallel LLC Commercial License v1.0  
  Parallel LLC Commercial License v1.0
====================================

IMPORTANT—READ CAREFULLY.  This Commercial License (“Agreement”) is a
legal contract between Parallel LLC (“Licensor”) and the licensee
identified in the Order Form or invoice (“Licensee”).  By installing,
copying, accessing, or otherwise using the Software, Licensee agrees to
be bound by this Agreement.

1.  Definitions
    1.1 “Software” means the source code, object code, scripts, models,
         and all accompanying documentation found in this repository.
    1.2 “Authorized Users” means Licensee’s employees or contractors who
         are bound by written agreement to terms no less protective of
         Licensor’s rights than this Agreement.
    1.3 “Derivative Work” has the meaning set forth in 17 U.S.C. § 101.

2.  Grant of License
    2.1 **Production Use.**  Subject to payment of all applicable fees,
         Licensor grants Licensee a worldwide, non-exclusive,
         non-transferable license to (a) use, reproduce, and modify the
         Software, and (b) distribute the Software and Derivative Works
         as part of Licensee’s products or services, including
         software-as-a-service (SaaS).
    2.2 **Sublicensing.**  Licensee may sublicense distribution rights
         under Section 2.1(b) to its end customers solely in executable
         form and only pursuant to terms at least as protective of
         Licensor as this Agreement.
    2.3 **Reservation of Rights.**  All rights not expressly granted are
         reserved by Licensor.

3.  Fees & Payment
    3.1 License fees are specified in the Order Form and are due within
         thirty (30) days of invoice.  Late payments accrue interest at
         1.5 % per month or the maximum allowed by law, whichever is
         less.

4.  Support & Updates
    4.1 Licensor will provide commercially reasonable support during the
         term purchased.  Updates are provided at Licensor’s discretion
         and are governed by this Agreement unless accompanied by a new
         license.

5.  Confidentiality
    5.1 The Software and any non-public documentation are “Confidential
         Information.”  Licensee will not disclose Confidential
         Information except to Authorized Users and will protect it with
         at least the same care used for its own secrets.

6.  Intellectual-Property Protection
    6.1 Licensee shall not remove or alter any copyright, trademark, or
         proprietary notices.
    6.2 Licensee shall defend, indemnify, and hold harmless Licensor
         from any claim arising out of Licensee’s use or distribution of
         the Software.

7.  Warranty Disclaimer
    7.1 THE SOFTWARE IS PROVIDED “AS IS” WITHOUT WARRANTY OF ANY KIND,
         EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION THE IMPLIED
         WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
         PURPOSE, AND NON-INFRINGEMENT.

8.  Limitation of Liability
    8.1 LICENSOR WILL NOT BE LIABLE FOR ANY INDIRECT, SPECIAL,
         INCIDENTAL, OR CONSEQUENTIAL DAMAGES, OR LOST PROFITS, ARISING
         OUT OF OR RELATED TO THIS AGREEMENT, EVEN IF ADVISED OF THE
         POSSIBILITY OF SUCH DAMAGES.  LICENSOR’S TOTAL LIABILITY SHALL
         NOT EXCEED THE FEES PAID BY LICENSEE IN THE TWELVE (12) MONTHS
         PRECEDING THE CLAIM.

9.  Term & Termination
    9.1 This Agreement begins on the Effective Date and continues for
         the term stated in the Order Form unless terminated earlier.
    9.2 Either party may terminate for material breach after thirty (30)
         days’ written notice if the breach is not cured.
    9.3 Upon termination, all rights granted to Licensee cease, and
         Licensee must destroy all copies of the Software in its
         possession.

10. Governing Law & Dispute Resolution
    10.1 This Agreement is governed by the laws of the Commonwealth of
          Virginia, U.S.A., without regard to conflict-of-law rules.
    10.2 Any dispute shall be resolved by binding arbitration in
          Fairfax County, Virginia, under the Commercial Arbitration
          Rules of the American Arbitration Association.

11. Entire Agreement; Amendments
    11.1 This Agreement, together with any Order Form, constitutes the
          complete and exclusive understanding between the parties and
          supersedes all prior proposals and agreements.  Any amendment
          must be in writing and signed by both parties.

© 2025 Parallel LLC.  All rights reserved.  
  To obtain a paid commercial license, e-mail <edwinsalguero@parallelLLC.com>.

© 2025 Parallel LLC
---