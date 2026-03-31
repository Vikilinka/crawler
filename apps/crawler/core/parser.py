import aiohttp
from aiohttp import ClientTimeout
from bs4 import BeautifulSoup
from typing import List
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET

class SitemapParser:

    @staticmethod
    async def parse_sitemap_urls(session: aiohttp.ClientSession, base_url: str, timeout: int) -> list[str]:
        sitemap_url = urljoin(base_url, '/sitemap.xml')
        urls: list[str] = []
        try:
            async with session.get(sitemap_url, timeout=ClientTimeout(total=timeout)) as response:
                if response.status == 200:
                    content = await response.text()
                    urls = SitemapParser._parse_sitemap_content(content, base_url)
        except Exception:
            pass  # sitemap.xml может отсутствовать
        
        return urls
    
    @staticmethod
    def _parse_sitemap_content(content: str, base_url: str) -> List[str]:
        urls = []
        try:
            root = ET.fromstring(content)
            
            # Определяем namespace
            ns = {}
            if root.tag.startswith('{'):
                ns_end = root.tag.find('}')
                ns['ns'] = root.tag[1:ns_end]
            
            # Находим все URL элементы
            if ns:
                url_elements = root.findall('.//ns:url/ns:loc', ns)
                if not url_elements:
                    url_elements = root.findall('.//ns:urlset/ns:url/ns:loc', ns)
                if not url_elements:
                    # Пробуем без namespace
                    url_elements = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            else:
                url_elements = root.findall('.//loc')
            
            for elem in url_elements:
                if elem.text:
                    url = elem.text.strip()
                    # Проверяем, что URL принадлежит тому же домену
                    if SitemapParser._is_same_domain(url, base_url):
                        urls.append(url)
                        
        except ET.ParseError:
            pass  # Не валидный XML
        
        return urls
    
    @staticmethod
    def _is_same_domain(url: str, base_url: str) -> bool:
        try:
            parsed_url = urlparse(url)
            parsed_base = urlparse(base_url)
            return parsed_url.netloc == parsed_base.netloc
        except Exception:
            return False


class HtmlParser:
    
    @staticmethod
    def extract_links(html: str, base_url: str) -> list[str]:
        links: list[str] = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            for tag in soup.find_all('a', href=True):
                href = tag['href']
                if not isinstance(href, str):
                    continue
                href = href.strip()
                if href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                    continue
                absolute_url = urljoin(base_url, href)
                if HtmlParser._is_same_domain(absolute_url, base_url):
                    clean_url = absolute_url.split('#')[0]
                    if clean_url not in links:
                        links.append(clean_url)
                        
        except Exception:
            pass
        
        return links
    
    @staticmethod
    def _is_same_domain(url: str, base_url: str) -> bool:
        try:
            parsed_url = urlparse(url)
            parsed_base = urlparse(base_url)
            return parsed_url.netloc == parsed_base.netloc
        except Exception:
            return False
