#!/usr/bin/env python3
"""Skill Compass — decide which skills to learn NOW, NEXT, or LATER.

Reads a learner profile (interests, current skill levels, to-do tasks with
deadlines, a small skill catalog, and a practice log) and sorts every skill
into a bucket using a transparent, explainable score:

  NOW   — a task due soon needs it and you're below the level it needs
          (just-in-time learning: it's blocking real work).
  NEXT  — needed for a task further out, or a prerequisite of a NOW skill
          that can wait a little.
  LATER — only your interests pull on it (just-in-case learning: worth it,
          but no task is waiting on it).
  HAVE  — you already meet every level asked of it.

Pure Python 3, no packages.

Usage:
    python skill_compass.py plan profile.json [--html compass.html] [--as-of YYYY-MM-DD]
    python skill_compass.py log  profile.json --skill python --hours 1.5 \
                                 --note "wrote a CSV parser" [--level 2] [--date YYYY-MM-DD]

Levels are 0-3: 0 = none, 1 = basics, 2 = working (can do it unaided),
3 = fluent (can teach it / handle edge cases).
"""
import argparse
import datetime as dt
import html
import json
import sys

LEVEL_NAMES = {0: "none", 1: "basics", 2: "working", 3: "fluent"}
DEFAULT_EFFORT = 10          # hours per level step when the catalog doesn't say
DEFAULT_INTEREST_TARGET = 2  # level an interest-only skill aims for
NOW_DAYS = 21                # task due within this window -> NOW
NEXT_DAYS = 90               # task due within this window -> NEXT
STALE_DAYS = 7               # NOW skill with no practice for this long -> nudge


# ---------------------------------------------------------------- loading ---
def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def parse_date(s):
    return dt.date.fromisoformat(s) if s else None


def label_of(catalog, sid):
    return catalog.get(sid, {}).get("label", sid)


# ------------------------------------------------------------ progress log --
def replay_log(profile):
    """Start from profile['skills'] and replay the practice log in date order.

    A log entry with a 'level' records that the learner now sits at that
    level; hours logged before it no longer count toward the next step.
    Returns {skill: {"level", "hours_since_level", "last_practice"}}.
    """
    state = {}
    for sid, lvl in profile.get("skills", {}).items():
        state[sid] = {"level": int(lvl), "hours_since_level": 0.0, "last_practice": None}
    for e in sorted(profile.get("log", []), key=lambda e: e.get("date", "")):
        sid = e["skill"]
        st = state.setdefault(sid, {"level": 0, "hours_since_level": 0.0, "last_practice": None})
        d = parse_date(e.get("date"))
        if d and (st["last_practice"] is None or d > st["last_practice"]):
            st["last_practice"] = d
        if "level" in e and e["level"] is not None:
            st["level"] = int(e["level"])
            st["hours_since_level"] = 0.0
        else:
            st["hours_since_level"] += float(e.get("hours", 0))
    return state


# ---------------------------------------------------------------- scoring ---
def prereq_closure(catalog, sid, seen=None):
    """All prerequisites of sid (transitively), in learn-first order."""
    seen = seen if seen is not None else set()
    order = []
    for p in catalog.get(sid, {}).get("requires", []):
        if p in seen:
            continue
        seen.add(p)
        order.extend(prereq_closure(catalog, p, seen))
        order.append(p)
    return order


def urgency(days):
    """0..1 — how hard a deadline pulls. Overdue/imminent work pulls hardest."""
    if days is None:
        return 0.15
    if days <= 7:
        return 1.0
    if days <= NOW_DAYS:
        return 0.8
    if days <= 45:
        return 0.55
    if days <= NEXT_DAYS:
        return 0.35
    return 0.15


