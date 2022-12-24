from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories import FollowRepository, LinkRepository
from db.utils.db_session import get_session
from services import LinkService


async def get_link_repository(
    session: AsyncSession = Depends(get_session),
) -> LinkRepository:
    return LinkRepository(session)


async def get_follow_repository(
    session: AsyncSession = Depends(get_session),
) -> FollowRepository:
    return FollowRepository(session)


async def get_link_service(
    link_repository: LinkRepository = Depends(get_link_repository),
    follow_repository: FollowRepository = Depends(get_follow_repository),
) -> LinkService:
    return LinkService(
        link_repository=link_repository, follow_repository=follow_repository
    )
