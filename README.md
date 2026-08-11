# Harini Research Toolkit

A Claude Code / Cowork plugin marketplace holding one plugin: **Harini Research Toolkit** — research skills for magnetic / coil-based neural stimulation.

## Install

Add this repo as a marketplace, then install the plugin:

```
/plugin marketplace add mharini2205/Harini-research-toolkit
/plugin install harini-research-toolkit@harini-research-toolkit
```

In Cowork, use **Add marketplace** and enter `mharini2205/Harini-research-toolkit`.

## Skills

- **authorship-association** — Identify and verify the people behind a paper or patent, and map how they, their institutions, and the prior art connect.
- **computational-science** — Coil E-field/lead-field modeling, neural activation, thermal safety (Joule heating + bioheat), and reading dense biophysics papers.
- **prior-art-map** — Search and maintain a prior-art / patent landscape map in a source-linked Excel mapper.
- **researcher-dossier** — Build a verified, IP-aware DOCX dossier on a named researcher or competitor.
- **research-paper-brief** — Turn a paper (or set of papers) into a fixed-structure brief plus a visual one-pager.
- **simnibs-tms-setup** — Translate a physical stimulation target into SimNIBS 4.x TMS inputs and read the induced E-field back out at depth.

## Layout

```
.claude-plugin/marketplace.json        <- marketplace manifest (what Cowork looks for)
plugins/harini-research-toolkit/       <- the plugin itself
  .claude-plugin/plugin.json
  skills/
```

This repo is the single source of truth — install by syncing the marketplace above,
not by uploading a packaged `.plugin` file.
