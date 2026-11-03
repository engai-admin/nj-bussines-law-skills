# NJ Business-Law Deadline Catalog

Common deadlines for a New Jersey business-law practice. Each entry gives the rule and how to run it through the calculator. **Rule text changes — every entry is a starting point to confirm against the current rule, statute, or order**, and a court order or case management order setting a specific date always controls.

Calculator flags: `P="--profile profiles/nj-superior-court.json"`.

## Contents
1. Superior Court — pleadings
2. Superior Court — motions
3. Superior Court — discovery
4. Post-judgment and appeals
5. Federal court (D.N.J.)
6. Limitations periods (business claims)
7. Transactional and compliance deadlines
8. Ethics and fee-related deadlines

---

## 1. Superior Court — pleadings
| Deadline | Period | Rule | Calculator |
|---|---|---|---|
| Answer / counterclaim | 35 days after service of summons & complaint | R. 4:6-1(a) | `--trigger <service date> --days 35 $P` |
| Answer to counterclaim or crossclaim | 35 days after service | R. 4:6-1(a) | same |
| Reply (where permitted) | 20 days after service of answer | R. 4:6-1(a) | `--days 20` |
| Responsive pleading after R. 4:6 motion denied | 10 days after notice of the court's action | R. 4:6-1(b) | `--days 10` |
| Extension by consent | up to 60 days, written consent filed with the pleading; further extensions only by order | R. 4:6-1(c) | note, don't calculate |

Mail: if a paper was served by **ordinary mail**, add `--service mail` (R. 1:3-3 adds 5 days, eff. 2022-04-01). Personal service of process is the norm for the complaint.

## 2. Superior Court — motions (counted backward from the return date)
| Deadline | Period | Rule | Calculator |
|---|---|---|---|
| File & serve motion | ≥16 days before return date | R. 1:6-3(a) | `--trigger <return date> --days 16 --direction before $P` |
| Opposition / cross-motion | ≥8 days before | R. 1:6-3(a)–(b) | `--days 8 --direction before` |
| Reply | ≥4 days before (period under 7 days → weekends/holidays excluded under R. 1:3-1) | R. 1:6-3(a) | `--days 4 --direction before` (profile applies the short-period rule) |
| Summary judgment motion | ≥28 days before return date; returnable ≥30 days before trial | R. 4:46-1 | `--days 28 --direction before` |
| SJ opposition / cross-motion | ≥10 days before | R. 4:46-1 | `--days 10 --direction before` |
| SJ response | ≥4 days before | R. 4:46-1 | `--days 4 --direction before` |

If serving motion papers by ordinary mail, add `--service mail`: the profile moves the mailing date back 3 business days because mail service is complete only on (presumed) receipt.

## 3. Superior Court — discovery
| Deadline | Period | Rule | Notes |
|---|---|---|---|
| Interrogatory answers | 60 days after service | R. 4:17-4(b) | Extension only by motion filed within the 60 days; consent orders enlarging time are prohibited |
| Document request responses | 35 days after service (a defendant may respond within 50 days after service of the summons & complaint, whichever is later) | R. 4:18-1(b)(2) | |
| Requests for admission | 30 days after service | R. 4:22-1 | **Deemed admitted** if no timely answer/objection — calendar these first |
| Discovery end date | Set by track assignment | R. 4:24-1, R. 4:5A | Use the date in the track assignment notice; consensual extension and motion rules in R. 4:24-1(c) — confirm current text |
| Complex Business Litigation Program | case management order controls | R. 4:102, 4:103; Dir. #01-19 | Presumptive for complex commercial/construction cases ≥ $200,000 |

## 4. Post-judgment and appeals (confirm each)
| Deadline | Period | Rule |
|---|---|---|
| Motion for reconsideration | 20 days after service of the order/judgment | R. 4:49-2 |
| Motion for new trial | 20 days after verdict/decision | R. 4:49-1(b) |
| Notice of appeal (final judgment) | 45 days after entry | R. 2:4-1(a) |
| Motion for leave to appeal (interlocutory) | 20 days after service of the order | R. 2:5-6(a) |

