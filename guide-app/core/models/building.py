from typing import TYPE_CHECKING, List

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .organization import Organization


class Building(Base):
    """Модель здания."""
    __tablename__ = "buildings"

    address: Mapped[str] = mapped_column(
        String(512),
        comment="Адрес здания",
    )
    latitude: Mapped[float] = mapped_column(
        Float(precision=10, asdecimal=False),
        comment="Широта",
    )
    longitude: Mapped[float] = mapped_column(
        Float(precision=10, asdecimal=False),
        comment="Долгота",
    )
    organizations: Mapped[List["Organization"]] = relationship(
        back_populates="building",
        cascade="all, delete-orphan",
    )

    def __str__(self) -> str:
        return f"{self.address}"
