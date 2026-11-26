
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CHAR,
    DateTime,
    ForeignKey,
    Index,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class ApiClient(Base):
    __tablename__ = "api_clients"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    key_hash: Mapped[str] = mapped_column(
        CHAR(64), nullable=False, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    links: Mapped[list["Link"]] = relationship(back_populates="client")


class Link(Base):
    __tablename__ = "links"

    __table_args__ = (
        Index("idx_links_client", "client_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    code: Mapped[str | None] = mapped_column(
        String(16), nullable=True, unique=True
    )
    long_url: Mapped[str] = mapped_column(
        String(2048), nullable=False
    )
    client_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("api_clients.id"),
        nullable=False,
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    client: Mapped["ApiClient"] = relationship(back_populates="links")
    clicks: Mapped[list["Click"]] = relationship(back_populates="link")


class Click(Base):
    __tablename__ = "clicks"

    __table_args__ = (
        Index("idx_clicks_link_time", "link_id", "clicked_at"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    link_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("links.id"),
        nullable=False,
    )
    clicked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False
    )
    referrer: Mapped[str | None] = mapped_column(
        String(512), nullable=True
    )
    user_agent: Mapped[str | None] = mapped_column(
        String(512), nullable=True
    )
    ip_hash: Mapped[str | None] = mapped_column(
        CHAR(64), nullable=True
    )

    link: Mapped["Link"] = relationship(back_populates="clicks")