def analyse(profile, as_of):
    catalog = profile.get("catalog", {})
    state = replay_log(profile)
    interests = {i["name"].lower(): float(i.get("weight", 1)) for i in profile.get("interests", [])}
    max_w = max(interests.values(), default=1.0)
    hours_per_week = float(profile.get("hours_per_week", 5))

    # 1. Collect demand on every skill from tasks (direct needs + prerequisites).
    demand = {}  # sid -> dict

    def entry(sid):
        return demand.setdefault(sid, {
            "target": 0, "task_pull": 0.0, "nearest_days": None,
            "tasks": [], "via": set(),
        })

    for t in profile.get("tasks", []):
        if t.get("done"):
            continue
        due = parse_date(t.get("due"))
        days = (due - as_of).days if due else None
        imp = float(t.get("importance", 2)) / 3.0
        pull = imp * urgency(days)
        for need in t.get("needs", []):
            sid, lvl = need["skill"], int(need.get("level", 2))
            chain = [(sid, lvl, None)] + [(p, max(1, lvl - 1), sid) for p in prereq_closure(catalog, sid)]
            for s, l, parent in chain:
                e = entry(s)
                e["target"] = max(e["target"], l)
                e["task_pull"] = max(e["task_pull"], pull)
                if days is not None and (e["nearest_days"] is None or days < e["nearest_days"]):
                    e["nearest_days"] = days
                if t["title"] not in e["tasks"]:
                    e["tasks"].append(t["title"])
                if parent:
                    e["via"].add(parent)

    # 2. Interests pull on catalog skills tagged with them.
    for sid, meta in catalog.items():
        tags = [x.lower() for x in meta.get("interests", [])]
        w = max((interests.get(x, 0) for x in tags), default=0)
        if w <= 0:
            continue
        e = entry(sid)
        e["interest_pull"] = w / max_w
        e["interest_tags"] = [x for x in tags if x in interests]
        e["interest_target"] = int(meta.get("interest_level", DEFAULT_INTEREST_TARGET))

    # 3. Gap, effort, bucket, score.
    rows = []
    for sid, e in demand.items():
        st = state.get(sid, {"level": 0, "hours_since_level": 0.0, "last_practice": None})
        meta = catalog.get(sid, {})
        # Tasks decide NOW/NEXT; interests can only raise the bar for LATER.
        task_gap = max(0, e["target"] - st["level"]) if e["tasks"] else 0
        if task_gap:
            target = e["target"]
        else:
            target = max(e["target"], e.get("interest_target", 0))
        gap = max(0, target - st["level"])
        effort_step = float(meta.get("effort_hours", DEFAULT_EFFORT))
        remaining = max(0.0, gap * effort_step - st["hours_since_level"]) if gap else 0.0
        ip = e.get("interest_pull", 0.0)
        d = e["nearest_days"]

        if gap == 0:
            bucket = "HAVE"
        elif task_gap and d is not None and d <= NOW_DAYS:
            bucket = "NOW"
        elif task_gap:
            bucket = "NEXT"
        else:
            bucket = "LATER"

        # Score orders skills inside a bucket: task pull dominates, interest
        # breaks ties, and cheap wins (small remaining effort) float up.
        score = 0.65 * (e["task_pull"] if task_gap else 0) + 0.25 * ip + 0.10 * (1 / (1 + remaining / 10))
        score *= 1 if gap else 0.2

        reasons = []
        if e["tasks"] and not task_gap and gap:
            reasons.append(f"already enough for your tasks (level {e['target']}) — this is growth beyond them")
        elif e["tasks"]:
            when = "no deadline" if d is None else ("overdue" if d < 0 else f"due in {d} d")
            reasons.append(f"needed for {len(e['tasks'])} task(s), nearest {when}")
        if e["via"]:
            reasons.append("prerequisite of " + ", ".join(label_of(catalog, v) for v in sorted(e["via"])))
        if ip:
            reasons.append("matches interest: " + ", ".join(e.get("interest_tags", [])))

        stale = None
        if bucket == "NOW":
            lp = st["last_practice"]
            if lp is None:
                stale = "not started yet"
            elif (as_of - lp).days > STALE_DAYS:
                stale = f"no practice for {(as_of - lp).days} days"

        rows.append({
            "id": sid, "label": label_of(catalog, sid), "bucket": bucket,
            "level": st["level"], "target": target, "gap": gap, "task_gap": task_gap,
            "remaining_hours": round(remaining, 1), "score": round(score, 3),
            "reasons": reasons, "tasks": e["tasks"], "stale": stale,
            "first_step": meta.get("first_step", ""),
            "toolkit_skill": meta.get("toolkit_skill", ""),
            "requires": meta.get("requires", []),
        })

    # Order: bucket, then prerequisites before dependents, then score.
    bucket_rank = {"NOW": 0, "NEXT": 1, "LATER": 2, "HAVE": 3}
    rows.sort(key=lambda r: (bucket_rank[r["bucket"]], -r["score"]))
    rows = order_prereqs_first(rows)

    # 4. Capacity check — can the NOW list fit before its deadlines?
    now_rows = [r for r in rows if r["bucket"] == "NOW"]
    now_hours = sum(r["remaining_hours"] for r in now_rows)
    nearest = min((demand[r["id"]]["nearest_days"] for r in now_rows), default=None)
    weeks = max(1, (nearest or 0)) / 7 if nearest is not None else None
    capacity = round(hours_per_week * weeks, 1) if weeks else None

    # 5. Task risk — for each open task, hours of learning still standing in the way.
    task_rows = []
    for t in profile.get("tasks", []):
        if t.get("done"):
            continue
        due = parse_date(t.get("due"))
        days = (due - as_of).days if due else None
        blocking = []
        for need in t.get("needs", []):
            for s in [need["skill"]] + prereq_closure(catalog, need["skill"]):
                r = next((x for x in rows if x["id"] == s), None)
                if r and r["task_gap"] and s not in [b["id"] for b in blocking]:
                    blocking.append(r)
        hrs = round(sum(b["remaining_hours"] for b in blocking), 1)
        avail = round(hours_per_week * max(days, 0) / 7, 1) if days is not None else None
        if not blocking:
            status = "ready"
        elif avail is not None and hrs > avail:
            status = "at risk"
        else:
            status = "on track"
        task_rows.append({
            "title": t["title"], "due": t.get("due"), "days": days,
            "blocking": [b["label"] for b in blocking], "hours": hrs,
            "available": avail, "status": status,
        })
    task_rows.sort(key=lambda x: (x["days"] is None, x["days"] if x["days"] is not None else 0))

    return {
        "person": profile.get("person", ""), "as_of": as_of.isoformat(),
        "hours_per_week": hours_per_week, "rows": rows, "tasks": task_rows,
        "now_hours": round(now_hours, 1), "capacity": capacity, "nearest_now_days": nearest,
    }


