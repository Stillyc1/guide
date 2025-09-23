from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from .organization import Organization


class PhoneNumber(Base):
    """Модель номера телефона."""
    __tablename__ = "phone_numbers"

    number: Mapped[str] = mapped_column(
        String(11),
        comment="Номер телефона"
    )
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id")
    )
    organization: Mapped["Organization"] = relationship(
        back_populates="phone_numbers"
    )
