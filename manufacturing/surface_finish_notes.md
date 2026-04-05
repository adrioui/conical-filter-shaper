# Surface Finish Notes — Rev 0.1

> Source: `cad/params.py` constants `*_RA_UM`.  
> All Ra values in µm. Measurement method: contact profilometer per ISO 4287.

| Part | Face | Ra (µm) | Method | Reason |
|------|------|---------|--------|--------|
| Half-Shell L / R | Filter contact face (outer cone surface) | ≤ 0.8 | CNC milling + light hand-polish | Clean paper release; no drag or tearing |
| Tip Insert Block | Filter contact tip face (−Z, dimple) | ≤ 0.4 | Turning + electropolish | Hygiene + smooth filter center contact |
| Cam Ring | Cam track floor | ≤ 1.6 | End-mill, sharp tooling | Reduce follower pin wear |
| Cam Ring | Outer rim at detent dimple zone | ≤ 0.8 | Turning | Consistent detent feel, ball seating |
| Handle Housing | Ring bore (interior) | ≤ 1.6 | Boring + anodize | Ring rotation feel |
| Ejection Rod | Full OD | ≤ 0.4 | CNC turning + ground or precision-turned | Low friction in bore |

---

## Anodize Masking Instructions

Apply **before** Type II anodize treatment. Mask with plugs or tape:

| Part | Feature to Mask | Why |
|------|----------------|-----|
| Handle Housing | All M3 tapped holes (4× SHCS bores + detent set screw bore) | Anodize fills threads |
| Cam Ring | 3× detent dimples on outer rim | Anodize in dimple changes depth → unpredictable detent feel |
| Base Cap | All tapped holes | Same as above |

**Critical note on Cam Ring:** Detent dimple depth is `1.4 ± 0.1 mm`. Anodize layer
(Type II = 8–12 µm each side) would reduce this by ~0.02 mm — acceptable, but masking
is still required to prevent buildup of anodize seal material that could unpredictably
alter the dimple profile and break-out force.

---

## Electropolish Requirement

| Part | Faces | Standard |
|------|-------|----------|
| Tip Insert Block | All external faces | ASTM B912 or equivalent. Final Ra ≤ 0.4 µm |

Electropolish is applied **after** all machining and inspection. Parts must be free of
burrs before electropolish treatment.

---

## Fin Blade — DO NOT ANNEAL

The Seam Guide Fin (`overlap_fin`) is laser-cut from SS 301 **half-hard** spring steel.
The half-hard condition (proof stress ≥ 520 MPa) is essential for the serration retention
mechanism and fin rigidity.

**DO NOT** anneal, heat-treat, or post-process with any thermal operation after laser cutting.
Deburr by hand or vibratory finishing only.
