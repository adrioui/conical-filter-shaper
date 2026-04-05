# Coffee Tool V1 — Manufacturability & Materials Analysis

> **Scope:** Low-volume first article (1–20 units), Indonesia context, espresso/filter workflow.  
> **Assumed operating envelope:** water 20–96 °C (cold rinse to near-boiling), ambient kitchen humidity, daily contact with fresh/spent coffee grounds, cleaning agents (citric acid, Cafiza/Puly), occasional steam proximity. No direct steam-pressure contact assumed.
>
> **Status note:** authoritative V1 product/workflow scope now lives in `docs/design_spec.md` and `cad/params.py`, and assumes **standard pre-seamed conical paper filters** rather than flat circular discs. This document is best treated as materials/process guidance until its older section naming is fully reconciled with the current mechanism.

---

## 1. Thermal & Chemical Constraints Table

| Condition | Value | Impact |
|-----------|-------|--------|
| Max water temp (espresso flush) | ~93–96 °C | Eliminates PLA, limits ABS |
| Max surface temp (steam wand proximity) | ~110–120 °C intermittent | Eliminates standard POM homopolymer if sustained; copolymer POM or PA66 fine |
| Chemical: espresso cleaning tablets | pH 10–12 alkaline | Eliminates unsealed zinc die-cast; attacks standard anodize below 40 µm |
| Chemical: citric acid descaling | pH 2–3 | Attacks mild steel; degrades unsealed aluminum; fine for SS304+, POM, PA66, PEEK |
| Food contact (direct ground/water) | FDA 21 CFR / EU 10/2011 | Requires food-grade polymer grades; raw SLA resin **not** safe without post-cure + FDA-compliant resin |
| Humidity | Continuous | PA66 absorbs moisture → dimensional change; use PA66-GF30 or switch to POM |

---

## 2. Component-by-Component Material Recommendations

### 2.1 Dock (Main Body / Housing)

The dock is the structural base — largest part, sets the aesthetic tone, rarely contacts hot liquid directly but handles wet grounds and cleaning chemicals.

#### ✅ Recommended: 6061-T6 Aluminium (anodized)
| Property | Value |
|----------|-------|
| Density | 2.7 g/cm³ |
| Yield strength | 276 MPa |
| Max service temp | >200 °C (irrelevant here) |
| Machinability | Excellent — short chips, fast feeds |
| Anodize (Type II, 15–25 µm) | Hard, food-safe, corrosion-resistant |
| Indonesia sourcing | Widely available as billet/plate; Glodok / Surabaya suppliers carry 6061 |

**Finish:** Type II anodize in hard-black or natural. Avoid Type III (hard anodize) for V1 — cost premium not justified. Seal with PTFE or nickel seal for acid/alkali resistance.

**V1 process:** CNC milled from 6061 billet. For 1–5 units, use local CNC shop (Bekasi/Cikarang industrial zone) or order from Jlc3DP / JLCPCB CNC online (ships Jakarta in ~10–14 days).

#### Alternative: PA66-GF30 (30% glass-filled Nylon 66) injection moulded
- Lower cost at volume (>500 units), but mould cost ~Rp 15–40 juta for V1 makes no sense.
- Print with FDM for proof-of-concept only; not a production option without mould.

#### ❌ Avoid
- **PLA**: Tg ~60 °C, warps/creeps near espresso-temperature rinse
- **ABS**: Tg ~105 °C but off-gasses at ≥ 80 °C, poor chemical resistance to alkaline cleaners
- **Zinc die-cast (Zamak)**: Corrodes in citric acid, heavy, V1 tooling cost prohibitive
- **Raw wood/bamboo**: Hygroscopic, difficult to sanitize reliably

---

### 2.2 Moving Arms (Articulating/Folding Arms)

Arms are repetitively flexed, need dimensional stability over humidity cycling, and may contact wet grounds.

#### ✅ Recommended: POM-C (Acetal Copolymer) — CNC-turned/milled rods or sheet stock

| Property | Value |
|----------|-------|
| Tg / HDT | ~115–125 °C (HDT at 1.8 MPa) |
| Tensile strength | 60–70 MPa |
| Water absorption (24 h) | 0.2% (excellent — much better than PA) |
| Chemical resistance | Excellent to mild acids, alkalis, oils |
| Food contact | FDA-compliant grades readily available (Delrin® 507 or equivalent) |
| Machinability | Outstanding — close tolerances, self-lubricating |
| Indonesia sourcing | POM-C rod/sheet available from PT Ensinger Indonesia (Jakarta), Graha Polymer, or import Tokopedia listings |

