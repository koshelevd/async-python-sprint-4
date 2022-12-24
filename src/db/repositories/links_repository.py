from sqlalchemy import insert, select

from db.repositories.base_repository import RepositoryBase
from db.tables import Link, User


class LinkRepository(RepositoryBase):
    """Link repository"""

    model = Link

    async def ping(self) -> bool:
        """Ping"""
        query = select(Link.id).limit(1)
        expr = await self.session.execute(query)
        return expr.scalars().all()

    async def batch_create(
        self, links: list[dict[str, User | None]]
    ) -> list[Link]:
        """Batch create"""
        query = insert(Link).returning(Link).values(links)
        expr = await self.session.execute(query)
        return expr.scalars().all()
