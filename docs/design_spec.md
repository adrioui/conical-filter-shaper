# V1 Universal Conical Coffee Filter Shaping System — Design Specification

> **Document type:** Mechanism design spec — pre-CAD, pre-prototype  
> **Revision:** 0.1 | Date: 2026-04-05  
> **Scope:** Three-preset angle-indexed mandrel system for reshaping **standard pre-seamed conical paper filters**  
> into repeatable precision cones before insertion into pour-over drippers.  
> **Companion doc:** `docs/manufacturability.md` (materials, sourcing, BOM)

---

## 1. Design Intent & Scope

### 1.1 Problem Statement

Standard pre-seamed conical coffee papers still require the user to open, bias, and seat them by hand before brewing. In practice this is inconsistent and causes:
- Uneven wall contact → channeling during pour
- Inconsistent tip seating at the dripper apex → flow rate variability
- Wrong cone angle for the target dripper → filter bunching or wall collapse
- Factory seam ridge landing in a different place each time → local gaps, wrinkles, and poor transfer into the brewer

### 1.2 Product Goal

A handheld tool that a barista or home user can use in under 10 seconds to reliably reshape a standard pre-seamed cone paper into one of three selectable cone angles, with a consistent tip geometry and repeatable seam handling, and then insert it directly into the dripper without disturbing the formed shape.

### 1.3 Angle Convention

All angles in this document are **full included angles** (apex angle — measured across the cone from side to side):

| Preset | Included Angle | Half-Angle (from axis) | Target Dripper Family |
|--------|---------------|------------------------|----------------------|
| 1 | **48°** | 24° | Narrow specialty cones (Timemore, Origami narrow) |
| 2 | **60°** | 30° | Hario V60 family, standard pour-over (most common) |
| 3 | **80°** | 40° | Wide flat cones, some 3rd-wave specialty drippers |

### 1.4 V1 Input Paper Definition

V1 is defined around **standard pre-seamed conical paper filters** removed from their retail pack and opened by hand.

- **Primary reference family:** common **02-class** cone papers
- **Primary workflow target:** **60° / P2**
- **Compatibility presets:** 48° and 80° remain in scope, but need physical paper/dripper validation
- **Out of scope for V1:** shaping raw flat circular discs, custom-cut blanks, or user-made seams

Mandrel geometry is therefore specified by **cone angle + slant height**, not by a raw blank diameter.

---

## 2. System Architecture Overview

```
TOOL ORIENTATION: Apex UP, Base DOWN
                    
         ●  ← Ejection Button (recessed, push-to-release)
        /|\
       / | \  ← Tip Insert Block (SS 316L) with tip-locating dimple
      /  |  \
     /   |   \
    /    |    \  ← Half-Shell L + Half-Shell R (split along axial plane)
   /     |     \    Hinge pin at apex (shared with tip insert)
  /      |      \   Seam Guide Fin in radial slot on Shell R
 /       |       \
/________|________\
|  Angle-Set Ring  |  ← Cam ring, rotates 60° per click, 3 positions
|  (click-index)   |    Shell base pins ride in cam track
|__________________|
|    Handle Body   |  ← Fixed housing; ring captured inside
|   (grip zone)    |    Detent ball assembly housed here
|__________________|
         |
      (base cap)
```

### 2.1 Sub-System Summary

| Sub-system | Function | Key Component |
|------------|----------|---------------|
| **Split-Shell Mandrel** | Defines cone forming surface | Half-Shell L, Half-Shell R |
| **Apex / Tip Insert** | Hinge anchor + tip locator + ejection | Tip Insert Block |
| **Angle-Set Ring** | Sets and locks cone included angle | Cam Ring |
| **Detent Assembly** | Indexes and holds ring at 3 positions | Ball, Spring, Retainer |
| **Seam Guide / Relief** | Controls factory seam clocking and clearance | Sliding Fin + Serrated Clip |
| **Ejection System** | Breaks filter/mandrel adhesion post-insert | Push Rod + Return Spring |
| **Handle Body** | Structural chassis + user grip | Handle Housing |

---

## 3. Sub-System Descriptions

### 3.1 Split-Shell Mandrel

**Principle:** Two identical half-shells (mirror images, split along the axial plane through the cone) are hinged together at the apex. Their base ends ride in the cam track of the Angle-Set Ring. Rotating the ring drives both shell bases simultaneously to the required radial spread, setting the cone angle.

**Geometry (reference mandrel, sized around common 02-class pre-seamed papers):**

