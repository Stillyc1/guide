from typing import TYPE_CHECKING, List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .organization_activities_table import organization_activities_table

if TYPE_CHECKING:
    from .phone_number import PhoneNumber
    from .building import Building
    from .activity import Activity


class Organization(Base):
    """Модель организации."""
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(
        String(256),
        comment="Название организации"
    )
    phone_numbers: Mapped[List["PhoneNumber"]] = relationship(
        back_populates="organization"
    )
    building_id: Mapped[int] = mapped_column(
        ForeignKey("buildings.id", ondelete="CASCADE",),
        index=True,
    )
    building: Mapped["Building"] = relationship(
        back_populates="organizations"
    )
    activities: Mapped[List["Activity"]] = relationship(
        secondary=organization_activities_table,
        back_populates="organizations",
        lazy="selectin",
    )

    def __str__(self) -> str:
        return f"{self.name}"
