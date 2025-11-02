from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint

from .base import Base

organization_activities_table = Table(
    "organization_activities",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("organization_id", Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True),
    Column("activity_id", Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False, index=True),
    UniqueConstraint("organization_id", "activity_id", name="uq_organization_activity"),
    comment="Связь многие-ко-многим между организациями и видами деятельности"
)
