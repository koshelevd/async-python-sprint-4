from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.tables.base import BaseModel
from dto.links_schemas import LinkType


class Link(BaseModel):
    """URL short link model."""

    __tablename__ = "links"

    original_url = Column(String(255), nullable=False, comment="Original URL")

    link_type = Column(
        Enum(LinkType, name='link_type'), default=LinkType.public,
        nullable=False, comment="Link type"
    )

    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=True, comment="User"
    )
    user = relationship(
        "User", back_populates="links", remote_side="User.id", lazy="noload"
    )

    follows = relationship("Follow", back_populates="link", lazy="noload",
                           cascade="all, delete",
                           passive_deletes=True, )

    def __repr__(self):
        return (f"<Link(id={self.id}, original_url={self.original_url}, "
                f"link_type={self.link_type}, user={self.user})>")
