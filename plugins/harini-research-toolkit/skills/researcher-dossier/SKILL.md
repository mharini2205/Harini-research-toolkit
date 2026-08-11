---
name: researcher-dossier
description: Build a structured researcher/competitor dossier. Use whenever you name a researcher, professor, lab head, author, or inventor and want them profiled, verified, classified, or assessed for competitive/IP relevance — e.g. "profile Dr. X", "who is X and are they a competitor", "make me a dossier on X", "verify X's patents", "should we worry about X's freedom-to-operate". Also trigger when checking whether a named person overlaps with the magnetic/micro-coil/neural-stimulation prior art. Produces a verified, source-linked DOCX under /profiles/ and classifies the person as competitor, potential collaborator, or citation source.
---

# Researcher Dossier

Turn a person's name into a verified, IP-aware dossier that tells you three things fast:
who they are, whether their work overlaps the prior art, and what to do about it (cite,
collaborate, or watch for freedom-to-operate).

**First read `references/context.md`** — it holds the shared context, the prior-art
lineages, the classification framework, and sourcing rules you must reconcile against.
Everything below assumes that context.

## Workflow

1. **Disambiguate the person.** Confirm the field/institution before profiling — same-surname
   authors are a common trap (exclude false matches explicitly). If the name is ambiguous and
   you can't resolve it from context, ask one clarifying question.

2. **Gather primary evidence** (use connected tools where available, else web):
   - Publications: PubMed / PMC, Google Scholar, journal pages. Capture DOI + PubMed ID.
   - Patents: Google Patents for numbers/titles/grant dates; **cross-check inventor and
     assignee on Justia and Espacenet**. Record official granted titles, not paraphrases.
   - Affiliation, role, lab focus, and any relevant methods or hardware.

3. **Reconcile against the shared context** in `context.md`. If this person is already known,
   update rather than restate; if new, prepare to add them to the memory.

4. **Classify** into the framework — competitor / potential collaborator / citation source —
   and map to a prior-art lineage (magnetic/micro-coil, TI, electrical neural-interface,
   coil-hardware/thermal) or state "no overlap". **Always state the FTO implication in plain terms.**

5. **Verify before writing.** Every paper and patent needs a working source link. Never
   fabricate a citation, patent number, grant date, or inventor. If web results conflict,
   trust the authoritative registry and note the discrepancy. Add a dated verification note.

6. **Write the DOCX** with the bundled builder — don't hand-roll a docx-js script each time.
   Fill a JSON spec (schema in `references/dossier_spec.example.json`) with the sections below,
   then run:

   ```bash
   npm install docx            # once, in a writable dir (e.g. the outputs folder)
   node scripts/build_dossier.js <spec.json>
   ```

   Set the spec's `output` to `/profiles/Surname_Institution.docx`. Validate with the `docx`
   skill's `scripts/office/validate.py` if you want a check. Append a one-line entry to
   `/profiles/_profiles_log.md` (Date | Name | Institution | Classification | FTO | File — create
   the table if absent). Then present the file and give the bottom line in chat. Only
   fall back to a custom docx-js script if the spec can't express something the dossier needs.

## Dossier structure

```
# [Full name] — [one-line identity]
Bottom line: [competitor / collaborator / citation source] + FTO implication in one sentence.

## Who they are
Role, institution, training, research focus.

## Publications relevant to the work
Each with a one-line "why it matters" + DOI and PubMed/PMC links.

## Patents
Official granted title, number, grant date, inventors/assignee, Google Patents link,
and a one-line "Why it matters" under each.

## Classification & prior-art mapping
Lineage(s) touched or "no overlap". Competitor / collaborator / citation-source call.
Explicit freedom-to-operate statement.

## Verification note
Date checked, sources consulted, and any unresolved conflict flagged.
```