# ADR-001: CadQuery as Source of Truth

**Date:** 2026-04-05  
**Status:** Accepted

## Context

We need a CAD format that is:
- Version-controllable (text diffable)
- Parametric (all dims derived from a single params file)
- Agent-friendly (an AI agent can read and modify it without a GUI)
- Capable of exporting to all standard manufacturing formats

## Decision

Use **CadQuery** (Python-based parametric CAD) as the sole source of truth.  
All geometry is expressed in Python code in `cad/`.  
Generated exports (STEP/STL/SVG/DXF) are derived artifacts — gitignored.

## Consequences

✅ Full version history on all geometry (git blame on a dimension change)  
✅ Parameters in `params.py` are testable with pytest  
✅ Agent can read/modify dimensions without launching any GUI  
✅ CI can regenerate exports automatically  
❌ Cannot open `.py` files directly in FreeCAD/Fusion 360 (must import STEP)  
❌ Requires Python + CadQuery install for anyone editing geometry

## Alternatives Considered

- **FreeCAD + FCStd files**: Binary-heavy, poor git diff, GUI-required
- **OpenSCAD**: Text-based but limited surface modeling; no STEP export
- **Fusion 360**: Cloud-locked, binary, not agent-accessible
