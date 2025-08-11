from fastapi import APIRouter
from backend.app.core.elasticsearch import get_es_client

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

    response = es.search(
        index="apod",
        query=query,
        from_=skip,
        size=limit,
    )

    es.close()

    total_hits = response["hits"]["total"]["value"]
    hits = response["hits"].get("hits", [])

    return {
        "hits": hits,
        "total_hits": total_hits,
    }
