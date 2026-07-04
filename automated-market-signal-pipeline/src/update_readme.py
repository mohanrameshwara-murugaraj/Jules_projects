import re
import json
import logging
from src.config import BASE_DIR, METRICS_DIR, REPORTS_DIR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_readme(ticker: str):
    """Update the README.md with the latest signal and metrics."""
    readme_path = BASE_DIR / "README.md"
    signal_path = REPORTS_DIR / "latest_signal.md"
    metrics_path = METRICS_DIR / f"{ticker}_metrics.json"
    backtest_path = METRICS_DIR / "backtest_results.json"

    if not readme_path.exists():
        logging.warning("README.md not found. A new one will be created.")
        with open(readme_path, 'w') as f:
            f.write("# Automated Market Signal Pipeline\n\n<!-- AUTO_DASHBOARD_START -->\n<!-- AUTO_DASHBOARD_END -->\n")

    # Read current README
    with open(readme_path, 'r') as f:
        readme_content = f.read()

    # Prepare Dashboard Content
    dashboard_content = f"## 📊 Latest Pipeline Dashboard ({ticker})\n\n"

    if signal_path.exists():
        with open(signal_path, 'r') as f:
            dashboard_content += f.read() + "\n\n"

    dashboard_content += "### Model Metrics (Train/Test Split)\n"
    if metrics_path.exists():
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
        dashboard_content += f"- **MAE:** {metrics.get('MAE', 0):.2f}\n"
        dashboard_content += f"- **RMSE:** {metrics.get('RMSE', 0):.2f}\n"
        dashboard_content += f"- **MAPE:** {metrics.get('MAPE', 0):.2f}%\n\n"

    dashboard_content += "### Backtest Results (Historical MA Strategy vs B&H)\n"
    if backtest_path.exists():
        with open(backtest_path, 'r') as f:
            bt_metrics = json.load(f)
        dashboard_content += f"- **Strategy Return:** {bt_metrics.get('total_strategy_return_pct', 0):.2f}%\n"
        dashboard_content += f"- **Market Return:** {bt_metrics.get('total_market_return_pct', 0):.2f}%\n"
        dashboard_content += f"- **Win Rate:** {bt_metrics.get('win_rate_pct', 0):.2f}%\n"
        dashboard_content += f"- **Max Drawdown:** {bt_metrics.get('max_drawdown_pct', 0):.2f}%\n\n"

    dashboard_content += "### Visualizations\n\n"
    dashboard_content += "![Signal Dashboard](reports/figures/signal_dashboard.png)\n\n"
    dashboard_content += "![Price History](reports/figures/price_history.png)\n\n"
    dashboard_content += "![Forecast](reports/figures/forecast.png)\n\n"
    dashboard_content += "![Backtest](reports/figures/backtest.png)\n\n"

    dashboard_content += "⚠️ **DISCLAIMER:** *This is a forecasting and signal research pipeline for educational and portfolio purposes only. It does NOT provide financial advice and is NOT a live trading bot.*\n\n"

    dashboard_content += "---\n\n"
    dashboard_content += "## About This Project\n\n"
    dashboard_content += "This project is an automated ML lifecycle pipeline for generating stock/crypto forecasting and signals. It fetches daily market data, engineers technical features, trains forecasting models, generates research signals (BUY/SELL/HOLD), and backtests historical performance.\n\n"

    dashboard_content += "### Why Prophet over LSTM?\n"
    dashboard_content += "For this specific GitHub Actions automated pipeline, **Prophet** was chosen over an LSTM model for several reasons:\n"
    dashboard_content += "- **Resource Constraints:** GitHub Actions free runners have limited CPU and no GPU. LSTMs are computationally heavy and slow to train on CPUs.\n"
    dashboard_content += "- **Reliability:** Prophet is more robust to outliers and missing data without extensive tuning, making it ideal for an automated, unattended daily run.\n"
    dashboard_content += "- **Interpretability:** Prophet provides clear trend and seasonality decomposition, plus uncertainty intervals, which is highly valuable for signal generation.\n\n"

    dashboard_content += "### How to Run Locally\n"
    dashboard_content += "1. Clone the repository.\n"
    dashboard_content += "2. Install dependencies: `pip install -r requirements.txt`\n"
    dashboard_content += "3. Run the pipeline for a specific ticker: `python src/run_pipeline.py --ticker BTC-USD`\n\n"

    dashboard_content += "### Limitations\n"
    dashboard_content += "- The model assumes past price patterns are predictive of future prices, which is notoriously difficult in financial markets.\n"
    dashboard_content += "- The current backtesting strategy is a simple moving average crossover, not a full walk-forward evaluation of the Prophet forecasts, to maintain fast automated daily runs.\n\n"

    dashboard_content += "### Future Improvements\n"
    dashboard_content += "- LSTM experiment branch\n"
    dashboard_content += "- MLflow/W&B tracking\n"
    dashboard_content += "- Telegram notification\n"
    dashboard_content += "- Streamlit dashboard\n"
    dashboard_content += "- Docker deployment\n\n"

    # Replace content between markers
    pattern = r"(<!-- AUTO_DASHBOARD_START -->).*?(<!-- AUTO_DASHBOARD_END -->)"
    replacement = rf"\1\n{dashboard_content}\n\2"

    new_readme_content = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)

    # Add markers if not present
    if new_readme_content == readme_content and "<!-- AUTO_DASHBOARD_START -->" not in readme_content:
        new_readme_content += f"\n\n<!-- AUTO_DASHBOARD_START -->\n{dashboard_content}\n<!-- AUTO_DASHBOARD_END -->"

    with open(readme_path, 'w') as f:
        f.write(new_readme_content)

    logging.info("README.md updated with latest dashboard.")

if __name__ == "__main__":
    from src.config import DEFAULT_TICKER
    update_readme(DEFAULT_TICKER)
