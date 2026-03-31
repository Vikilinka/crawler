from essentials.elastic.search import es


class ElasticClient:
    def test(self) -> str:
        return str(es.info())
