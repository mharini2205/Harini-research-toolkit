---
name: skill-compass
description: >-
  Decide which skills a person should learn NOW, NEXT, or LATER, based on their
  interests and their actual to-do work. Builds a small learner profile
  (interests, current skill levels 0-3, tasks with deadlines and the skills
  they need), sorts every skill into Now / Next / Later / Have with a plain
  reason for each, checks whether the Now list fits the hours available before
  the deadline, flags tasks at risk, and keeps a practice log so the plan moves
  as the person learns. Use whenever someone asks "what should I learn first",
  "which skills do I need for this project", "I have too much to learn — help
  me prioritise", "am I ready for this task", "update my learning plan", "log
  that I practised X", or wants a learning roadmap tied to their goals,
  research work, job applications, or career interests.
---

# Skill Compass

## What this skill is for

Early-career researchers usually have two lists fighting for the same evening:
things they *want* to learn (interests) and things their work *needs* them to
learn (tasks). Mixing them causes one of two failures — learning shiny things
while a deadline slips, or only ever firefighting and never growing.

The compass keeps them apart with one rule:

> **Tasks decide Now and Next. Interests decide Later.**

| Bucket | Meaning | Learning style |
|---|---|---|
| **NOW** | A task due within 21 days needs this skill and you're below the level it needs | *Just-in-time* — learn only as much as the task needs |
| **NEXT** | A task needs it, but the deadline is further out | Start small, spaced practice |
| **LATER** | Only your interests pull on it (or it's growth beyond what tasks need) | *Just-in-case* — worth doing, nothing is waiting |
| **HAVE** | You already meet every level asked of it | Maintain; teach someone |

Prerequisites inherit urgency: if SimNIBS is NOW and needs NumPy, NumPy is NOW
too, and is listed first.

## Workflow

1. **Build or load the profile.** If the person has a `skill_profile.json`,
   load it. Otherwise interview briefly (one message, not a questionnaire) and
   write one, using `references/profile.example.json` as the template. You need:
   - **interests** — 2-5 themes with weight 1-3 (e.g. neuromodulation: 3).
   - **skills** — honest current levels, 0 none · 1 basics · 2 working
     (can do it unaided) · 3 fluent (can teach it). When unsure, pick the lower.
   - **tasks** — real to-do items with a due date, importance 1-3, and the
     skills + level each needs. Break vague goals ("get into AI-for-science")
     into interests, not tasks. A task needs a deliverable and a date.
   - **catalog** — per skill: `label`, `requires` (prerequisites),
     `effort_hours` (hours per level step), `interests` it serves,
     `first_step`, and `toolkit_skill` if a skill in this toolkit gives hands-on
     practice (e.g. `simnibs-tms-setup`, `prior-art-map`,
     `research-paper-brief`).
   - **hours_per_week** they can realistically spend learning.

2. **Run the compass.**
   ```bash
   python scripts/skill_compass.py plan skill_profile.json --html skill_compass.html
   ```
   It prints a Markdown plan and writes a visual one-pager (four columns, a
   capacity check, and a task-risk table). Plain Python 3, no packages.

3. **Read it back as a coach, not a report.** Lead with the single most
   important NOW skill and its first step. Then:
   - If **capacity doesn't fit**, say so plainly and offer the three honest
     levers: push a deadline, lower the target level to "just enough", or get
     help on one skill. Don't silently reshuffle the buckets.
   - Name any task **at risk** and what's in the way.
   - Mention LATER items in one line — they're a reward, not a to-do.

4. **Log practice as it happens.** When the person says they practised or
   levelled up, record it:
   ```bash
   python scripts/skill_compass.py log skill_profile.json --skill numpy --hours 2 --note "vectorised the field loop"
   python scripts/skill_compass.py log skill_profile.json --skill fem-basics --level 1 --note "solved 1-D heat eq. by hand"
   ```
   Hours reduce the remaining effort; a `--level` entry records a new level and
   resets the counter. Re-run `plan` and point out what moved (e.g. "FEM hit
   the level SimNIBS needs — it dropped out of NOW into LATER").

## Judgement rules

- **Level up on evidence, not hours.** Only log a new level when the person can
  show it: "I ported the script and it ran" is level 2; "I watched a course" is
  hours, not a level.
- **"Not started yet" is the most useful warning.** A NOW skill with no
  practice logged, or none in 7+ days, is the likeliest cause of a missed
  deadline — raise it first.
- **Don't inflate targets.** A task that needs "run one SimNIBS example"
  needs level 1-2, not 3. Over-targeting is what makes Now lists overflow.
- **Mark done tasks `"done": true`** instead of deleting them, so the history
  of why a skill was learned stays visible.
- **Keep it personal.** The profile is the learner's own data — save it in
  their folder, not inside the plugin, and don't publish it unless asked.

## How the ordering works (so you can explain it)

Within a bucket, skills are ordered prerequisites-first, then by a score:

```
score = 0.65 × task pull  +  0.25 × interest pull  +  0.10 × quick-win bonus
task pull     = (importance / 3) × urgency(days to the nearest deadline)
urgency       = 1.0 (≤7 d) · 0.8 (≤21 d) · 0.55 (≤45 d) · 0.35 (≤90 d) · 0.15 (later / none)
interest pull = highest matching interest weight / your top weight
quick-win     = 1 / (1 + remaining hours / 10)
```

The weights are deliberately simple and shown in the output's reasons, so the
person can disagree with a specific reason rather than a black box. Tune the
window constants (`NOW_DAYS`, `NEXT_DAYS`, `STALE_DAYS`) at the top of the
script if their work runs on longer cycles.
