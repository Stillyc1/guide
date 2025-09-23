from typing import TYPE_CHECKING

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from .organization import Organization


class Building(Base):
    """Модель здания."""
    __tablename__ = "buildings"

    address: Mapped[str] = mapped_column(
        String,
        comment='Адрес здания'
    )
    latitude: Mapped[float] = mapped_column(
        Float,
        comment='Широта'
    )
    longitude: Mapped[float] = mapped_column(
        Float,
        comment='Долгота'
    )
    organizations: Mapped[list["Organization"]] = relationship(
        back_populates="building"
    )
