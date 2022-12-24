from sqlalchemy import select

from db.repositories.base_repository import RepositoryBase
from db.tables import Link, User


class UserRepository(RepositoryBase):
    """User repository"""

    model = User

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Get user by email.

        :param email: users email
        :return: user
        """

        query = select(User).filter_by(email=email)
        expr = await self.session.execute(query)
        return expr.scalar_one_or_none()

    async def get_user_links(self, user_id: int) -> list[Link]:
        """
        Get user status.

        :param user_id: user id
        :return: user links
        """

        query = select(Link).filter_by(user_id=user_id)
        expr = await self.session.execute(query)
        return expr.scalars().all()
