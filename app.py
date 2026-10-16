"""Minimal TestDemo2 application."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/health-extra")
def health_extra() -> dict[str, str]:
    return {"status": "ok"}