**Why POM over PA66?** Moisture absorption of PA66 is 2.5–3.5% vs POM's 0.2%. Arms need repeatable geometry at pivot interface — POM stays true.

**Why POM over aluminium arms?** Weight, tactile feel (plastic pivot is quieter), and ability to machine snap-fit or living-hinge features if needed.

#### Alternative: 6061-T6 aluminium arms (anodized)
- Elegant if dock is also aluminium (material family consistency).
- Higher unit cost for small qty, heavier, no self-lubrication at pivot.

#### ❌ Avoid for arms
- **PETG / FDM printed**: Layer delamination under cyclic pivot load; creep at hinge
- **Polycarbonate (PC)**: Stress-cracks in alkaline cleaner; UV yellowing

---

### 2.3 Pivot (Pin / Shaft / Bushing)

The pivot is the highest-wear interface. It sees cyclic rotation, potential grit contamination from grounds, and moisture.

#### ✅ Recommended Pivot Pin: SS 316L (austenitic stainless, passivated)

| Property | Value |
|----------|-------|
| Corrosion resistance | Excellent — molybdenum content resists chloride/acid |
| Hardness (annealed) | ~170 HB — adequate for light wear |
| Food contact | Yes — industry standard for bar tools |
| Form factor | Standard 3 mm or 4 mm shoulder bolt / dowel pin |
| Indonesia sourcing | SS 316 dowel pins widely available; Fastenal Indonesia, PT Sinar Baja, or Tokopedia |

**Bushing / Bearing interface:** Press a POM or IGUS iglide® J bush into the arm bore. POM-on-SS316 gives a self-lubricating, corrosion-free pivot needing zero maintenance. Clearance: 0.05–0.10 mm (H7/f7 fit).

#### Alternative: Titanium Grade 5 (Ti-6Al-4V) pin
- Premium aesthetic (matte grey, very light), biocompatible, but 5–8× the cost of SS for a prototype.
- Reserve for production V2 if brand positioning demands it.

#### ❌ Avoid
- **Brass (CuZn)**: Leaches zinc/copper over time into coffee runoff — not food-safe
- **Mild steel**: Rusts immediately in wet coffee environment
- **Aluminium pin in aluminium bore**: Galling without hard anodize on one surface

---

### 2.4 Detents (Click / Position Lock Mechanism)

Detents define tactile feedback positions (open, half-open, closed, etc.). Two viable approaches:

#### Option A — Ball Detent (Recommended for V1)

**Components:**
- 3 mm SS304 ball bearing (or SS316L)
- 0.5–0.8 mm compressed-length spring (SS302 or Hastelloy C for acid environments)
- Blind pocket in arm + mating dimples in dock or pivot plate

| Property | Ball + Spring |
|----------|---------------|
| Repeatability | ±0.3–0.5° depending on dimple radius |
| Feel | Positive click, adjustable preload via spring selection |
| Sourcing | SS ball: PT Bola Baja / standard bearing supplier; spring: custom or imported from Alibaba spring kits |
| Cost per detent (5 pcs) | ~Rp 3.000–8.000 hardware only |

**Design note:** Dimple depth ≈ 30% of ball radius for clear click without excessive force. Laser-etch or CNC-spot the dimples in the SS rail/plate for precision.

#### Option B — Spring Leaf / Snap Tab (Simpler but less precise)
- A cantilevered POM leaf integrated into arm body snaps over a ridge in dock.
- Zero extra hardware, but wears faster and less precise.
- Acceptable for proof-of-concept iteration only.

#### ❌ Avoid
- **Magnetic detents (neodymium)**: NdFeB corrodes if plating chips, coffee particles stick to exposed magnet
- **Friction/set-screw detent**: Not repeatable, loosens over use

---

### 2.5 Overlap Stop (Mechanical Travel Limit)

Prevents arms from colliding or over-rotating beyond design intent.

#### ✅ Recommended: Integrated hard stop pin in SS304 + POM bumper

**Design:**  
- A 3–4 mm SS304 shoulder bolt or turned pin press-fitted into the dock acts as a positive stop.
- A short sleeve of POM (or Neoprene/NBR-70 O-ring) over the pin absorbs impact, dampens sound.
- Arm contacts the cushioned pin at travel limit.

