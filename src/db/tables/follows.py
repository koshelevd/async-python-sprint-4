from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.tables.base import BaseModel


class Follow(BaseModel):
    """Model stores info about following a link."""

    __tablename__ = "follows"

    link_id = Column(
        Integer, ForeignKey("links.id"), nullable=False, comment="Link ID"
    )
    link = relationship(
        "Link", back_populates="follows", remote_side="Link.id", lazy="noload"
    )

    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=True, comment="User ID"
    )
    user = relationship(
        "User", back_populates="follows", remote_side="User.id", lazy="noload"
    )

    def __repr__(self):
        return f"<Follow(id={self.id}, link_id={self.link_id})>"
