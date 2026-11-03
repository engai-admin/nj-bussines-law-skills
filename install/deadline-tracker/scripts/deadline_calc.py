#!/usr/bin/env python3
"""Legal deadline calculator and calendar exporter (standard library only).

Subcommands
  calc      Compute a deadline from a trigger date.
  holidays  List the court holidays used for a year.
  ics       Turn a JSON list of deadlines into an .ics calendar file with reminders.

Defaults follow the Federal Rules of Civil Procedure:
  * Rule 6(a)(1): exclude the trigger day, count every day (incl. weekends/holidays),
    include the last day; if it is a Saturday, Sunday or legal holiday, continue to
    the next day that is not.
  * Rule 6(a)(5): when counting BACKWARD from an event, "next day" means continuing
    backward (earlier).
  * Rule 6(d): when service is by mail (or another method that adds time), add 3 days
    after the period would otherwise expire, then roll again if needed.
State rules differ (court-day counting, short-period weekend exclusion, extra days for
mail, state court holidays). Pass a --profile JSON to apply them; for New Jersey state
courts use profiles/nj-superior-court.json (R. 1:3-1, R. 1:3-3, NJ Judiciary holidays). Results are a
calculation aid only and must be verified by the responsible attorney.

Examples
  python deadline_calc.py calc --trigger 2026-11-02 --days 21
  python deadline_calc.py calc --trigger 2026-11-02 --days 14 --service mail
  python deadline_calc.py calc --trigger 2027-03-15 --days 7 --direction before
  python deadline_calc.py calc --trigger 2026-11-02 --months 24      # e.g. limitations period
  python deadline_calc.py calc --trigger 2026-11-02 --days 10 --unit court
  python deadline_calc.py calc --trigger 2026-11-03 --days 35 --profile ../profiles/nj-superior-court.json
  python deadline_calc.py holidays --year 2027
  python deadline_calc.py ics --input deadlines.json --output deadlines.ics
"""
import argparse
import calendar
import datetime as dt
import json
import sys
import uuid

D = dt.date


# ---------------------------------------------------------------- holidays
def _nth_weekday(year, month, weekday, n):
    """n-th weekday (Mon=0) of month; n=-1 for last."""
    if n > 0:
        first = D(year, month, 1)
        offset = (weekday - first.weekday()) % 7
        return first + dt.timedelta(days=offset + 7 * (n - 1))
    last = D(year, month, calendar.monthrange(year, month)[1])
    offset = (last.weekday() - weekday) % 7
    return last - dt.timedelta(days=offset)


def _observed(day):
    if day.weekday() == 5:
        return day - dt.timedelta(days=1)
    if day.weekday() == 6:
        return day + dt.timedelta(days=1)
    return day


def federal_holidays(year):
    """US federal legal holidays (5 U.S.C. 6103) with observed dates."""
    fixed = {
        "New Year's Day": D(year, 1, 1),
        "Juneteenth National Independence Day": D(year, 6, 19),
        "Independence Day": D(year, 7, 4),
        "Veterans Day": D(year, 11, 11),
        "Christmas Day": D(year, 12, 25),
    }
    floating = {
        "Birthday of Martin Luther King, Jr.": _nth_weekday(year, 1, 0, 3),
        "Washington's Birthday": _nth_weekday(year, 2, 0, 3),
        "Memorial Day": _nth_weekday(year, 5, 0, -1),
        "Labor Day": _nth_weekday(year, 9, 0, 1),
        "Columbus Day": _nth_weekday(year, 10, 0, 2),
        "Thanksgiving Day": _nth_weekday(year, 11, 3, 4),
    }
    out = {}
    for name, day in fixed.items():
        out[day] = name
        obs = _observed(day)
        if obs != day and obs.year == year:
            out[obs] = f"{name} (observed)"
    out.update({d: n for n, d in floating.items()})
    # New Year's Day of next year observed on Dec 31 of this year
    ny_next = _observed(D(year + 1, 1, 1))
    if ny_next.year == year:
        out[ny_next] = "New Year's Day (observed)"
    return out


