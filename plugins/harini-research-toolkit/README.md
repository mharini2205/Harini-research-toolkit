# Harini Research Toolkit

Research skills for magnetic / coil-based neural stimulation: identifying who did what on a
paper or patent, modeling coil/neural/thermal physics, landscaping prior art, profiling
researchers and competitors, briefing papers, and setting up SimNIBS TMS simulations.

## Skills

- **authorship-association** — Identify and verify the people behind a paper or patent, and map how they, their institutions, and prior art connect.
- **computational-science** — Coil E-field/lead-field modeling, neural activation, thermal safety (Joule heating + bioheat), and reading dense biophysics papers.
- **prior-art-map** — Search and maintain a prior-art / patent landscape map in a source-linked Excel mapper.
- **researcher-dossier** — Build a verified, IP-aware DOCX dossier on a named researcher or competitor.
- **research-paper-brief** — Turn a paper (or set of papers) into a fixed-structure brief plus a visual one-pager, closing with what it means for your own work.
- **simnibs-tms-setup** — Translate a physical stimulation target into SimNIBS 4.x TMS inputs and read the induced E-field back out at depth.

## Shared context

authorship-association, computational-science, prior-art-map, and researcher-dossier each ship
a `references/context.md` with the prior-art lineages and house style/sourcing conventions —
each skill reads its own copy first. The four copies are identical by design (skills stay
self-contained); if you edit one, copy it over the other three.

**To adapt this toolkit to a different research field**, rewrite the Scope, Core vocabulary,
and Prior-art lineages sections of `context.md` — the classification framework, output
conventions, and verification rules are domain-agnostic and carry over unchanged.

## Install

Drop this plugin into Cowork or Claude Code; skills load automatically and trigger based on the
phrasing described in each SKILL.md (e.g. "profile Dr. X", "prior art on microchannel coil
arrays", "what dI/dt for 3.5 T").

Bundled builders: `research-paper-brief` uses plain Python 3, `researcher-dossier` needs Node
plus a one-time `npm install docx`, and `simnibs-tms-setup`'s `kernel.py` needs `numpy`.
