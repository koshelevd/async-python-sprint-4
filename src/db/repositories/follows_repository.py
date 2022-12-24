from db.repositories.base_repository import RepositoryBase
from db.tables import Follow


class FollowRepository(RepositoryBase):
    """Follow repository"""

    model = Follow