| Property | Value |
|----------|-------|
| Impact energy | Low (hand-operated) — POM absorbs adequately |
| Chemical resistance | POM + SS304 both excellent |
| Sound | Quiet — POM dampens metal-on-metal click |
| Repairability | Pin/sleeve replaceable independently |

**Alternative soft stop:** A 3 mm NBR-70 (food-grade nitrile rubber) O-ring seated in a groove on the pin. NBR is FDA 21 CFR 177.2600 compliant, handles 120 °C, resists oils and mild acids. Commonly sourced as standard O-ring sizes from PT Seal Indo or any hydraulic supplier.

#### ❌ Avoid
- **Pure rubber bumper without retention**: Will migrate or fall out over cleaning cycles
- **Aluminium-on-aluminium stop**: Galling, dents over cycles

---

### 2.6 Insertion Core (The Element Inserted into Basket / Portafilter)

This is the most critical food-contact and dimensional-precision component. It contacts coffee grounds, hot water, and must fit precise portafilter/basket bore tolerances (typically 57–58.5 mm for E61/commercial).

#### ✅ Primary Recommendation: SS 304 or SS 316L — CNC Turned / Polished

| Property | SS 304 | SS 316L |
|----------|--------|---------|
| Food contact | ✅ FDA/EU compliant | ✅ Superior (molybdenum) |
| Max service temp | >800 °C | >800 °C |
| Corrosion (acid) | Good | Excellent |
| Polishability | Ra 0.2 µm achievable | Same |
| Machinability | Good (work-hardens — use sharp tooling, carbide inserts) | Slightly harder to machine |
| Cost delta | Baseline | +15–25% |
| Indonesia sourcing | SS 304 tube/rod: PT Gunung Steel, Krakatau Steel distributors | SS 316 rod: import or Tokopedia industrial |

**Recommended spec:**  
- Material: SS 316L (food prep, direct contact)  
- Surface: Electropolished or hand-buffed to Ra ≤ 0.4 µm on contact faces  
- Dimensional tolerance: ±0.05 mm on OD to match basket bore  
- Mark with laser: "316L" and lot number for traceability  

#### Alternative: PEEK (Polyether Ether Ketone) — Machined

For a **lighter, non-metallic** insertion core:

| Property | PEEK |
|----------|------|
| HDT | 152 °C @ 1.82 MPa — excellent for espresso temps |
| Chemical resistance | Excellent — resists all coffee cleaning agents |
| Food grade | Yes — PEEK Medical/Food grade (Victrex 150G or equivalent) |
| Machinability | Good — slow feeds, sharp tooling, coolant |
| Density | 1.32 g/cm³ — much lighter than SS |
| Cost | High — Rp 800.000–2.000.000/kg for food-grade rod |
| Availability in Indonesia | Limited — import from Ensinger Singapore, ~1–2 week lead |

**PEEK is ideal if:** The insertion core houses needle pins or has complex geometry hard to machine from SS, or if you want visible food-safe branding ("PEEK food-grade core").

#### ❌ Absolutely Avoid for insertion core
- **Zinc / Zamak die-cast**: Acid-corrodes, leaches
- **Anodized aluminium** (direct ground contact): Anodize chips over time, aluminium oxide ingestion risk
- **FDM-printed PLA/ABS/PETG**: Porous layer structure traps bacteria; not food-safe under hot water
- **Standard SLA resin**: Not food-safe unless specifically FDA-compliant resin (Formlabs BioMed Amber etc.) + full post-cure — impractical and expensive for functional parts

---

## 3. Material Summary Table

| Component | V1 Prototype Material | Production Material | Food-safe? | Heat ok? |
|-----------|----------------------|--------------------|-----------:|:--------:|
| Dock | 6061-T6 Al, Type II anodized | Same or PA66-GF30 injection | ✅ | ✅ |
| Moving Arms | POM-C (Acetal Copolymer) | POM-C or 6061 Al | ✅ | ✅ |
| Pivot Pin | SS 316L shoulder bolt/dowel | SS 316L | ✅ | ✅ |
| Pivot Bushing | POM-C press-fit sleeve | IGUS iglide J | ✅ | ✅ |
| Detent Ball | SS 304 3 mm ball bearing | SS 316L | ✅ | ✅ |
| Detent Spring | SS 302 compression spring | SS 302 or Hastelloy | ✅ | ✅ |
| Overlap Stop Pin | SS 304 shoulder bolt | SS 304 | ✅ | ✅ |
| Overlap Stop Damper | POM sleeve or NBR-70 O-ring | NBR-70 O-ring | ✅ | ✅ |
| Insertion Core | SS 316L turned + polished | SS 316L or PEEK | ✅ | ✅ |

