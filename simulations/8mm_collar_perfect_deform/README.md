# Perfect DEFORM-Ready Setup — 8 mm Steel Collar / 14B

## Status

This package is DEFORM-ready, but native DEFORM was not executed in this environment because DEFORM is proprietary and not installed here.

## Correct final point

The final bore is **Ø8.50**, not Ø8.08. This follows the Punch IV drawing. The smaller Ø7.80 / Ø7.75 punch nose is lead/relief only.

## Final geometry

- OD target: Ø10.25 mm
- OD limit: J max Ø10.31 mm
- Length target: 8.06 mm
- Length limit: K max 8.13 mm
- Functional bore: Ø8.50 mm
- Die IV: Ø10.25 × 8.06 final land
- Punch IV: Ø8.50 working land
- KO Pin IV: Ø8.40 face, eject only

## DEFORM operation sequence

1. Upset preform: L 3.10, OD Ø11.55, ID Ø2.00
2. Backward extrusion: L 5.20, OD Ø10.95, ID Ø5.90
3. Semi-finish: L 7.15, OD Ø10.55, ID Ø7.80
4. Final calibration: L 8.06, OD Ø10.25, ID Ø8.50

## DEFORM setup

- Analysis: 2D axisymmetric cold forming
- Billet: plastic low-carbon steel, 0.15%C max, annealed/spheroidized
- Tools: rigid die inserts, punches, KO pins
- Friction: shear friction m = 0.08–0.12
- Remeshing: enabled every operation
- Mesh refinement: punch nose/bore wall, die land entry, front taper, final OD calibration land
- Output variables: effective strain, effective stress, damage, contact pressure, load-stroke
