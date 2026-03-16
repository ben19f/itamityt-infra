from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud import get_link, log_click
from database import get_db  # теперь импорт из database.py, без цикла

router = APIRouter()

@router.get("/r/{link_id}")
async def redirect_link(link_id: str, request: Request, db: AsyncSession = Depends(get_db)):
    link = await get_link(db, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    await log_click(db, link_id, request.client.host, request.headers.get("user-agent"))

    return RedirectResponse(url=link.original_url)