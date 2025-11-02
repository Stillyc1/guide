from core.schemas.base import Base


class BuildingSchema(Base):
    address: str
    latitude: float
    longitude: float
