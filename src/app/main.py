from fastapi import FastAPI
from src.app import routers


app = FastAPI(
    title="MLOps学習用",
    description="",
    version="0.1 beta"
    )

app.include_router(routers.router, prefix="", tags=[""])
