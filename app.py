from typing import Annotated

from fastapi import FastAPI, Query


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.get("/health")
def health() -> dict[str, str | int]:
    return {"status": "ok", "planner_version": 1}


@app.get("/echo")
def echo(text: Annotated[str, Query(min_length=1, max_length=16)]) -> dict[str, str]:
    return {"text": text}
