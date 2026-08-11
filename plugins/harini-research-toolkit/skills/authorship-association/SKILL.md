---
name: authorship-association
description: Identify, verify, and map the people behind a paper or patent, and the associations between them, their institutions, and prior art. Use whenever you want to know who actually did the work or how people/labs connect — e.g. "who did the surgery in this cochlea study", "extract the authors and figure out who ran the experiments", "is this the same author X", "who is connected to this micro-coil work", "map the collaboration network around this patent", "which authors overlap with the prior art". Trigger for author-contribution analysis, identity verification across sources, and building the association/network map that links authors, inventors, institutions, and prior-art lineages.
---

# Authorship & Association

Work out who really did the work behind a paper or patent, confirm they are who you think,
and map how the people, labs, and prior art connect. This is the intelligence layer beneath
dossiers and prior-art maps: it turns an author list into a verified, connected picture.

**First read `references/context.md`** for the lineages and sourcing rules. Reconcile
everyone you find against that memory.

## Three jobs (do whichever the request needs)

### 1. Attribution — who did what
Mine the paper's **author-contributions / acknowledgements** and affiliations to infer roles
(who designed, collected data, performed surgery, supervised). Build the case from evidence:
- Quote the contributions statement verbatim where it settles a question.
- Use affiliations (e.g. Neurosurgery / Otolaryngology departments imply hands-on surgical
  roles) and the CRediT credit pattern to infer roles:
  - Investigation / Methodology, *no* Supervision → hands-on junior doing the bench/surgical work.
  - Supervision (± Conceptualization, Funding) → oversight, protocol design, not the hands-on work.
  - "Contributed equally to experiment design and data collection" → both were physically present
    executing the experiments — treat as a direct statement, not an inference.
- State the conclusion strongly *and* show the independent lines of evidence supporting it, so
  the reader can trust it. Separate "the paper explicitly says" from "this is a reasoned inference".

### 2. Identity verification — is this the same person
Confirm a named person matches an external profile/record using converging signals: shared PI,
institution, research topic, and a shared publication. Rare-name + multiple matches ≈ almost
certainly the same person; say so with your confidence and the signals used. If a source is
blocked, tell the reader exactly which signals to check rather than guessing.

### 3. Association mapping — how they connect
Map the network: author ↔ co-author ↔ institution ↔ PI ↔ patent ↔ prior-art lineage.
Surface who anchors a lineage, who bridges labs, and which associations imply an FTO or
collaboration angle. A compact table or an adjacency list is usually clearest; offer
a diagram if the network is large.

## Verification rules

- Every person, role claim, and link rests on a citable source (DOI/PubMed, patent record,
  official lab/institution page). Never fabricate an affiliation, a contribution, or a link.
- Exclude same-surname false matches explicitly.
- When a website or record is inaccessible, don't infer its contents — state the blocker and
  give the reader the checklist of confirming signals.

## Output

Default to a concise chat answer with the evidence laid out. When the result is a recurring
or large network, produce a compact table or adjacency list — and offer a diagram if it makes
the connections easier to read.