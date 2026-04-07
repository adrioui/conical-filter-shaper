# Design Specification — Universal Coffee Filter Ruler v3

**Revision**: v3.0 (Bevel Gauge with Tapered Arms)  
**Date**: 2026-04-07  
**Status**: Specified, CAD reimplementation pending

## 1. Design Intent

An adjustable bevel-gauge style tool for folding coffee filter papers to precise cone angles (40°–85°) and serving as a compact dripper stand. Inspired by the Suprima SD1R ruler. First adjustable filter folding tool on the market.

## 2. Product Form

Two identical tapered stainless steel arms joined at their narrow ends by a pivot bolt with a knurled thumbscrew lock. The arms spread to set the desired cone angle.

```
FOLDED:                      OPEN AT 60°:
┌──────────────┐                  ╲        ╱
│ 130×80×4mm   │                   ╲  60° ╱
│ ~125g        │                    ╲    ╱
│ pocket-sized │                     ╲  ╱
└──────────────┘                      ●  ← pivot + thumbscrew
```

## 3. Arm Specifications

**Quantity**: 2 (identical left/right)

| Parameter | Value |
|-----------|-------|
| Shape | Trapezoid (tapered) |
| Length (pivot hole to tip) | 120mm |
| Width at pivot end | 25mm |
| Width at tip end | 65mm |
| Thickness | 1.2mm |
| Material | SS304 stainless steel |
| Finish | #4 brushed (120-150 grit) |
| Edge radius | R0.3mm (all edges deburred) |
| Pivot hole | Ø5.3mm (M5 clearance), centered, 10mm from narrow edge |

### 3.1 Arm Features

1. **Filter size arc marks** (laser etched, 0.1mm deep V-grooves):
   - 01 arc at R=95mm from pivot hole center
   - 02 arc at R=116mm from pivot hole center
   - 03 arc at R=137mm from pivot hole center (partial, may extend beyond tip)

2. **Protractor scale** (on one arm only, near pivot):
   - Range: 40°–85°
   - Major divisions: every 5°
   - Minor divisions: every 1°
   - Laser etched with contrast fill

3. **Named angle presets** (etched labels on protractor):
   - 48°: "SD1R"
   - 55°: "SD1"
   - 60°: "V60"
   - 80°: "UFO"

4. **Inner straight edge** (folding reference):
   - Must be geometrically straight
   - R0.3mm edge radius for clean paper folds
   - This is the primary functional surface

## 4. Pivot Assembly

| Component | Specification |
|-----------|---------------|
| Bolt | M5 × 12mm shoulder bolt, SS316 |
| Shoulder diameter | 8mm |
| Shoulder length | 4mm |
| Washer | PTFE, 10mm OD × 5.3mm ID × 0.5mm thick |
| Thumbscrew | M5 knurled, SS304, Ø15mm head, 8mm head height |

**Stack order** (Z-axis, bottom to top):
1. Bottom arm: 1.2mm
2. PTFE washer: 0.5mm
3. Top arm: 1.2mm
4. Thumbscrew head

Total mechanical stack: 2.9mm + bolt/screw hardware

## 5. Angle Measurement System

The protractor scale is etched near the pivot on the top arm. The reference indicator is the straight inner edge of the bottom arm, visible through the gap between arms.

**Accuracy target**: ±0.5° when read at the scale

## 6. Filter Folding Operation

1. Loosen thumbscrew
2. Open arms to target angle (read from protractor scale)
3. Tighten thumbscrew to lock
4. Place V60 filter paper on top of both arms (centered on pivot)
5. Fold filter paper down along both straight inner edges
6. Crease firmly — the fold converts the filter to the target cone angle
7. Remove filter and insert into dripper

**The math**: A V60 filter is a 180° sector. Folding it at angle θ creates a cone with half-angle α where sin(α) = θ/360°. By setting the ruler to angle θ_target and folding, the excess paper wraps to create the desired cone angle.

## 7. Dripper Stand Operation

1. Open arms to match dripper's cone angle
2. Place ruler on flat surface or cup rim
3. Set dripper into the V-opening
4. Dripper rim rests on both arm surfaces
5. V-cradle provides lateral stability; arm weight provides counterweight

**V-opening width** at distance d from pivot: `w = 2 × d × sin(angle/2)`

Example: V60-02 at 60°, d=116mm → w = 2 × 116 × sin(30°) = 116mm ✓

## 8. Material Properties

### SS304 Stainless Steel
| Property | Value |
|----------|-------|
| Tensile strength | 515 MPa |
| Yield strength | 205 MPa |
| Density | 8.0 g/cm³ |
| Corrosion resistance | Excellent |
| Food-grade | Yes |
| Magnetic | Slightly (after cold work) |

## 9. Manufacturing Process

1. **Laser cut** arms from 1.2mm SS304 sheet (nest for material efficiency)
2. **Deburr** all edges to R0.3mm (tumble or manual)
3. **Brush finish** #4 (belt sanding, 120-150 grit, linear along length)
4. **Laser etch** features:
   - Protractor scale (40°–85°, 1° divisions)
   - Arc marks (R=95, 116, 137mm)
   - Named presets (SD1R, SD1, V60, UFO)
   - Logo/branding
5. **Contrast fill** etched marks (black paint fill, wipe clean)
6. **Assemble**: bottom arm + PTFE washer + top arm + shoulder bolt + thumbscrew
7. **QC**: angle accuracy, edge straightness, smooth rotation, torque check

## 10. Tolerances

| Feature | Tolerance |
|---------|-----------|
| Arm length | ±0.1mm |
| Arm width | ±0.1mm |
| Pivot hole position | ±0.05mm |
| Pivot hole diameter | ±0.02mm |
| Inner edge straightness | 0.05mm over 120mm |
| Angle scale accuracy | ±0.5° |
| Arc mark radius accuracy | ±0.2mm |
| Thickness | ±0.05mm |
| Edge radius | R0.3 ±0.1mm |
| Overall flatness | 0.1mm over 120mm |

## 11. Bill of Materials

| # | Part | Qty | Material | Est. Cost (500 qty) |
|---|------|-----|----------|--------------------:|
| 1 | Tapered Arm | 2 | SS304, 1.2mm | $0.80 ea |
| 2 | M5 Shoulder Bolt | 1 | SS316 | $0.35 |
| 3 | PTFE Washer | 1 | PTFE | $0.08 |
| 4 | M5 Knurled Thumbscrew | 1 | SS304 | $0.65 |
| | **Total COGS** | | | **~$3.18** |

## 12. Weight Estimate

| Part | Weight |
|------|--------|
| Arm (each) | ~52g |
| Arm × 2 | 104g |
| Shoulder bolt | 8g |
| PTFE washer | <1g |
| Thumbscrew | 12g |
| **Total** | **~125g** |

Arm area: (25+65)/2 × 120 = 5400mm² → 5400 × 1.2mm = 6480mm³ = 6.48cm³ × 8.0g/cm³ = 51.8g

## 13. Revision History

| Version | Date | Description |
|---------|------|-------------|
| v1.0 | 2026-04-05 | Initial: flat base plate with T-slot rails + sliding arms (aluminum) |
| v2.0 | 2026-04-06 | Hinged V-shape: two narrow rectangular SS304 legs with magnetic pivot |
| **v3.0** | **2026-04-07** | **Bevel gauge: two tapered SS304 arms with simple thumbscrew pivot** |
