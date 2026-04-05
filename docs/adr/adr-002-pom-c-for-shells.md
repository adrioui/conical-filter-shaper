# ADR-002: POM-C for Shell Halves

**Date:** 2026-04-05  
**Status:** Accepted

## Context

Shell halves form the filter contact surface. Material requirements:
- Ra ≤ 0.8 µm achievable with standard CNC
- Self-lubricating (no coating needed for paper release)
- Dimensionally stable under humidity and temperature cycling (kitchen environment)
- Food-safe (FDA-compliant grades available)
- Machinable to close tolerances (±0.05 mm on cam follower boss)

## Decision

Use **POM-C (Acetal Copolymer)** — food-grade grade (e.g. equivalent to Delrin 507).

## Reasons

- Water absorption 0.2% (vs PA66 at 2.5–3.5%) → minimal dimensional change
- Self-lubricating → paper releases cleanly, no dragging or tearing
- HDT ~115°C — adequate for kitchen environment (max 96°C water contact)
- Excellent machinability, close tolerances achievable
- Indonesia: available from PT Ensinger Indonesia (Jakarta)

## Consequences

✅ No secondary finish or coating on filter contact faces  
✅ Pivot bores are dimensionally stable across humidity changes  
❌ Creep under sustained load at elevated temperature (>60°C for months) — mitigated by
   using POM-C (copolymer > homopolymer for creep resistance) and limiting cam follower
   boss wall to ≥ 2.5 mm

## Alternatives Considered

- **PA66-GF30**: Better strength but 3.5% moisture absorption → shell dimensions drift
- **PEEK**: Overkill for cost; excellent but unnecessary thermal margin
- **6061-T6 Aluminium shells**: Possible for V2; heavier, more expensive, no self-lubrication at seam
