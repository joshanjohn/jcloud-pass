from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Metadata(BaseModel):
    created: datetime
    updated: Optional[datetime]
    size: Optional[float] = 0
    path: str