---

## 4. Prototype-to-Production Roadmap

### Phase 0 — Concept Validation (Week 1–3)
**Goal:** Prove geometry, fit, and ergonomics. Not food-safe. Desk-only testing.

| Activity | Method | Cost (IDR) | Lead Time |
|----------|--------|-----------|-----------|
| Full assembly mock-up | FDM print (PETG or ASA) — Bambu Lab / local print shop | Rp 150.000–400.000 | 1–2 days |
| Pivot/detent simulation | Print at 0.15 mm layer height; manually add SS ball + spring | Included | — |
| Fit check vs portafilter | Direct test on basket | — | — |
| Geometry iteration | Re-print modified STL | Rp 50.000/revision | 1 day |

**Tooling needed:** None. A pair of digital calipers, a portafilter, and access to a local 3D printing service (Tokopedia: "jasa 3D printing Jakarta" = ~Rp 5.000–10.000/gram PETG).

---

### Phase 1 — Functional Prototype / Alpha (Week 4–8)
**Goal:** Real materials, real tolerances, food-safe functional testing. 1–3 units.

| Component | Process | Vendor type | Unit cost est. (IDR) |
|-----------|---------|------------|---------------------|
| Dock | CNC milled 6061-T6, Type II anodize | Local CNC shop Bekasi / Cikarang | Rp 350.000–800.000 |
| Arms (×2–4) | CNC milled POM-C from rod stock | Same shop or lathe work | Rp 80.000–200.000 ea |
| Pivot pins (×n) | SS 316L shoulder bolt M3/M4, standard | Tokopedia / PT Sinar Baja | Rp 5.000–15.000 ea |
| POM bushings | Turned POM-C, 3–5 mm bore | Same CNC shop | Rp 20.000–40.000 ea |
| Ball detent hardware | SS ball + spring kit | Tokopedia/Alibaba import | Rp 3.000–8.000/detent |
| Insertion core | SS 316L CNC turned, hand polished | CNC shop + manual polish | Rp 200.000–500.000 |
| Stop pin + NBR O-ring | SS 304 bolt + O-ring | Tokopedia | Rp 10.000–25.000 |
| **Total materials + machining (1 unit)** | | | **Rp 800.000–2.000.000** |

**Notes:**
- CNC shop recommendation: Kawasan Industri Pulogadung (Jakarta), KIIC Karawang, or Rungkut Surabaya.  
- Ask for 3-axis CNC, ISO 9001 shop if possible for traceability.  
- Budget an extra 30% for first-article rejection and re-run.

---

### Phase 2 — Beta / User Testing (Month 3–5)
**Goal:** 5–20 units for barista testers. Finalize tolerances. Document failure modes.

| Activity | Detail | Cost est. |
|----------|--------|----------|
| Production DFM review | Work with CNC shop on fixturing, reduce ops | Rp 500.000–1.500.000 (engineering time) |
| Batch CNC (10 units dock + core) | Negotiate batch rate, same material | Rp 4.000.000–12.000.000 |
| Hardware BOM (10 units) | Pins, balls, springs, O-rings | Rp 500.000–1.000.000 |
| Anodize batch (Type II, 10 pcs) | Minimum charge at anodize shop | Rp 500.000–800.000 |
| Electropolish insertion cores (10 pcs) | Outsource to SS fab shop | Rp 300.000–600.000 |
| Packaging (kraft box, foam insert) | Local packaging supplier | Rp 30.000–80.000/unit |
| **Total Beta batch (10 units)** | | **≈ Rp 8.000.000–18.000.000** |
| **Per-unit beta cost** | | **≈ Rp 800.000–1.800.000** |

---

### Phase 3 — Small Production Run V1 (Month 6–12)
**Goal:** 50–200 units. Target end-consumer price Rp 500.000–1.500.000.

