from models import Link, Click
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def get_link(db: AsyncSession, link_id: str):
    result = await db.execute(select(Link).where(Link.link_id == link_id))
    return result.scalars().first()

async def log_click(db: AsyncSession, link_id: str, ip: str, user_agent: str):
    click = Click(link_id=link_id, ip=ip, user_agent=user_agent)
    db.add(click)
    await db.commit()
    return click
