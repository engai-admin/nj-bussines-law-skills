---
name: deadline-tracker
description: Calculate, organize, and track deadlines for a New Jersey business-law practice — NJ Superior Court and D.N.J. deadlines counted from service, filing, orders or return dates (R. 1:3-1, R. 1:3-3, R. 1:6-3, R. 4:6-1, R. 4:46-1, discovery rules), NJ limitations periods for business claims, bulk-sale (C-9600) notice before closing, annual reports, franchise and contract notice/renewal/cure windows, earn-out and escrow dates — then keep a deadline log and export a calendar with reminders. Use this skill whenever an attorney or legal staff member asks "when is X due", mentions being served, a return date, motion, order, case management order, limitations period, closing date, notice or renewal window, or wants a docket or deadline calendar — even if they don't use the word "deadline".
---

# Deadline Tracker — NJ Business Law

Missed deadlines are the most common source of legal malpractice claims, so this skill is built on two ideas: **show your work** and **never let a date look more certain than it is**. Calculate with the deterministic script, explain each step, and mark every result UNVERIFIED until the attorney confirms it.

The default jurisdiction is **New Jersey**: NJ Superior Court (Law Division, Chancery Division, Special Civil Part) for state matters, and the District of New Jersey for federal matters. Business-law deadlines from statutes, transactions, and contracts are first-class citizens alongside court deadlines.

## 1. Identify the deadline precisely

For each deadline establish:

- **Forum / source type** — NJ state court, D.N.J., an agency (Division of Taxation, Division of Revenue), a statute, or a contract.
- **Trigger event and date** — service of the summons and complaint, service of a paper, entry of an order or judgment, a motion **return date**, a closing date, accrual of a claim, a contract effective/renewal date. Most errors start here (entry vs. service of an order; date of mailing vs. receipt).
- **Governing rule or source** — cite it. `references/nj-business-deadlines.md` catalogs the common NJ ones; if the user's deadline isn't there, name the rule you believe applies and mark it for confirmation.
- **Period, unit, and direction** — calendar vs. business/court days; after the trigger vs. before an event (NJ motion deadlines count **backward** from the return date).
- **Service method** when the period runs from service of a paper — ordinary mail changes the result in NJ.

Ask for anything missing that would change the date, or state the assumption prominently if the user isn't present.

## 2. Calculate with the script

Use `scripts/deadline_calc.py`. Don't count in your head: weekends, NJ court holidays (Good Friday, General Election Day, NJ's third-Friday Juneteenth), recess days, and short-period rules are where errors happen.

```bash
P="--profile profiles/nj-superior-court.json"
python scripts/deadline_calc.py calc --trigger 2026-11-03 --days 35 $P                         # answer, R. 4:6-1
python scripts/deadline_calc.py calc --trigger 2026-12-11 --days 16 --direction before $P      # motion, R. 1:6-3
python scripts/deadline_calc.py calc --trigger 2026-12-11 --days 8 --direction before --service mail $P
python scripts/deadline_calc.py calc --trigger 2026-12-15 --days 10 --unit court --direction before $P  # bulk-sale notice
python scripts/deadline_calc.py calc --trigger 2026-11-02 --years 6 $P                          # contract SOL
python scripts/deadline_calc.py calc --trigger 2026-11-03 --days 21                             # D.N.J. (FRCP default)
python scripts/deadline_calc.py holidays --year 2027 $P
```

What the NJ profile does (details in `references/jurisdiction-profiles.md`):
- **R. 1:3-1** — exclude the trigger day, include the last day, roll past Saturdays, Sundays, and legal holidays; periods **under 7 days** exclude weekends and holidays entirely (matters for 4-day replies).
- **R. 1:3-3** — adds **5 days** (not 3) after service by ordinary mail.
- **Backward deadlines served by mail** — moves mailing back 3 business days, since mail service is complete on presumed receipt.
- **NJ Judiciary holidays** loaded from the Supreme Court's holiday orders for Jan 2026 – Jun 2028.
- **Uncertain closure days** (Judicial College days, December recess, the day after Thanksgiving, which in past years was deemed a legal holiday by a separate order) are resolved **conservatively**: the earlier date wins, with a warning telling the attorney to check for an order.
- A **warning** appears whenever dates fall outside the verified calendar window; extend the profile from the next annual holiday order.

For D.N.J. use no profile (FRCP 6 default), and for motions pull the motion-day calendar under L.Civ.R. 7.1.

Reason explicitly about what the script can't decide:
- Limitations accrual, the discovery rule, tolling, Tort Claims Act notice, statutes of repose, and the affidavit-of-merit clock.
- A court order or case management order setting a specific date overrides rule-based math.
- eCourts filing cutoffs and court-closure days declared on short notice (weather, emergencies).
- Contract counting language: "business days", "within", "no later than", notice-effective-on-receipt clauses.
- Bulk-sale notice is counted in the Division of Taxation's business days and measured by **receipt** — recommend sending well before the computed date.

## 3. Report each deadline

| Field | Example |
|---|---|
| Matter | Acme LLC v. Smith Supply Co. |
| Deadline | Answer and counterclaim |
| Due | **Tue 2026-12-08** |
| Trigger | Summons & complaint personally served 2026-11-03 |
| Rule / source | R. 4:6-1(a) — 35 days |
| Calculation | 35 calendar days → 2026-12-08 (open day, no roll) |
| Assumptions | Law Division; no consent extension under R. 4:6-1(c) |
| Status | **UNVERIFIED — attorney to confirm** |

Then propose internal warning dates (e.g., draft due 7 days before, client review 3 days before).

## 4. Keep the deadline log

When tracking several deadlines or matters, keep one log (table, spreadsheet, or tracker — whatever the firm uses; Microsoft Lists works well) with columns: Matter, Deadline, Due date, Weekday, Trigger, Rule/source, Owner, Warning date, Status (Open / Done / Extended / Vacated), Verified by & date, Notes. Sort by due date. For "what's coming up", report overdue items first, then the next 7, 30, and 90 days.

When a deadline moves (consent extension, order, adjourned return date), keep the old date and the reason in Notes and recompute the dependent deadlines (opposition and reply dates move with the return date).

Transactional matters need a log too: at signing or closing, extract every dated obligation from the agreement (notice windows, earn-out statements, escrow releases, survival-period expirations, renewal opt-outs) into the log.

## 5. Calendar export

```bash
python scripts/deadline_calc.py ics --input deadlines.json --output deadlines.ics
```

Each item: `{"date": "2026-12-08", "title": "Answer due", "matter": "Acme v. Smith", "source": "R. 4:6-1(a)", "verified": false, "reminders_days": [14, 7, 3, 1]}`. The .ics imports into Outlook, Google, and Apple calendars. If a calendar connector is available and the user asks, events can be created there instead — confirm before writing to their calendar.

## Non-negotiables

- Every computed date is **UNVERIFIED** until the attorney confirms it; the attorney owns the docket.
- Always show the counting steps and any WARNING lines from the script.
- Don't present a rule's period from memory as settled; cite the rule and flag it, since NJ rules are amended (R. 1:3-3 went from 3 to 5 days in 2022).
- Matter names and facts are confidential: no web searches using client facts.
