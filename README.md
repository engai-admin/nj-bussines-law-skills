# Attorney Skills Pack — NJ Business Law (v2 — 2026-11-02)

Four Claude skills for a New Jersey business-law practice. v2 retargets the v1 general-practice pack to NJ business law: same skill names, so installing v2 replaces v1.

| Skill | What it does | NJ-specific content |
|---|---|---|
| **contract-review** | First-pass review based on which side the client is on: key-terms table, issues rated High/Medium/Low with replacement language, missing provisions, version comparison | `references/nj-contract-law.md`: *Atalese* arbitration waivers, bulk-sale (C-9600) mechanics in APAs, non-compete reasonableness + pending S1407/A1829, N.J.S.A. 10:5-12.8 NDA limits, ABC test, Franchise Practices Act, Sales Reps' Rights Act, CFA/TCCWNA/Plain Language Act, NJ Data Privacy Act, usury; playbook defaults to NJ law/venue |
| **case-management** | Intake → matter summary + conflict list + NJ engagement checks; forum selection; phased task plans; sourced chronologies; caseload review; client updates | `references/nj-practice.md`: forum table (Small Claims $5k, Special Civil $20k, Law Div., CBLP ≥$200k, Chancery, D.N.J.), first-filing checklist (CIS, R. 4:5-1(b)(2), R. 1:38-7), RPC/Court Rule intake ethics, Division of Revenue/Taxation touchpoints; NJ matter phases |
| **legal-drafting** | First drafts with placeholders, no fabricated citations, and drafter's notes | `references/nj-drafting.md`: NJ captions and certifications, RPC 3.4(g) demand-letter limit, RPC 1.13 entity-client language, NJ LLC/corporate consent cites, APA bulk-sale clause, R. 1:20A-6 fee pre-action notice, client-education handout format |
| **deadline-tracker** | Deterministic deadline math, deadline log, .ics export | `profiles/nj-superior-court.json` (R. 1:3-1 incl. <7-day rule, R. 1:3-3 **5-day** mail rule, NJ Judiciary holidays Jan 2026–Jun 2028, uncertain recess days resolved conservatively); `references/nj-business-deadlines.md` (pleadings, motions 16/8/4 and SJ 28/10/4, discovery 60/35/30, appeals, limitations, bulk sale, annual reports, franchise notice, fee notice) |

## Maintenance
- **Each summer:** add the next NJ court-year holiday/recess order to the NJ profile and extend `calendar_verified_through`.
- **Each November:** when the Court issues the day-after-Thanksgiving order, move that date from `uncertain_closures` to `extra_holidays`.
- Watch: NJ non-compete bills (S1407/A1829), *Atalese* developments and FAA preemption, rule amendments.
- Replace `default-playbook.md` with the firm's own positions; add firm templates to legal-drafting.

## Sources used for v2 (verified 2026-11-02)
NJ Courts holiday orders 2025-26, 2026-27, 2027-28; R. 1:3-1; R. 1:3-3 (amended eff. 2022-04-01); R. 1:6-3; R. 4:6-1; R. 4:46-1; R. 1:20A-6; NJ Division of Taxation bulk-sale FAQ; NJ Courts CBLP page; Special Civil Part limits (eff. 2022-07-01).

## Verified calculator behavior (NJ profile)
- Answer, served 2026-11-03 + 35 days → Tue 2026-12-08
- 35 days landing on Thanksgiving 2026 → Fri 2026-11-27 with a warning (possible recess day)
- Motion 16 days before a 2026-12-11 return date lands in Judicial College days → moved back to Fri 2026-11-20
- Opposition 8 days before 2026-12-11, served by mail → mail by Mon 2026-11-30
- Bulk-sale notice for a 2026-12-15 closing → received by Tue 2026-12-01 (send earlier)
