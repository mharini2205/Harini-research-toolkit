---
name: research-paper-brief
description: >-
  Turn a research paper into a short, structured brief anyone can skim in a
  minute: seven fixed sections — objective, hypothesis, experiment workflow,
  outcomes, future directions, main authors, and research institutes — plus a
  saved visual one-pager. Use whenever someone uploads or points to a paper
  (PDF, preprint, DOI, or link) and wants it explained, summarized, broken
  down, distilled, or "TL;DR"-ed — e.g. "summarize this paper", "what did they
  actually do", "give me the workflow", "who wrote this and where are they
  from", "make me a one-pager". Trigger even without the word "brief" — a paper
  plus intent to understand it fast is enough. Also use for multi-paper
  synthesis — several papers (e.g. "these 4-5 thermal-safety papers") pulled
  into one comparison with an extraction table, pattern summary, and
  white-space/gap read — and whenever a brief should close with what the work
  means for your own project.
---

# Research Paper Brief

## What this skill is for

People drowning in literature don't need a paper re-narrated in full — they need
the load-bearing parts pulled out fast: what question the authors chased, what
they bet the answer was, what they actually did in the lab, what came out, where
it's heading, and who's behind it. This skill produces exactly that, in a fixed
seven-section shape so every brief looks the same and can be compared at a glance.

The output is two things:

1. A **medium-depth Markdown brief** in the chat (a short paragraph per section — enough to understand the method and findings without opening the paper).
2. A **saved visual one-pager** (an HTML file) where each section is a labeled block, the experiment is drawn as a left-to-right / top-down flow of steps, and a plain-words walkthrough sits beneath that flow.

## House style & framing

A brief isn't finished until it answers *"why does this matter to us?"* The
recurring lenses the work is read through: coil E-field / neural activation
modeling, thermal safety (Joule heating), tissue dielectric properties, volume
conduction, and prior-art / freedom-to-operate.

Two house habits, applied by default:

- **Close with a "Why it matters" line.** After the seven sections, add one or
  two sentences on what the paper means for your work — a method you could borrow,
  a prior-art risk, a number that informs the thermal or activation model, or a
  gap you can claim. This is *your* interpretation, not the paper's, so it sits
  in its own callout (the `note` field) and is clearly labeled. Omit it only
  when the paper has no plausible relevance.
- **Numbers are precious, plain language wins.** Prefer analogies and a clean
  visual over dense exposition. Carry the numbers a conclusion rests on; drop the
  rest.

## Modes

State the mode if it isn't obvious from the request; default to single-paper brief.

- **Single-paper brief** (default) — the seven-section brief + one-pager below.
- **Multi-paper synthesis** — several papers pulled into one comparison (see
  "Multi-paper synthesis mode"). Triggered by things like "these 4-5 papers on
  X", the thermal-safety prior-art pattern, or any "compare across papers" ask.
- **Lens framing** — the reader can set the analytical lens: *hypothesis-mapping*
  ("what don't we know we don't know here?", classify as threat / asset / neutral)
  or *writing* ("draft this into the gap argument"). Keep the seven-section
  spine; let the lens shape the emphasis and the "Why it matters" line.

## Inputs you might get

- A PDF uploaded to the session (the common case) — read it directly.
- A DOI, PubMed/bioRxiv/medRxiv link, arXiv id, or paper title — look it up (see "Fetching a paper you weren't handed").
- Pasted text (abstract or full sections) — work from what's given, and say so if it's only the abstract.

If you only have an abstract, still produce all seven sections, but flag any that you inferred rather than read (e.g. "workflow inferred from abstract — full methods not available").

## The seven sections — always these, in this order

Use these exact section names so briefs are consistent and comparable:

