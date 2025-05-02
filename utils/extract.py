import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from typing import List, Dict
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('scraper.log'), logging.StreamHandler()]
)

BASE_URL = "https://fashion-studio.dicoding.dev"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((requests.RequestException,)),
    before_sleep=lambda _: logging.warning("Retrying due to network error...")
)
def fetch_page(page: int) -> requests.Response:
    """Fetch a single page with retry logic"""
    if page == 1:
        url = BASE_URL  # Page 1 has no suffix
    else:
        url = f"{BASE_URL}/page{page}"  # Page 2 and onward follow this pattern

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error(f"Failed to fetch page {page}: {str(e)}")
        raise


def parse_product(product: BeautifulSoup) -> Dict:
    try:
        title_tag = product.find("h3", class_="product-title")
        price_tag = product.find("span", class_="price")
        rating_tag = product.find("p", string=lambda s: s and "Rating:" in s)
        color_tags = product.find_all("p", string=lambda s: s and "Colors" in s)
        size_tag = product.find("p", string=lambda s: s and "Size:" in s)
        gender_tag = product.find("p", string=lambda s: s and "Gender:" in s)

        if not all([title_tag, price_tag, rating_tag, size_tag, gender_tag]):
            raise ValueError("Missing required HTML elements")

        title = title_tag.text.strip()
        price_str = price_tag.text.strip().replace("$", "").replace(",", "")
        price = float(price_str)

        rating_str = product.find("p", string=lambda s: s and "Rating" in s).text
        rating_value = rating_str.split("⭐")[-1].split("/")[0].strip()

        try:
            rating = float(rating_value)
        except ValueError:
            raise ValueError("Invalid Rating format")


        colors = int(color_tags[0].text.strip().split(" ")[0]) if color_tags else 0
        sizes = size_tag.text.strip().split(":")[-1].strip()
        gender = gender_tag.text.strip().split(":")[-1].strip().lower()

        return {
            "title": title,
            "price_usd": price,
            "rating": rating,
            "colors": colors,
            "sizes": sizes,
            "gender": gender,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logging.error(f"Error parsing product: {str(e)}")
        return None



def extract_data(pages: int = 50) -> List[Dict]:
    """Main extraction function for scraping product data"""
    logging.info("Starting scraping process")
    all_products = []
    timestamp = datetime.now().isoformat()
    
    for page in range(1, pages + 1):
        try:
            response = fetch_page(page)
            soup = BeautifulSoup(response.content, "html.parser")
            products = soup.find_all("div", class_="collection-card")

            
            if not products:
                logging.warning(f"No products found on page {page}")
                break
                
            for product in products:
                parsed = parse_product(product)
                if parsed:
                    all_products.append(parsed)
            
            logging.info(f"Page {page} scraped successfully: {len(products)} products")
            
        except Exception as e:
            logging.error(f"Critical error on page {page}: {str(e)}")
            break
            
    logging.info(f"Scraping completed. Total products: {len(all_products)}")
    return all_products

def main():
    test_data = extract_data(pages=2)
    print(f"Scraped {len(test_data)} products")

if __name__ == "__main__":
    main()
