from celery import Task
from collections import deque
from datetime import datetime
from typing import List, Set, Dict, Any, Optional
from aiohttp import ClientTimeout
import aiohttp
import asyncio
from essentials.celery.worker import app
from essentials.database.orm import Session, engine, create_db_and_tables
from apps.crawler.models import CrawlSession, CrawledUrl
from apps.crawler.core.config import CrawlerConfig
from apps.crawler.core.parser import SitemapParser, HtmlParser


class CrawlerTask:

    def __init__(self, task: Task):
        self.task = task
        self.visited: set[str] = set()
        self.queue: deque = deque()
        self.session: Session | None = None

    def _init_db(self):
        create_db_and_tables()
        self.session = Session(engine)

    def _close_db(self):
        if self.session:
            self.session.close()

    async def crawl_domain(self, domain: str) -> dict[str, Any]:
        self._init_db()
        try:
            # Создание сессии краулинга в БД
            crawl_session = CrawlSession(
                domain=domain,
                status='running',
                started_at=datetime.utcnow()
            )
            assert self.session is not None
            self.session.add(crawl_session)
            self.session.commit()
            self.session.refresh(crawl_session)
            self.visited = set()
            self.queue = deque()

            async with aiohttp.ClientSession() as http_session:
                # Получаем URL из sitemap
                sitemap_urls = await SitemapParser.parse_sitemap_urls(
                    http_session,
                    domain,
                    CrawlerConfig.REQUEST_TIMEOUT
                )
                # Добавляем URL из sitemap в очередь
                for url in sitemap_urls:
                    if url not in self.visited:
                        self.queue.append(url)
                        self.visited.add(url)

                # Если sitemap не найден, начинаем с главной страницы
                if not self.queue:
                    self.queue.append(domain)
                    self.visited.add(domain)

                # Обновление общего количество URL
                crawl_session.total_urls = len(self.visited)
                assert self.session is not None
                self.session.commit()

                # Обработка очереди
                await self._process_queue(http_session, crawl_session)

                # Завершение сессии
                crawl_session.status = 'completed'
                crawl_session.completed_at = datetime.utcnow()
                crawl_session.crawled_urls = len([u for u in crawl_session.urls])
                self.session.commit()

                return {
                    'session_id': crawl_session.id,
                    'domain': domain,
                    'status': 'completed',
                    'total_urls': crawl_session.total_urls,
                    'crawled_urls': crawl_session.crawled_urls
                }

        except Exception as e:
            if self.session:
                # Помечаем сессию как failed
                crawl_session.status = 'failed'
                crawl_session.completed_at = datetime.utcnow()
                self.session.commit()

            return {
                'session_id': crawl_session.id if 'crawl_session' in locals() else None,
                'domain': domain,
                'status': 'failed',
                'error': str(e)
            }
        finally:
            self._close_db()

    async def _process_queue(
        self,
        http_session: aiohttp.ClientSession,
        crawl_session: CrawlSession
    ):
        while self.queue and len(self.visited) <= CrawlerConfig.MAX_URLS_PER_SESSION:
            url = self.queue.popleft()
            # Скачиваем страницу
            status_code, content, error = await self._fetch_url(http_session, url)
            # Сохраняем результат в БД
            crawled_url = CrawledUrl(
                session_id=crawl_session.id,
                url=url,
                status_code=status_code,
                content=content if status_code == 200 else None,
                error=error
            )
            assert self.session is not None
            self.session.add(crawled_url)
            self.session.commit()
            # Извлекаем новые ссылки из HTML
            if status_code == 200 and content:
                new_links = HtmlParser.extract_links(content, url)
                for link in new_links:
                    if link not in self.visited:
                        self.queue.append(link)
                        self.visited.add(link)
            # Обновляем счетчик
            crawl_session.crawled_urls = len([u for u in crawl_session.urls])
            self.session.commit()

    async def _fetch_url(
        self,
        session: aiohttp.ClientSession,
        url: str
    ) -> tuple[int, str | None, str | None]:
        try:
            timeout = ClientTimeout(total=CrawlerConfig.REQUEST_TIMEOUT)
            async with session.get(url, timeout=timeout) as response:
                content = await response.text()
                return response.status, content, None
        except asyncio.TimeoutError:
            return 0, None, 'Timeout'
        except Exception as e:
            return 0, None, str(e)


@app.task(bind=True)
def crawl_domain_task(self: Task, domain: str) -> Dict[str, Any]:
    crawler = CrawlerTask(self)
    result = asyncio.run(crawler.crawl_domain(domain))
    return result


@app.task(bind=True)
def crawl_all_domains_task(self: Task, domains: list[str] | None = None) -> dict[str, Any]:
    if domains is None:
        domains = CrawlerConfig.DOMAINS
    task_ids: list[dict[str, str]] = []
    for domain in domains:
        # Запускаем задачу для каждого домена из массива
        result = crawl_domain_task.delay(domain)
        task_ids.append({
            'domain': domain,
            'task_id': result.id
        })

    return {
        'message': 'Crawling started for all domains',
        'tasks': task_ids
    }
