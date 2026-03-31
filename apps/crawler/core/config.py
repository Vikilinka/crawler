from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

class CrawlerConfig:
    # Добавлен единый массив доменов
    DOMAINS = [
        'https://new.etu.ru',
        'https://abit.etu.ru',
    ]
    REQUEST_TIMEOUT = 30
    MAX_URLS_PER_SESSION = 1000
    REQUEST_DELAY = 100

class CrawlStartRequest(BaseModel):
    domains: Optional[List[str]] = None  # Если None, используются домены из конфига


class CrawlStatusResponse(BaseModel):
    id: int
    domain: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    total_urls: int
    crawled_urls: int

class CrawlUrlResponse(BaseModel):
    id: int
    url: str
    status_code: int
    crawled_at: datetime
    error: Optional[str] = None


class CrawlSessionDetailResponse(BaseModel):
    session: CrawlStatusResponse
    urls: List[CrawlUrlResponse]