| Decision point | Option A (stay local) | Option B (shift to China) |
|----------------|----------------------|--------------------------|
| CNC dock + arms | Local CNC batch, blanket PO | Chinese CNC service (JLCPCB, PCBWay, Xometry) |
| Unit cost dock | Rp 250.000–450.000 | Rp 150.000–300.000 (inc. shipping) |
| Lead time | 2–3 weeks | 10–20 days air, 35–45 days sea |
| MOQ | 20–50 pcs | 10–20 pcs |
| Quality control | Easier to visit/inspect | Need inspection agent or 3rd party QC |
| Indonesia TKDN benefit | Yes (local content) | No |

**Recommendation for V1 production:** Stay local (Jakarta/Surabaya) for first 50–100 units to maintain design iteration speed and quality control. Shift China for cost optimization only at 200+ units/batch.

---

## 5. Full BOM — V1 Single Unit (Indicative, IDR)

| # | Item | Spec | Qty | Unit Cost (IDR) | Subtotal |
|---|------|------|-----|----------------|----------|
| 1 | Dock body | 6061-T6 CNC + Type II anodize | 1 | 600.000 | 600.000 |
| 2 | Moving arm | POM-C CNC | 2 | 150.000 | 300.000 |
| 3 | Pivot pin | SS 316L M4 shoulder bolt, DIN 6912 | 2 | 12.000 | 24.000 |
| 4 | Pivot bushing | POM-C turned, H7/f7 | 4 | 30.000 | 120.000 |
| 5 | Detent ball | SS 304, 3 mm | 2 | 4.000 | 8.000 |
| 6 | Detent spring | SS 302, D3×0.3×8 mm | 2 | 5.000 | 10.000 |
| 7 | Detent plug/set screw | SS M3 grub screw | 2 | 3.000 | 6.000 |
| 8 | Overlap stop pin | SS 304 M4 shoulder bolt | 1 | 10.000 | 10.000 |
| 9 | Stop damper O-ring | NBR-70, 4×2 mm, food grade | 1 | 3.000 | 3.000 |
| 10 | Insertion core | SS 316L CNC turned + polished | 1 | 400.000 | 400.000 |
| 11 | Assembly fasteners (misc) | SS M3 socket head cap screws | 6 | 2.000 | 12.000 |
| 12 | Thread locker | Loctite 243 (medium, removable) | tiny qty | 3.000 | 3.000 |
| **TOTAL MATERIAL + MACHINING** | | | | | **≈ Rp 1.496.000** |

> **Add:** 20% overhead / waste / re-run buffer → **≈ Rp 1.800.000 COGS**  
> **Add:** Packaging + labelling → **Rp 50.000–100.000**  
> **Landed V1 unit COGS → ≈ Rp 1.850.000–1.900.000**

_At 3× markup (standard for specialty tools): retail ~Rp 5.500.000–6.000.000. At 2× (brand-building): ~Rp 3.800.000._

---

## 6. Assembly Considerations

### 6.1 Sequence
1. **Core sub-assembly first:** Press POM bushings into arm bores (H7/f7 press, ~0.01–0.02 mm interference). Use arbor press or bench vise with smooth jaws — never hammer (splits POM).
2. **Install detent balls + springs:** Pack spring into blind bore, set ball, retain with M3 grub screw (hand-tight, then 1/8-turn back to avoid preloading). Apply one drop Loctite 243 to grub threads.
3. **Mount arms to dock:** Thread SS 316L shoulder bolt through arm bushing into dock. Do not overtorque — shoulder bolt should rotate freely in dock thread; arm movement resistance comes from bushing-pivot clearance only.
4. **Verify detent engagement:** Arms should click clearly at each designed position with ~0.5–1 N·m tactile resistance. Adjust grub screw depth if too light or too stiff.
5. **Insert overlap stop pin:** Thread or press-fit into dock pocket. Slide NBR O-ring onto pin shank before seating.
6. **Fit insertion core:** If press or friction fit into dock throat — test insertion/removal force. Target 10–20 N insertion with clean hands. Too tight = add 0.05 mm to bore; too loose = reduce 0.02 mm.
7. **Final torque pass:** All fasteners torqued to spec with SS hex key. Check no fasteners proud of surfaces that will contact user or portafilter.

### 6.2 Critical Tolerances

| Interface | Recommended Fit | Tolerance (mm) |
|-----------|----------------|----------------|
| Pivot pin OD / bushing ID | f7/H7 running clearance | Pin: −0.010/−0.028; Bore: +0.000/+0.018 |
| Bushing OD / arm bore | P6/H7 press fit (POM in AL) | Bushing: +0.012/+0.021 |
| Insertion core OD / basket bore | g6/H7 close clearance | Core: −0.004/−0.016 |
| Detent ball pocket depth | 45–50% ball diameter | Dimple radius = 0.55 × ball radius |
| Overlap stop clearance | 0.1–0.2 mm at full travel | Prevents stress concentration |

