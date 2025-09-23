from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint

from .base import Base

organization_activities_table = Table(
    "organization_activities",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("organization_id", ForeignKey("organizations.id"), nullable=False),
    Column("activity_id", ForeignKey("activities.id"), nullable=False),
    UniqueConstraint("organization_id", "activity_id", name="idx_unique_organization_activity")
)
