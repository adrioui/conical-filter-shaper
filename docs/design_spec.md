# V1 Universal Filter Ruler — Design Specification

> **Document type:** Product design specification  
> **Revision:** 1.0 | Date: 2026-04-06  
> **Scope:** Adjustable angle ruler for folding coffee filter papers into precise cone angles  
> **Companion doc:** `docs/manufacturability.md` (materials, sourcing, BOM)

---

## 1. Design Intent & Scope

### 1.1 Problem Statement

When folding circular coffee filter papers into cone shapes, achieving consistent angles is difficult without specialized tools. Inconsistent folds lead to:
- Variable brew extraction times
- Unpredictable pour-over behavior
- Difficulty reproducing successful recipes
- Wasted time and paper on trial-and-error folding

### 1.2 Product Goal

A precision aluminum ruler with adjustable sliding arms that enables users to:
- Set any angle between 40° and 85° (included angle)
- Fold circular filter papers into precise, repeatable cone shapes
- Mark preset angles with magnetic markers for quick recall
- Measure overlap distances for consistent seam placement

### 1.3 Target Users

- Specialty coffee enthusiasts
- Baristas seeking consistent brew results
- Coffee educators teaching filter folding techniques
- Home brewers wanting professional-quality results

---

## 2. System Architecture

```
TOP VIEW (arms at60°)
                            
      ┌─────────────────────────────┐
      │         BASE PLATE          │
      │   ┌───────────────────────┐ │
      │   │     MAGNETIC TRACK     │ │
      │   │  ●●●●●●●●  ← markers   │ │
      │   └───────────────────────┘ │
      │                             │
      │ ╲      T-SLOT       ╱       │
      │    ╲    RAIL     ╱          │
      │      ╲        ╱            │
      │        ╲    ╱← sliding arms│
      │          ╲╱                 │
      │           │                │
      │     ┌─────┴─────┐          │
      │     │  PIVOT    │          │
      │     │  ORIGIN   │          │
      │     └───────────┘          │
      │                             │
      │  40°    60°    85°          │ ← angle scale
      └─────────────────────────────┘
```

### 2.1 Component Summary

| Component | Function | Key Feature |
|-----------|----------|-------------|
| **Base Plate** | Structural foundation | T-slot rails, angle scale, magnetic track |
| **Sliding Arms** (×2) | Define fold angle | Vernier scale, fold guide edge |
| **Cam Locks** (×2) | Lock arm position | Quarter-turn eccentric cam |
| **Magnetic Markers** (×8) | Angle presets | Color-coded, N52 magnets |
| **Ferrous Strip** | Marker retention | Zinc-plated mild steel inset |
| **PTFE Strips** (×2) | Low-friction sliding | Ultra-smooth arm movement |

---

## 3. Component Details

### 3.1 Base Plate

The structural foundation machined from 6061-T6 aluminum.

**Dimensions:**
- Length: 200 mm (Standard) or 150 mm (Travel)
- Width: 120 mm (Standard) or 90 mm (Travel)
- Thickness: 8 mm

**Features:**
- Two T-slot rails for sliding arm engagement
- Magnetic track recess (1mm deep) for ferrous strip
- Laser-etched angle scale (1° minor ticks,5° major ticks)
- Vernier scale reference marks
- Filter size guide circles (01,02, 03 sizes)
- Overlap measurement scale (0–20 mm)
- Four silicone foot pads (recessed, adhesive-mounted)

**Tolerances:**
- T-slot width: 6.0 +0.02/−0.00 mm
- T-slot depth: 5.0 ±0.05 mm
- Flatness: 0.05 mm overfull length
- Surface finish: Ra ≤0.8 μm before anodize

**Materials & Finish:**
- Material: 6061-T6 Aluminum
- Finish: Type III hard anodize (space grey or matte black)
- Secondary: Laser etch + black paint fill for scales

### 3.2 Sliding Arms

Two identical arms that pivot from the center-top of the base plate.

**Dimensions:**
- Length: 150 mm
- Width: 25 mm
- Thickness: 6 mm

**Features:**
- T-slot engagement tab at bottom (5mm depth)
- Raised fold guide edge (3mm height, R2mm rounded)
- Vernier scale on inner edge
- Cam lock mounting hole (M5 shoulder bolt)

**Tolerances:**
- Width: 25.0 ±0.05 mm
- Thickness: 6.0 ±0.05 mm
- T-tab engagement: ±0.02 mm

**Materials & Finish:**
- Material: 6061-T6 Aluminum
- Finish: Type III hard anodize (space grey)