### 6.3 DFM Flags (Avoid These in CAD)

| Issue | Risk | Fix |
|-------|------|-----|
| Blind tapped holes in aluminium <M3 | Strip on first clean | Use M4 minimum, or helicoil inserts |
| Thin POM arm wall <1.5 mm at pivot | Crack under torque | Min 2.5 mm wall at bore |
| Sharp inside corners on SS core | Stress riser, difficult to polish | R0.5 mm minimum all internal radii |
| Detent spring pocket no chamfer | Assembly difficulty | 45° × 0.3 mm entry chamfer |
| Undercuts on dock requiring 5-axis | Cost driver | Design for 3-axis + 2 setups only |
| Anodize masking not specified | Threads filled with anodize | Call out "mask all tapped holes before anodize" in drawing |

### 6.4 Cleaning & Maintenance Protocol (User Manual Note)
- Disassemble pivot pins monthly (quarter-turn shoulder bolt).
- Soak POM arms + dock in warm soapy water or dilute citric acid (1%). Pat dry — do not dishwasher (high-temp cycle degrades anodize seal).
- Insertion core: Rinse under tap after each use. Weekly wipe with food-grade mineral oil for SS lustre.
- Never use bleach/chlorine cleaners — attacks SS passivation layer.
- Inspect O-ring damper annually; replace NBR-70 if cracked (Rp 3.000 part).

---

## 7. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| CNC tolerance stack on pivot → arms bind | Medium | High | Add 0.02 mm to bushing bore tolerance; test-fit before anodize |
| POM arm creep at elevated detent force | Low | Medium | Limit grub screw preload; use POM-C (copolymer > homopolymer for creep) |
| Insertion core OD drift from SS work-hardening | Medium | High | Use sharp carbide inserts, flood coolant, measure every 5 pcs in batch |
| Anodize flaking on dock near threads | Low | Medium | Specify mask all threaded features; re-tap after anodize |
| NBR O-ring swell in coffee oils | Low | Low | Test 1-week soak in espresso + Cafiza solution; switch to FKM (Viton) if needed |
| Local CNC shop geometric accuracy (IT7 vs IT8) | Medium | Medium | Provide go/no-go gauge specs with order; request first article inspection report |
| SS 316L lead time in Indonesia | Low | Low | Stock 5× insertion core worth of rod as buffer |

---

## 8. Quick Reference — Indonesia Sourcing Directory

| Material / Part | Supplier / Channel | Notes |
|----------------|-------------------|-------|
| 6061-T6 aluminium billet/plate | PT Alumindo Light Metal (Sidoarjo), PT Indal Aluminium | Buy standard stock sizes; cut to near-net |
| POM-C rod / sheet | PT Ensinger Indonesia (Jakarta), Tokopedia "POM rod acetal" | Specify "food grade" or "natural white" |
| SS 316L rod / bar | PT Krakatau Wajatama distributors, PT Gunung Raja Paksi | Check mill cert for 316L (not 316) |
| Fasteners SS 304/316 | PT Sinar Baja Electric, Tokopedia "baut stainless M4" | Buy ISO 4762 socket head caps |
| NBR O-rings food grade | PT Seal Indo, Tokopedia "O-ring NBR 70 food grade" | Specify FDA 21 CFR 177.2600 |
| Type II anodize | Bengkel anodizing Pulogadung / Rungkut | Min batch ~20 pcs; specify "seal after anodize" |
| CNC machining (3-axis) | Kawasan Industri Pulogadung, KIIC Karawang, Rungkut Surabaya | Send STEP + PDF drawing; request FAIR |
| SLA prototype (geometry test only) | Tokopedia "jasa SLA print", 3Dconnexion.id, Anker3D | Non-food-safe; geometry/ergonomics only |
| PEEK rod (if selected for core) | Import via Ensinger Singapore → Jakarta forwarding | 1–2 week lead, high cost |
| Ball bearings SS 3mm | SKF / NSK distributor Jakarta, Tokopedia "bola baja 3mm" | Buy 50 pcs for testing budget |

---

*Document generated: 2026-04-05 | Version 0.1 — Pre-design freeze*  
*Revise after Phase 0 FDM geometry is confirmed.*
