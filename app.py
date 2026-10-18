"""Draft-only static review fixture: intentional unbounded input retention."""
from fastapi import FastAPI, Query

app = FastAPI()
RETAINED_INPUTS: list[str] = []


@app.get("/bounded-echo")
def bounded_echo(text: str = Query(..., min_length=1, max_length=64)):
    RETAINED_INPUTS.append(text)
    return {"text": text}
