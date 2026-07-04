import pandas as pd
import matplotlib.pyplot as plt
import json
import logging
from src.config import PROCESSED_DATA_DIR, METRICS_DIR, FIGURES_DIR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set clean professional style
plt.style.use('seaborn-v0_8-whitegrid')

def create_visualizations(ticker: str):
    """Generate and save clean, professional charts."""

    features_path = PROCESSED_DATA_DIR / f"{ticker}_features.csv"
    forecast_path = METRICS_DIR / f"{ticker}_forecast.csv"
    backtest_path = METRICS_DIR / "backtest_curve.csv"
    signal_path = METRICS_DIR / "latest_signal.json"

    if not features_path.exists():
        logging.error("Missing features data for visualizations.")
        return

    df = pd.read_csv(features_path)
    df['Date'] = pd.to_datetime(df['Date'])

    # 1. Price History with MAs
    plt.figure(figsize=(12, 6), dpi=300)
    plt.plot(df['Date'], df['Close'], label='Close Price', color='#2ca02c', linewidth=1.5)
    plt.plot(df['Date'], df['MA_7'], label='7-Day MA', color='#ff7f0e', linestyle='--', alpha=0.8)
    plt.plot(df['Date'], df['MA_21'], label='21-Day MA', color='#1f77b4', linestyle='--', alpha=0.8)
    plt.title(f"{ticker} Price History & Moving Averages", fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price (USD)', fontsize=12)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "price_history.png")
    plt.close()

    # 2. Prophet Forecast Chart
    if forecast_path.exists():
        df_forecast = pd.read_csv(forecast_path)
        df_forecast['ds'] = pd.to_datetime(df_forecast['ds'])

        # Merge actuals to show continuity
        latest_date = df['Date'].max()
        future_mask = df_forecast['ds'] > latest_date
        historical_mask = df_forecast['ds'] <= latest_date

        plt.figure(figsize=(12, 6), dpi=300)

        # Plot actual close for recent context (last 90 days)
        recent_actuals = df.tail(90)
        plt.plot(recent_actuals['Date'], recent_actuals['Close'], label='Actual Close', color='black', linewidth=1.5)

        # Plot forecast
        plt.plot(df_forecast.loc[future_mask, 'ds'], df_forecast.loc[future_mask, 'yhat'], label='Forecast', color='blue', linewidth=2)

        # Confidence interval
        plt.fill_between(
            df_forecast.loc[future_mask, 'ds'],
            df_forecast.loc[future_mask, 'yhat_lower'],
            df_forecast.loc[future_mask, 'yhat_upper'],
            color='blue', alpha=0.2, label='Confidence Interval'
        )

        plt.title(f"{ticker} Prophet Forecast (Next 7 Days)", fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price (USD)', fontsize=12)
        plt.legend()
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / "forecast.png")
        plt.close()

    # 3. Signal Dashboard Chart (Latest Price, Forecast, Signal)
    if signal_path.exists() and forecast_path.exists():
        with open(signal_path, 'r') as f:
            signal_data = json.load(f)

        fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
        ax.axis('off')

        signal_text = signal_data.get('signal', 'UNKNOWN')
        color = 'green' if signal_text == 'BUY' else 'red' if signal_text == 'SELL' else 'gray'

        ax.text(0.5, 0.8, f"Latest Signal: {signal_text}", ha='center', va='center', fontsize=20, fontweight='bold', color=color)
        ax.text(0.5, 0.6, f"Latest Close: ${signal_data.get('latest_close', 0):.2f}", ha='center', va='center', fontsize=14)
        ax.text(0.5, 0.4, f"Forecast Price: ${signal_data.get('forecast_price', 0):.2f}", ha='center', va='center', fontsize=14)
        ax.text(0.5, 0.2, f"Expected Return: {signal_data.get('expected_return_pct', 0):.2f}%", ha='center', va='center', fontsize=14)

        plt.title(f"{ticker} Signal Summary", fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / "signal_dashboard.png")
        plt.close()

    # 4. Backtest Cumulative Return
    if backtest_path.exists():
        df_backtest = pd.read_csv(backtest_path)
        df_backtest['Date'] = pd.to_datetime(df_backtest['Date'])

        plt.figure(figsize=(12, 6), dpi=300)
        plt.plot(df_backtest['Date'], df_backtest['Cum_Market_Return'], label='Buy & Hold', color='gray', linewidth=1.5)
        plt.plot(df_backtest['Date'], df_backtest['Cum_Strategy_Return'], label='MA Strategy', color='purple', linewidth=1.5)
        plt.title(f"{ticker} Strategy vs Buy & Hold Cumulative Return", fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Cumulative Return Multiplier', fontsize=12)
        plt.legend()
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / "backtest.png")
        plt.close()

    logging.info("Visualizations generated and saved.")

if __name__ == "__main__":
    from src.config import DEFAULT_TICKER
    create_visualizations(DEFAULT_TICKER)
