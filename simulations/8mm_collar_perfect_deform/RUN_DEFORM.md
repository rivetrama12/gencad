# Run DEFORM — 8 mm Steel Collar / 14B

## Status

Native DEFORM must be run on a workstation with DEFORM-2D/3D installed and licensed. This ChatGPT/GitHub runtime cannot execute the proprietary DEFORM solver.

This folder defines the corrected DEFORM job basis and operation sequence for manual build or automation inside DEFORM.

## Correct final point

- Final OD target: Ø10.25 mm
- OD limit: J max Ø10.31 mm
- Final length target: 8.06 mm
- Length limit: K max 8.13 mm
- Functional bore: Ø8.50 mm
- Nominal pin: Ø8.00 mm
- Die IV: Ø10.25 × 8.06 final land
- Punch IV: Ø8.50 working land
- Punch IV Ø7.80 / Ø7.75 nose: lead-relief only
- KO Pin IV: Ø8.40 face, eject only

## DEFORM model type

Use **DEFORM-2D axisymmetric cold forming**.

### Objects

| Object | Type | Notes |
|---|---|---|
| Billet | Plastic | Low-carbon steel, 0.15%C max, annealed/spheroidized |
| Die inserts | Rigid | Four operation die cavities |
| Punches | Rigid | Punch IV controls Ø8.50 final bore |
| KO pins | Rigid | Eject only; KO IV face Ø8.40 |

### Starting simulation controls

- Temperature: room temperature / cold forming
- Friction: shear friction m = 0.08–0.12
- Remeshing: enabled every operation
- Mesh refinement zones:
  - punch nose
  - bore wall
  - die land entry
  - final OD land
  - front taper
- Damage model: Cockcroft-Latham or normalized damage if available
- Post variables:
  - effective strain
  - effective stress
  - damage
  - contact pressure
  - load-stroke
  - velocity/material flow

## Operation sequence

| Operation | Name | Output L | Output OD | Output ID | Purpose |
|---:|---|---:|---:|---:|---|
| 1 | Upset preform | 3.10 | Ø11.55 | Ø2.00 | Centered preform |
| 2 | Backward extrusion | 5.20 | Ø10.95 | Ø5.90 | Bore opening and wall flow |
| 3 | Semi-finish | 7.15 | Ø10.55 | Ø7.80 | Prepare for final sizing |
| 4 | Final calibration | 8.06 | Ø10.25 | Ø8.50 | Finished collar output |

## Manual DEFORM run procedure

1. Create a new DEFORM-2D axisymmetric cold-forming project.
2. Define billet material as annealed low-carbon steel, 0.15%C max.
3. Use the four operation outputs above as the target progression.
4. Build/import rigid tools for each station:
   - Die I–IV
   - Punch I–IV
   - KO Pin I–IV
5. Set contact friction m = 0.08–0.12.
6. Enable remeshing before each large deformation zone collapses mesh quality.
7. Run Operation 1.
8. Transfer deformed billet to Operation 2.
9. Transfer Operation 2 billet to Operation 3.
10. Transfer Operation 3 billet to Operation 4.
11. Export post results:
    - effective strain plot
    - effective stress plot
    - damage plot
    - load-stroke curve
    - contact pressure plot
    - final section geometry

## Pass/fail after DEFORM run

| Check | Pass condition |
|---|---|
| OD | Final OD ≤ Ø10.31 mm |
| Length | Final K ≤ 8.13 mm |
| Bore | Final bore close to Ø8.50 mm and clears actual Ø8 mm pin |
| Nose/taper | No lap or fold |
| Bore corner | No excessive damage |
| Ejection | KO pin does not bell-mouth or resize bore |
| Load | Below 14B station capacity |

## Correction rules

- OD oversize: adjust Die IV land, not Punch IV.
- Bore wrong: adjust Punch IV working land, not KO Pin IV.
- Bore bell-mouth: reduce KO Pin IV interference/projection and polish face.
- Collar short/long: correct blank volume, shut height, or final stop.
- Fold at front taper: increase radius, soften transition, or reduce per-station deformation.
- High damage at bore corner: increase punch radius, improve lubrication, reduce reduction ratio, or add intermediate station change.