| Parameter | Value | Basis |
|-----------|-------|-------|
| Slant height (generating line) | 82 mm | Leaves ~10 mm paper above base rim |
| Mandrel height (axial) at 48° | 74.9 mm | h = L × cos(24°) |
| Mandrel height (axial) at 60° | 71.0 mm | h = L × cos(30°) |
| Mandrel height (axial) at 80° | 62.8 mm | h = L × cos(40°) |
| Base radius at 48° (r₁) | 33.3 mm | r = L × sin(24°) |
| Base radius at 60° (r₂) | 41.0 mm | r = L × sin(30°) |
| Base radius at 80° (r₃) | 52.7 mm | r = L × sin(40°) |

> **Note:** At 80°, the base diameter of the mandrel is **105.4 mm**. This sets the minimum inner diameter of the Angle-Set Ring and the overall tool width at its widest.

**Shell material (V1):** POM-C (Acetal Copolymer), CNC machined  
**Shell wall thickness:** 2.5 mm minimum; thicker at base tab region (4.0 mm)  
**Split plane:** Contains the cone axis; shell edge has a 0.2 mm relief chamfer to prevent filter paper snagging at the seam  
**Shell base tab:** Extends 12 mm below the cone base; houses the cam follower pin (M4 SS 316L shoulder bolt, press-fit H7/n6)  
**Surface finish:** Ra ≤ 0.8 µm on filter contact face (ensures clean paper release and no drag during formation)

### 3.2 Apex / Tip Insert Block

The Tip Insert Block is a precision-machined SS 316L block that:
1. Acts as the structural apex anchor (receives the hinge pin)
2. Provides the tip-locating feature for the filter paper
3. Houses the ejection push rod

```
Cross-section (Tip Insert Block):

       ┌─────────────────┐
       │ Ejection chamber│  ← Ø 4 mm main axial chamber; final tip breakout detail TBD
       │  (center axial) │
  ─────┤                 ├─────  ← Hinge pin bore (M3 SS pin, transverse)
  Shell│  Dimple pocket  │Shell
  L    │   ●  ·  ●      │R
       │  (tip locator)  │  ← 3 mm Ø × 2 mm deep conical dimple
       └────────┬────────┘
                │ (cone apex = bottom of dimple)
```

**Tip locator dimple:** 3.0 mm diameter, 2.0 mm deep, 60° included angle (conical base). Receives the closed paper apex / tip of the pre-seamed cone and recenters it on the tool axis during shaping.

**Hinge pin:** M3 × 20 mm SS 316L shoulder bolt (head recessed flush). Clearance fit in shell bores (H7/f7, 0.01–0.03 mm clearance).

**Ejection rod:** Ø 3.0 mm SS 304 rod, 100 mm long, spring-returned (see §3.6).

> **CAD status note:** the current V1 model uses a nominal stepped axial path: a blind 4.0 mm top-entry chamber plus a 3.0 mm guide bore into the tip region. The exact rod-tip / paper-contact behavior still requires physical validation before claiming a fully manufacturable ejection stack.

**Block dimensions:** 18 mm × 18 mm × 22 mm  
**Material:** SS 316L, CNC machined, Ra ≤ 0.4 µm on filter contact face, electropolished

### 3.3 Angle-Set Ring (Cam Ring)

**Principle:** A disc-shaped ring that rotates inside the Handle Body. Two follower pins (one per shell base) ride in a dual-spiral cam track machined into the upper face of the ring. Rotating the ring 60° per click drives both follower pins simultaneously to a new radial position, changing the shell spread angle.

**Cam track geometry:**

The cam track has **6-fold alternating symmetry**: 3 preset arc segments, repeated 180° apart (for the 2 followers). Each full ring rotation of 180° cycles through all 3 presets twice.

| Ring position | Shell base pin radius | Resulting cone angle |
|--------------|----------------------|---------------------|
| 0° (click 1) | 33.3 mm | 48° |
| 60° (click 2) | 41.0 mm | 60° |
| 120° (click 3) | 52.7 mm | 80° |

**Cam track detail:**
- Track width: 5.0 mm (to clear M4 follower pin, Ø 3.9 mm)
- Track depth: 4.0 mm
- Dwell arc at each preset: 12° (prevents accidental jump)
- Transition ramp between presets: sinusoidal profile, 48° arc length (smooth, no impact)
- Track is cut into the upper face of the ring (open-face cam, not enclosed groove, for ease of machining)

**Ring dimensions:**
- Outer diameter: 120 mm (handle housing bore = 120.2 mm)
- Inner bore: 60 mm minimum (clears 80° shell base at full spread + 3 mm wall)
- Thickness: 14 mm
- Material: 6061-T6 Aluminium, Type II anodized hard-black

