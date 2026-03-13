from fastapi import FastAPI
from app.api.router import router

app = FastAPI(
    title="itamityt API"
)

app.include_router(router)