from fastapi import APIRouter, Depends
from fastapi.params import Query
from fastapi.responses import RedirectResponse

from api.depends import get_current_user, get_link_service
from db.tables import User
from dto.links_schemas import (
    LinkDTO,
    LinkStatusDTO,
    PingStatus,
    ShortLinkEntity,
    ShortURLEntity,
)
from services import LinkService

router = APIRouter()


@router.get(
    "/ping", summary="Check service DB availability", response_model=PingStatus
)
async def ping(link_service: LinkService = Depends(get_link_service)):
    """Check service DB availability."""
    return await link_service.ping()


@router.get("/{link_id}/status", summary="Get link's status info")
async def get_link_status(
    link_id: int,
    full_info: bool = Query(default=False, alias="full-info"),
    max_result: int = Query(default=10, alias="max-result"),
    offset: int = 0,
    link_service: LinkService = Depends(get_link_service),
) -> list[LinkStatusDTO] | int:
    """Get link's status info."""
    status = await link_service.get_link_status(
        link_id, full_info, max_result, offset
    )
    return status


@router.post("/", summary="Create short link", response_model=ShortLinkEntity)
async def create_short_link(
    data: LinkDTO,
    user: User | None = Depends(get_current_user),
    link_service: LinkService = Depends(get_link_service),
) -> ShortLinkEntity:
    """Create short link for passed url."""
    link = await link_service.create_short_link(
        original_url=data.original_url, link_type=data.type, user=user
    )
    return link


@router.patch("/{link_id}", summary="Update short link")
async def update_short_link(
    link_id: int,
    data: LinkDTO,
    user: User | None = Depends(get_current_user),
    link_service: LinkService = Depends(get_link_service),
) -> None:
    """Update short link."""
    await link_service.update_short_link(
        link_id, data.original_url, data.type, user
    )


@router.get(
    "/{link_id}", summary="Get original link", response_class=RedirectResponse
)
async def get_original_link(
    link_id: int,
    user: User | None = Depends(get_current_user),
    link_service: LinkService = Depends(get_link_service),
) -> RedirectResponse:
    """Get original link by short link id."""
    link = await link_service.get_original_link(link_id, user)
    return link.original_url


@router.delete("/{link_id}", summary="Delete short link")
async def delete_short_link(
    link_id: int,
    user: User | None = Depends(get_current_user),
    link_service: LinkService = Depends(get_link_service),
) -> None:
    """Delete short link by id."""
    await link_service.delete_short_link(link_id, user)
    return None


@router.post(
    "/shorten",
    summary="Batch create short links",
    response_model=list[ShortURLEntity],
)
async def batch_create_short_links(
    data: list[LinkDTO],
    user: User | None = Depends(get_current_user),
    link_service: LinkService = Depends(get_link_service),
) -> list[ShortURLEntity]:
    """Batch short link creating."""
    links = await link_service.batch_create_short_links(data, user)
    return links
