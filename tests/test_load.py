import pytest
import pandas as pd
import os
import logging
from unittest import mock
from utils.load import save_to_csv

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'title': ['Product A', 'Product B'],
        'price_idr': [150000.0, 250000.0],
        'rating': [4.5, 3.8],
        'colors': [2, 3],
        'sizes': ['S,M', 'L,XL'],
        'gender': ['men', 'women'],
        'timestamp': ['2025-05-03T00:00:00', '2025-05-03T00:00:00']
    })

def test_save_csv_success(tmp_path, sample_df, caplog):
    caplog.set_level(logging.INFO)

    test_path = tmp_path / "output.csv"
    result = save_to_csv(sample_df, str(test_path))

    assert result is True
    assert os.path.exists(test_path)

    df_read = pd.read_csv(test_path)
    assert len(df_read) == 2
    assert list(df_read.columns) == list(sample_df.columns)

    assert f"Data successfully saved to {test_path}" in caplog.text


def test_save_csv_path_creation(tmp_path, sample_df):
    nested_path = tmp_path / "nested/dirs/output.csv"
    
    result = save_to_csv(sample_df, str(nested_path))
    
    assert result is True
    assert os.path.exists(nested_path)

def test_save_csv_permission_error(tmp_path, sample_df, caplog):
    test_path = tmp_path / "output.csv"
    
    with mock.patch('pandas.DataFrame.to_csv') as mock_save:
        mock_save.side_effect = PermissionError("Write protected")
        result = save_to_csv(sample_df, str(test_path))
    
    assert result is False
    assert "Permission denied: Write protected" in caplog.text

def test_save_csv_invalid_data(tmp_path, caplog):
    empty_df = pd.DataFrame()
    target_path = tmp_path / "empty.csv"

    result = save_to_csv(empty_df, target_path)

    assert result is False
    assert "No data to save" in caplog.text
    assert not target_path.exists()


def test_save_csv_disk_full(tmp_path, sample_df, caplog):
    test_path = tmp_path / "large.csv"
    
    with mock.patch('pandas.DataFrame.to_csv') as mock_save:
        mock_save.side_effect = OSError(28, "No space left on device")
        result = save_to_csv(sample_df, str(test_path))
    
    assert result is False
    assert "Failed to save data: [Errno 28] No space left on device" in caplog.text

def test_save_csv_invalid_path(sample_df, caplog):
    caplog.set_level(logging.INFO)
    result = save_to_csv(sample_df, "/invalid/path/?.csv")
    assert result is False
    assert "OSError while saving: [Errno 22] Invalid argument" in caplog.text

