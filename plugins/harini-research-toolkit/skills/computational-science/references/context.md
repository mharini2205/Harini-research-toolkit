# Shared context & memory

This file is the shared "contextual memory" that every skill in this toolkit loads. It
captures the vocabulary of the field, the house style, and the sourcing conventions the
skills assume. Read it first, then apply the skill-specific instructions.

## Scope

This toolkit supports research on **magnetic / electromagnetic stimulation of neural tissue** —
coil-based induction of neural activation as an alternative to electrode-based stimulation.
Work spans scientific-literature analysis, patent / prior-art landscaping, and computational
modeling of coil fields, neural activation, and thermal safety.

## Core vocabulary (use precisely)

- **Micro-coil stimulation** — sub-mm insulated coils that activate neurons via the induced
  electric field, not direct current injection.
- **Activating function (AF)** — Rattay's second spatial derivative of the extracellular
  potential (or the projected E-field) along the nerve; `AF = d(E·t̂)/ds`. Predicts where
  a fiber is depolarized.
- **Lead field** — induced E-field per unit coil drive, from the magnetic vector potential
  via a quasi-static Biot-Savart line integral: `E = Σ_k (dI_k/dt)·L_k(r)`.
- **Beamforming / focality** — LCMV-style closed-form optimization of channel currents to
  focus AF at a target nerve segment: `s* = R⁻¹c / (cᵀR⁻¹c)`; report a focality ratio.
- **Bioheat / thermal safety** — Joule heating `Q = I²R` (or `Q_e = σE²`) coupled to the
  Pennes bioheat equation; benchmark against **ISO 14708-1** (≤ 2 °C tissue rise) and the
  80 / 50 mW·cm⁻² heat-flux references.
- **Dielectric properties** — tissue σ and εᵣ from the **IFAC-CNR calculator** (Gabriel
  4-Cole-Cole model). Where no entry exists for a target tissue, use documented proxies
  (e.g. Nerve, BoneCortical, CerebroSpinalFluid/BodyFluid, Cartilage) queried at the
  operating frequency.
- **TI-TMS** — temporal-interference transcranial magnetic stimulation (an adjacent lineage).

## Prior-art lineages (landscape map)

Triage every patent/paper into one of these prior-art lineages, or mark "no overlap":

1. **Magnetic / micro-coil neural stimulation** — the core lineage.
2. **Temporal-interference (TI) / deep stimulation** — TI-TMS, interferential fields.
3. **Electrical neural-interface stimulation** — classical electrode-nerve interface modeling.
4. **Coil hardware & thermal** — coil geometry (phased/microchannel arrays), heat-sinking,
   thermometry.

## Classification framework (people & assets)

Classify each researcher/patent as one or more of:
- **Overlapping IP** — overlapping method/hardware; a potential freedom-to-operate (FTO) concern.
- **Potential collaborator** — complementary method/validation capability, no IP conflict.
- **Citation source** — methodological reference only; no hardware/IP overlap.

Always state the FTO implication explicitly (e.g. "zero IP/hardware overlap, no FTO concern").

## Output conventions

- **Dossiers** → DOCX saved under `/profiles/` (e.g. `Surname_Institution.docx`), logged.
- **Prior-art maps** → Excel (.xlsx) with one row per asset and reference/thermal row blocks.
- **Paper explainers** → narrative Markdown, ending with a "why this matters" interpretation.
- **Models** → documented, parameterized Python module + (where useful) an offline HTML explorer.

## Sourcing & verification rules (non-negotiable)

- Every claim gets a real, clickable source: papers → **DOI + PubMed/PMC**; patents →
  **Google Patents** (cross-check inventor/assignee on **Justia / Espacenet**).
- Never fabricate a citation, patent number, grant date, or inventor. If a fact can't be
  verified, say so and flag it rather than guessing.
- Separate what is **measured** from what is **modeled** from what is **assumed**.
