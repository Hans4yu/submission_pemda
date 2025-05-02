import pytest
import requests_mock
import requests
from utils.extract import extract_data
import logging
from utils import extract

@pytest.fixture
def mock_product_html():
    return """
    <div class="collection-card">
        <div style="position: relative;">
            <img src="https://picsum.photos/280/350?random=26" class="collection-image" alt="T-shirt 26">
        </div>
        <div class="product-details">
            <h3 class="product-title">Test Product</h3>
            <div class="price-container"><span class="price">$10.00</span></div>
            <p>Rating: ⭐ 4.5 / 5</p>
            <p>2 Colors</p>
            <p>Size: S, M, L</p>
            <p>Gender: Men</p>
        </div>
    </div>
    """

@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m

def test_scrape_products_success(mock_requests, mock_product_html):
    mock_requests.get(
        "https://fashion-studio.dicoding.dev/",
        text=f"<html><body>{mock_product_html * 3}</body></html>"
    )
    
    results = extract_data(pages=1)
    
    assert len(results) == 3
    assert results[0]['title'] == "Test Product"
    assert results[0]['price_usd'] == 10.0
    assert results[0]['rating'] == 4.5
    assert results[0]['colors'] == 2
    assert results[0]['sizes'] == "S, M, L"
    assert results[0]['gender'] == 'men'
    assert isinstance(results[0]['timestamp'], str)

def test_scrape_products_http_error(mock_requests, caplog):
    mock_requests.get(
        "https://fashion-studio.dicoding.dev/",
        status_code=404
    )
    
    with caplog.at_level(logging.ERROR):
        results = extract_data(pages=1)

    assert len(results) == 0
    assert "Failed to fetch page 1" in caplog.text

def test_scrape_products_timeout(mock_requests, caplog):
    mock_requests.get(
        "https://fashion-studio.dicoding.dev/",
        exc=requests.exceptions.ConnectTimeout
    )
    
    with caplog.at_level(logging.ERROR):
        results = extract_data(pages=1)

    assert len(results) == 0
    assert "Failed to fetch page 1" in caplog.text

def test_scrape_products_invalid_parsing(mock_requests, caplog):
    # Simulasi produk dengan detail kosong
    mock_requests.get(
        "https://fashion-studio.dicoding.dev/",
        text="<html><body><div class='collection-card'></div></body></html>"
    )
    
    with caplog.at_level(logging.ERROR):
        results = extract_data(pages=1)

    assert len(results) == 0
    assert "Error parsing product" in caplog.text



def test_scrape_products_main_function(capsys, monkeypatch):
    # Patch extract_data agar predictable
    monkeypatch.setattr(extract, "extract_data", lambda pages=2: [{"title": "Sample"}])

    # Jalankan fungsi main
    extract.main()

    captured = capsys.readouterr()
    assert "Scraped 1 products" in captured.out
