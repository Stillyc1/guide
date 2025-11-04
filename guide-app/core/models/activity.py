from typing import Optional, TYPE_CHECKING, List

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
        index=True,
    )
    parent: Mapped[Optional["Activity"]] = relationship(
        "Activity",
        remote_side="Activity.id",
        back_populates="child_activities"
    )

    child_activities: Mapped[List["Activity"]] = relationship(
        "Activity",
        back_populates="parent",
        cascade="all, delete-orphan",
    )
    level: Mapped[int] = mapped_column(
        Integer,
        default=1,
        comment="Уровень вложенности",
        index=True,
    )
    organizations: Mapped[List["Organization"]] = relationship(
        secondary=organization_activities_table,
        back_populates="activities",
        lazy="selectin",
    )

    def __str__(self) -> str:
        return f"{self.name} (уровень {self.level})"

    def update_levels(self, parent_level: int = 0) -> None:
        self.level = parent_level + 1
        for child in self.child_activities:
            child.update_levels(self.level)

    def validate_level(self) -> bool:
        if self.level > 3:
            return False
        if self.parent and self.parent.level >= 3:
            return False
        return True
