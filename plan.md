# Implementation Plan — `cad/components/cam_ring.py`

## Goal
Replace the stub in `cam_ring.py` with a minimal, honest, buildable CadQuery solid: annular disc body + cam track grooves on the +Z face + detent dimples on the outer rim. No fake features.

---

## Current State

- **`cam_ring.py`**: stub that raises `NotImplementedError`. Docstring already describes the intended geometry accurately.
- **`cad/utils/cam_geometry.py`**: fully implemented. `cam_track_for_preset_radii(params)` returns two lists of `CamTrackPoint(angle_deg, radius_mm)` — one per follower pin. Pure math, tested in `test_cam_geometry.py`.
- **`cad/params.py`**: all cam ring dimensions are defined (`CAM_RING_OD_MM=120`, `CAM_RING_BORE_MM=60`, `CAM_RING_THICKNESS_MM=14`, `CAM_TRACK_WIDTH_MM=5`, `CAM_TRACK_DEPTH_MM=4`, detent dimple params, etc.).
- **`tests/test_components.py`**: three relevant tests exist — `test_cam_ring_builds`, `test_cam_ring_od`, `test_cam_ring_thickness` — all currently skip via `build_or_skip`.
- **All other components are also stubs** — no existing implemented component to copy from.

---

## Tasks

### 1. Build the annular disc body
- **File:** `cad/components/cam_ring.py`
- **Changes:**
  - Start on the XY plane at origin.
  - `cq.Workplane("XY").cylinder(CAM_RING_THICKNESS_MM, CAM_RING_OD_MM / 2)` — or equivalently `circle(OD/2).extrude(thickness)`.
  - Cut the central bore: `.circle(CAM_RING_BORE_MM / 2).cutThruAll()`.
  - Center the ring so origin is at ring center, Z=0 at bottom face, Z=+thickness at top face (+Z = up toward shells per origin convention).
- **Acceptance:** `test_cam_ring_builds` passes, `test_cam_ring_od` passes (bbox X/Y span ≈ 120 mm ± 0.5), `test_cam_ring_thickness` passes (bbox Z span ≈ 14 mm ± 1.0).

### 2. Cut the dual-spiral cam track into the +Z face
- **File:** `cad/components/cam_ring.py`
- **Changes:**
  - Call `cam_track_for_preset_radii(params)` to get `(track_L, track_R)`.
  - For each track, convert the polar `(angle_deg, radius_mm)` points to Cartesian XY coordinates.
  - Build a CadQuery spline (or polyline) wire from those XY points on a workplane at Z = `CAM_RING_THICKNESS_MM` (the +Z top face).
  - Sweep a rectangular cross-section (`CAM_TRACK_WIDTH_MM` wide × `CAM_TRACK_DEPTH_MM` deep) along the wire to form a solid representing the track volume.
  - Alternatively (simpler, more robust): iterate the track points and at each point cut a cylindrical pocket (Ø = `CAM_TRACK_WIDTH_MM`, depth = `CAM_TRACK_DEPTH_MM`) into the +Z face, creating a densely-sampled slotted track. This avoids spline sweep failures but produces a faceted approximation. Given n_transition_points=64 per segment and 6 segments, the ~400+ overlapping pockets will produce a smooth-enough channel.
  - **Recommended approach:** Use CadQuery's `sweep()` along a spline wire. Build a 2D circle of radius `CAM_TRACK_WIDTH_MM / 2` on a plane perpendicular to the wire at its start, then sweep. Cut from the body. If sweep proves fragile, fall back to the pocket-array approach.
  - **Practical simplest approach (most likely to succeed first try):** Convert polar points to XY, create a `cq.Workplane` at Z=thickness, use `.pushPoints(xy_coords).hole(CAM_TRACK_WIDTH_MM, CAM_TRACK_DEPTH_MM)` — but `hole()` is through-all. Instead: `.pushPoints(xy_coords).circle(CAM_TRACK_WIDTH_MM / 2).cutBlind(-CAM_TRACK_DEPTH_MM)`. This stamps overlapping cylindrical pockets along the track centerline. With 400+ tightly-spaced points, the union of cylinders forms a continuous groove.
  - **Even better CQ approach:** Build a closed wire from the track points (offset outward and inward by half the track width to get inner/outer edges), make a face, and `cutBlind` from the top face. This gives clean walls. Specifically:
    1. For each `CamTrackPoint`, compute inner edge at `(r - w/2, θ)` and outer edge at `(r + w/2, θ)`.
    2. Convert both edge curves to XY.
    3. Create a closed wire: outer edge forward → cap arc → inner edge backward → cap arc.
    4. Make a face from the wire on the Z=thickness workplane.
    5. `cutBlind(-CAM_TRACK_DEPTH_MM)`.
    6. Repeat for second follower track.
  - Choose whichever approach builds cleanly. Start with the offset-wire approach; fall back to dense-pocket if wire operations fail.
