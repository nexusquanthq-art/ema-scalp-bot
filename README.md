# EMA Scalp Strategy Bot

Professional crypto scalping bot using EMA pullback strategy with institutional-grade risk management.

## Strategy Logic

### Bullish Setup (Long)
1. EMA 20 > EMA 50 (uptrend confirmed)
2. Price pulls back to EMA 20
3. Bullish candle closes above EMA 20
4. Volume ratio > 0.8 (above average volume)
5. Entry at candle close

### Bearish Setup (Short)
1. EMA 20 < EMA 50 (downtrend confirmed)
2. Price pulls back to EMA 20
3. Bearish candle closes below EMA 20
4. Volume ratio > 0.8 (above average volume)
5. Entry at candle close

## Risk Management

- **ATR-based stop loss** - Dynamic stops based on market volatility
- **1:2 Risk/Reward ratio** - Professional standard
- **Position sizing** - Calculated from account balance and risk percentage
- **Configurable leverage** - Adjustable per account
- **Max open trades limit** - Prevents overtrading

## Kill Switch Protection

The bot includes a safety system that:
- Tracks consecutive losses
- Bans trading after 3 consecutive losses (60 minute cooldown)
- Limits trades to 5 per hour
- Tracks total win rate
- Auto-resets after cooldown expires

## Auto Withdraw

- Automatically withdraws profits to your wallet
- Configurable percentage
- Minimum profit threshold
- Supports multiple networks

## Multi-Account Support

- Connect multiple exchange accounts
- Manage all accounts from one bot
- Per-account trade limits
- Testnet support for testing

## Project Structure

```
core/
├── __init__.py          - Path setup
├── strategy_scalp.py    - EMA pullback strategy
├── risk.py              - Position sizing calculator
├── kill_switch.py       - Safety system
├── executor.py          - Trade execution engine
├── exchange.py          - Multi-exchange connection manager
├── data.py              - OHLCV data fetcher
└── auto_withdraw.py     - Automatic profit withdrawal
```

## Installation

```bash
pip install ccxt pandas numpy
```

## Dependencies

- `ccxt` - Exchange connectivity
- `pandas` - Data manipulation
- `numpy` - Numerical calculations

## Configuration

The bot requires a `config/` folder with:
- `settings.py` - Trading parameters
- `accounts.py` - Exchange API keys

**Note:** Configuration files are not included in this repository.

For full setup, configuration, and optimization:
Contact: **Telegram @Nexushqh**

## Features

- EMA 20/50 pullback detection
- ATR-based dynamic stop losses
- Volume confirmation filter
- Automatic position sizing
- Kill switch safety system
- Auto profit withdrawal
- Multi-exchange support
- Testnet mode for testing
- Comprehensive logging

## Disclaimer

This bot is for educational purposes only. It does not constitute financial advice. Trading cryptocurrency involves significant risk. Only trade with capital you can afford to lose. Past performance does not guarantee future results.

## License

All Rights Reserved - See LICENSE file

## Author

**Nexus**
- Telegram: @Nexushqh