def order_prereqs_first(rows):
    """Within each bucket, move a skill's prerequisites ahead of it."""
    out, placed = [], set()
    by_id = {r["id"]: r for r in rows}

    def place(r, stack=()):
        if r["id"] in placed or r["id"] in stack:
            return
        for p in r["requires"]:
            pr = by_id.get(p)
            if pr and pr["bucket"] == r["bucket"]:
                place(pr, stack + (r["id"],))
        placed.add(r["id"])
        out.append(r)

    for r in rows:
        place(r)
    return out


# ----------------------------------------------------------------- output ---
def lvl(n):
    return f"{n} ({LEVEL_NAMES.get(n, '?')})"


def to_markdown(a):
    L = [f"# Skill Compass — {a['person'] or 'learner'} (as of {a['as_of']})", ""]
    for b, title in [("NOW", "Learn now (blocking work due soon)"),
                     ("NEXT", "Learn next (needed, but not yet urgent)"),
                     ("LATER", "Learn later (interest-driven, no task waiting)"),
                     ("HAVE", "Already have")]:
        rs = [r for r in a["rows"] if r["bucket"] == b]
        L.append(f"## {b} — {title}")
        if not rs:
            L += ["_nothing here_", ""]
            continue
        for r in rs:
            if b == "HAVE":
                L.append(f"- **{r['label']}** — level {lvl(r['level'])}")
                continue
            line = (f"- **{r['label']}** — level {r['level']} → {r['target']}, "
                    f"~{r['remaining_hours']} h left. " + "; ".join(r["reasons"]) + ".")
            if r["stale"]:
                line += f" ⚠ {r['stale']}."
            L.append(line)
            if r["first_step"]:
                L.append(f"  - First step: {r['first_step']}")
            if r["toolkit_skill"]:
                L.append(f"  - Practice with the toolkit skill `{r['toolkit_skill']}`.")
        L.append("")
    if a["capacity"] is not None:
        verdict = "fits" if a["now_hours"] <= a["capacity"] else "does NOT fit — defer or ask for help"
        L += ["## Capacity",
              f"NOW list needs ~{a['now_hours']} h; at {a['hours_per_week']} h/week you have "
              f"~{a['capacity']} h before the nearest deadline ({a['nearest_now_days']} d). Verdict: {verdict}.", ""]
    L.append("## Tasks")
    for t in a["tasks"]:
        due = t["due"] or "no deadline"
        blk = ", ".join(t["blocking"]) or "nothing"
        L.append(f"- **{t['title']}** ({due}) — {t['status']}; learning in the way: {blk} (~{t['hours']} h)")
    return "\n".join(L) + "\n"


