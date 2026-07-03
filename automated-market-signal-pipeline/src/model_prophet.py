import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import json
import logging
from src.config import PROCESSED_DATA_DIR, MODELS_DIR, METRICS_DIR, FORECAST_HORIZON

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_and_evaluate_prophet(ticker: str):
    """Train Prophet model, evaluate it, and forecast future prices."""
    prophet_data_path = PROCESSED_DATA_DIR / f"{ticker}_prophet.csv"
    if not prophet_data_path.exists():
        logging.error(f"Prophet data not found for {ticker} at {prophet_data_path}")
        return None, None

    df = pd.read_csv(prophet_data_path)
    df['ds'] = pd.to_datetime(df['ds'])

    if len(df) < 30:
        logging.warning("Not enough data to train Prophet robustly.")
        return None, None

    # Train/Test Split (last 30 days for testing)
    test_size = 30
    train = df.iloc[:-test_size]
    test = df.iloc[-test_size:]

    # Train Model
    logging.info("Training Prophet model...")
    model = Prophet(daily_seasonality=True)
    model.fit(train)

    # Evaluate
    future_test = model.make_future_dataframe(periods=test_size)
    forecast_test = model.predict(future_test)

    predictions = forecast_test.iloc[-test_size:]['yhat'].values
    actuals = test['y'].values

    mae = mean_absolute_error(actuals, predictions)
    rmse = np.sqrt(mean_squared_error(actuals, predictions))
    mape = np.mean(np.abs((actuals - predictions) / actuals)) * 100

    metrics = {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape
    }

    metrics_path = METRICS_DIR / f"{ticker}_metrics.json"
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    logging.info(f"Evaluation metrics saved to {metrics_path}")

    # Retrain on full data for actual forecasting
    logging.info("Retraining on full dataset for future forecast...")
    final_model = Prophet(daily_seasonality=True)
    final_model.fit(df)

    # Save model
    model_path = MODELS_DIR / f"{ticker}_prophet.pkl"
    joblib.dump(final_model, model_path)
    logging.info(f"Model saved to {model_path}")

    # Forecast
    future = final_model.make_future_dataframe(periods=FORECAST_HORIZON)
    forecast = final_model.predict(future)

    # Save forecast
    forecast_path = METRICS_DIR / f"{ticker}_forecast.csv"
    forecast.to_csv(forecast_path, index=False)
    logging.info(f"Forecast saved to {forecast_path}")

    return final_model, forecast

if __name__ == "__main__":
    from src.config import DEFAULT_TICKER
    train_and_evaluate_prophet(DEFAULT_TICKER)
