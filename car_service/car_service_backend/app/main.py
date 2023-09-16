"""Entry point for FastAPI REST"""

from typing import Union

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator 

app = FastAPI()
instrumentator = Instrumentator().instrument(app)

@app.get("/")
def read_root():
    return {"Hello": "World!"}


@app.on_event("startup")
async def _startup():
    instrumentator.expose(app)
