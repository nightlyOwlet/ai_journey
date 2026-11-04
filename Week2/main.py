
from typing import Optional
from pydantic import BaseModel, Field

# 1. Define the model schema
class DriverProfile(BaseModel):
    # Required fields
    name: int
    employers: list[PastEmployer]  

class PastEmployer(BaseModel):
    name: str
    position: str
    start_month: Optional[str] = Field(None, description="Start month in YYYY-MM format")
    end_month: Optional[str] = Field(None, description="End month in YYYY-MM format")
    commercial_driving: bool
    reason_for_leaving: Optional[str] = Field(None, description="Reason for leaving the employer")

