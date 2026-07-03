import yfinance as yf
import pandas as pd
import logging
from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR, PERIOD, INTERVAL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_data(ticker: str) -> pd.DataFrame:
    """Fetch OHLCV data using yfinance."""
    logging.info(f"Fetching data for {ticker} (Period: {PERIOD}, Interval: {INTERVAL})")

    try:
        df = yf.download(ticker, period=PERIOD, interval=INTERVAL, progress=False)

        if df.empty:
            logging.error(f"No data fetched for {ticker}.")
            return pd.DataFrame()

        # Flatten MultiIndex columns if present (yfinance behavior can vary)
        if isinstance(df.columns, pd.MultiIndex):
             # We just take the first level for standard OHLCV names if they're tuple-like
             # or flatten them. Usually, if requesting a single ticker, the second level is the ticker name.
             df.columns = df.columns.get_level_values(0)

        df.reset_index(inplace=True)
        # Rename 'Datetime' to 'Date' if it exists
        if 'Datetime' in df.columns:
            df.rename(columns={'Datetime': 'Date'}, inplace=True)

        # Ensure 'Date' column is timezone-naive
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            if df['Date'].dt.tz is not None:
                df['Date'] = df['Date'].dt.tz_localize(None)

        # Clean missing values
        df.dropna(inplace=True)

        # Save raw data
        raw_path = RAW_DATA_DIR / f"{ticker}.csv"
        df.to_csv(raw_path, index=False)
        logging.info(f"Raw data saved to {raw_path}")

        return df

    except Exception as e:
        logging.error(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

def prepare_prophet_data(df: pd.DataFrame, ticker: str):
    """Prepare and save data in Prophet format (ds, y)."""
    if df.empty or 'Date' not in df.columns or 'Close' not in df.columns:
        logging.error("Invalid DataFrame for Prophet preparation.")
        return

    prophet_df = pd.DataFrame({
        'ds': pd.to_datetime(df['Date']),
        'y': df['Close']
    })

    prophet_path = PROCESSED_DATA_DIR / f"{ticker}_prophet.csv"
    prophet_df.to_csv(prophet_path, index=False)
    logging.info(f"Prophet data saved to {prophet_path}")

if __name__ == "__main__":
    from src.config import DEFAULT_TICKER
    df = fetch_data(DEFAULT_TICKER)
    if not df.empty:
        prepare_prophet_data(df, DEFAULT_TICKER)
