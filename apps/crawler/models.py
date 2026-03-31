from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class CrawlerBase(SQLModel):
    __table_args__ = {'schema': 'crawler'}

class CrawlSession(CrawlerBase, table=True):
    __tablename__ = 'crawlsession'

    id: int | None = Field(default=None, primary_key=True)
    domain: str = Field(index=True)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = Field(default=None)
    status: str = Field(default='pending')
    total_urls: int = Field(default=0)
    crawled_urls: int = Field(default=0)
    urls: list['CrawledUrl'] = Relationship(back_populates='session')


class CrawledUrl(CrawlerBase, table=True):
    __tablename__ = 'crawledurl'
    id: int | None = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key='crawler.crawlsession.id', index=True)
    url: str = Field(index=True)
    status_code: int = Field(default=0, index=True)
    content: str | None = Field(default=None)
    error: str | None = Field(default=None)
    crawled_at: datetime = Field(default_factory=datetime.utcnow)
    session: CrawlSession = Relationship(back_populates='urls')
