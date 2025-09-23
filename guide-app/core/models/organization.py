from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base, organization_activities_table

if TYPE_CHECKING:
    from .phone_number import PhoneNumber
    from .building import Building
    from .activity import Activity


class Organization(Base):
    """Модель организации."""
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(
        String,
        comment='Название организации'
    )
    phone_numbers: Mapped[list["PhoneNumber"]] = relationship(
        back_populates="organization"
    )
    building_id: Mapped[int] = mapped_column(
        ForeignKey("buildings.id")
    )
    building: Mapped["Building"] = relationship(
        back_populates="organizations"
    )
    activities: Mapped[list["Activity"]] = relationship(
        secondary=organization_activities_table,
        back_populates="organizations"
    )
