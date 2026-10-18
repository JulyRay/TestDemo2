"""Bounded text echo API for the Draft-only QA repair experiment."""
from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/bounded-echo")
def bounded_echo(text: str = Query(..., min_length=1, max_length=64)):
    return {"text": text}
