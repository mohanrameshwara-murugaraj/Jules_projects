# Automated Market Signal Pipeline

<!-- AUTO_DASHBOARD_START -->
## 📊 Latest Pipeline Dashboard (BTC-USD)

# Latest Market Signal: BTC-USD
**Generated on:** 2026-07-03 17:57:13 UTC

- **Signal:** `HOLD`
- **Latest Close:** $62157.42
- **Forecast Price (Next Day):** $63199.78
- **Expected Return:** 1.68%
- **Confidence Band:** $58043.95 - $68260.87


### Model Metrics (Train/Test Split)
- **MAE:** 5672.00
- **RMSE:** 5947.97
- **MAPE:** 9.19%

### Backtest Results (Historical MA Strategy vs B&H)
- **Strategy Return:** 21.83%
- **Market Return:** -2.19%
- **Win Rate:** 51.51%
- **Max Drawdown:** -32.60%

### Visualizations

![Signal Dashboard](reports/figures/signal_dashboard.png)

![Price History](reports/figures/price_history.png)

![Forecast](reports/figures/forecast.png)

![Backtest](reports/figures/backtest.png)

⚠️ **DISCLAIMER:** *This is a forecasting and signal research pipeline for educational and portfolio purposes only. It does NOT provide financial advice and is NOT a live trading bot.*

---

## About This Project

This project is an automated ML lifecycle pipeline for generating stock/crypto forecasting and signals. It fetches daily market data, engineers technical features, trains forecasting models, generates research signals (BUY/SELL/HOLD), and backtests historical performance.

### Why Prophet over LSTM?
For this specific GitHub Actions automated pipeline, **Prophet** was chosen over an LSTM model for several reasons:
- **Resource Constraints:** GitHub Actions free runners have limited CPU and no GPU. LSTMs are computationally heavy and slow to train on CPUs.
- **Reliability:** Prophet is more robust to outliers and missing data without extensive tuning, making it ideal for an automated, unattended daily run.
- **Interpretability:** Prophet provides clear trend and seasonality decomposition, plus uncertainty intervals, which is highly valuable for signal generation.

### How to Run Locally
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the pipeline for a specific ticker: `python src/run_pipeline.py --ticker BTC-USD`

### Limitations
- The model assumes past price patterns are predictive of future prices, which is notoriously difficult in financial markets.
- The current backtesting strategy is a simple moving average crossover, not a full walk-forward evaluation of the Prophet forecasts, to maintain fast automated daily runs.

### Future Improvements
- LSTM experiment branch
- MLflow/W&B tracking
- Telegram notification
- Streamlit dashboard
- Docker deployment


<!-- AUTO_DASHBOARD_END -->
