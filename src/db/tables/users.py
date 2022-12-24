from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import relationship

from db.tables.base import BaseModel


class User(BaseModel):
    """User model."""

    __tablename__ = "users"

    email = Column(String(255), nullable=False, comment="Email")
    password = Column(String(255), nullable=False, comment="Password")

    links = relationship("Link", back_populates="user", lazy="noload")
    follows = relationship("Follow", back_populates="user", lazy="noload")

    __table_args__ = (
        UniqueConstraint(
            "email",
        ),
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
