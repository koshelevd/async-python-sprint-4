from datetime import datetime
from enum import Enum

from pydantic import HttpUrl

from dto.base import BaseSchema, ORMBaseSchema


class LinkType(str, Enum):
    """Link type."""

    public = "public"
    private = "private"


class BaseLinkSchema(ORMBaseSchema):
    original_url: HttpUrl


class LinkDTO(BaseLinkSchema):
    type: LinkType | None = LinkType.public


class ShortLinkEntity(ORMBaseSchema):
    short_link: HttpUrl


class LinkStatusDTO(ORMBaseSchema):
    redirect_timestamp: datetime
    user: str | None


class PingStatus(BaseSchema):
    status: str = "OK"


class ShortURLEntity(ORMBaseSchema):
    short_url: HttpUrl
    url_id: int


class UserStatusEntity(ORMBaseSchema):
    short_id: int
    short_url: HttpUrl
    original_url: HttpUrl
    type: LinkType