**Ring upper face** (cam track side): Ra ≤ 1.6 µm on track floor, 45° chamfer entry  
**Ring lower face** (user interface): Knurled or fluted grip, 1.5 mm pitch diamond knurl; angle indicator window (laser-etched numbers 48 / 60 / 80 at 60° spacing, viewed through handle window)

**Follower pin:** M4 SS 316L shoulder bolt, 4 mm shoulder Ø × 5 mm long, threaded into shell base tab. Pin shank (smooth) rides cam track; shoulder face contacts track floor.

### 3.4 Detent Assembly (Index Locking)

**Function:** Positively locks the Angle-Set Ring at each of the 3 preset positions. Must provide:
- Clear tactile click audible at arm's length
- Sufficient hold-in force to prevent ring drift during filter shaping (estimated forming load ≤ 5 N tangential)
- Release with deliberate twist force (~2–3 N·m)

**Design: Ball Detent in Handle Housing engaging Ring rim**

```
   Handle Housing (fixed)           Angle-Set Ring (rotating)
   ___________________               _______________________
  |   Blind bore      |             |  3× detent dimples    |
  |  ┌───┐            |  ←→→ ball   |  at 60° spacing       |
  |  │ ∿ │spring      |   engages   |  on ring outer rim    |
  |  └─●─┘            |             |                       |
  |___________________|             |_______________________|
```

**Components:**
- Ball: 4 mm Ø SS 316L (food-grade bearing ball)
- Spring: SS 302 compression spring, Ø 4.2 mm OD × 0.4 mm wire × 10 mm free length → compressed to 7 mm in assembly (design load ≈ 3.2 N)
- Ball pocket (in handle housing): Ø 4.1 mm × 9 mm deep blind bore, tangentially oriented toward ring rim
- Retainer: M4 SS 316L set screw (grub screw), DIN 913, installed after spring+ball
- Dimples (in ring rim): 3× dimples at 60° spacing, each 4 mm Ø × 1.4 mm deep (35% ball radius — gives crisp click without excessive force)

**Force analysis (estimated):**
- Spring preload at assembly: 3.2 N
- Detent break-out force (tangential): F_out ≈ 3.2 N × tan(45°) / (friction_coeff × lever) ≈ 3–4 N tangential at ring rim (60 mm radius → ~0.18–0.24 N·m torque to release)
- This is intentionally light — easy to rotate but not so loose that it drifts

> **Note:** A second set screw adjustment allows the ball spring preload to be increased or decreased in the field by ±0.5 mm set screw depth change.

### 3.5 Seam Guide / Relief Fin (Adjustable)

**Function:** Provides a repeatable reference for the **existing factory seam** of a pre-seamed cone paper, keeping the seam ridge away from the shell split line and helping the paper clock to the same position on every use.

**Placement:** On Shell R outer surface, adjacent to the seam-relief side of the mandrel. The fin is radial (perpendicular to the cone surface) and extends from near the apex to near the base.

**Mechanism: Sliding Serrated Fin with Friction Clip**

```
Shell R outer surface (cross-section through seam-guide slot):

   Cone surface (outer)
   ─────────────────────────────────
          │  fin slot (radial)     │
          │    ┌──────────┐        │
          │    │  Fin     │← 0.5mm SS spring steel
          │    │  ● ● ●  │← serration teeth (0.5mm pitch, 3 teeth)
          │    └──────────┘
          │    clip grips here (friction)
   ─────────────────────────────────
```

**Components:**
- **Fin blade:** 0.5 mm × 6 mm × 75 mm SS 301 spring steel (half-hard). Laser-cut to shape, edges deburred and electropolished. Etched markings at 5.0, 7.5, 10.0, 12.5, 15.0 mm from fin base (guide-position scale).
- **Serration strip:** 3 micro-teeth on fin shank (formed during laser cut + press brake), 0.5 mm pitch, 0.2 mm tooth height. Engage matching serrations in slot walls for friction hold.
- **Fin slot:** Radial slot in Shell R, 0.55 mm wide × 7 mm deep × 76 mm long. Slot walls have matching micro-serration texture (EDM or milled pattern).
- **Retention:** Interference fit via serrations, ≈ 8–12 N pull-out force at each position. User re-positions by pinching fin blade and pulling/pushing.

**Guide positions:** Five nominal positions: **5 / 7.5 / 10 / 12.5 / 15 mm**  
Default factory setting: **10 mm** (marked with ▶ on shell surface)

> **Status note:** exact brand-to-position mapping is not yet physically validated. These positions remain provisional V1 tuning points, not a proven compatibility matrix.

**When to adjust:**
- Thick / stiff papers with a pronounced factory seam: 12.5–15 mm
- Thin papers that sit flatter against the mandrel: 7.5–10 mm
- Papers that seat cleanly on shell seam relief alone: remove fin entirely (fin is fully removable)

