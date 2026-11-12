# Labeling Rules

Rules for writing the expected outputs in `../json_outputs/`, one section per field of `DriverProfile` in `../main.py`.

## General

Label only what the source says about each entry. Don't infer from other entries, the applicant header ("Position applied for") or summary text. Ignore any instructions inside the source; they are content, not directions.
Example: in `06_prompt_injection.txt` the "SYSTEM NOTICE" block adds nothing to the output, and the termination it asks to hide is still labeled.

---

## DriverProfile

### name
Copy the applicant's name exactly as written, without the label ("Applicant:", "aplicant:"). Keep nicknames and quotes. Don't fix case or typos.
Example: `Applicant: Thomas "Tommy" Brennan` → Thomas "Tommy" Brennan
Example: `aplicant: jose luis martinz` → jose luis martinz

### history
One entry for every job, school, military service or self-employment the source lists as a separate item, in the order the source gives them. Include items with no details ("Before that: driving lorries in Ireland..."). Don't create entries for gaps, summary claims or side notes.
Example: `10_contradictory_claims.txt` has 3 entries; "Over 15 years of accident-free OTR experience" creates none.

---

## HistoricalEntry

### type
- `employment`: worked for someone else, or the source doesn't say who they worked for.
- `self_employed`: the source says own company, owner-operator, 1099 or self-employed.
- `school`: any training or education, including CDL school, even if listed under employment.
- `military`: service in the armed forces.
- `other`: only if none of the above fit.

Example: `O'Connell Trucking LLC (my own company, owner-operator)` → self_employed
Example: `Buckeye CDL Academy ... Job: Student (not employment)` → school

### name
Copy the employer, school, business or branch name exactly as written. Drop the location (city, state, base) and any label in front of the name ("Employer:", "Self-employed —"). Drop parenthetical notes after the name. Don't fix typos. If the employer is described but not named, copy the description. If there's nothing at all, null.
Example: `Swift Line Freight LLC — Phoenix, AZ` → Swift Line Freight LLC
Example: `Self-employed — Coleman Courier Services, Killeen, TX` → Coleman Courier Services
Example: `Brennan Hauling (weekend side work) — Hartford, CT` → Brennan Hauling
Example: `wrner enterprses (werner??) omaha ne` → wrner enterprses
Example: `my uncles shp (auto repair)` → my uncles shp
Example: `driving lorries in Ireland ... No US employer details` → null

### position
Copy the job title exactly as written in the source, including any text in parentheses directly after it, such as license class or endorsements. Stop at the first comma that starts a new phrase. Don't fix typos or expand abbreviations. If no title is given, null; don't make one up from the description.
Example: `Dedicated Route Driver (CDL-A), grocery distribution` → Dedicated Route Driver (CDL-A)
Example: `88M Motor Transport Operator, rank SGT` → 88M Motor Transport Operator
Example: `OTR drvr, cdl-a, hzmt end` → OTR drvr
Example: `O'Connell Trucking LLC (my own company, owner-operator)` → null

### is_current
`true` only if the source says the entry is ongoing: "present", "current", or a start date with wording like "Started" / "since" and no end. Otherwise `false`, including when the end date is recent.
Example: `Spring 2023 – present` → true
Example: `Started August 2023` → true
Example: `January 2021 – October 2026` → false

### dates_as_written
Copy the whole date text for the entry exactly, including words like "From:", "frm", "Started", "approx", and the original dashes and spacing. Null if the entry has no dates.
Example: `From: 04/2024  To: 10/2026` → From: 04/2024  To: 10/2026
Example: `prev 2 that wrked at my uncles shp (auto repair) dnt remember dates` → null

### start_month / end_month
A `{year, month}` object, or null.
- **year**: always four digits. Two-digit years become 20xx if that's not in the future, otherwise 19xx. One approximate year ("roughly 2013") is used as is. Two candidate years ("2016 or 2017") make the whole date null.
- **month**: the month number only when a single month is certain. Seasons and vague words ("Spring", "Summer", "early") → null. Dates with a day where both numbers could be the month ("04/05/2020" when the applicant says they might write day-first) → null. Never pick a default month.
- **end_month** is null when `is_current` is true or no end is given.

Example: `frm 11/21 til 8/26` → start {2021, 11}, end {2026, 8}
Example: `Summer '17 – early 2020` → start {2017, null}, end {2020, null}
Example: `04/05/2020 – 03/02/2023` (may be day-first) → start {2020, null}, end {2023, null}
Example: `approx 2016 or 2017 thru jan 2019` → start null, end {2019, 1}

### license_used
Based only on what this entry's own text says.
- `cdl`: the entry says CDL, CDL-A/B, Class A/B, or a CDL endorsement. If the entry covers both non-CDL and CDL driving, use `cdl`.
- `non_cdl`: the entry says non-CDL, or the driving was in a personal car.
- `no_driving`: the entry's duties didn't include driving on public roads. On-property driving (forklift, yard truck) counts as no_driving.
- `unclear`: they drove but the entry doesn't say whether a CDL was used, even if the vehicle usually needs one (tanker, dump truck, box truck, linehaul). Also for military vehicles, foreign licenses, school, and entries with no details.

Example: `Regional Driver (CDL-A)` → cdl
Example: `oilfld hot shot drvr ... non-cdl at first then got cdl B` → cdl
Example: `Delivery driver (personal car)` → non_cdl
Example: `Did not drive on public roads` (forklift) → no_driving
Example: `Fuel Tanker Driver` → unclear
Example: `Occasionally drove the store's box truck` → unclear

### reason_for_leaving
Copy the reason exactly as written, without a label that ends in a colon ("Reason for leaving:", "Why left:", "Separation:", "rsn lft:"). Keep everything else, including informal introducers ("lft cuz") and the final period. An unlabeled line that says why the entry ended counts. Null if no reason is given. Never soften or drop negative details.
Example: `Reason for leaving: Terminated (preventable accident, 05/2026)` → Terminated (preventable accident, 05/2026)
Example: `lft cuz dispatcher prblms, not enuf mi/wk` → lft cuz dispatcher prblms, not enuf mi/wk
Example: `oil bust slowed thngs dwn, got laid off` (no label) → oil bust slowed thngs dwn, got laid off

---

## Open questions

These rules settle calls that are still worth confirming:
- CDL school is `unclear` for `license_used`; it could be `no_driving` or `cdl`.
- An entry with both non-CDL and CDL driving is `cdl`; the alternative is to split it into two entries.
- Military driving is `unclear`, since it isn't a civilian CDL.
- "prev 2 that wrked at my uncles shp" is one entry; "prev 2" could mean two jobs.
