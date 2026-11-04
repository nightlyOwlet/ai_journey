
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from enum import Enum

class CommercialDriving(Enum):
    Yes = "yes"
    No = "no"
    Unclear = "unclear"

class YearMonth(BaseModel):
    year: int = Field(..., ge=1950, le=2026)
    month: Optional[int] = Field(..., ge=1, le=12)

class PastEmployer(BaseModel):
    name: str
    position: str
    start_month: Optional[YearMonth] = Field(..., description="Month and year the driver started this job; month null if only the year is given")
    end_month: Optional[YearMonth] = Field(..., description="Month and year the driver ended this job; month null if only the year is given")
    commercial_driving: CommercialDriving = Field(..., description="Driving was part of the job, whether or not a CDL was required; 'unclear' if the source doesn't say")
    reason_for_leaving: Optional[str] = Field(..., description="Reason for leaving the employer")


class DriverProfile(BaseModel):
    # Required fields
    name: str
    employers: list[PastEmployer]  

def main():
    # Example usage of the DriverProfile model
    example_profile = DriverProfile(
        name="Mark",
        employers=[
            PastEmployer(
                name="Company A",
                position="Driver",
                start_month=YearMonth(year=2020, month=1),
                end_month=YearMonth(year=2022, month=6),
                commercial_driving=CommercialDriving.Yes,
                reason_for_leaving="Career advancement"
            ),
            PastEmployer(
                name="Company B",
                position="Delivery Driver",
                start_month=YearMonth(year=2018, month=5),
                end_month=YearMonth(year=2019, month=12),
                commercial_driving=CommercialDriving.Unclear,
                reason_for_leaving="Relocation"
            )
        ]
    )

    print(example_profile.model_dump_json(indent=4))

# This starts the script
if __name__ == "__main__":
    main()