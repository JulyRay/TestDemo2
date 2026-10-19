from fastapi import FastAPI, Query


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.get("/planner-health")
def health():
    return {"status": "ok", "planner_version": 1}


@app.get("/planner-echo")
def echo(text: str = Query(..., min_length=1, max_length=16)):
    return {"text": text}