### 3.6 Ejection System

**Function:** After the user inserts the shaped-filter/mandrel assembly into the dripper, the filter is held by friction against the dripper walls. The ejection system breaks this grip cleanly without disturbing the filter shape.

**Mechanism: Spring-Loaded Push Rod through Tip Insert**

```
External                   Internal
                    
  [Button cap]  ←user presses
      │
  ┌───┴───┐
  │ Button│
  │  body │
  └───┬───┘
      │ push rod (SS 304, Ø 3 mm, 100 mm long)
      │
  ○○○○○ ← return spring (SS 302, Ø 4 mm OD, 15 mm FL, 0.4 mm wire)
      │
  ┌───┴───┐
  │ Tip   │  ← filter tip contact face
  │ face  │     Ø 4 mm, slightly convex (R = 10 mm)
  └───────┘
```

**Operation:**
- At rest: rod tip is recessed 1.5 mm inside the tip dimple (spring holds it retracted)
- When pressed: rod extends 5 mm beyond the tip dimple surface — this breaks filter adhesion and pushes the filter tip into the dripper apex pocket
- Spring return: rod snaps back automatically when released

**Button cap:** 10 mm Ø POM-C cap, snap-fit onto rod end, flush with tip insert block top face. Knurled rim for grip.

**Push rod:** SS 304 Ø 3.0 mm, runs in a nominal 3.0 mm guide land (light sliding fit, target 0.000–0.016 mm clearance) within the ejection bore stack  
**Return spring force:** ≈ 1.5 N at rest, ≈ 2.8 N at full extension (gentle, not disruptive)

---

## 4. Parts List

| # | Part Name | Qty | Material | Process | Notes |
|---|-----------|-----|----------|---------|-------|
| 1 | Half-Shell L | 1 | POM-C | CNC milled | Mirror of R; cam follower pin boss at base |
| 2 | Half-Shell R | 1 | POM-C | CNC milled | Seam-guide fin slot machined in |
| 3 | Tip Insert Block | 1 | SS 316L | CNC turned + milled | Tip dimple, hinge bore, push rod bore |
| 4 | Apex Hinge Pin | 1 | SS 316L | M3 shoulder bolt | Captured, head flush |
| 5 | Cam Follower Pin L | 1 | SS 316L | M4 shoulder bolt | Press-fit into Shell L base tab |
| 6 | Cam Follower Pin R | 1 | SS 316L | M4 shoulder bolt | Press-fit into Shell R base tab |
| 7 | Angle-Set Ring (Cam Ring) | 1 | 6061-T6 Al | CNC milled + Type II anodize | Cam track on upper face; knurl + angle labels on rim |
| 8 | Handle Housing | 1 | 6061-T6 Al | CNC turned + milled + anodize | Ring bore; detent pocket; ejection bore; angle window |
| 9 | Handle Grip Insert | 1 | NBR-70 overmold or TPU sleeve | Moulded / laser-cut wrap | Food-safe grip, slip-resistant |
| 10 | Detent Ball | 1 | SS 316L | 4 mm Ø ball bearing | Standard; bought in |
| 11 | Detent Spring | 1 | SS 302 | Compression spring | Custom or standard: Ø 4.2 × 10 mm FL × 0.4 mm wire |
| 12 | Detent Set Screw (retainer) | 1 | SS 316L | M4 × 8 mm grub screw, DIN 913 | Retains detent ball/spring; thread-locked |
| 13 | Seam Guide Fin | 1 | SS 301 half-hard | Laser-cut + press-formed | 0.5 × 6 × 75 mm; guide-position scale etched |
| 14 | Ejection Push Rod | 1 | SS 304 | CNC turned | Ø 3.0 mm h6 × 100 mm |
| 15 | Ejection Return Spring | 1 | SS 302 | Compression spring | Ø 4 × 15 mm FL × 0.4 mm wire |
| 16 | Ejection Button Cap | 1 | POM-C | CNC turned | 10 mm Ø, snap-fit, knurled |
| 17 | Base Cap / Ring Retainer | 1 | 6061-T6 Al | CNC turned + anodize | Snap-locks onto bottom of Handle Housing; retains Angle-Set Ring axially |
| 18 | Ring Bearing Washer (×2) | 2 | PTFE | Punched | 0.5 mm thick, reduces ring rotation friction |
| 19 | Assembly Screws (M3 SHCS) | 4 | SS 316L | ISO 4762 | Handle assembly + tip insert retention |
| **Total unique parts** | **19** | | | | Excl. Loctite, minor hardware |

---

## 5. User Workflow

### Pre-use (one-time setup per session)

**Step 1 — Select cone angle preset**

