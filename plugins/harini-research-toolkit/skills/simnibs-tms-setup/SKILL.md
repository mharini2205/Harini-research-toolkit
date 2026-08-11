---
name: simnibs-tms-setup
description: >-
  Set up and interpret a SimNIBS 4.x TMS simulation —
  translate a physical stimulation target (peak B-field in Tesla or %MSO, a
  skin-to-target depth) into the exact values SimNIBS wants, and read the
  induced E-field back out at depth. Use whenever the reader is filling in the
  SimNIBS TMS tab or reading its output — e.g. "what dI/dt for 3.5 T", "how
  do I set the coil-to-skin distance", "measure the field 4 cm below the
  scalp", "what does coil-cortex distance 18 mm mean", "what does this
  SimNIBS error mean". Covers the dI/dt intensity conversion, the GUI-field
  meanings (Skin Distance vs target depth), depth-targeting from a matsimnibs
  matrix via the sphere-ROI pattern, and interpreting the sim-log / GUI errors.
  Ships kernel.py helpers didt_from_B, didt_from_mso, target_at_depth,
  read_E_at_depth.
---

# SimNIBS TMS setup & readout

Help the reader go from a *physical* TMS target to the *inputs SimNIBS actually
takes*, and back from the output mesh to a field value at a chosen depth. The
recurring confusion this skill resolves: **SimNIBS never takes Tesla or a
target depth as an input** — intensity enters only as `dI/dt`, and depth is a
coordinate you evaluate in the solved mesh, not a GUI field.

Read `references/context.md` (via the computational-science skill) for
house style: lead with the bottom line, explain the
"why", separate measured/modeled/assumed, cite real sources, never fabricate a
number. Verify quantitatively — the kernel helpers below are auto-loaded; run
them and report numbers you have run.

## The three things people conflate

| User says | What it maps to in SimNIBS | Where it goes |
|---|---|---|
| "3.5 T" / "%MSO" | intensity → **`dI/dt` (A/s)**, linear in field | the **dI/dt** box |
| "coil-to-skin distance" | **Skin Distance** = coil-casing→scalp air gap (mm) | the **Skin Distance** box |
| "skin-to-target depth" (e.g. 4 cm) | a **coordinate** N mm below the scalp | NOT a GUI field — evaluate in the mesh |

## 1. Intensity: dI/dt (the only intensity input)

The coil file stores the E-field per unit `dI/dt`, and output E is **exactly
linear** in `dI/dt`. GUI default is `1e6 A/s` (= 1 A/us) — a placeholder,
usually far too low for a real pulse.

**Why B and dI/dt scale together (derivation to give the reader):** quasi-static,
every step is linear in coil current `I(t)`. Biot-Savart `B = k_B*I`; vector
potential `A = k_A*I`; Faraday `E = -dA/dt = -k_A*(dI/dt)`. For a pulse
`I = I_pk*sin(2*pi*f*t)`: `B_pk = k_B*I_pk` and `(dI/dt)_max = 2*pi*f*I_pk`.
Divide → `(dI/dt)/B = 2*pi*f/k_B` = a **fixed coil+pulse constant**. So one
known `(dI/dt, B)` pair fixes the line:

    didt_target = didt_ref * (B_target / B_ref)      # didt_from_B()

- `didt_from_B(3.5, 1.4e8, 2.0)` → `2.45e8 A/s` (245 A/us). The generic
  figure-8 anchor is ~1.4e8 A/s at ~2.0 T (100% MSO) — **flag it as generic
  and tell the reader to replace it with the coil's own calibration.**
- Best practice: read `dI/dt` straight off the **MagVenture display** at the
  working %MSO — then no Tesla assumption is needed. `didt_from_mso()` wraps a
  linear %MSO calibration if only %MSO is known.
- 3.5 T peak at the coil face is **above typical clinical output** (commercial
  rTMS ~0.3-2 T at the scalp) — call this out when writing it up.

