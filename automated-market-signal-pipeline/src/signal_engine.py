import pandas as pd
import json
import logging
from datetime import datetime
from src.config import PROCESSED_DATA_DIR, METRICS_DIR, REPORTS_DIR, BUY_THRESHOLD, SELL_THRESHOLD

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_signal(ticker: str):
    """Generate BUY/SELL/HOLD signal based on forecast."""
    features_path = PROCESSED_DATA_DIR / f"{ticker}_features.csv"
    forecast_path = METRICS_DIR / f"{ticker}_forecast.csv"

    if not features_path.exists() or not forecast_path.exists():
        logging.error(f"Missing data or forecast for {ticker}")
        return None

    df_features = pd.read_csv(features_path)
    df_forecast = pd.read_csv(forecast_path)

    # Get latest actual close
    latest_actual = df_features.iloc[-1]
    latest_close = latest_actual['Close']
    latest_date = latest_actual['Date']

    # Get next day forecast
    # Forecast dataframe has historical + future. Find the first row where ds > latest_date
    df_forecast['ds'] = pd.to_datetime(df_forecast['ds'])
    future_forecast = df_forecast[df_forecast['ds'] > pd.to_datetime(latest_date)]

    if future_forecast.empty:
        logging.error("No future forecast available.")
        return None

    next_day_forecast = future_forecast.iloc[0]
    forecast_price = next_day_forecast['yhat']
    lower_band = next_day_forecast['yhat_lower']
    upper_band = next_day_forecast['yhat_upper']

    expected_return = (forecast_price - latest_close) / latest_close

    if expected_return >= BUY_THRESHOLD:
        signal = "BUY"
    elif expected_return <= SELL_THRESHOLD:
        signal = "SELL"
    else:
        signal = "HOLD"

    signal_data = {
        "ticker": ticker,
        "timestamp": datetime.now().isoformat(),
        "latest_close": float(latest_close),
        "forecast_price": float(forecast_price),
        "expected_return_pct": float(expected_return * 100),
        "lower_band": float(lower_band),
        "upper_band": float(upper_band),
        "signal": signal
    }

    # Save to JSON
    signal_json_path = METRICS_DIR / "latest_signal.json"
    with open(signal_json_path, 'w') as f:
        json.dump(signal_data, f, indent=4)

    # Save to Markdown
    signal_md_path = REPORTS_DIR / "latest_signal.md"
    md_content = f"""# Latest Market Signal: {ticker}
**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

- **Signal:** `{signal}`
- **Latest Close:** ${latest_close:.2f}
- **Forecast Price (Next Day):** ${forecast_price:.2f}
- **Expected Return:** {expected_return * 100:.2f}%
- **Confidence Band:** ${lower_band:.2f} - ${upper_band:.2f}
"""
    with open(signal_md_path, 'w') as f:
        f.write(md_content)

    logging.info(f"Signal generated: {signal} (Expected Return: {expected_return*100:.2f}%)")
    return signal_data

if __name__ == "__main__":
    from src.config import DEFAULT_TICKER
    generate_signal(DEFAULT_TICKER)
