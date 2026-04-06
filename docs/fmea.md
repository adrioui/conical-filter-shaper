# Failure Mode & Effects Analysis (FMEA) — V1

> Source: Design Spec — `docs/design_spec.md`  
> Project: Universal Filter Ruler  
> Updated: 2026-04-06

---

## 1. Failure Modes

| # | Failure Mode | Root Cause | Effect | Severity | Likelihood | Mitigation | Detection |
|---|-------------|-----------|--------|----------|-----------|------------|-----------|
| F1 | **Arms don't slide smoothly** | PTFE strip debris; T-slot burr; contamination | User frustration; inconsistent angle | Medium | Low | R0.5mm edge break; cleaning instructions | Visual + feel |
| F2 | **Cam lock doesn't hold** | Wear on cam body; insufficient torque; debris | Arm drifts during use | Medium | Low | Designedfor ≥50 N hold; user-tightenable | Function test |
| F3 | **Angle scale misaligned** | Laser etch positioning error | Inaccurate readings | High | Low | QC optical comparator check | QC sampling |
| F4 | **Vernier scale unreadable** | Poor contrast; etch depth insufficient | User can't read precision | Medium | Medium | Black paint fill; Ra spec for etch surface | Visual QC |
| F5 | **Magnetic markers fall off** | Weak magnet; adhesive failure; ferrous strip detachment | Preset angles lost | Low | Low | N52 magnet ≥0.5 kg pull; adhesive backup | Pull test |
| F6 | **T-slot engagement loose** | Tolerance stack; wear over time | Arm wobble; inaccurate angle | Medium | Medium | H7/h6 sliding fit spec; ±0.02mm on engagement | Go/No-go gauge |
| F7 | **Base plate warps** | Thermal stress; machining stress; anodize fill | Non-flat base; angle error | Low | Very Low | Stress-relief after machining; flatness spec 0.05mm | Surface plate check |
| F8 | **PTFE strip dislodges** | Insufficient press-fit; contamination | Increased friction | Low | Low | Press-fit with undersize groove | Visual + feel |
| F9 | **Anodize chips at edges** | Sharp corners; impact damage | Poor aesthetics; corrosion risk | Low | Low | R1mm edge break all corners | Visual |
| F10 | **Hardware loosens** | Vibration; thermal cycling | Cam wobble; foot pad detachment | Medium | Low | Belleville washer under cam bolt; adhesive foot pads | Function test |

---

## 2. Priority Tests for V1 Validation

| Priority | Test | Pass Criterion |
|----------|------|----------------|
| 1 | Angle accuracy across range | ±0.5° at 40°, 60°, 85° |
| 2 | T-slot sliding smoothness | <5 N to move arm across full travel |
| 3 | Cam lock hold force | ≥50 N resistance to arm push when locked |
| 4 | Vernier scale readability | 0.5° resolution visible under normal lighting |
| 5 | Magnetic marker pull force | ≥0.5 kg per marker |
| 6 | 500-cycle durability | No measurable wear after 500 open/close cycles |
| 7 | Flatness verification | ≤0.05 mm over200 mm length |

---

## 3. Critical Tolerances

| Feature | Tolerance | Impact if Out of Spec |
|---------|-----------|----------------------|
| T-slot width | +0.02/−0.00 mm | Arm wobble; angle error |
| T-slot depth | ±0.05 mm | Arm engagement depth |
| Arm width | ±0.05 mm | T-slot fit |
| Arm thickness | ±0.05 mm | Cam lock engagement |
| Angle scale accuracy | ±0.5° | Measurement error |
| Magnetic track depth | ±0.1 mm | Marker flush fit |

---

## 4. Manufacturing Critical Points

### 4.1 T-Slot Machining
- Use sharp tooling to prevent burrs
- Check slot width with go/No-go gauge
- Deburr all edges before anodize

### 4.2 Anodize Process
- Type III hard coat (25–50 μm)
- Mask T-slot floors for PTFE fit
- Seal after anodize

### 4.3 Laser Etch
- Etch depth:0.05–0.15 mm
- Black paint fillfor contrast
- Verify readability under normal indoor lighting

---

## 5. User Maintenance

| Task | Frequency | Method |
|------|-----------|--------|
| Clean T-slot | Monthly | Compressed air + brush |
| Wipe PTFE strips | As needed | Dry cloth |
| Check foot pads | Quarterly | Inspect for wear; replace if loose |
| Verify angle calibrate | Annually | Compare to reference gauge |

---

*Document version: 1.0*  
*Status: Ready for prototype validation*