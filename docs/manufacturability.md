# Universal Filter Ruler — Manufacturability & Materials Analysis

> **Status:** Production-ready specification  
> **Scope:** Low-volume first article (1–100 units), Indonesia context  
> **Updated:** 2026-04-06

---

## 1. Manufacturing Context

### 1.1 Production Strategy

| Phase | Volume | Method | Location |
|-------|--------|--------|----------|
| Prototype | 1–5 units | CNC local | Jakarta/Bandung |
| Alpha | 5–20 units | CNC batch | Local |
| Production V1 | 50–200 units | CNC + anodize outsource | Local |

### 1.2 Material Properties Summary

| Material | Use | Key Properties |
|----------|-----|-----------------|
| 6061-T6 Aluminum | Base plate, arms, cam lever | Excellent machinability, good anodizing |
| SS 316 | Cam body, shoulder bolts | Corrosion resistant, food-safe |
| N52 Neodymium | Magnetic markers | High pull force per size |
| PTFE | Slide strips | Ultra-low friction, self-lubricating |
| Mild steel | Ferrous strip | Magnetic attraction when plated |

---

## 2. Component Manufacturing

### 2.1 Base Plate

**Material:** 6061-T6 Aluminum sheet/plate  
**Rawstock:** 210×130×10 mm (oversized for machining)  
**Finished:** 200×120×8 mm  

**Operations:**
1. CNC mill: Profile, T-slots, magnetic track recess
2. Deburr: All edges, R1mm break
3. Anodize: Type III hard coat (25–50 μm)
4. Laser etch: Angle scales, vernier marks,filter size circles
5. Paint fill: Black contrast in etched areas

**Critical features:**
- T-slot parallelism: 0.05 mm over 180 mm
- T-slot width tolerance: +0.02/−0.00 mm
- Flatness: 0.05 mm overall

**Estimated unit cost (100 qty):** IDR 95,000

### 2.2 Sliding Arms

**Material:** 6061-T6 Aluminum bar  
**Rawstock:**160×30×8 mm  
**Finished:** 150×25×6 mm  

**Operations:**
1. CNC mill: Profile, T-tab, fold guide ridge, cam mount hole
2. Deburr: All edges, R2mm on fold guide
3. Anodize: Type III hard coat
4. Laser etch: Vernier scale on inner edge
5. Paint fill: Black contrast

**Estimated unit cost (100 qty):** IDR 25,000 ea×2 = IDR50,000

### 2.3 Cam Lock Assembly

**Components:**
- Cam body: SS 316, eccentric, 90° throw
- Lever: 6061-T6 Al, 25mm, knurled end
- Shoulder bolt: M5×10mm, SS 316
- Belleville washer: M5, spring steel

**Sourcing:** Taiwan import or local equivalent  
**Estimated unit cost (100 qty):** IDR 12,000 ea ×2 = IDR 24,000

### 2.4 Magnetic Markers

**Housing:** 6061-T6 Al, Ø6×3mm, turned  
**Magnet:** N52 Neodymium, Ø5×2mm, pressed-in  
**Finish:** Type II anodize, color-coded  

**Manufacturing:** CNC turn housing → anodize → press-fit magnet → adhesive backup  
**Estimated unit cost (100 qty):** IDR 2,000 ea ×8 = IDR 16,000

### 2.5 Ferrous Strip

**Material:** Mild steel, zinc plated  
**Dimensions:** 180×6×1 mm  

**Sourcing:** Local laser cutter or strip stock  
**Estimated unit cost:** IDR 4,000

### 2.6 PTFE Slide Strips

**Material:** PTFE sheet, 0.5mm thick  
**Dimensions:** 180×6mm  

**Sourcing:** Die-cut from bulk sheet  
**Estimated unit cost:** IDR 2,000 ea ×2 = IDR 4,000

---

## 3. Assembly Hardware

| Item | Spec | Qty | Source | Unit Cost |
|------|------|-----|--------|-----------|
| M3×8 SHCS | SS A2-70 | 4 | Local hardware | IDR 500 |
| M5 Shoulder Bolt | SS 316 | 2 | Import | IDR 3,000 |
| Belleville Washer M5 | Spring steel | 2 | Import | IDR 1,000 |
| Silicone Foot Pad | Ø8mm, adhesive | 4 | Local | IDR 500 |

**Totalhardware:** IDR 2,000

---

## 4. Processing BOM

| Process | Applies To | Supplier | Cost |
|---------|-----------|----------|------|
| Hard Anodize Type III | Base + Arms | Anodize shop | IDR 20,000 |
| Laser Etch (scales) | Base + Arms | Laser shop | IDR 12,000 |
| Paint Fill (contrast) | Base + Arms | Manual | IDR 5,000 |
| Color Anodize Type II | Magnetic markers | Anodize shop | IDR 8,000 |

**Total processing:** IDR 45,000

---

## 5. Cost Summary Per Unit

