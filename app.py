"""Small quality-check API."""

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/health-quality")
def health_quality():
    return {"status": "ok", "quality_version": 1}


@app.get("/echo")
def echo(text: str = Query(..., min_length=1, max_length=40)):
    return {"text": text}
