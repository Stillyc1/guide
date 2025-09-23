from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .organization_activities_table import organization_activities_table

if TYPE_CHECKING:
    from .organization import Organization


class Activity(Base):
    """Модель вида деятельности."""
    __tablename__ = "activities"

    name: Mapped[str] = mapped_column(
        String,
        comment='Название деятельности'
    )
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("activities.id"),
        nullable=True,
    )
    parent: Mapped["Activity"] = relationship(
        back_populates="sub_activities",
    )
    level_parent: Mapped[int] = mapped_column(
        Integer,
        default=1,
        comment="Уровень вложенности"
    )
    sub_activities: Mapped[list["Activity"]] = relationship(
        back_populates="parent"
    )
    organizations: Mapped[list["Organization"]] = relationship(
        secondary=organization_activities_table,
        back_populates="activities",
    )
