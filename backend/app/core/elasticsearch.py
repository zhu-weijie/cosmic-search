import time
from elasticsearch import Elasticsearch, ConnectionError as ESConnectionError


def get_es_client():
    max_retries = 15
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            # Using 127.0.0.1 is slightly more explicit than localhost
            client = Elasticsearch("http://127.0.0.1:9200")

            if client.ping():
                print("Successfully connected to Elasticsearch.")
                return client
        except ESConnectionError:
            print(
                f"Connection failed. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})"
            )
            time.sleep(retry_delay)

    raise ConnectionError("Could not connect to Elasticsearch after several attempts.")