CSS = """
:root{--bg:#f4f5f8;--card:#fff;--ink:#1a1d24;--muted:#6b7280;--line:#e3e6ec;
--now:#d9480f;--now-soft:#fff1e8;--next:#2f5fe0;--next-soft:#eef2fe;
--later:#2b8a3e;--later-soft:#ebf8ee;--have:#6b7280;--have-soft:#f1f3f7;--warn:#b56b12}
@media (prefers-color-scheme:dark){:root{--bg:#121417;--card:#1b1e23;--ink:#e8eaee;
--muted:#9aa1ad;--line:#2c3038;--now:#ff8a4c;--now-soft:#2e1d14;--next:#7d9bff;
--next-soft:#1a2238;--later:#6fcf85;--later-soft:#15291b;--have:#9aa1ad;--have-soft:#22262c;--warn:#f0b35a}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}
.page{max-width:1100px;margin:0 auto;padding:28px 16px}
h1{font-size:22px;margin:0 0 4px}.sub{color:var(--muted);margin-bottom:22px}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.col{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}
.col h2{font-size:12px;letter-spacing:.1em;text-transform:uppercase;margin:0 0 2px}
.col .why{color:var(--muted);font-size:12px;margin-bottom:10px}
.NOW h2{color:var(--now)}.NEXT h2{color:var(--next)}.LATER h2{color:var(--later)}.HAVE h2{color:var(--have)}
.card{border-radius:10px;padding:10px 12px;margin-bottom:8px}
.NOW .card{background:var(--now-soft)}.NEXT .card{background:var(--next-soft)}
.LATER .card{background:var(--later-soft)}.HAVE .card{background:var(--have-soft)}
.card b{display:block}.meta{font-size:12px;color:var(--muted)}
.bar{height:6px;border-radius:3px;background:var(--line);margin:6px 0;overflow:hidden}
.bar i{display:block;height:100%}
.NOW .bar i{background:var(--now)}.NEXT .bar i{background:var(--next)}
.LATER .bar i{background:var(--later)}.HAVE .bar i{background:var(--have)}
.step{font-size:12.5px;margin-top:4px}.warn{color:var(--warn);font-size:12px;font-weight:600}
.panel{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin-top:14px}
.panel h2{font-size:12px;letter-spacing:.1em;text-transform:uppercase;margin:0 0 8px;color:var(--muted)}
table{width:100%;border-collapse:collapse;font-size:13px}
td,th{text-align:left;padding:6px 8px;border-top:1px solid var(--line);vertical-align:top}
th{color:var(--muted);font-weight:600;border-top:0}
.pill{border-radius:10px;padding:1px 8px;font-size:12px;font-weight:600;white-space:nowrap}
.ready{background:var(--later-soft);color:var(--later)}.ontrack{background:var(--next-soft);color:var(--next)}
.atrisk{background:var(--now-soft);color:var(--now)}
.tablewrap{overflow-x:auto}
"""


