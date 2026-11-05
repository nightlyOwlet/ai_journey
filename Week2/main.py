
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from enum import Enum

class DrivingLicense(Enum):
    Cdl = "cdl"
    NonCdl = "non-cdl"
    NA = "NA"
class HistoricalEntryType(Enum):
    School = "School"
    Employment = "Employment"
    Military = "Military"
    Other = "Other"
    SelfEmployed = "Self-Employed"

class YearMonth(BaseModel):
    year: int = Field(..., ge=1950, le=2026)
    month: Optional[int] = Field(..., ge=1, le=12)

class HistoricalEntry(BaseModel):
    is_current: bool = Field(..., description="True if this is the current position, false if it is a past position")
    name: Optional[str]
    position: Optional[str]
    type: HistoricalEntryType = Field(..., description="Type of historical entry (e.g., School, Employment, Military. Use Other of none of the above apply)")
    dates_as_written: str
    start_month: Optional[YearMonth] = Field(..., description="Month and year the driver started this job; month null if only the year is given")
    end_month: Optional[YearMonth] = Field(..., description="Month and year the driver ended this job; month null if only the year is given")
    commercial_driving: DrivingLicense = Field(..., description="Driving was part of the job, whether or not a CDL was required; 'unclear' if the source doesn't say")
    reason_for_leaving: Optional[str] = Field(..., description="Reason for leaving the employer")

class DriverProfile(BaseModel):
    # Required fields
    name: str
    employers: list[HistoricalEntry]  

def main():
    # Example usage of the DriverProfile model
    example_profile = DriverProfile(
        name="Mark",
        employers=[
            HistoricalEntry(
                type=HistoricalEntryType.Employment,
                is_current=False,
                name="Company A",
                position="Driver",
                dates_as_written="January 2020 - June 2022",
                start_month=YearMonth(year=2020, month=1),
                end_month=YearMonth(year=2022, month=6),
                commercial_driving=DrivingLicense.Cdl,
                reason_for_leaving="Career advancement"
            )
        ]
    )

    print(example_profile.model_dump_json(indent=4))

# This starts the script
if __name__ == "__main__":
    main()