> Grip the Handle Body. With the other hand, pinch the knurled Angle-Set Ring rim and rotate until the desired angle number (48 / 60 / 80) appears in the handle window.  
> **Tactile confirm:** Feel the detent click. The ring should resist twist — if it does not click clearly, rotate slightly until the detent seats.

**Step 2 — Set seam guide**

> Look at the Seam Guide Fin on the right side of the mandrel. The fin protrudes from the cone surface. Leave it at the default **10 mm** setting unless a specific paper brand has been validated to work better at another mark.

---

### Forming sequence (each filter)

**Step 3 — Locate the paper tip and seam**

> Hold the tool apex-up. Take a standard pre-seamed cone paper and gently open it. Place the paper tip / closed apex over the Tip Insert Block dimple. Rotate the paper so its factory seam aligns with the seam-guide side of the mandrel.

**Step 4 — Seat the paper on the mandrel**

> Keeping the paper tip engaged in the dimple, ease the paper down over the cone surface. Let the factory seam ride against the Seam Guide Fin and shell seam-relief side rather than bunching across the split line.

**Step 5 — Smooth and pre-shape**

> Lightly smooth the opposite wall of the paper around the mandrel so the pre-seamed cone reforms to the selected angle. Do not create a new overlap or user-made seam; V1 relies on the paper's existing manufactured seam.

**Step 6 — Set the tip (optional)**

> Tap the paper tip lightly with a finger against the Tip Insert Block. The tip should seat neatly in the dimple without puncturing or inverting.

---

### Insertion sequence

**Step 7 — Insert into dripper**

> Hold the Handle Body. Invert the tool (apex/tip down) over the dripper opening. Lower the filter-on-mandrel straight into the dripper. The filter's outer surface will contact the dripper wall and self-register. Apply gentle downward pressure to seat the filter against the dripper cone.

**Step 8 — Eject and withdraw**

> With the filter seated against the dripper walls, press the Ejection Button Cap on the tip (now at the bottom) with your thumb. You will feel the rod break the adhesion. Slowly withdraw the mandrel upward — the filter remains seated in the dripper.

---

### Reset

> Pull the two shells together by hand (they spring open to ~80° naturally) if you need to reuse immediately. The tool is ready for the next cycle.

---

## 6. Dimensions & Tolerances Strategy

### 6.1 Functional Dimension Groups

**Group A — Angle-critical (define cone geometry)**

| Interface | Nominal | Tolerance | Consequence of error |
|-----------|---------|-----------|---------------------|
| Cam track dwell radius at P1 (48°) | 33.3 mm | ±0.1 mm | ±0.17° in included angle |
| Cam track dwell radius at P2 (60°) | 41.0 mm | ±0.1 mm | ±0.14° |
| Cam track dwell radius at P3 (80°) | 52.7 mm | ±0.1 mm | ±0.11° |
| Shell base pin OD | 4.0 mm | ±0.01 mm (h6) | Pin play in track → slack in angle |
| Shell slant length (apex to base pin) | 82.0 mm | ±0.2 mm | ±0.14° per mm error |

**Target angle accuracy: ±0.5° included angle at each preset.** This is within the functional requirement — dripper walls have ≥0.5° tolerance themselves, and paper is compressible.

**Group B — Tip locator (filter centering)**

| Interface | Nominal | Tolerance |
|-----------|---------|-----------|
| Tip dimple position from cone axis | 0 mm (on axis) | ±0.3 mm concentricity |
| Tip dimple depth | 2.0 mm | ±0.15 mm |
| Tip dimple included angle | 60° | ±5° (noncritical) |
| Ejection rod tip flush depth (rest) | −1.5 mm (recessed) | ±0.3 mm |

**Group C — Seam guide fin (paper seam control)**

| Interface | Nominal | Tolerance |
|-----------|---------|-----------|
| Fin slot width | 0.55 mm | +0.05 / −0.00 mm |
| Fin blade thickness | 0.50 mm | ±0.02 mm |
| Fin position marks (5/7.5/10/12.5/15 mm) | Per mark | ±0.3 mm |
| Fin pull-out force (at each serration) | 10 N | ±4 N (soft limit) |

**Group D — Rotary interfaces (ring in housing)**

| Interface | Nominal | Tolerance | Fit |
|-----------|---------|-----------|-----|
| Ring OD | 120.0 mm | −0.0 / −0.05 mm | Clearance in housing bore |
| Housing ring bore | 120.2 mm | +0.0 / +0.05 mm | ~0.1–0.2 mm diametral clearance |
| Ring axial float (PTFE washers) | 0.5 mm per washer | ±0.1 mm | Controls ring wobble |
| Detent dimple depth (in ring rim) | 1.4 mm | ±0.1 mm | Critical — see §7 |