def to_html(a):
    e = html.escape
    blurbs = {"NOW": "Blocking work due soon", "NEXT": "Needed, not urgent yet",
              "LATER": "Interest only — no task waiting", "HAVE": "Already at the level needed"}
    cols = []
    for b in ["NOW", "NEXT", "LATER", "HAVE"]:
        cards = []
        for r in (x for x in a["rows"] if x["bucket"] == b):
            pct = 100 if not r["target"] else min(100, int(100 * r["level"] / r["target"]))
            parts = [f"<b>{e(r['label'])}</b>",
                     f"<div class='meta'>level {r['level']} → {r['target']}"
                     + (f" · ~{r['remaining_hours']} h left" if r["gap"] else "") + "</div>",
                     f"<div class='bar'><i style='width:{pct}%'></i></div>"]
            if r["reasons"] and b != "HAVE":
                parts.append(f"<div class='meta'>{e('; '.join(r['reasons']))}</div>")
            if r["stale"]:
                parts.append(f"<div class='warn'>⚠ {e(r['stale'])}</div>")
            if r["first_step"] and b != "HAVE":
                parts.append(f"<div class='step'><b style='display:inline'>First step:</b> {e(r['first_step'])}</div>")
            if r["toolkit_skill"] and b != "HAVE":
                parts.append(f"<div class='meta'>Practice with <code>{e(r['toolkit_skill'])}</code></div>")
            cards.append("<div class='card'>" + "".join(parts) + "</div>")
        body = "".join(cards) or "<div class='meta'>Nothing here.</div>"
        cols.append(f"<div class='col {b}'><h2>{b}</h2><div class='why'>{blurbs[b]}</div>{body}</div>")

    cap = ""
    if a["capacity"] is not None:
        fits = a["now_hours"] <= a["capacity"]
        cap = (f"<div class='panel'><h2>Capacity</h2>NOW needs <b>~{a['now_hours']} h</b>; at "
               f"{a['hours_per_week']} h/week you have <b>~{a['capacity']} h</b> before the nearest "
               f"deadline ({a['nearest_now_days']} days). "
               + ("It fits." if fits else "<span class='warn'>It doesn't fit — defer a task, "
                  "narrow the target level, or get help on one skill.</span>") + "</div>")

    trs = []
    for t in a["tasks"]:
        cls = {"ready": "ready", "on track": "ontrack", "at risk": "atrisk"}[t["status"]]
        trs.append(f"<tr><td>{e(t['title'])}</td><td>{e(t['due'] or '—')}</td>"
                   f"<td><span class='pill {cls}'>{t['status']}</span></td>"
                   f"<td>{e(', '.join(t['blocking']) or '—')}</td><td>{t['hours']} h</td></tr>")
    tasks = ("<div class='panel'><h2>Tasks</h2><div class='tablewrap'><table><tr><th>Task</th><th>Due</th>"
             "<th>Status</th><th>Learning in the way</th><th>Hours</th></tr>" + "".join(trs) + "</table></div></div>")

    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>Skill Compass</title><style>{CSS}</style></head><body><div class='page'>"
            f"<h1>Skill Compass{(' — ' + e(a['person'])) if a['person'] else ''}</h1>"
            f"<div class='sub'>What to learn now, next, and later · as of {a['as_of']}</div>"
            f"<div class='cols'>{''.join(cols)}</div>{cap}{tasks}</div></body></html>")


# -------------------------------------------------------------------- cli ---
def cmd_plan(args):
    profile = load(args.profile)
    as_of = parse_date(args.as_of or profile.get("as_of")) or dt.date.today()
    a = analyse(profile, as_of)
    sys.stdout.write(to_markdown(a))
    if args.html:
        with open(args.html, "w", encoding="utf-8") as f:
            f.write(to_html(a))
        print(f"\nHTML written to {args.html}")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(a, f, indent=2)


def cmd_log(args):
    profile = load(args.profile)
    entry = {"date": args.date or dt.date.today().isoformat(), "skill": args.skill,
             "hours": args.hours}
    if args.note:
        entry["note"] = args.note
    if args.level is not None:
        entry["level"] = args.level
    profile.setdefault("log", []).append(entry)
    with open(args.profile, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Logged {args.hours} h of {args.skill}" + (f", now level {args.level}" if args.level is not None else ""))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    pp = sub.add_parser("plan", help="sort skills into NOW / NEXT / LATER")
    pp.add_argument("profile")
    pp.add_argument("--html", help="also write a visual HTML compass")
    pp.add_argument("--json", help="also write the raw analysis as JSON")
    pp.add_argument("--as-of", help="pretend today is this date (YYYY-MM-DD)")
    pp.set_defaults(func=cmd_plan)
    pl = sub.add_parser("log", help="record practice (and optionally a new level)")
    pl.add_argument("profile")
    pl.add_argument("--skill", required=True)
    pl.add_argument("--hours", type=float, default=0)
    pl.add_argument("--note")
    pl.add_argument("--level", type=int, choices=[0, 1, 2, 3])
    pl.add_argument("--date")
    pl.set_defaults(func=cmd_log)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
