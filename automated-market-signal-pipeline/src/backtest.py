import pandas as pd
import numpy as np
import json
import logging
from src.config import PROCESSED_DATA_DIR, METRICS_DIR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_backtest(ticker: str):
    """Simple backtest comparing moving average crossover vs Buy and Hold."""
    # Since walk-forward Prophet is very slow for daily automated runs,
    # we'll do a simple moving average crossover backtest to demonstrate evaluation structure.

    features_path = PROCESSED_DATA_DIR / f"{ticker}_features.csv"
    if not features_path.exists():
        logging.error(f"Features not found for {ticker}")
        return

    df = pd.read_csv(features_path)
    if len(df) < 22:
         logging.warning("Not enough data for backtest.")
         return

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)

    # Simple Strategy: Buy when MA_7 > MA_21, Sell when MA_7 < MA_21
    df['Signal'] = 0
    df.loc[df['MA_7'] > df['MA_21'], 'Signal'] = 1

    # Calculate Strategy Returns (shift signal by 1 to prevent lookahead bias)
    df['Strategy_Return'] = df['Signal'].shift(1) * df['Returns']
    df['Strategy_Return'] = df['Strategy_Return'].fillna(0)

    # Cumulative Returns
    df['Cum_Market_Return'] = (1 + df['Returns']).cumprod()
    df['Cum_Strategy_Return'] = (1 + df['Strategy_Return']).cumprod()

    # Metrics
    total_market_return = df['Cum_Market_Return'].iloc[-1] - 1
    total_strategy_return = df['Cum_Strategy_Return'].iloc[-1] - 1

    # Win rate (percentage of positive return days when invested)
    invested_days = df[df['Signal'].shift(1) == 1]
    win_rate = (invested_days['Strategy_Return'] > 0).mean() if not invested_days.empty else 0

    # Max Drawdown for Strategy
    rolling_max = df['Cum_Strategy_Return'].cummax()
    drawdown = df['Cum_Strategy_Return'] / rolling_max - 1
    max_drawdown = drawdown.min()

    results = {
        "ticker": ticker,
        "strategy": "MA_7_vs_MA_21_Crossover",
        "total_market_return_pct": float(total_market_return * 100),
        "total_strategy_return_pct": float(total_strategy_return * 100),
        "win_rate_pct": float(win_rate * 100),
        "max_drawdown_pct": float(max_drawdown * 100)
    }

    results_path = METRICS_DIR / "backtest_results.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=4)

    # Save cumulative returns for visualization
    df[['Date', 'Cum_Market_Return', 'Cum_Strategy_Return']].to_csv(METRICS_DIR / "backtest_curve.csv", index=False)

    logging.info(f"Backtest completed. Strategy Return: {total_strategy_return*100:.2f}%, Market Return: {total_market_return*100:.2f}%")
    return results

if __name__ == "__main__":
    from src.config import DEFAULT_TICKER
    run_backtest(DEFAULT_TICKER)
