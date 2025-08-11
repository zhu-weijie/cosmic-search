from elasticsearch import Elasticsearch


def get_es_client():
    client = Elasticsearch("http://localhost:9200")
    if not client.ping():
        raise ConnectionError("Could not connect to Elasticsearch")
    return client
