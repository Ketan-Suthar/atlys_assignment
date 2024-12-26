from fastapi import FastAPI, HTTPException, Depends
from functools import lru_cache
from redis import Redis
from config import Settings
from models import ScraperSettings
from services import Scraper, StorageInterface
from services import StorageFactory, RedisCache
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",  # React app address, for front-end
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@lru_cache()
def get_settings():
    return Settings()

def authenticate(token: str):
    if token != Settings.STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_redis_client():
    return Redis(host=Settings.REDIS_HOST, port=Settings.REDIS_PORT)


@app.get('/')
def read_root():
    return {'Ping': 'Pong'}


@app.post("/scrape/")
def start_scraping(
    settings: ScraperSettings,
    token: str = Depends(authenticate),
    redis_client: Redis = Depends(get_redis_client)
):
    storage: StorageInterface = StorageFactory.create_storage()
    cache = RedisCache(redis_client)
    scraper = Scraper(settings, storage, cache)
    scrape_response: dict = scraper.scrape()
    scrape_response['status'] = "Scraping completed."
    return scrape_response
