from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import get_link, create_link
from schemas import LinkCreate, LinkOut
from main import get_db

links_router = APIRouter(prefix="/links", tags=["links"])

@links_router.post("/", response_model=LinkOut, status_code=201)
async def add_link(link: LinkCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_link(db, link.link_id)
    if existing:
        raise HTTPException(status_code=400, detail="Link already exists")

    new_link = await create_link(
        db,
        link_id=link.link_id,
        original_url=link.original_url,
        owner_user_id=link.owner_user_id
    )
    return new_link