class Calendar:
    """Court calendar. `uncertain_closures` are days the court may or may not treat as legal
    holidays (e.g. recess days not yet deemed holidays by order). They are resolved in the
    conservative direction: treated as OPEN when counting forward (earlier deadline) and as
    CLOSED when counting backward (earlier deadline), with a note either way."""

    def __init__(self, profile=None):
        self.profile = profile or {}
        self._cache = {}
        self.uncertain = {D.fromisoformat(i["date"]): i.get("name", "possible court closure")
                          for i in self.profile.get("uncertain_closures", [])}

    def holidays(self, year):
        if year not in self._cache:
            hol = {}
            if self.profile.get("federal_holidays", True):
                hol.update(federal_holidays(year))
            for item in self.profile.get("extra_holidays", []):
                day = D.fromisoformat(item["date"])
                if day.year == year:
                    hol[day] = item.get("name", "Court holiday")
            for item in self.profile.get("removed_holidays", []):
                hol.pop(D.fromisoformat(item), None)
            self._cache[year] = hol
        return self._cache[year]

    def why_closed(self, day, step=1):
        if day.weekday() == 5:
            return "Saturday"
        if day.weekday() == 6:
            return "Sunday"
        hol = self.holidays(day.year).get(day)
        if hol:
            return hol
        if step < 0 and day in self.uncertain:
            return f"{self.uncertain[day]} (uncertain closure — treated as closed, conservative when counting backward)"
        return None

    def is_open(self, day, step=1):
        return self.why_closed(day, step) is None


# ---------------------------------------------------------------- core math
def add_months(day, months):
    m = day.month - 1 + months
    y = day.year + m // 12
    m = m % 12 + 1
    return D(y, m, min(day.day, calendar.monthrange(y, m)[1]))


def roll(day, cal, step, notes):
    while not cal.is_open(day, step):
        notes.append(f"{day.isoformat()} ({day:%a}) is closed — {cal.why_closed(day, step)}; moving "
                     f"{'forward' if step > 0 else 'backward'}.")
        day += dt.timedelta(days=step)
    if step > 0 and day in cal.uncertain:
        notes.append(f"WARNING: {day.isoformat()} is a possible court closure ({cal.uncertain[day]}). Kept as the "
                     f"deadline (conservative). If the court deems it a legal holiday, the deadline extends to the "
                     f"next open day — check for an order.")
    return day


def count_court_days(start, n, cal, step):
    day, counted = start, 0
    while counted < n:
        day += dt.timedelta(days=step)
        if cal.is_open(day, step):
            counted += 1
    return day


def compute(trigger, *, days=0, months=0, years=0, unit="calendar", direction="after",
            service=None, cal=None, profile=None):
    cal = cal or Calendar(profile)
    profile = profile or {}
    step = 1 if direction == "after" else -1
    notes = []
    roll_on = profile.get("roll_when_closed", True)

    if months or years:
        total = months + 12 * years
        end = add_months(trigger, step * total)
        notes.append(f"Added {total} month(s) {'after' if step > 0 else 'before'} the trigger "
                     f"(same day-of-month, clamped to month end).")
    else:
        short_limit = profile.get("exclude_weekends_holidays_if_period_under")
        short = bool(short_limit and days < short_limit and unit != "court")
        if unit == "court" or short:
            why = (f"period under {short_limit} days — weekends and legal holidays excluded by the profile's rule"
                   if short else "weekends and holidays skipped")
            notes.append(f"Counting {days} court day(s) ({why}).")
            end = count_court_days(trigger, days, cal, step)
        else:
            notes.append(f"Counting {days} calendar day(s); trigger day excluded, last day included.")
            end = trigger + dt.timedelta(days=step * days)

    if roll_on:
        end = roll(end, cal, step, notes)

    if service:
        if step < 0 and service in profile.get("service_backward", {}):
            rule = profile["service_backward"][service]
            n, u = rule.get("days", 0), rule.get("unit", "calendar")
            if n:
                end = count_court_days(end, n, cal, -1) if u == "court" else end - dt.timedelta(days=n)
                notes.append(f"Serving by {service}: send {n} {'business' if u == 'court' else 'calendar'} day(s) "
                             f"earlier so service is complete by the deadline ({rule.get('source', 'profile rule')}).")
                if roll_on:
                    end = roll(end, cal, -1, notes)
        else:
            extra = profile.get("service_extra_days", {"mail": 3, "personal": 0, "electronic": 0}).get(service)
            if extra is None:
                raise SystemExit(f"Unknown service method '{service}' for this profile.")
            if extra:
                end = end + dt.timedelta(days=step * extra)
                notes.append(f"Added {extra} day(s) for service by {service}.")
                if roll_on:
                    end = roll(end, cal, step, notes)

    lo, hi = profile.get("calendar_verified_from"), profile.get("calendar_verified_through")
    if lo and hi:
        span = sorted([trigger, end])
        if span[0] < D.fromisoformat(lo) or span[1] > D.fromisoformat(hi):
            notes.append(f"WARNING: dates outside the profile's verified court calendar ({lo} to {hi}). "
                         f"Court holidays for that period are NOT loaded beyond federal ones — check the "
                         f"court's holiday order and update the profile.")
    return end, notes