## 2. Skin Distance (coil→scalp gap, mm)

Coil-casing-to-scalp air gap; SimNIBS defaults to ~4 mm for hair. **This is
not the target depth.** Convert cm→mm by ×10. Some coils set the zero/reference
point inside a thick casing, so an unusually large value (e.g. 33 mm) can be a
casing offset, not a real air gap.

## 3. Target depth: a coordinate, not a field

To get the field at depth D below the skin: compute the point, then sample it.

- **`target_at_depth(matsimnibs, depth_mm, skin_gap_mm=4)`** → coil_center,
  inward unit normal, scalp_pt, target. The matrix is what SimNIBS prints in
  the sim log / stores per POSITION: column 3 = coil centre, column 2
  (z-axis) = coil normal (points *away* from scalp, so inward = -z). If the
  target lands outside the head, the sign flipped — negate.
- **`read_E_at_depth(mesh, matsimnibs, depth_mm=40, r_mm=3)`** → the
  **sphere-ROI pattern**: keep elements whose centre is within `r_mm` of the
  target, take the volume-weighted average of the field. This is the canonical
  SimNIBS way to turn a coordinate into a field value (fields live at element
  centres, so you average a small neighbourhood, weighted by element volume).
  - `field='magnE'` for |E| (V/m), `'E'` for the 3-vector.
  - `r_mm` ~1-2 mm tight probe, 5-10 mm regional average.
  - **Do NOT crop to grey matter for a deep (>~2 cm) target** — the point is
    below cortex; cropping throws away the elements you want.

GUI-only routes when the reader won't script: (a) run with **"Interpolate to NIfTI
volume"** ticked, open `*_magnE.nii.gz` on the T1 in FSLeyes/MRIcron/freeview,
move the crosshair 40 mm inward (viewers report mm), read the voxel; (b) open
the `.msh` in Gmsh, **Mesh → Inspect**, click the element at depth.

## 4. Reading the sim log

- **`INFO: matsimnibs:`** the 4x4 placement — feed it straight into
  `target_at_depth` / `read_E_at_depth`.
- **`INFO: coil-cortex distance: N mm`** = distance along the normal from coil
  to the **grey-matter surface** = coil-skin gap + scalp + skull + CSF. Subtract
  the skin gap for the skin→cortex thickness (e.g. 18.05 - 4 ≈ 14 mm, a normal
  head). A deep target (4 cm from skin) sits *past* this — quantify how far
  ("~26 mm past cortex") so the reader knows it's subcortical.
- **`INFO: Coil file:`** confirm it's the intended coil. A `Magstim_70mm_Fig8`
  in the log when the user meant the **MagVenture MST Twin** is a real
  mismatch — field magnitude and dI/dt calibration both depend on the coil;
  tell them to re-Browse the correct `.ccd`.

## 5. Common GUI errors

- **`stat: path should be string, bytes, os.PathLike or integer, not
  NoneType`** — a required **file path is empty/None**; the GUI didn't validate
  before calling `os.stat`. In order of likelihood: the **coil .ccd/.tcd**
  (re-Browse it), the **subject m2m folder / head .msh** (not loaded/moved), or
  an empty **output folder**. On Windows also check for a moved file or an
  awkward path. Ask which step it popped on and for the console traceback — the
  full traceback names the None variable exactly.

## Depth reality check (why intensity matters at depth)

Induced E falls steeply with depth (illustrative on-axis figure-8, ~2.5 cm
wing): ~63% at 1.5 cm, ~48% at 2 cm, ~26% at 3 cm, **~15% at 4 cm** of the
near-surface value. So a deep target keeps only a fraction of the surface
field; raising `dI/dt` (linear) is the only lever, at the cost of a larger,
less-focal surface field. This is the depth-vs-focality trade that motivates a
near-target micro-coil approach — tie the two together when relevant.