1. **Objective** — the concrete goal of the study in one or two sentences. What were they trying to find out or build? Not the broad field, the specific aim.
2. **Hypothesis** — the testable claim the study was set up to support or refute. Many papers (especially methods/engineering papers) don't state one explicitly; if so, write the implicit hypothesis and mark it *(implicit)*.
3. **Experiment workflow** — the method at two zoom levels: (a) an ordered sequence of compact blocks (the skim view), and (b) a plain-words step-by-step walkthrough of the same procedure that a non-specialist could follow (the "explain it to me" view). This is the heart of the brief. See "How to build the workflow blocks" below.
4. **Outcomes generated** — the key results and what they mean. Lead with the headline finding, then the supporting numbers (effect sizes, p-values, accuracy, error rates — whatever the paper leans on). Distinguish what was measured from what the authors concluded.
5. **Future directions** — where the authors (or you, clearly labeled) think this goes next: open questions, stated limitations, proposed follow-ups.
6. **Main authors** — the people who did the work. Lead author(s), senior/corresponding author, and anyone the paper credits with the core experiments. Note the corresponding author explicitly. Keep it to the handful who matter, not the full masthead.
7. **Research institutes** — the labs, universities, hospitals, or companies the work came out of, mapped to the authors where possible (author affiliations, plus any stated funder or host institution).

Keep each section to a short paragraph. If a section genuinely isn't in the paper, say so briefly rather than padding or inventing — a trustworthy "not reported" beats a confident guess.

## How to build the workflow blocks

The workflow is what makes this brief more useful than an abstract. Read the
methods and reconstruct what was actually done as a chain of discrete steps —
each block is one meaningful stage, phrased as an action.

Aim for **4–8 blocks**. Fewer than 4 usually means you've collapsed real steps;
more than 8 means you're transcribing rather than distilling. Each block should
have a short title (2–4 words) and one line of detail (the how / the key
parameter / the sample size). Order them the way the work flowed.

Good block titles are concrete stages, not vague labels:

**Example — a drug-screening study:**
Input: "We assembled a library of 2,400 compounds, ran a high-throughput viability screen against the cell line, validated the top 30 hits in dose-response, tested the 5 strongest in a mouse xenograft model, and profiled the lead compound's off-target binding."
Blocks:
1. **Assemble library** — 2,400 small-molecule compounds curated
2. **HTS viability screen** — screened against target cell line
3. **Dose-response validation** — top 30 hits confirmed with IC50 curves
4. **In vivo test (mouse)** — 5 leads evaluated in xenograft model
5. **Off-target profiling** — lead compound's selectivity characterized

Notice each block is a stage a reader could point to, the sample counts ride
along in the block where they matter, and validation and profiling are their own
steps because they're distinct analyses. Adapt this shape to any field — the
point is an ordered chain of concrete actions, not these specific steps.

### The plain-words procedure (the companion to the blocks)

The blocks are terse on purpose — good for a glance, but a reader outside the
field can't always tell what "dose-response validation" or "quasi-static FEM
solve" actually *means*. So alongside the blocks, write a **plain-words
step-by-step** of the same procedure: one or two jargon-free sentences per step,
in the order the work happened, that someone who isn't a specialist could follow.

Rules of thumb:

- **Mirror the workflow steps** — roughly one plain-words step per block, same
  order. It's fine to merge or split where that reads more naturally.
