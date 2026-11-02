# Jurisdiction Profiles

A profile is a JSON file that tells `deadline_calc.py` how a court system counts time. With no profile the script applies the federal rule (FRCP 6(a), 3 days for mail under 6(d), federal legal holidays) — use that for the **District of New Jersey**.

## Included: `profiles/nj-superior-court.json`

For NJ state courts (Law Division, Chancery Division, Special Civil Part, Tax Court time computation follows the same Part I rule — confirm for Tax Court specifics).

| Behavior | Rule |
|---|---|
| Exclude trigger day; include last day; roll past Sat/Sun/legal holiday | R. 1:3-1 |
| Periods under 7 days exclude Sat/Sun/legal holidays | R. 1:3-1 |
| +5 days after service by ordinary mail (amended from 3 days, eff. April 1, 2022) | R. 1:3-3 |
| Backward deadlines served by ordinary mail: mail 3 business days earlier (service complete on presumed receipt) | R. 1:6-3 — confirm |
| Holidays: federal list plus Good Friday, General Election Day, and Juneteenth on NJ's third Friday in June | NJ Supreme Court holiday orders |
| Lincoln's Birthday is **not** a court holiday in the 2025-26 through 2027-28 orders | same |
| Verified calendar window | 2026-01-01 to 2028-06-30 |

**Uncertain closures.** The NJ orders list Statewide Judicial College days and December recess days as "emergent matters only", and in recent years the Court has issued a separate order deeming the day after Thanksgiving a recess day and "the same as a legal holiday" for computing time. Whether a particular recess or college day counts as a legal holiday under R. 1:3-1 may require checking for an order, so the profile lists them as `uncertain_closures`. They are treated as open when counting forward and closed when counting backward, which always produces the earlier, safer date, plus a warning.

**Annual maintenance (each summer):** the Supreme Court issues the next court year's holiday and recess order (July 1 – June 30). Add the new Good Friday, Election Day, Juneteenth (third Friday in June), recess and Judicial College dates, then move `calendar_verified_through` forward and record the order in `source`. Watch for the November order on the day after Thanksgiving and move that date from `uncertain_closures` to `extra_holidays` once it issues.

## Fields

| Field | Meaning |
|---|---|
| `name`, `source` | Description, the rules/orders used, and who verified them |
| `calendar_verified_from` / `_through` | Window the holiday list is verified for; outside it the script warns |
| `federal_holidays` | Start from federal legal holidays (true/false) |
| `extra_holidays` | Additional closure dates (`date`, `name`) |
| `removed_holidays` | Federal holidays on which this court is open (e.g., federal Juneteenth when NJ observes a different day) |
| `uncertain_closures` | Possible closures resolved conservatively, with a warning |
| `roll_when_closed` | Move a deadline off a closed day (true) |
| `exclude_weekends_holidays_if_period_under` | Short-period rule threshold (NJ: 7) |
| `service_extra_days` | Days added after a forward period, per service method |
| `service_backward` | For backward deadlines, how much earlier to send when serving by a method that is complete on receipt (`days`, `unit`, `source`) |

## Adding another court
Copy `profiles/TEMPLATE-state.json` (e.g., for a New York or Pennsylvania matter), fill it from that court's time-computation rule and holiday calendar, record sources, and have an attorney sign off.
