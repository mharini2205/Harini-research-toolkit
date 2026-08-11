---
name: prior-art-map
description: Run and maintain a prior-art / patent landscape map. Use whenever you want to search patents or literature around a coil, stimulation, or thermal concept and organize the hits — e.g. "prior art on microchannel coil arrays", "patent search for phased-array coils", "find prior art on magnetic auditory stimulation", "add these thermal references to the mapper", "map the IP landscape for X". Trigger for freedom-to-operate scans, competitive IP landscaping, and building or extending the Excel prior-art mapper with reference/thermal row blocks. Produces a deduped, source-linked .xlsx with a "why it matters" note per asset.
---

# Prior-Art Map

Search the patent and literature landscape around a concept, triage each hit against the
prior-art lineages, and record it in the Excel mapper with a working source link and a plain
"why it matters" note.

**First read `references/context.md`** for the lineages, classification framework, sourcing
rules, and known assets. Build on that.

## Workflow

1. **Frame the concept.** Restate what's being landscaped (e.g. "microchannel cooling channels
   in stimulation coils") and the angle: freedom-to-operate, novelty check, or competitive map.

2. **Search broadly, then narrow.**
   - Patents: Google Patents (and cross-check on Justia / Espacenet). Capture number, official
     title, assignee/inventors, priority/grant dates, and the specific claim relevant to the work.
   - Literature: PubMed/PMC, journals, and connected research tools. Capture DOI + PubMed ID.
   - Include the canonical references for the sub-topic (e.g. thermal: Pennes 1948 bioheat;
     Elwassif 2006/2012 DBS heat models; Epstein & Davey 2002 and figure-of-eight coil heating;
     ISO 14708-1). Group these as a reference/thermal row block.

3. **Deduplicate** against the existing mapper before adding rows. Match on the stable key —
   patent number (family, not just one jurisdiction) or DOI — not the title, since the same
   asset surfaces under slightly different titles across searches. Don't create duplicates.

4. **Triage each asset** into a prior-art lineage (magnetic/micro-coil, TI, electrical
   neural-interface, coil-hardware/thermal) or "no overlap", and note the FTO relevance.

5. **Verify.** Every row needs a real link. Never invent a patent number, date, or citation.
   If you can't confirm a specific reference (e.g. a half-remembered "Author Year" paper),
   say so and offer the strongest verified analog instead — don't fabricate the missing one.

6. **Write / extend the .xlsx** using the `xlsx` skill. Preserve existing structure when
   adding to a mapper the user already has; create a fresh one only when none exists. Then
   present the file and summarize what was added and any FTO flags.

## Mapper columns (default)

`Asset ID | Type (patent/paper) | Title | Inventors/Authors | Assignee/Journal |
Number/DOI | Date | Lineage | FTO relevance | Why it matters | Source link | Verified?`

Reference/thermal blocks can be added as labeled row groups beneath the main assets so the
canonical background sits alongside the competitive hits.

## Notes

- Distinguish a genuine FTO concern (an overlapping claim the work would practice) from mere
  background art. Be explicit — this map feeds real IP decisions.
- When a search comes up empty for a specific claimed reference, an honest "not found, here's
  the closest verified alternative" is far more useful than a confident wrong citation.
- Offer a diagram of the landscape when the asset set is large enough to benefit from one. 