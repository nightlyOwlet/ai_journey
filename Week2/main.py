from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class LicenseUsed(Enum):
    Cdl = "cdl"
    NonCdl = "non_cdl"
    NoDriving = "no_driving"
    Unclear = "unclear"


class HistoricalEntryType(Enum):
    School = "school"
    Employment = "employment"
    SelfEmployed = "self_employed"
    Military = "military"
    Other = "other"


class YearMonth(BaseModel):
    year: int = Field(..., ge=1950, le=2100, description="Four-digit year, e.g. 2021")
    month: Optional[int] = Field(..., ge=1, le=12, description="Month number 1-12; null if the source gives only the year or a season")

    @model_validator(mode="after")
    def not_in_future(self):
        today = date.today()
        if (self.year, self.month or 1) > (today.year, today.month):
            raise ValueError(f"{self.month or '??'}-{self.year} is in the future")
        return self


class HistoricalEntry(BaseModel):
    type: HistoricalEntryType = Field(
        ...,
        description=(
            "Kind of entry: 'employment' (worked for an employer), 'self_employed' (own business, "
            "owner-operator or 1099 contractor), 'school' (any training or education, including CDL school), "
            "'military' (service in the armed forces), 'other' only if none of these apply"
        ),
    )
    name: Optional[str] = Field(..., description="Employer, school, business or military branch, as written; null if not given")
    position: Optional[str] = Field(..., description="Job title, role or program, as written; null if not given")
    is_current: bool = Field(..., description="True if the source says this entry is ongoing (e.g. 'present', or a start date with no end); otherwise false")
    dates_as_written: Optional[str] = Field(..., description="The dates for this entry copied exactly from the source; null if no dates are given")
    start_month: Optional[YearMonth] = Field(..., description="When this entry started; null if not given or too vague to place in a year")
    end_month: Optional[YearMonth] = Field(..., description="When this entry ended; null if it is current or the end is not given")
    license_used: LicenseUsed = Field(
        ...,
        description=(
            "License used for driving in this entry: "
            "'cdl' if they drove using a CDL; "
            "'non_cdl' if they drove on public roads for this entry without a CDL (including in a personal vehicle); "
            "'no_driving' if driving on public roads was not part of this entry (on-property driving such as forklifts or yard trucks counts as no_driving); "
            "'unclear' if they drove but the source doesn't say whether a CDL was used, or it can't be told whether they drove"
        ),
    )
    reason_for_leaving: Optional[str] = Field(..., description="Why this entry ended, as written; null if not given")

    @model_validator(mode="after")
    def check_dates(self):
        if self.is_current and self.end_month is not None:
            raise ValueError("a current entry cannot have an end_month")
        s, e = self.start_month, self.end_month
        if s and e:
            if s.month is None or e.month is None:
                before = e.year < s.year
            else:
                before = (e.year, e.month) < (s.year, s.month)
            if before:
                raise ValueError("end_month is before start_month")
        return self


class DriverProfile(BaseModel):
    name: str = Field(..., description="Applicant's full name, as written")
    history: list[HistoricalEntry] = Field(..., description="Every employment, self-employment, school, military or other entry in the source, in the order given")


def main():
    # Example usage of the DriverProfile model
    example_profile = DriverProfile(
        name="Mark",
        history=[
            HistoricalEntry(
                type=HistoricalEntryType.Employment,
                name="Company A",
                position="Driver",
                is_current=False,
                dates_as_written="January 2020 - June 2022",
                start_month=YearMonth(year=2020, month=1),
                end_month=YearMonth(year=2022, month=6),
                license_used=LicenseUsed.Cdl,
                reason_for_leaving="Career advancement",
            ),
        ],
    )

    print(example_profile.model_dump_json(indent=4))


# This starts the script
if __name__ == "__main__":
    main()
