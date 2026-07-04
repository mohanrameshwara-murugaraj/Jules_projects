import pytest
import pandas as pd
import json
import re
from pathlib import Path

# Need to mock the constants/paths, or use a temporary directory for tests
from src.features import engineer_features
from src.update_readme import update_readme

# A small mock dataset
def get_mock_data():
    return pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=30),
        'Open': range(100, 130),
        'High': range(105, 135),
        'Low': range(95, 125),
        'Close': range(100, 130),
        'Volume': [1000] * 30
    })

def test_engineer_features(tmp_path, monkeypatch):
    import src.features
    monkeypatch.setattr(src.features, "PROCESSED_DATA_DIR", tmp_path)

    df = get_mock_data()
    result_df = engineer_features(df, "TEST_TICKER")

    assert 'Returns' in result_df.columns
    assert 'MA_7' in result_df.columns
    assert 'MA_21' in result_df.columns
    assert 'Volatility_21' in result_df.columns
    assert 'Momentum_14' in result_df.columns
    assert not result_df['Returns'].isnull().any()

    # Verify file was saved
    assert (tmp_path / "TEST_TICKER_features.csv").exists()

def test_signal_logic():
    latest_close = 100.0
    forecast_price = 105.0 # +5%

    expected_return = (forecast_price - latest_close) / latest_close
    assert expected_return == 0.05

    signal = "HOLD"
    if expected_return >= 0.02:
        signal = "BUY"
    elif expected_return <= -0.02:
        signal = "SELL"

    assert signal == "BUY"

def test_readme_markers_logic():
    readme_content = "# Test\n\n<!-- AUTO_DASHBOARD_START -->\nOld content\n<!-- AUTO_DASHBOARD_END -->"
    dashboard_content = "New content"

    pattern = r"(<!-- AUTO_DASHBOARD_START -->).*?(<!-- AUTO_DASHBOARD_END -->)"
    replacement = rf"\1\n{dashboard_content}\n\2"

    new_readme_content = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)

    assert "New content" in new_readme_content
    assert "Old content" not in new_readme_content
