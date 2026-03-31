from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import select, Session
from sqlalchemy import desc as sqlalchemy_desc
from datetime import datetime
from apps.crawler.models import CrawlSession, CrawledUrl
from apps.crawler.core.config import (
    CrawlerConfig, 
    CrawlStartRequest, 
    CrawlStatusResponse, 
    CrawlUrlResponse,
    CrawlSessionDetailResponse
)
from apps.crawler.tasks import crawl_domain_task, crawl_all_domains_task
from essentials.database.orm import SessionDep
import typing

router = APIRouter()
crawler_router = router


@router.post('/start', response_model=dict)
def start_crawling(request: Optional[CrawlStartRequest] = None) -> dict:
    if request and request.domains:
        domains = request.domains
    else:
        domains = CrawlerConfig.DOMAINS
    task_ids = []
    for domain in domains:
        task = crawl_domain_task.delay(domain)
        task_ids.append({
            'domain': domain,
            'task_id': task.id
        })
    
    return {
        'message': 'Crawling started',
        'tasks': task_ids
    }


@router.post('/start/all', response_model=dict)
def start_crawling_all() -> dict:
    task = crawl_all_domains_task.delay()
    return {
        'message': 'Crawling started for all domains',
        'task_id': task.id
    }


@router.get('/sessions', response_model=List[CrawlStatusResponse])
def get_sessions(
    session: SessionDep,
    limit: int = Query(10, ge=1, le=100),
    domain: Optional[str] = None
) -> List[CrawlStatusResponse]:
    query = select(CrawlSession).order_by(sqlalchemy_desc(CrawlSession.__table__.c.started_at)).limit(limit)
    
    if domain:
        query = select(CrawlSession).where(CrawlSession.domain == domain).order_by(sqlalchemy_desc(CrawlSession.__table__.c.started_at)).limit(limit)
    
    sessions = session.exec(query).all()
    
    return [
        CrawlStatusResponse(
            id=s.id,
            domain=s.domain,
            status=s.status,
            started_at=s.started_at,
            completed_at=s.completed_at,
            total_urls=s.total_urls,
            crawled_urls=s.crawled_urls
        )
        for s in sessions
    ]


@router.get('/sessions/{session_id}', response_model=CrawlSessionDetailResponse)
def get_session_detail(session: SessionDep, session_id: int) -> CrawlSessionDetailResponse:
    crawl_session = session.get(CrawlSession, session_id)
    if not crawl_session:
        raise HTTPException(status_code=404, detail='Session not found')
    
    urls = session.exec(
        select(CrawledUrl).where(CrawledUrl.session_id == session_id).limit(100)
    ).all()
    
    return CrawlSessionDetailResponse(
        session=CrawlStatusResponse(
            id=crawl_session.id,
            domain=crawl_session.domain,
            status=crawl_session.status,
            started_at=crawl_session.started_at,
            completed_at=crawl_session.completed_at,
            total_urls=crawl_session.total_urls,
            crawled_urls=crawl_session.crawled_urls
        ),
        urls=[
            CrawlUrlResponse(
                id=u.id,
                url=u.url,
                status_code=u.status_code,
                crawled_at=u.crawled_at,
                error=u.error
            )
            for u in urls
        ]
    )


@router.get('/urls', response_model=List[CrawlUrlResponse])
def get_urls(
    session: SessionDep,
    session_id: Optional[int] = Query(None),
    status_code: Optional[int] = Query(None),
    limit: int = Query(100, ge=1, le=1000)
) -> List[CrawlUrlResponse]:
    query = select(CrawledUrl).order_by(sqlalchemy_desc(CrawledUrl.__table__.c.crawled_at)).limit(limit)
    if session_id:
        query = select(CrawledUrl).where(CrawledUrl.session_id == session_id).order_by(sqlalchemy_desc(CrawledUrl.__table__.c.crawled_at)).limit(limit)
    if status_code is not None:
        query = select(CrawledUrl).where(CrawledUrl.status_code == status_code).order_by(sqlalchemy_desc(CrawledUrl.__table__.c.crawled_at)).limit(limit)
    
    urls = session.exec(query).all()
    
    return [
        CrawlUrlResponse(
            id=u.id,
            url=u.url,
            status_code=u.status_code,
            crawled_at=u.crawled_at,
            error=u.error
        )
        for u in urls
    ]

@router.get('/status-codes', response_model=dict)
def get_status_codes_summary(session: SessionDep) -> dict:
    urls = session.exec(select(CrawledUrl)).all()
    status_counts: dict[str, int] = {}
    for url in urls:
        code = str(url.status_code)
        status_counts[code] = status_counts.get(code, 0) + 1
    
    return {
        'total_urls': len(urls),
        'status_codes': status_counts
    }



