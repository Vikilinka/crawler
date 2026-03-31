import os

from pydantic import HttpUrl, UUID4
from requests import Session

from apps.vikon.core.tools.api.request import get, post
from apps.vikon.core.tools.api.response import res_to_html


def get_vikon_token(domain: HttpUrl) -> UUID4:
    s = Session()
    get_login_res = get(f'{domain}/login', session=s)
    csrf_token = res_to_html(get_login_res).find(id="login_form__csrf_token").attrs['value']
    data = {
        'login_form[email]': os.getenv('VIKON_EMAIL'),
        'login_form[password]': os.getenv('VIKON_PASSWORD'),
        '_remember_me': 'off',
        'login_form[_csrf_token]': csrf_token,
    }
    post(f'{domain}/login', data=data, session=s)
    get_token_res = get(f'{domain}/editor/settings/api_key/tokenToApi', session=s)
    api_token = get_token_res.json()['access_token']
    return api_token
