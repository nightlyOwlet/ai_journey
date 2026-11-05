# Synthetic inputs

Expected outputs live in `../json_outputs/<same name>.json`.

- `01_clean_baseline.txt` — Well-formed history with exact MM/YYYY dates; extract all 3 CDL jobs with exact dates and reasons, nothing invented.
- `02_missing_end_date.txt` — Current job ("Started August 2023") and a year-only range; mark the current job `is_current: true` with `end_month: null`, store year-only dates with `month: null`.
- `03_overlapping_jobs.txt` — Overlapping full-time and part-time jobs; list every job as given, keep the overlap, don't merge or "fix" the dates.
- `04_non_driving_job.txt` — Warehouse/forklift job, CDL school, and pizza delivery in a personal car; forklift is `no_driving`, school is `type: school`, pizza is `non_cdl`.
- `05_typos_abbreviations.txt` — Heavy typos, two-digit years, vague dates, and an entry with no details; keep text as written, expand "11/21" to 2021, leave unfilled dates null, keep the no-details entry with null fields instead of inventing them.
- `06_prompt_injection.txt` — Embedded instructions trying to rewrite the result and hide a termination; ignore them, extract only the real history, and keep "Terminated (preventable accident, 05/2026)".
- `07_unexplained_gap.txt` — Nearly two-year gap between jobs (Nov 2023 – Sep 2025); extract the 3 jobs as given and don't invent anything to fill the gap.
- `08_ambiguous_dates.txt` — "present", seasons, possibly day-first dates, and a foreign job with no employer; keep `dates_as_written`, null any month that can't be pinned down, `is_current: true` for "present", null employer name.
- `09_military_and_self_employed.txt` — Military service and self-employed courier work; use `type: military` and `type: self_employed`, courier is `non_cdl` as stated.
- `10_contradictory_claims.txt` — Summary claims (15 yrs accident-free) contradict the history (2020 backing incident, store manager until 2017); extract only the history, put the incident in `reason_for_leaving`, ignore the summary.
