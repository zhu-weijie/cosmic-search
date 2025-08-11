import json
from fastapi import APIRouter
from app.core.elasticsearch import get_es_client

router = APIRouter()


@router.get("/search")
def search(search_query: str, skip: int = 0, limit: int = 10):
    es = get_es_client()

    query = {
        "bool": {
            "must": [
                {
                    "multi_match": {
                        "query": search_query,
                        "fields": ["title", "explanation"],
                    }
                }
            ]
        }
    }

    print("--- Elasticsearch Query ---")
    print(json.dumps({"query": query}, indent=2))

    response = es.search(
        index="apod",
        body={
            "query": query,
            "from": skip,
            "size": limit,
        },
    )

    print("\n--- Elasticsearch Response ---")
    print(json.dumps(response.body, indent=2))

    es.close()

    total_hits = response["hits"]["total"]["value"]
    hits = response["hits"].get("hits", [])

    return {
        "hits": hits,
        "total_hits": total_hits,
    }
