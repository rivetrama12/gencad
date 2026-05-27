# DEFORM Setup Plan — 8 mm Steel Collar / 14B

## Important

Native DEFORM was not executed in the ChatGPT runtime because the DEFORM solver/pre-post is not installed. This folder provides the DEFORM-style operation chain, corrected stage output geometry, and setup instructions for building the model in DEFORM.

## Process type

Use **2D axisymmetric cold forming**. Define billet as plastic/deformable and all punches/dies/KO pins as rigid tools.

## Corrected final geometry

- Collar OD target: Ø10.25 mm
- OD limit from collar sheet: J max Ø10.31 mm
- Collar length target: 8.06 mm
- Length limit from collar sheet: K max 8.13 mm
- Functional bore: Ø8.50 mm
- Die IV final cavity: Ø10.25 × 8.06
- Punch IV working land: Ø8.50
- Punch IV small nose: Ø7.80 / Ø7.75 lead-relief, not through-bore sizing
- KO Pin IV face: Ø8.40, eject only

## DEFORM operation chain

1. Operation 1 — Upset preform: output L ≈ 3.10, OD ≈ Ø11.55, ID ≈ Ø2.00
2. Operation 2 — Backward extrusion: output L ≈ 5.20, OD ≈ Ø10.95, ID ≈ Ø5.90
3. Operation 3 — Semi-finish: output L ≈ 7.15, OD ≈ Ø10.55, ID ≈ Ø7.80
4. Operation 4 — Final calibration: output L 8.06, OD Ø10.25, ID Ø8.50

## Starting DEFORM controls

- Material: low-carbon steel 0.15%C max, annealed/spheroidized
- Temperature: room temperature
- Friction: shear friction m = 0.08–0.12
- Mesh: fine mesh at punch nose, die land entry, bore wall, and final OD land
- Remesh: enabled each operation
- Damage checks: Cockcroft-Latham / normalized damage if available
- Output variables: effective strain, effective stress, velocity, damage, contact pressure, load-stroke

## Acceptance after simulation

- OD after springback/plating allowance must stay under Ø10.31
- K must stay under 8.13
- Bore must remain close to Ø8.50 and clear actual 8 mm lockbolt pin
- No lap/fold at front taper
- No excessive damage at inner bore corner or die land entry