### 3.3 Cam LockMechanism

Eccentric cam lock for securing arm position.

**Specifications:**
- Throw: 90° (quarter-turn)
- Lever length: 25 mm
- Clamp force: ≥50 N when locked
- Material (cam body): SS316 (passivated)
- Material (lever): 6061-T6 Al (Type III hard anodize)
- Bolt: M5 shoulder bolt, SS316

**Operation:**
- Single-handed operation
- Positive lock indication
- Field-replaceable

### 3.4 Magnetic Markers

Color-coded markers for preset angle positions.

**Specifications:**
- Quantity: 8 total (4 colors ×2 each)
- Colors: Red, Blue, Green, Yellow
- Diameter: 6 mm
- Height: 4 mm
- Magnet: N52 Neodymium, Ø5×2 mm
- Housing: 6061-T6 Al, Type II anodize (color-matched)
- Pull force: ≥0.5 kg

**Internal Structure:**
- Aluminum housing (anodized)
- N52 magnet pressed into housing
- Adhesive backup for security

### 3.5 Ferrous Strip

Mild steel inset that anchors magnetic markers.

**Specifications:**
- Length:180 mm
- Width: 6 mm
- Thickness: 1 mm
- Material: Mild steel, zinc plated
- Mounting: Press-fit into base plate recess

### 3.6 PTFE Slide Strips

Ultra-smooth bearing surfaces for arm sliding.

**Specifications:**
- Quantity: 2
- Length: 180 mm
- Width: 6 mm
- Thickness: 0.5 mm
- Material: PTFE (polytetrafluoroethylene)
- Mounting: Press-fit into T-slot floor

---

## 4. Angle Measurement System

### 4.1 Operating Range

| Parameter | Value |
|-----------|-------|
| Minimum angle | 40° |
| Maximum angle | 85° |
| Range |45° |
| Measurement type | Full included angle |

### 4.2 Scale Accuracy

| Feature | Tolerance |
|---------|-----------|
| Primary scale | ±0.1° at each major tick |
| Vernier scale | 0.5° resolution |
| Overall accuracy | ±0.5° verified at QC |

### 4.3 Vernier Scale Principle

The vernier scale on each sliding arm provides 0.5° resolution:
- Primary scale: 1° ticks on base plate
- Vernier scale: 0.5° subdivisions on arm edge
- Alignment method: Match vernier line to closest primary tick

---

## 5. Assembly Procedure

1. **Install PTFE strips**: Press-fit PTFE strips into T-slot floors
2. **Install ferrous strip**: Press-fit zinc-plated strip into magnetic track recess
3. **Insert arms**: Slide arms into T-slot rails from top
4. **Install cam locks**: Thread M5 shoulder bolts through cam bodies into arm mounting holes
5. **Apply foot pads**: Adhere silicone pads to recessed positions on base plate bottom
6. **Attach markers**: Place magnetic markers on ferrous strip at desired preset angles
7. **QC verification**: Check angle accuracy at 40°, 60°, 85° using calibration jig

---

## 6. Quality Control Points

### 6.1 Critical Dimensions (100% inspection)

- T-slot width and fit
- Sliding smoothness (PTFE coefficient)
- Angle scale accuracy
- Cam lock hold force

### 6.2 Sampling Inspection (10%)

- Anodize thickness
- Laser etch depth
- Edge finish
- Marker pull force

---

## 7. Dimensions Reference Card

```
UNIVERSALFILTER RULER — STANDARD VERSION

          200 mm
    ┌─────────────────────┐
    │    ┌───────────┐    │
    │    │  FERROUS  │    │  120 mm
    │    │  TRACK    │    │
    │    └───────────┘    │
    │ ╲    T-SLOTS    ╱   │
    │   ╲           ╱     │
    │     ╲       ╱       │
    │       ╲   ╱← arms  │
    │         ╲╱          │
    │          │pivot    │
    │      ┌───┴───┐     │
    │      │ SCALE │     │
    │      │40-85°│     │
    └─────────────────────┘

Arms: 150×25×6 mm each
Base: 200×120×8 mm
Total folded height: 15 mm
Weight: ~350 g
```

---

## 8. Open Items

| # | Item | Status |
|---|------|--------|
| 1 | Validate filter size circles against real papers | Pending |
| 2 | User testing for vernier readability | Pending |
| 3 | Cam lock torque specification | Pending |
| 4 | Marker color standardization | Pending |

---

*Companion document: `docs/manufacturability.md` — materials, sourcing, COGS*  
*Next step: Prototype validation and user testing*