from typing import List

from core.schemas.activity import ActivitySchema
from core.schemas.base import Base
from core.schemas.building import BuildingSchema
from core.schemas.phone_number import PhoneNumberSchema


class OrganizationSchema(Base):
    name: str
    phone_numbers: List[PhoneNumberSchema] = []
    building: BuildingSchema
    activities: List[ActivitySchema] = []
