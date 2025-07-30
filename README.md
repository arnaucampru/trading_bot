# IBKR Trading Bot (Flask)

This is a Flask-based web dashboard to schedule and execute trading operations using the Interactive Brokers (IBKR) API.

## ✅ What it currently does

- Web dashboard to add new operations (symbol, size, direction, entry/exit time, stop loss, take profit)
- Operations are stored in a local database
- Scheduler runs in background and sends orders to IBKR at the programmed entry time
- Bracket orders are created using stop loss and take profit

## ⚠️ What needs to be fixed

- Orders are **not being reliably sent to IBKR** at the scheduled time
- There might be some misconfiguration or logic error in the scheduler or connection to IBKR
- No need to build new features or strategy logic — just ensure the existing system works correctly

## 🔧 Technologies

- Python 3
- Flask
- IBKR TWS API (via ib_insync)
- SQLite (via SQLAlchemy)

## 🚀 Getting started

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python run.py
