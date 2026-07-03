import pandas as pd
import numpy as np
import logging
from src.config import PROCESSED_DATA_DIR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def engineer_features(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Engineer technical features and save to processed directory."""
    if df.empty:
        logging.warning("Empty dataframe provided to feature engineering.")
        return df

    try:
        # Sort by date just in case
        df = df.sort_values('Date').copy()

        # Calculate Returns
        df['Returns'] = df['Close'].pct_change()

        # Calculate Moving Averages
        df['MA_7'] = df['Close'].rolling(window=7).mean()
        df['MA_21'] = df['Close'].rolling(window=21).mean()

        # Calculate Volatility (21-day rolling standard deviation of returns)
        df['Volatility_21'] = df['Returns'].rolling(window=21).std() * np.sqrt(365) # annualized roughly for crypto, 252 for stock

        # Calculate Price Momentum (e.g., Close today / Close N days ago)
        df['Momentum_14'] = df['Close'] / df['Close'].shift(14) - 1

        # Fill NaN values that resulted from rolling calculations
        df = df.bfill()

        # Save full processed features
        processed_path = PROCESSED_DATA_DIR / f"{ticker}_features.csv"
        df.to_csv(processed_path, index=False)
        logging.info(f"Processed features saved to {processed_path}")

        return df
    except Exception as e:
        logging.error(f"Error during feature engineering for {ticker}: {e}")
        return df

if __name__ == "__main__":
    from src.config import RAW_DATA_DIR, DEFAULT_TICKER
    raw_path = RAW_DATA_DIR / f"{DEFAULT_TICKER}.csv"
    if raw_path.exists():
        df = pd.read_csv(raw_path)
        engineer_features(df, DEFAULT_TICKER)
