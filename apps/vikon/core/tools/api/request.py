from typing import Any

from urllib3 import Retry

from pydantic import HttpUrl

from requests import Session, Response
from requests.adapters import HTTPAdapter


def get(url: HttpUrl, session: Session = None, **kwargs) -> Response:
    s = session or Session()
    try:
        retries = Retry(total=10,
                        backoff_factor=1,
                        backoff_max = 120,
                        status_forcelist=frozenset([413, 429, 503]),
                        backoff_jitter=5.0)
        s.mount(url, HTTPAdapter(max_retries=retries))
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 240
        res = s.get(url, **kwargs)
    finally:
        s.adapters.pop(url)
    return res

def post(url: HttpUrl, data: Any = None, json: Any = None, session: Session = None, **kwargs) -> Response:
    s = session or Session()
    if 'timeout' not in kwargs:
        kwargs['timeout'] = 60
    return s.post(url, data=data, json=json, **kwargs)

def delete(url: HttpUrl, session: Session = None, **kwargs) -> Response:
    s = session or Session()
    if 'timeout' not in kwargs:
        kwargs['timeout'] = 60
    return s.delete(url, **kwargs)
