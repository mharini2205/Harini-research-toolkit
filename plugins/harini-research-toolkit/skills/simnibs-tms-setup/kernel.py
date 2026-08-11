"""Helpers for SimNIBS TMS dosing, depth-targeting, and E-field readout.

Auto-loaded when the simnibs-tms-setup skill is loaded. See SKILL.md for the
physics and the GUI/log walkthrough.
"""
import numpy as np

# Default coil->scalp air gap SimNIBS uses (mm) — accounts for hair.
DEFAULT_SKIN_GAP_MM = 4.0
# SimNIBS default dI/dt placeholder in the GUI (A/s = 1 A/us).
SIMNIBS_DEFAULT_DIDT = 1.0e6


def didt_from_B(B_target, didt_ref, B_ref):
    """dI/dt (A/s) for a target peak B-field, by linear B<->dI/dt scaling.

    In the quasi-static regime B and dI/dt are both linear in coil current, so
    their ratio is a fixed coil+pulse constant. One measured (didt_ref, B_ref)
    pair anchors the line:  didt_target = didt_ref * (B_target / B_ref).

    Anchor tip: read didt_ref straight off the MagVenture display at a known
    %MSO; you then don't even need a Tesla value. A generic figure-8 anchor is
    ~1.4e8 A/s at ~2.0 T (100% MSO) — replace with your coil's calibration.
    """
    return float(didt_ref) * (float(B_target) / float(B_ref))


def didt_from_mso(mso_percent, a=1.5662, b=-2.3237):
    """dI/dt (A/s) from stimulator output %MSO via a linear calibration.

    didt[A/us] = a*(%MSO) + b, returned in A/s. Defaults are one calibrated
    MagVenture device (a=1.5662, b=-2.3237); ALWAYS prefer the dI/dt your own
    stimulator display reports at that %MSO.
    """
    didt_A_per_us = a * float(mso_percent) + b
    return didt_A_per_us * 1.0e6


def target_at_depth(matsimnibs, depth_mm=40.0, skin_gap_mm=None):
    """3D coordinate a given depth BELOW the skin, from a coil placement matrix.

    matsimnibs: 4x4 array (as SimNIBS prints in the sim log / stores per
    POSITION). Column 3 = coil-centre xyz; column 2 (z-axis) = coil normal,
    which points AWAY from the scalp, so inward = -z.

    Returns dict: coil_center, inward (unit), scalp_pt, target (all mm).
    scalp_pt = coil_center + skin_gap*inward;  target = scalp_pt + depth*inward.
    If the target lands OUTSIDE the head, the normal sign was flipped — negate.
    """
    if skin_gap_mm is None:
        skin_gap_mm = DEFAULT_SKIN_GAP_MM
    M = np.asarray(matsimnibs, dtype=float)
    coil_center = M[:3, 3]
    z_axis = M[:3, 2]
    inward = -z_axis / np.linalg.norm(z_axis)
    scalp_pt = coil_center + float(skin_gap_mm) * inward
    target = scalp_pt + float(depth_mm) * inward
    return {
        "coil_center": coil_center,
        "inward": inward,
        "scalp_pt": scalp_pt,
        "target": target,
    }


def read_E_at_depth(mesh, matsimnibs, depth_mm=40.0, r_mm=3.0,
                    skin_gap_mm=None, field="magnE", tissue_tag=None):
    """Volume-weighted E-field in a sphere ROI at a depth below the skin.

    mesh: a loaded simnibs mesh, OR a path to a *_scalar.msh output file.
    Computes the target with target_at_depth(), keeps elements whose centre is
    within r_mm of it (the sphere-ROI pattern), and returns the volume-weighted
    average of `field` ('magnE' for |E| in V/m; 'E' for the 3-vector mean).

    Do NOT crop to grey matter for a deep (>~2 cm) target — the point is below
    cortex. Pass tissue_tag (a simnibs.ElementTags value) only to restrict to a
    known tissue.

    Returns dict: target, value, n_elements, depth_mm.
    """
    import simnibs  # deferred: not in the starter env
    if isinstance(mesh, str):
        mesh = simnibs.read_msh(mesh)

    geo = target_at_depth(matsimnibs, depth_mm=depth_mm, skin_gap_mm=skin_gap_mm)
    target = geo["target"]

    m = mesh
    if tissue_tag is not None:
        m = m.crop_mesh(tissue_tag)

    centers = m.elements_baricenters()[:]
    vols = m.elements_volumes_and_areas()[:]
    roi = np.linalg.norm(centers - target, axis=1) < float(r_mm)
    n = int(roi.sum())
    if n == 0:
        raise ValueError(
            "no mesh elements within %.1f mm of target %s -- increase r_mm "
            "or check the normal sign (target may be outside the head)"
            % (r_mm, target))

    vals = m.field[field][:]
    sel = vals[roi]
    w = vols[roi]
    if sel.ndim == 1:
        value = float(np.average(sel, weights=w))
    else:
        value = np.average(sel, axis=0, weights=w)
    return {
        "target": target,
        "value": value,
        "n_elements": n,
        "depth_mm": float(depth_mm),
    }
