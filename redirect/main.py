from fastapi import FastAPI, HTTPException, Request, Depends
from starlette.responses import RedirectResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import settings
from models import Base
from crud import get_link, log_click
from routers import links_router  # наш CRUD для ссылок

DATABASE_URL = settings.database_url

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI(title="Itamityt Redirect Service")

async def get_db():
    async with async_session() as session:
        yield session

# Подключаем роуты CRUD ссылок
app.include_router(links_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/rserv/{link_id}")
async def redirect_link(link_id: str, request: Request, db: AsyncSession = Depends(get_db)):
    link = await get_link(db, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    await log_click(db, link_id, request.client.host, request.headers.get("user-agent"))

    return RedirectResponse(url=link.original_url)