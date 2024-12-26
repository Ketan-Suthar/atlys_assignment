import traceback

from bs4 import BeautifulSoup
import requests
import time
from models.settings import ScraperSettings
from models.product import Product
from services.storage import StorageInterface, RedisCache
from config import Settings
import re

class Scraper:
    def __init__(self, settings: ScraperSettings, storage: StorageInterface, cache: RedisCache):
        self.settings = settings
        self.storage = storage
        self.cache = cache

    def __get_item_details(self, item, products, scrape_response):
        # print(item)
        title = item.find('div', class_='mf-product-thumbnail').find('a').find('img')['alt']
        title = str(title).replace('- Dentalstall India', '').strip()
        price = item.find('span', class_='price').find('bdi').get_text(strip=True)
        price = re.findall(r'[\d.]+', price)
        price = '-0.0' if len(price) == 0 else price[0]
        image_url = item.find('div', class_='mf-product-thumbnail').find('a').find('img')['data-lazy-src']
        print(f'item: {title}:{price}:{image_url}')

        cache_key = f"product:{title}"
        cached_price = self.cache.get(cache_key)
        print(f'checking cache: {cached_price}=={price}')

        if cached_price and float(cached_price) == float(price):
            print(f'CACHE HIT: for item: {title} price is still same: {price}')
            scrape_response['unchanged'] += 1
            return  # Skip unchanged items

        image_path = f"images/{title.replace(' ', '_')}.jpg"
        self.download_image(image_url, image_path)

        products.append(Product(product_title=title, product_price=float(price), path_to_image=image_path))
        self.cache.set(cache_key, price, expiry=Settings.CACHE_EXPIRY)
        scrape_response['scrapped'] += 1

    def scrape(self) -> dict:
        base_url = "https://dentalstall.com/shop/page/"
        products = []
        session = requests.Session()
        scrape_response = {
            'scrapped': 0,
            'unchanged': 0,
        }

        if self.settings.proxy:
            session.proxies = {"http": self.settings.proxy, "https": self.settings.proxy}

        for page in range(1, self.settings.max_pages + 1):
            url = f"{base_url}{page}/"
            print(url)
            try:
                response = session.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                product_items = soup.find_all('li', class_='product')
                print(f'item on {page}:{len(product_items)}')

                for item in product_items:  # Replace with actual selector
                    try:
                        self.__get_item_details(item, products, scrape_response)
                    except Exception as e: # noqa
                        print('Something went wrong while fetching item details:')
                        traceback.print_exc()
            except requests.RequestException:
                time.sleep(5)
                continue

        existing_products = self.storage.load()
        updated_products = existing_products + products
        self.storage.save(updated_products)

        print(f"Scraped and updated {len(products)} products.")
        return scrape_response

    @staticmethod
    def download_image(url: str, path: str):
        response = requests.get(url, stream=True)
        with open(path, "wb") as f:
            f.write(response.content)
