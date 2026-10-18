"""Controlled Draft-only QA repair fixture; initial upper-bound defect is intentional."""
from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/bounded-echo")
def bounded_echo(text: str = Query(..., min_length=1, max_length=63)):
    return {"text": text}
