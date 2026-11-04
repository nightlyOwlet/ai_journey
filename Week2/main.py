
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime

class PastEmployer(BaseModel):
    name: str
    position: str
    start_month: Optional[str] = Field(None, description="Start month in MM-YYYY format")
    end_month: Optional[str] = Field(None, description="End month in MM-YYYY format")
    commercial_driving: bool
    reason_for_leaving: Optional[str] = Field(None, description="Reason for leaving the employer")

    @field_validator("start_month", "end_month",  mode="before")
    @classmethod
    def validate_mm_yyyy(cls, value):
        # If it's already a date object, pass it through
        if isinstance(value, date):
            return value
        
        # If it's a string, try parsing it from the MM-YYYY format
        if isinstance(value, str):
            try:
                # parsed date defaults to the 1st day of that month
                return str(datetime.strptime(value, "%m-%Y").date())
            except ValueError:
                raise ValueError("Date must be in MM-YYYY format (e.g., 12-2026)")
        
        if value is None:
            return None

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
                start_month="01-2020",
                end_month="06-2021",
                commercial_driving=True,
                reason_for_leaving="Career advancement"
            ),
            PastEmployer(
                name="Company B",
                position="Delivery Driver",
                start_month="05-2018",
                end_month="12-2019",
                commercial_driving=False,
                reason_for_leaving="Relocation"
            )
        ]
    )

    print(example_profile.model_dump_json(indent=4))

# This starts the script
if __name__ == "__main__":
    main()