| Category | Cost (IDR) | Cost (USD) |
|----------|-----------|-----------| 
| Base plate | 95,000 | $5.90 |
| Arms (×2) | 50,000 | $3.10 |
| Cam locks (×2) | 24,000 | $1.50 |
| Magnetic markers (×8) | 16,000 | $1.00 |
| Ferrous strip | 4,000 | $0.25 |
| PTFE strips (×2) | 4,000 | $0.25 |
| Hardware | 2,000 | $0.12 |
| Processing | 45,000 | $2.80 |
| Assembly labor | 12,000 | $0.75 |
| QC inspection | 8,000 | $0.50 |
| **TOTAL COGS** | **260,000** | **$16.15** |

> Conservative estimate: IDR 313,000 for financial planning

---

## 6. Supplier Directory (Indonesia)

### Local Suppliers

| Component | Supplier Type | Location | Lead Time |
|-----------|--------------|----------|-----------|
| Aluminum stock | Metal distributor | Jakarta/Tangerang | 3–5 days |
| CNC machining | Job shop | Tangerang/Bandung | 2–3 weeks |
| Anodizing | Surface treatment | Bekasi/Tangerang | 1 week |
| Laser etching | Laser service | Jakarta | 3–5 days |
| Hardware (M3, etc.) | Fastener shop | Local | 1–3 days |

### Import Suppliers

| Component | Source | Platform | Lead Time | MOQ |
|-----------|--------|----------|-----------|-----|
| N52 magnets | China | Alibaba | 3–4 weeks | 500 |
| Cam mechanisms | Taiwan | Direct | 4–6 weeks | 200 |
| PTFE strip | China | Alibaba | 2–3 weeks | 10m |
| Shoulder bolts | China/Taiwan | Alibaba | 3–4 weeks | 200 |

---

## 7. Quality Control

### 7.1 Critical Dimensions (100% inspection)

| Feature | Tolerance | Method |
|---------|-----------|--------|
| T-slot width | +0.02/−0.00 mm | Go/No-go gauge |
| T-slot depth | ±0.05 mm | Depth micrometer |
| Angle scale accuracy | ±0.5° | Optical comparator |
| Cam lock hold force | ≥50 N | Force gauge |
| Marker pull force | ≥0.5 kg | Spring scale |

### 7.2 Sampling Inspection (10%)

| Feature | Specification | Method |
|---------|--------------|--------|
| Anodize thickness | 25–50 μm | Eddy current |
| Laser etch depth |0.05–0.15 mm | Profilometer |
| Edge finish | R1mm all corners | Visual |
| Surface roughness | Ra ≤0.8 μm | Profilometer |

---

## 8. DFM Guidelines

### 8.1 Recommended Practices

| Guideline | Reason |
|-----------|--------|
| Minimise 5-axis features | Cost driver |
| Keep wall thickness ≥1.5mm | Machinability |
| Use standard hole sizes | Tooling availability |
| Specify anodize masking | Prevent thread fill |
| Allow +0.05mm for anodize | Coating thickness |

### 8.2 Avoid

| Feature | Problem |
|---------|---------|
| Blind tapped holes <M3 | Strip risk |
| Sharp internal corners <R0.5mm | Tool wear |
| Thin sections <1mm | Vibration |
| Deep pockets >10× diameter | Tool reach |

---

## 9. Packaging

| Item | Qty | Cost (IDR) |
|------|-----|-----------| 
| Retail box (recycled cardboard) | 1 | 10,000 |
| Foam insert | 1 | 5,000 |
| Quick start guide | 1 | 2,000 |
| QR code card | 1 | 1,000 |
| Sticker pack | 1 | 2,000 |
| Hex key (2.5mm) | 1 | 2,000 |
| Marker storage pouch | 1 | 3,000 |
| **Total packaging** | | **25,000** |

---

## 10. Inventory Planning

### 10.1 Initial Order (100 units)

| Item | Qty Needed | Order Qty | Buffer |
|------|-----------|-----------|--------|
| Base plate stock | 100 | 110 | 10% |
| Arm stock | 200 | 220 | 10% |
| Cam locks | 200 | 250 | 25% |
| Magnets | 800 | 1,000 | 25% |
| Ferrous strips | 100 | 120 | 20% |
| Hardware kits | 100 | 120 | 20% |
| Packaging | 100 | 120 | 20% |

### 10.2 Reorder Points

| Item | Safety Stock | Reorder Point | Reorder Qty |
|------|--------------|---------------|-------------|
| Base plates | 20 units | 30 units | 50 units |
| Magnets | 200 pcs | 300 pcs | 500 pcs |
| Cam locks | 40 pcs | 60 pcs | 100 pcs |
| Packaging | 20 sets | 30 sets | 50 sets |

---

*BOM version: 1.0 — See Bill of Materials.md for detailed part list*  
*Manufacturing status: Ready for prototyping*