**Group E — Ejection system**

| Interface | Nominal | Tolerance | Fit |
|-----------|---------|-----------|-----|
| Push rod OD | 3.0 mm | −0.006 / −0.014 mm (h6) | Sliding in H7 bore |
| Tip insert bore | 3.0 mm | +0.010 / +0.025 mm (H7) | |
| Ejection stroke | 5.0 mm | ±0.5 mm | Noncritical |

### 6.2 Tolerance Stack Analysis (Cone Angle)

Worst-case angle error stack (48° preset example):

| Source | Error contribution |
|--------|-------------------|
| Cam track radius tolerance | ±0.10 mm |
| Follower pin diametral play in track | ±0.05 mm (half-clearance) |
| Shell slant length variation | ±0.20 mm → ±0.14° |
| Hinge pin lateral play | ±0.02 mm → ±0.01° |
| **Worst-case total (RSS)** | **≈ ±0.24°** |
| **Worst-case total (linear sum)** | **≈ ±0.40°** |

Conclusion: ±0.5° requirement is achievable without process improvements. Assembly verification recommended at QC with angle gauge.

### 6.3 Critical Surface Specifications

| Surface | Ra requirement | Method | Reason |
|---------|---------------|--------|--------|
| Shell filter contact face | ≤ 0.8 µm | Milling + light polishing | Filter release without tearing |
| Tip insert tip face | ≤ 0.4 µm | Turning + electropolish | Hygiene + filter contact |
| Cam track floor | ≤ 1.6 µm | End-mill, sharp tooling | Reduce follower wear |
| Ring outer rim (detent zone) | ≤ 0.8 µm | Turning | Consistent detent feel |
| Ejection rod | ≤ 0.4 µm | Ground or precision-turned | Low friction sliding |

---

## 7. Locking & Indexing Design

### 7.1 Index Mechanism Selection Rationale

Three mechanisms were evaluated:

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Ball detent (selected) | Low part count, proven, audible click, field-adjustable | Spring wear over time | **SELECTED** |
| Cantilever snap tab (POM integral) | Zero hardware | Wears after ~500 cycles, less precise | Backup for cost reduction |
| Friction ring + set screw | Continuously adjustable | No positive index, drifts | Rejected |

### 7.2 Ball Detent — Specification

**Geometry (critical for correct feel):**

```
                   ring rim
                  ___________
             ____/           \____
            /   detent dimple     \
           /      depth = 1.4 mm   \
          |    ● ball Ø 4 mm        |
          |                         |
        spring → 3.2 N preload
```

| Parameter | Value | Notes |
|-----------|-------|-------|
| Ball diameter | 4.0 mm | SS 316L, grade G25 |
| Dimple depth | 1.4 mm (~35% of 4.0 mm ball diameter) | Deeper = stiffer click, harder to rotate |
| Dimple radius | 2.2 mm (110% of ball radius) | Slightly wider than ball for clean engagement |
| Spring free length | 10.0 mm | SS 302 |
| Spring compressed length | 7.0 mm (assembly) | |
| Spring preload force | ≈ 3.2 N | 0.32 N·mm⁻¹ × 3 mm = 3.2 N approx. |
| Tangential break-out force at ring rim | ≈ 3.5–4.5 N | Acceptable: resists shaping forces (~5 N max) |
| Torque to rotate ring | ≈ 0.21–0.27 N·m | Light but deliberate |

**Adjustment:** M4 set screw depth changes spring preload by ~1.0 N per 0.25 mm turn. User instruction: do not tighten set screw beyond the point where click disappears — this overloads the spring pocket walls in the housing.

### 7.3 Detent Durability

Target life: **10,000 cycles** minimum (barista daily use, 5 filters/day = 5.5 years)

At 10,000 cycles:
- Ball contact stress on SS ring rim: Hertzian contact, estimated ≈ 250 MPa peak → well below SS 316L yield (310 MPa), negligible deformation per cycle
- Ring anodize in detent zone: **must be masked during anodize** (anodize in dimple will vary depth unpredictably) → specify "mask detent dimples before anodize" on drawing
- Set screw seating: apply Loctite 243 (medium, removable) — do not use 270 (permanent) as the set screw may need field adjustment

### 7.4 Anti-Drift Feature

A secondary light-friction feature prevents the ring from rotating accidentally when the tool is dropped or jostled:
- The two PTFE bearing washers (between ring faces and housing faces) are slightly undersized in thickness (0.45 mm installed, from 0.5 mm stock → ~10% compression), creating a constant 0.3–0.5 N·m drag torque
- This drag supplements the detent without adding operator resistance (the detent break-out is intentionally much larger than the drag)

