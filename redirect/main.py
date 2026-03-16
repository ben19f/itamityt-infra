from fastapi import FastAPI, HTTPException, Request, Depends
from starlette.responses import RedirectResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import settings

DATABASE_URL = settings.database_url

# import os

from models import Base
from crud import get_link, log_click

# DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI(title="Itamityt Redirect Service")

async def get_db():
    async with async_session() as session:
        yield session

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # создаем таблицы, если их нет
        await conn.run_sync(Base.metadata.create_all)

@app.get("/r/{link_id}")
async def redirect_link(link_id: str, request: Request, db: AsyncSession = Depends(get_db)):
    link = await get_link(db, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    # Логируем клик
    await log_click(db, link_id, request.client.host, request.headers.get("user-agent"))

    return RedirectResponse(url=link.original_url)
