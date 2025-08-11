from fastapi import FastAPI
from backend.app.api import search

app = FastAPI(title="CosmicSearch API")

app.include_router(search.router, prefix="/api/v1", tags=["search"])


@app.get("/")
def read_root():
    return {"message": "Welcome to CosmicSearch API. Visit /docs for documentation."}