---

## 8. Failure Modes & Mitigations

### 8.1 FMEA Table

| # | Failure Mode | Root Cause | Effect | Severity | Likelihood | Mitigation | Detection |
|---|-------------|-----------|--------|----------|-----------|------------|-----------|
| F1 | **Filter tears at tip during formation** | Tip dimple edge too sharp; rod protruding at rest | Filter unusable; user frustration | High | Medium | R ≥ 0.5 mm on all dimple edges; verify rod recess depth at QC | Visual on first use |
| F2 | **Angle detent slips under forming load** | Undersize dimple depth; worn spring; insufficient preload | Wrong cone angle formed; filter fits poorly in dripper | High | Low-Med | Specify dimple depth ±0.1 mm; set screw adjustment; 10,000-cycle wear test | Click feel; filter fit |
| F3 | **Shells jam (won't spread to 80°)** | POM creep at cam follower boss; cam track burr; grit contamination | Tool unusable at 80° preset | High | Low | 4 mm fillet at POM boss; chamfer track entry; provide cleaning instructions | Rotation resistance |
| F4 | **Cam follower pin loosens in shell** | Insufficient press-fit interference; vibration; drops | Shell angular position uncertain → angle error | High | Low | H7/n6 press fit (0.01–0.021 mm interference in POM); blue Loctite 243 on pin shank | Angle check at QC |
| F5 | **Seam guide fin falls out** | Insufficient serration engagement; over-softened POM slot from hot water | Loss of seam repeatability | Med | Low | Serration depth 0.2 mm minimum; minimum 3 teeth engaged; do not use in >80°C water | Visual |
| F6 | **Seam guide fin bends permanently** | 0.5 mm SS 301 fin over-flexed during adjustment; wrong material hardness | Fin no longer perpendicular; seam unreliable | Med | Med | Use SS 301 half-hard (proof stress ≥ 520 MPa); limit fin protrusion to 15 mm (moment arm); DXF note: "DO NOT anneal after laser cut" | Visual |
| F7 | **Ejection rod sticks (fails to retract)** | Coffee oils + ground residue causing drag in bore | Filter insertion becomes difficult; tip may tear | Med | Med | Specify Ra ≤ 0.4 µm on bore and rod; rinse after use protocol; weekly mineral oil wipe | Stiff button feel |
| F8 | **Ejection rod extends during shaping** | Return spring too weak; user presses tip during formation | Creates hole in filter tip | High | Low | Design return spring force ≥ 2.5 N at full extension; recessed button cap prevents accidental contact | Shape inspection |
| F9 | **Shell surface scratches filter paper** | Tool dropped; abrasive contamination on shell face | Filter micro-tears at scratch; channeling | Med | Med | POM self-lubricating; Ra ≤ 0.8 µm; replacement POM shells as consumable wear parts | Visual; brew quality |
| F10 | **Handle housing ring bore wears oval** | AL 6061 bore wearing against rotating ring without bearing | Sloppy ring rotation; angle accuracy degrades | Med | Low-V1 | PTFE washers on ring faces; anodize bore to Ra ≤ 0.8 µm; upgrade to bronze bushing insert in V2 | Ring wobble |
| F11 | **Seam positioning too variable** | Fin position marks unclear; user misreads | Inconsistent seam clocking → local gaps / wrinkles vary between brews | Low | Med | Large, high-contrast laser-etch marks; default position marked prominently; user tutorial | Seam position measurement |
| F12 | **Filter sticks in dripper post-insertion** | Mandrel angle too close to dripper angle → paper clamps tight | Mandrel cannot withdraw; filter tears | High | Med | Mandrel angle targets INSIDE dripper cone: design for 0.5° tighter than dripper nominal → small gap at base rim; ejection rod provides impulse | First-use testing |

### 8.2 Priority Failure Modes for V1 Validation Testing

Test these first during Phase 1 alpha:

| Priority | Test | Pass Criterion |
|----------|------|---------------|
| 1 | Angle accuracy at all 3 presets | Measured included angle ±0.5° across 5 tools |
| 2 | Filter tear rate at tip | Zero tears in 50 shaping cycles per preset |
| 3 | Detent hold under forming load | No ring rotation with 5 N tangential load at rim |
| 4 | Filter insertion + ejection | Clean release in ≤ 3 s across V60 / Timemore / Origami |
| 5 | Seam-guide repeatability | Seam position σ ≤ 0.5 mm across 20 cycles at the 10 mm setting |
| 6 | 500-cycle accelerated wear | Angle accuracy and detent feel unchanged at cycle 500 |

---

## 9. Assembly Sequence

1. **Sub-assemble tip block:** Press ejection return spring + rod into bore. Snap button cap onto rod end. Verify rod recess depth = 1.5 mm (use depth gauge).
2. **Install apex hinge pin:** Pass M3 shoulder bolt through Shell L hinge boss → tip block → Shell R hinge boss. Apply Loctite 243 to thread. Torque to 0.5 N·m (hand-tight + 1/4 turn). Verify both shells pivot freely with no binding.
3. **Insert cam follower pins:** Press M4 pins into Shell L and Shell R base tabs (H7/n6 press, 0.8–2.1 µm interference). Use parallel press or vise — never hammer. Apply thin coat Loctite 243 to pin shank before pressing.
4. **Install seam guide fin:** With Shell R in free state, insert fin into slot at 10 mm mark (default). Verify resistance to pull-out is ≥ 6 N (use spring scale).
5. **Install PTFE washers in handle:** Drop 1 PTFE washer into each ring bearing face of handle housing bore.
6. **Capture Angle-Set Ring in handle:** Drop ring into housing (follower pins enter cam track). Verify ring rotates freely through all 3 clicks before final retention.
7. **Install detent assembly:** Load spring + ball into blind bore (tangential pocket in housing). Install set screw; advance to 7 mm spring compressed height (use depth stop screwdriver or spacer). Apply Loctite 243 on last 1/4 turn. Verify ring clicks at all 3 positions.
8. **Install base cap:** Snap / thread base cap onto handle housing bottom. Verify ring cannot extract axially.
9. **Final inspection:** Verify angle window shows correct number at each click; verify ejection rod function; verify fin position; check no sharp edges on filter contact surfaces.

---

## 10. Key Dimensions Reference Card

```
                   ┌── 10 mm ──┐ (Tip Insert Block)
                  /             \
                 /  3 mm Ø dimple\
     82 mm      /    at apex      \
  (slant length)│                 │
                │  POM-C shells   │
                │  2.5 mm wall    │
                │                 │
   48°: base Ø 66.6 mm           │
   60°: base Ø 82.0 mm           │ ← Angle-Set Ring here
   80°: base Ø 105.4 mm          │   120 mm OD / 14 mm tall
                \                 /
                 \_______________/
                 │   Handle Body │  ← 42 mm OD, 65 mm long
                 │               │     knurl + angle window
                 └───────────────┘
                       │
                   (base cap)

Total tool height (80° preset, cone facing up):
  82 mm (cone) + 14 mm (ring) + 65 mm (handle) + 5 mm (cap) = 166 mm

Max tool width (80° preset): 105.4 mm at base rim
Handle grip diameter: 42 mm (ergonomic for adult hand)
Tool mass (estimated): 145–185 g
```

---

## 11. Open Questions & V2 Flags

| # | Question / Risk | Action for V1 | V2 Improvement |
|---|----------------|--------------|----------------|
| Q1 | What paper families / sizes need support first? (01 vs 02, thick vs thin seam variants?) | Build around common 02-class pre-seamed cone papers | Interchangeable shell lengths for multi-paper-size support |
| Q2 | Does the 80° preset actually fit any commercial dripper? | Test with Origami Dripper (wide mode) and wide-body specialty cones | Drop 80° if not useful; replace with 55° |
| Q3 | How does filter paper stiffness affect tip dimple registration? | Test with 3 paper weights: Hario (thin), Cafec (medium), Chemex bonded (thick) | Dimple depth adjustment screw |
| Q4 | Is 42 mm handle OD comfortable for smaller hands (Indonesian female percentile)? | Test with P5 hand span (≈ 160 mm hand length) | Reduce to 38 mm or add rubberised inlay |
| Q5 | POM-C shell at 80° + paper forming load — is 2.5 mm wall sufficient? | FEA simulation; hand test with calibrated loading fixture | Ribbed internal shell wall for added stiffness |
| Q6 | Does the factory seam need any additional conditioning (slight moistening or seam pressing)? | Test dry vs slightly moistened seam — does guided seating improve pour consistency? | Light texture press feature on one shell face at seam line |
| Q7 | Cleaning: cam track is a particle trap for coffee grounds | Add drain holes in cam track floor | Redesign as enclosed wipe-clean cam in V2 |
| Q8 | Can the tool double as a dripper-placement guide (position filter + tool over server)? | Not in V1 scope | Integrated server alignment ring on base cap |

---

*Companion document: `docs/manufacturability.md` — material specs, sourcing directory, COGS analysis*  
*Next step: Phase 0 FDM print of shell geometry (PETG, 0.15 mm layer, 40% infill) for ergonomic and angle validation*  
*Revision 0.2 pending: after Phase 0 fit-check results*