- **Expand the jargon and acronyms** the first time (e.g. "FEM — a way of
  splitting the head into millions of tiny tetrahedra and solving the physics in
  each one"). Reach for a short analogy where it earns its place, in line with
  the house preference for plain language and analogies.
- **Say what they did and why**, not just the term for it: "they soaked the coil
  in saline and mapped the field it produced, to check the model against reality"
  beats "bench characterization in saline."
- Keep it tight — this is a walkthrough, not a re-narration of the whole methods
  section. If a step needs a paragraph, the brief is drifting back toward the
  paper.

In the one-pager this renders as a numbered list directly under the block flow
(the `procedure` field — an array of plain-language step strings).

## Multi-paper synthesis mode

When the input is several papers on one question (the recurring case: 4-5
thermal-safety or prior-art papers feeding a single argument), don't produce five
separate briefs. Produce one synthesis, in this shape:

1. **Frame** (3-4 lines) — the specific question all the papers speak to, and why
   it matters in your context.
2. **Extraction table** — one row per paper, same columns for all. Choose columns
   from the question: e.g. for thermal safety — *paper · concern identified ·
   measurement method · mitigation tested · threshold/result · validation type
   (bench / phantom / pre-animal / in-vivo)*.
3. **Pattern summary** — 3-4 bullets on what the field converged on and where it
   disagrees.
4. **White space / gap** — what no paper tested; the opening you can claim. (Keep a
   specific, still-unpublished gap in private notes rather than a public brief if it's
   a patentable novelty.)
5. **Why it matters** — 2-3 lines: what this means for the protocol, the model,
   or the IP position.

Keep each paper's row faithful — a misattributed method or a garbled threshold
poisons the synthesis. For the visual, a table one-pager is fine here rather than
the seven-section block layout; the seven-section builder is for single papers.

## Recommended process

1. **Read the paper.** For a PDF, extract the text (see the PDF skill if you need table/figure extraction). Prioritize abstract, methods, and results/discussion — that's where all seven sections live.
2. **Draft the seven sections** as Markdown. Get the substance right first; don't touch the visual yet.
3. **Sanity-check the extraction.** Are the author affiliations mapped correctly? Is the corresponding author right? Are result numbers copied faithfully? This is where briefs most often go wrong — a misattributed institute or a garbled statistic undermines the whole thing.
4. **Present the Markdown brief in chat.**
5. **Generate the visual one-pager** with the bundled script (below) and save it to the outputs folder, then share it. In Cowork, present it with `present_files` so the person can open it.

## Generating the visual one-pager

Use the bundled script `scripts/build_brief.py`. It takes a small JSON file
describing the brief and writes a self-contained HTML one-pager (no external
dependencies, prints cleanly, each section a block, workflow rendered as a flow
of connected step-cards).

Write the brief content to a JSON file shaped like this, then run the script:

```bash
python scripts/build_brief.py brief.json output_onepager.html
```

The JSON schema (see `references/brief_schema.json` for the full version):

```json
{
  "title": "Paper title",
  "citation": "First-author et al., Journal, Year",
  "objective": "…",
  "hypothesis": "…",
  "workflow": [
    {"title": "Fabricate coils", "detail": "micro-coil arrays for implantable placement"},
    {"title": "Bench characterization", "detail": "field mapped in saline"}
  ],
  "procedure": [
    "First they built tiny coil arrays small enough to implant next to the target nerve.",
    "Then they dunked each coil in salt water — a stand-in for body tissue — and measured the magnetic field around it, to check their design behaved the way the model predicted."
  ],
  "outcomes": "…",
  "future_directions": "…",
  "authors": [
    {"name": "Jane Doe", "role": "first author"},
    {"name": "John Smith", "role": "corresponding author"}
  ],
  "institutes": ["MIT", "Massachusetts Eye and Ear"],
  "note": "Optional. One or two sentences on what this means for your work — omit if the paper has no relevance."
}
```

Don't hand-write HTML — the script keeps every brief visually consistent, which
is the point. If the person wants a different look, edit the script's template
rather than one-off HTML.

## Fetching a paper you weren't handed

If given a DOI / link / title instead of a file, retrieve the details before
writing. Pick the connector that fits the question (search the tools first to
load them; parameter names come from the tool definitions, don't guess):

- **PubMed** — biomedical metadata, abstracts, author lists and affiliations; the
  default for anything indexed in MEDLINE. Also resolves PMID/PMCID/DOI and pulls
  PMC full text when open-access.
- **bioRxiv / medRxiv** — preprints not yet in PubMed; use for recent, unpublished
  work and to check whether a preprint was later published.
- **Consensus** and **Elicit** — evidence/claim-level search across many papers;
  reach for these in *multi-paper synthesis mode* when the question is "what does
  the literature say about X" rather than "get me this one paper."
- **Scholar Gateway** — broad scholarly lookup and citation/affiliation resolution
  when PubMed doesn't cover the venue (engineering, physics, patents-adjacent).

If a needed connector isn't loaded, tell the reader it can be enabled from the
tools menu. If full text isn't reachable, build the brief from abstract +
metadata and clearly flag which sections are abstract-only.

Do not fabricate authors, affiliations, or results to fill a section. An honest
gap is more useful to a researcher than a plausible-looking invention.

## Depth and tone

Medium depth: a short paragraph per section, plain language, no hedging filler.
Assume the reader is technical but time-poor. Numbers are precious — carry the
ones the paper's conclusions rest on, and drop the rest. Don't editorialize;
where you add interpretation the paper didn't state, label it as yours.
