import pytest
import pandas as pd
import numpy as np
from utils.transform import transform_data

@pytest.fixture
def sample_raw_data():
    return [
        {'title': 'Product A', 'price_usd': 10.0, 'rating': 4.5, 'colors': ['red'],
         'sizes': ['S'], 'gender': 'women', 'timestamp': '2025-05-03T00:00:00'},
        {'title': 'Product A', 'price_usd': 10.0, 'rating': 4.5, 'colors': ['red'],
         'sizes': ['S'], 'gender': 'women', 'timestamp': '2025-05-03T00:00:00'},  # Duplicate
        {'title': None, 'price_usd': 'invalid', 'rating': 6.0, 'colors': [],
         'sizes': [], 'gender': 'unisex', 'timestamp': '2025-05-03T00:00:00'},     # Invalid
        {'title': 'Product B', 'price_usd': 25.99, 'rating': 3.2, 'colors': ['blue'],
         'sizes': ['M,L'], 'gender': 'men', 'timestamp': '2025-05-03T00:00:00'}
    ]

def test_transform_cleans_data(sample_raw_data):
    df = transform_data(sample_raw_data)
    assert len(df) == 2  # Duplicate removed, 1 invalid skipped
    assert df['title'].isna().sum() == 0
    assert df['price_idr'].between(10000, 1000000).all()

def test_currency_conversion(sample_raw_data):
    df = transform_data(sample_raw_data)
    assert pytest.approx(df['price_idr'].iloc[0]) == 10.0 * 16000
    assert df['price_idr'].dtype == np.float64

def test_data_types(sample_raw_data):
    df = transform_data(sample_raw_data)
    assert df['title'].dtype == 'string'
    assert df['price_idr'].dtype == 'float64'
    assert df['rating'].dtype == 'float64'
    assert df['colors'].dtype == 'int64'
    assert df['sizes'].dtype == 'string'
    assert df['gender'].dtype.name == 'category'
    assert pd.api.types.is_datetime64_any_dtype(df['timestamp'])

def test_error_handling():
    with pytest.raises(ValueError):
        transform_data("invalid input")

    df = transform_data([{'missing': 'fields'}])
    assert df.empty

    df = transform_data([{'title': 'Test', 'price_usd': 10.0}])
    assert df.empty


def test_size_parsing(sample_raw_data):
    df = transform_data(sample_raw_data)
    assert df['sizes'].iloc[1] == 'M,L'
    assert isinstance(df['sizes'].iloc[1], str)

def test_color_count(sample_raw_data):
    df = transform_data(sample_raw_data)
    assert df['colors'].iloc[0] == 1
    assert df['colors'].iloc[1] == 1

def test_timestamp_conversion(sample_raw_data):
    df = transform_data(sample_raw_data)
    assert pd.api.types.is_datetime64_any_dtype(df['timestamp'])
    assert df['timestamp'].dt.tz is None
