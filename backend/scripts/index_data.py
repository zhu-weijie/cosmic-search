import json
from tqdm import tqdm
from elasticsearch import Elasticsearch

from backend.app.core.config import INDEX_NAME_DEFAULT, INDEX_NAME_N_GRAM
from backend.app.core.elasticsearch import get_es_client


def create_index(es: Elasticsearch, index_name: str, use_n_gram: bool):
    es.indices.delete(index=index_name, ignore_unavailable=True)

    # Define a basic standard analyzer setting
    settings = {
        "analysis": {
            "analyzer": {"default": {"tokenizer": "standard", "filter": ["lowercase"]}}
        }
    }

    # Explicitly map fields and tell them to use the standard analyzer
    mappings = {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "standard",  # Explicitly use the standard analyzer
            },
            "explanation": {
                "type": "text",
                "analyzer": "standard",  # Explicitly use the standard analyzer
            },
            "date": {"type": "date"},
            "image_url": {"type": "keyword"},
        }
    }

    # For the N-Gram index, we still need the custom settings
    if use_n_gram:
        settings["analysis"]["analyzer"]["default"]["tokenizer"] = "n_gram_tokenizer"
        settings["analysis"]["tokenizer"] = {
            "n_gram_tokenizer": {
                "type": "edge_ngram",
                "min_gram": 1,
                "max_gram": 30,
                "token_chars": ["letter", "digit"],
            }
        }
        # N-gram fields also need to be explicitly defined as text
        mappings["properties"]["title"]["analyzer"] = "default"
        mappings["properties"]["explanation"]["analyzer"] = "default"

    es.indices.create(index=index_name, settings=settings, mappings=mappings)
    print(f"Index '{index_name}' created successfully with explicit field analyzers.")


def insert_documents(es: Elasticsearch, index_name: str, documents: list):
    operations = []
    for doc in tqdm(documents, desc=f"Indexing into {index_name}"):
        operations.append({"index": {"_index": index_name}})
        operations.append(doc)

    if operations:
        es.bulk(operations=operations)
        print(f"Indexed {len(documents)} documents into '{index_name}'.")


def main():
    with open("backend/data/sample_apod.json") as f:
        documents = json.load(f)

    es = get_es_client()

    # Index with standard tokenizer
    create_index(es, INDEX_NAME_DEFAULT, use_n_gram=False)
    insert_documents(es, INDEX_NAME_DEFAULT, documents)

    # Index with n-gram tokenizer
    create_index(es, INDEX_NAME_N_GRAM, use_n_gram=True)
    insert_documents(es, INDEX_NAME_N_GRAM, documents)

    es.close()


if __name__ == "__main__":
    main()
