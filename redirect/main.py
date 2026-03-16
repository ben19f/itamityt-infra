from fastapi import FastAPI
from models import Base
from routers.links_router import router as links_router
from database import engine  # только движок
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(title="Itamityt Redirect Service")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# подключаем роутер
app.include_router(links_router)