## 5. Federal court — District of New Jersey
Use the default FRCP calculation (no profile). Key items:
- Answer: 21 days after service (FRCP 12(a)(1)(A)(i)); 60 days if service waived (90 if outside the U.S.).
- Motions: D.N.J. L.Civ.R. 7.1(d) sets filing, opposition and reply deadlines **relative to the motion day** on the court's published motion-day calendar — pull the current calendar from njd.uscourts.gov and confirm the rule's day counts before calculating.
- D.N.J. holidays follow the federal list (no Good Friday/Election Day closures).

## 6. Limitations periods — business claims (confirm; discovery rule and tolling may apply)
| Claim | Period | Source |
|---|---|---|
| Breach of contract (non-goods) | 6 years | N.J.S.A. 2A:14-1 |
| Sale of goods (UCC Art. 2) | 4 years from breach | N.J.S.A. 12A:2-725 |
| Fraud / Consumer Fraud Act | 6 years | N.J.S.A. 2A:14-1 |
| Property damage / negligence (non-PI) | 6 years | N.J.S.A. 2A:14-1 |
| Personal injury | 2 years | N.J.S.A. 2A:14-2 |
| Defamation | 1 year | N.J.S.A. 2A:14-3 |
| CEPA (whistleblower) | 1 year | N.J.S.A. 34:19-5 |
| NJ Law Against Discrimination | 2 years | case law (Montells) — confirm |
| Wage claims (Wage Payment / Wage & Hour Law) | 6 years (since 2019 amendments) | confirm |
| Claims against a NJ public entity | **90-day notice of claim** (Tort Claims Act) | N.J.S.A. 59:8-8 |
| Professional malpractice vs. licensed professionals (e.g., accountants, architects, engineers) | Affidavit of merit due 60 days after the answer (one 60-day extension for good cause) | N.J.S.A. 2A:53A-27 |
| Construction lien (commercial) | lien claim lodged within 90 days after last work/materials | N.J.S.A. 2A:44A-6 — confirm |

Use `--years N` from the accrual date and flag accrual/tolling questions explicitly.

## 7. Transactional and compliance deadlines
| Deadline | Timing | Source | Calculator |
|---|---|---|---|
| **Bulk sale notice (Form C-9600)** — purchaser must notify Division of Taxation of any sale of business assets outside the ordinary course | **Received ≥10 business days before closing**; registered/certified mail or overnight courier only (no hand delivery/fax) | N.J.S.A. 54:50-38; Division of Taxation bulk-sale FAQ | `--trigger <closing> --days 10 --unit court --direction before $P`, then send several days earlier — the Division counts receipt, and its business days may differ from court days |
| Release of bulk-sale escrow | after Division clearance letter (Division generally responds within 10 business days of a complete notice) | Division FAQ | track, don't calculate |
| Annual report — NJ corporations and LLCs | due by the end of the entity's anniversary month; non-filing for consecutive years leads to revocation | N.J.S.A. 14A:4-5; 42:2C — confirm | calendar yearly |
| Franchise termination / non-renewal notice | 60 days' written notice (good cause required) | NJ Franchise Practices Act, N.J.S.A. 56:10-5 — confirm | `--days 60 --direction before` |
| Contract notice / renewal / option windows | per the contract | contract § | contract counting language controls; use calendar days unless it says "business days" |
| Earn-out statements, escrow releases, survival-period expirations | per purchase agreement | APA § | add to log at closing |

## 8. Ethics and fee-related deadlines
| Deadline | Timing | Source |
|---|---|---|
| Pre-action notice before suing a client for fees | Notice by certified **and** regular mail (or hand delivery) of the right to fee arbitration; suit only after 30 days; complaint must allege the notice or be dismissed | R. 1:20A-6 |
| Written fee terms for a new client | Before or within a reasonable time after starting the representation | RPC 1.5(b) |
| Contingent fee agreements | Must be in writing | RPC 1.5(c); R. 1:21-7 |
