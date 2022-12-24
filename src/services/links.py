from pydantic import HttpUrl
from sqlalchemy.exc import SQLAlchemyError

from utils.const import get_short_url
from db.repositories import FollowRepository, LinkRepository
from db.tables import Link, User
from dto.links_schemas import (
    LinkDTO,
    LinkStatusDTO,
    LinkType,
    PingStatus,
    ShortLinkEntity,
    ShortURLEntity,
)
from services.base_service import BaseService
from services.exceptions import (
    NotAuthorizedException,
    NotFoundValueException,
    ObjectIsGoneException,
)


class LinkService(BaseService):
    """Service for link creation."""

    model = Link

    def __init__(
        self,
        *,
        link_repository: LinkRepository,
        follow_repository: FollowRepository,
    ):
        self.link_repo = link_repository
        self.follow_repo = follow_repository
        super().__init__(obj_repo=self.link_repo)

    async def create_short_link(
        self,
        original_url: HttpUrl,
        link_type: LinkType | None,
        user: User | None,
    ) -> ShortLinkEntity:
        """
        Create short link.

        :param url: URL to shorten
        :param user: authorized user (optional)
        :return: created link
        """
        link_type = link_type if user else LinkType.public
        link = self.link_repo.create(
            original_url=original_url, user=user, link_type=link_type
        )
        self.link_repo.session.add(link)
        try:
            await self.link_repo.session.commit()
        except SQLAlchemyError:
            await self.link_repo.session.rollback()
            raise
        result = ShortLinkEntity(short_link=get_short_url(link.id))
        return result

    async def update_short_link(
        self,
        link_id: int,
        original_url: HttpUrl,
        link_type: LinkType,
        user: User | None,
    ) -> ShortLinkEntity:
        """
        Update short link.

        :param link_id: short link id
        :param original_url: URL to shorten
        :param user: authorized user (optional)
        :return: created link
        """
        link = await self.link_repo.get_by_id(link_id)
        if not link or link.is_deleted:
            raise NotFoundValueException(["link_id"])
        if user is None or link.user_id != user.id:
            raise NotAuthorizedException()
        link.original_url = original_url
        link.link_type = link_type
        try:
            await self.link_repo.session.commit()
        except SQLAlchemyError:
            await self.link_repo.session.rollback()
            raise
        result = ShortLinkEntity(short_link=get_short_url(link.id))
        return result

    async def get_original_link(self, link_id: int, user: User | None) -> Link:
        """
        Get original link by short link id. Save follow event.

        :param link_id: short link id
        :param user: authorized user (optional)
        :return: original link
        """
        link = await self.link_repo.get_by_id(link_id)
        if not link:
            raise NotFoundValueException(["link_id"])
        if link.is_deleted:
            raise ObjectIsGoneException(context=f"link_id: {link_id}")
        follow = self.follow_repo.create(link=link, user=user)
        self.follow_repo.session.add(follow)
        try:
            await self.follow_repo.session.commit()
        except SQLAlchemyError:
            await self.follow_repo.session.rollback()
            raise
        return link

    async def get_link_status(
        self, link_id: int, full_info: bool, max_result: int, offset: int
    ) -> list[LinkStatusDTO] | int:
        """
        Get link's status info.

        :param link_id: short link id
        :param full_info: flag for full info
        :param max_result: max result
        :param offset: offset
        :return: link
        """
        if not await self.link_repo.is_exists(id=link_id):
            raise NotFoundValueException(["link_id"])
        if not full_info:
            follows = await self.follow_repo.get_all(link_id=link_id)
            return len(follows)
        follows = await self.follow_repo.get_all(
            link_id=link_id, limit=max_result, offset=offset
        )
        result = [
            LinkStatusDTO(
                redirect_timestamp=follow.created_at, user=follow.user
            )
            for follow in follows
        ]
        return result

    async def ping(self):
        """Check service DB availability."""
        try:
            await self.link_repo.ping()
        except SQLAlchemyError:
            raise
        return PingStatus()

    async def delete_short_link(self, link_id: int, user) -> None:
        """
        Delete short link.

        :param link_id: short link id
        :return: None
        """
        link = await self.link_repo.get_by_id(link_id)
        if not link or link.is_deleted or link.user != user:
            raise NotFoundValueException(["link_id"])
        await self.link_repo.delete(link_id)
        try:
            await self.link_repo.session.commit()
        except SQLAlchemyError:
            await self.link_repo.session.rollback()
            raise

    async def batch_create_short_links(
        self, urls: list[LinkDTO], user: User | None
    ) -> list[ShortURLEntity]:
        """
        Create short links.

        :param urls: URLs to shorten
        :param user: authorized user (optional)
        :return: created links
        """
        data = [
            {
                "original_url": url.original_url,
                "user_id": user.id if user else None,
            }
            for url in urls
        ]
        links = await self.link_repo.batch_create(data)
        result = [
            ShortURLEntity(short_url=get_short_url(link.id), url_id=link)
            for link in links
        ]
        return result