- **Acceptance:** The resulting solid has the cam groove visible. Bounding box tests still pass (track cut doesn't change OD/bore). A new test (Task 5) verifies track exists.

### 3. Cut detent dimples on the outer rim
- **File:** `cad/components/cam_ring.py`
- **Changes:**
  - 3 dimples at `DETENT_SPACING_DEG` (60°) intervals on the outer cylindrical surface, in the lower half of the ring (−Z half, per docstring).
  - Each dimple: a spherical pocket of radius `DETENT_DIMPLE_RADIUS_MM` (2.2 mm), cut inward from the OD surface to depth `DETENT_DIMPLE_DEPTH_MM` (1.4 mm).
  - Implementation: For each of the 3 positions (0°, 60°, 120°):
    1. Compute the center point on the OD surface: `(OD/2 * cos(θ), OD/2 * sin(θ), z_center)` where `z_center = CAM_RING_THICKNESS_MM * 0.25` (lower quarter — the detent zone is on the lower half of the rim).
    2. Place a sphere of radius `DETENT_DIMPLE_RADIUS_MM` centered at `(x, y, z_center)` pushed inward by `(DETENT_DIMPLE_RADIUS_MM - DETENT_DIMPLE_DEPTH_MM)` along the radial direction, so the spherical cap depth is exactly `DETENT_DIMPLE_DEPTH_MM`.
    3. Subtract the sphere from the ring body.
  - CadQuery approach: Use a `cq.Solid.makeSphere()` positioned at each dimple center, then `.cut()` each sphere from the main body.
- **Acceptance:** 3 dimples visible. Bounding box still ≈120 mm OD (dimples are inward cuts, don't change envelope).

### 4. Add a label flat zone on the −Z face (cheap)
- **File:** `cad/components/cam_ring.py`
- **Changes:**
  - The spec says "laser-etched numbers 48 / 60 / 80 at 60° spacing on lower face." We can't model laser etching, but we can create a shallow flat pad or recessed area where labels would go — a minor annular recess on the −Z face, e.g., a 0.3 mm deep, 8 mm wide annular channel at (OD/2 - 8) to (OD/2 - 2) radius. This is a single `.cut()` operation.
  - **This is optional / "if cheap."** If it complicates the build, skip it. Add a code comment: `# Label zone: drawing callout only (laser-etch), not modelled.`
  - The knurl texture is explicitly NOT modelled (docstring says "drawing callout only").
- **Acceptance:** Component still builds. Comment present if skipped.

### 5. Add a 45° chamfer at cam track entry
- **File:** `cad/components/cam_ring.py`
- **Changes:**
  - Per the spec: "45° chamfer entry at track start." Add a chamfer or countersink at the entry point of each track on the +Z face.
  - CadQuery: After cutting the track groove, chamfer the top edge where the groove meets the +Z face. This could be done with `.edges()` selection + `.chamfer(1.0)` on the track top edges — but edge selection on swept cuts is finicky.
  - **Practical:** If edge selection is fragile, skip and add a `# TODO: 45° entry chamfer — requires edge selection on swept cut` comment. This is cosmetic/manufacturing detail, not structural.
- **Acceptance:** If implemented, entry is chamfered. If not, TODO comment exists.

---

## Files to Modify

- **`cad/components/cam_ring.py`** — Replace the stub `build()` body with real geometry (Tasks 1–5).

## New Files

- None required.

## Suggested Test Additions

Add these to `tests/test_components.py` inside the existing `TestComponentBoundingBoxes` class (or a new `TestCamRingGeometry` class):

### T1. `test_cam_ring_has_bore` (high value)
```python
def test_cam_ring_has_bore(self, params):
    """Central bore must exist — ring is not a solid disc."""
    from cad.components.cam_ring import build
    ring = build_or_skip(build, params=params)
    solid = ring.val()
    # Sample a point at ring center, mid-height — should be outside the solid
    import cadquery as cq
    center_pt = cq.Vector(0, 0, params.CAM_RING_THICKNESS_MM / 2)
    # If the bore exists, the center point is in empty space
    bb = solid.BoundingBox()
    # A simple check: the solid should not contain geometry at the origin
    # Use a cross-section at mid-height
    section = ring.workplane(offset=params.CAM_RING_THICKNESS_MM / 2).section()
    wires = section.wires().vals()
    assert len(wires) >= 2, "Expected at least 2 wires (outer + bore) in cross-section"
```

### T2. `test_cam_ring_has_detent_dimples` (medium value)
```python
def test_cam_ring_has_detent_dimples(self, params):
    """Ring volume with dimples should be less than a plain annular disc."""
    from cad.components.cam_ring import build
    ring = build_or_skip(build, params=params)
    import math
    solid = ring.val()
    actual_vol = solid.Volume()
    # Plain annular disc volume (no cuts)
    r_out = params.CAM_RING_OD_MM / 2
    r_in = params.CAM_RING_BORE_MM / 2
    plain_vol = math.pi * (r_out**2 - r_in**2) * params.CAM_RING_THICKNESS_MM
    # Cam track + dimples remove material, so actual < plain
    assert actual_vol < plain_vol, "Ring should have material removed (cam track + dimples)"
```

### T3. `test_cam_ring_volume_reasonable` (sanity guard)
```python
def test_cam_ring_volume_reasonable(self, params):
    """Volume shouldn't be less than 50% of plain disc (catches over-cutting bugs)."""
    from cad.components.cam_ring import build
    ring = build_or_skip(build, params=params)
    import math
    solid = ring.val()
    actual_vol = solid.Volume()
    r_out = params.CAM_RING_OD_MM / 2
    r_in = params.CAM_RING_BORE_MM / 2
    plain_vol = math.pi * (r_out**2 - r_in**2) * params.CAM_RING_THICKNESS_MM
    assert actual_vol > 0.50 * plain_vol, "Ring lost too much volume — geometry bug likely"
```

---

## Dependencies

| Task | Depends On |
|------|-----------|
| 2 (cam track) | 1 (body must exist to cut into) |
| 3 (detent dimples) | 1 (body must exist) |
| 4 (label zone) | 1 (body must exist); independent of 2, 3 |
| 5 (entry chamfer) | 2 (track must exist to chamfer entry) |
| Tests T1–T3 | Task 1 at minimum; ideally after Task 3 |

Build order: **1 → 2 → 3 → (4 if cheap) → (5 if clean) → add tests → run full suite.**

---

## Risks

1. **CadQuery spline sweep on the cam track may fail.** The polar-to-XY path has sharp curvature changes at dwell/transition boundaries. Mitigation: fall back to the dense-pocket approach (overlapping cylindrical cuts along the centerline). Less elegant but guaranteed to produce a valid solid.

2. **Offset wire approach (inner/outer track edges) may self-intersect** at the P3→P1 wrap-around transition where radius changes by ~19 mm over 48°. Mitigation: validate wire closure, or use the simpler centerline-pocket method.

3. **Detent sphere subtraction may produce thin slivers** if the sphere center is poorly placed relative to the OD surface. Mitigation: compute the sphere center analytically: `r_center = OD/2 - DETENT_DIMPLE_RADIUS_MM + DETENT_DIMPLE_DEPTH_MM` along each radial direction. This gives exactly the right cap depth.

4. **All other components are stubs**, so assembly-level integration testing is not possible yet. The cam ring can only be validated in isolation. This is fine — the test scaffold already expects this.

5. **CadQuery not installed in CI/dev environment** — tests will skip gracefully (existing `requires_cq` marker). No risk to non-CQ workflows.

6. **Label zone (Task 4) adds complexity for zero functional value in V1 CAD.** If it takes more than ~5 lines of CQ, skip it with a comment. The spec says "drawing callout only" for both knurl and labels.
