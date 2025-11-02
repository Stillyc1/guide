from typing import Optional

from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    id: Optional[int]
    model_config = ConfigDict(from_attributes=True)
