# Harini Research Toolkit

A [Claude Code](https://claude.com/claude-code) / Cowork plugin for deep-tech research groups:
six skills covering literature analysis, patent landscaping, researcher intelligence, and
computational modeling for **magnetic / coil-based neural stimulation** — and designed to be
re-pointed at your own research domain by editing one context file.

## Install

Add this repo as a marketplace, then install the plugin:

```
/plugin marketplace add mharini2205/Harini-research-toolkit
/plugin install harini-research-toolkit@harini-research-toolkit
```

In Cowork, use **Add marketplace** and enter `mharini2205/Harini-research-toolkit`.

## Skills

| Skill | What it does | Say something like |
|---|---|---|
| **research-paper-brief** | Turns a paper (or 4–5 papers) into a fixed seven-section brief plus a visual HTML one-pager | "summarize this paper", "make me a one-pager", "compare these thermal-safety papers" |
| **authorship-association** | Works out who actually did the work on a paper/patent, verifies identities, maps the people–lab–prior-art network | "who ran the experiments here", "is this the same J. Smith", "map the collaboration network around this patent" |
| **researcher-dossier** | Builds a verified, source-linked DOCX dossier on a named researcher and classifies them (competitor / collaborator / citation source) | "profile Dr. X", "is X a competitor", "verify X's patents" |
| **prior-art-map** | Searches patents + literature around a concept and maintains a deduped, source-linked Excel landscape mapper | "prior art on microchannel coil arrays", "map the IP landscape for X" |
| **computational-science** | Coil E-field / lead-field modeling, neural activation, thermal safety (Joule + bioheat), tissue dielectric lookups | "compute activation for a coil array", "does this coil stay under the 2 °C limit" |
| **simnibs-tms-setup** | Translates a physical TMS target (Tesla / %MSO, depth) into SimNIBS 4.x inputs and reads the E-field back out at depth | "what dI/dt for 3.5 T", "measure the field 4 cm below the scalp" |

Skills trigger automatically from phrasing like the examples above — no slash command needed.

## Requirements

- Claude Code or Cowork with plugin support. That's all for most skills.
- `research-paper-brief`'s one-pager builder runs on plain **Python 3** (no packages).
- `researcher-dossier`'s DOCX builder needs **Node** plus a one-time `npm install docx`.
- `simnibs-tms-setup` assumes you have **SimNIBS 4.x** for the actual simulations; its
  `kernel.py` helpers need `numpy` (and `simnibs` itself only for mesh readout).

## Adapting the toolkit to your own field

The domain knowledge lives in one place: `references/context.md` — the shared "contextual
memory" defining the field vocabulary, prior-art lineages, classification framework, and
sourcing rules. Four skills (authorship-association, computational-science, prior-art-map,
researcher-dossier) each ship an **identical copy** of it so every skill stays self-contained.

To re-point the toolkit at your domain:

1. Fork this repo.
2. Rewrite the **Scope**, **Core vocabulary**, and **Prior-art lineages** sections of
   `context.md` for your field. Keep the classification framework and sourcing rules — they
   are domain-agnostic.
3. Copy the edited file over all four `skills/*/references/context.md` locations (they must
   stay identical).
4. Optionally tune the trigger examples in each `SKILL.md` description to your vocabulary.

The output conventions (seven-section briefs, DOCX dossiers, Excel mappers) and the
verification rules (every claim needs a real link; never fabricate a citation) carry over
to any field unchanged.

## Layout

```
.claude-plugin/marketplace.json        <- marketplace manifest (what Cowork looks for)
plugins/harini-research-toolkit/       <- the plugin itself
  .claude-plugin/plugin.json
  skills/
    <skill-name>/SKILL.md              <- instructions + trigger description
    <skill-name>/references/           <- shared context, schemas, examples
    <skill-name>/scripts/              <- bundled builders (brief HTML, dossier DOCX)
```

This repo is the single source of truth — install by syncing the marketplace above,
not by uploading a packaged `.plugin` file.

## License

[MIT](LICENSE)
