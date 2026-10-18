"""Small quality pilot API."""

from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/health-quality")
def health_quality() -> dict[str, str | int]:
    return {"status": "ok", "quality_version": 1}


@app.get("/echo")
def echo(text: Annotated[str, Query(min_length=1, max_length=40)]) -> dict[str, str]:
    return {"text": text}
