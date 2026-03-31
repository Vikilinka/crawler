import os

from elasticsearch import Elasticsearch

authority = f'{os.getenv('ELASTIC_USERNAME')}:{os.getenv('ELASTIC_PASSWORD')}'
host = os.getenv('DSA_SEARCH_HOST')
port = 9200
es = Elasticsearch(f"https://{authority}@{host}:{port}", verify_certs=False)
