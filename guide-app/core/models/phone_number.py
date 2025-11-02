from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .organization import Organization


class PhoneNumber(Base):
    """Модель номера телефона."""
    __tablename__ = "phone_numbers"

    number: Mapped[str] = mapped_column(
        String(11),
        nullable=False,
        comment="Номер телефона в формате 79991234567"
    )
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    organization: Mapped["Organization"] = relationship(
        back_populates="phone_numbers",
        lazy="selectin"
    )

    def __str__(self) -> str:
        return self.number