# ---------------------------------------------------------------- ics
def _ics_escape(text):
    return (text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n"))


def build_ics(items, reminders=(30, 14, 7, 1)):
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//deadline-tracker skill//EN", "CALSCALE:GREGORIAN"]
    for it in items:
        day = D.fromisoformat(it["date"])
        summary = it.get("title", "Deadline")
        if it.get("matter"):
            summary = f"[{it['matter']}] {summary}"
        desc_parts = [it.get("description", "")]
        if it.get("source"):
            desc_parts.append(f"Source: {it['source']}")
        desc_parts.append("Verify: " + ("yes (attorney verified)" if it.get("verified") else "NOT YET VERIFIED"))
        lines += [
            "BEGIN:VEVENT",
            f"UID:{uuid.uuid4()}@deadline-tracker",
            f"DTSTAMP:{stamp}",
            f"DTSTART;VALUE=DATE:{day:%Y%m%d}",
            f"DTEND;VALUE=DATE:{(day + dt.timedelta(days=1)):%Y%m%d}",
            f"SUMMARY:{_ics_escape(summary)}",
            f"DESCRIPTION:{_ics_escape(chr(10).join(p for p in desc_parts if p))}",
        ]
        for r in it.get("reminders_days", reminders):
            lines += ["BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{_ics_escape(summary)}",
                      f"TRIGGER:-P{int(r)}D", "END:VALARM"]
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


# ---------------------------------------------------------------- cli
def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("calc")
    c.add_argument("--trigger", required=True, help="Trigger/event date YYYY-MM-DD")
    c.add_argument("--days", type=int, default=0)
    c.add_argument("--months", type=int, default=0)
    c.add_argument("--years", type=int, default=0)
    c.add_argument("--unit", choices=["calendar", "court"], default="calendar")
    c.add_argument("--direction", choices=["after", "before"], default="after")
    c.add_argument("--service", choices=["mail", "personal", "electronic", "other"], default=None,
                   help="mail = ordinary/regular mail")
    c.add_argument("--profile", help="Jurisdiction profile JSON (see references/jurisdiction-profiles.md)")
    c.add_argument("--json", action="store_true", help="Output JSON")

    h = sub.add_parser("holidays")
    h.add_argument("--year", type=int, required=True)
    h.add_argument("--profile")

    i = sub.add_parser("ics")
    i.add_argument("--input", required=True, help="JSON list of {date,title,matter,source,description,verified}")
    i.add_argument("--output", required=True)

    a = p.parse_args(argv)
    profile = {}
    if getattr(a, "profile", None):
        with open(a.profile) as f:
            profile = json.load(f)
    cal = Calendar(profile)

    if a.cmd == "calc":
        trig = D.fromisoformat(a.trigger)
        end, notes = compute(trig, days=a.days, months=a.months, years=a.years, unit=a.unit,
                             direction=a.direction, service=a.service, cal=cal, profile=profile)
        res = {"trigger": trig.isoformat(), "deadline": end.isoformat(), "weekday": f"{end:%A}",
               "profile": profile.get("name", "Federal (FRCP 6) default"), "steps": notes,
               "verified": False}
        if a.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"Deadline: {end:%A, %B %d, %Y} ({end.isoformat()})")
            print(f"Rules: {res['profile']}")
            for n in notes:
                print(f"  - {n}")
            print("Calculation aid only — confirm against the governing rule, any court order, and the court calendar.")
    elif a.cmd == "holidays":
        for day, name in sorted(cal.holidays(a.year).items()):
            print(f"{day.isoformat()}  {day:%a}  {name}")
        for day, name in sorted(cal.uncertain.items()):
            if day.year == a.year:
                print(f"{day.isoformat()}  {day:%a}  {name}  [UNCERTAIN — resolved conservatively]")
    elif a.cmd == "ics":
        with open(a.input) as f:
            items = json.load(f)
        with open(a.output, "w", newline="") as f:
            f.write(build_ics(items))
        print(f"Wrote {len(items)} event(s) to {a.output}")


if __name__ == "__main__":
    sys.exit(main())
