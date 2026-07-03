import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
METRICS_DIR = REPORTS_DIR / "metrics"

# Ensure directories exist
for d in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, FIGURES_DIR, METRICS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Data Fetching Config
DEFAULT_TICKER = "BTC-USD"
FALLBACK_TICKERS = ["AAPL", "MSFT", "ETH-USD"]
PERIOD = "2y"
INTERVAL = "1d"

# Modeling Config
FORECAST_HORIZON = 7  # days

# Signal Engine Config
BUY_THRESHOLD = 0.02   # +2% expected return
SELL_THRESHOLD = -0.02 # -2% expected return
