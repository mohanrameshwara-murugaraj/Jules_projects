import argparse
import logging
from src.config import DEFAULT_TICKER, FALLBACK_TICKERS
from src.data_fetcher import fetch_data, prepare_prophet_data
from src.features import engineer_features
from src.model_prophet import train_and_evaluate_prophet
from src.signal_engine import generate_signal
from src.backtest import run_backtest
from src.visualization import create_visualizations
from src.update_readme import update_readme

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline(ticker: str):
    """Run the complete end-to-end signal pipeline."""
    logging.info(f"=== Starting Pipeline for {ticker} ===")

    # 1. Fetch Data
    df = fetch_data(ticker)

    # Handle failure gracefully by trying fallbacks if requested
    if df.empty:
        logging.error(f"Failed to fetch data for {ticker}.")
        if ticker == DEFAULT_TICKER:
            for fallback in FALLBACK_TICKERS:
                logging.info(f"Attempting fallback ticker: {fallback}")
                df = fetch_data(fallback)
                if not df.empty:
                    ticker = fallback
                    break

        if df.empty:
            logging.error("All data fetch attempts failed. Exiting.")
            return

    # 2. Prepare Data
    prepare_prophet_data(df, ticker)
    df_features = engineer_features(df, ticker)

    if df_features.empty:
        logging.error("Feature engineering failed. Exiting.")
        return

    # 3. Train & Evaluate Prophet Model
    model, forecast = train_and_evaluate_prophet(ticker)
    if model is None:
        logging.error("Model training failed. Exiting.")
        return

    # 4. Generate Signal
    signal = generate_signal(ticker)
    if not signal:
        logging.error("Signal generation failed. Exiting.")
        return

    # 5. Backtest
    run_backtest(ticker)

    # 6. Visualizations
    create_visualizations(ticker)

    # 7. Update README
    update_readme(ticker)

    logging.info(f"=== Pipeline completed successfully for {ticker} ===")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Market Signal Pipeline")
    parser.add_argument("--ticker", type=str, default=DEFAULT_TICKER, help="Ticker symbol to process (e.g., BTC-USD, AAPL)")
    args = parser.parse_args()

    run_pipeline(args.ticker)
