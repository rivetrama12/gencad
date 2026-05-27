# Rectified FEA — 8 mm Steel Collar / 14B

This replaces the earlier surrogate output.

## Rectification

The earlier animation incorrectly treated the final bore as Ø8.08.  
Using the user's punch drawing, the final functional bore is now treated as **Ø8.50** from Punch IV. The small Ø7.80 / Ø7.75 nose is treated as a lead/relief feature, not the through-bore.

## Final connected geometry

- Collar OD target: Ø10.25 mm
- Collar OD limit J max: Ø10.31 mm
- Collar length target: 8.06 mm
- Collar length limit K max: 8.13 mm
- Functional bore target: Ø8.50 mm
- Die IV land: Ø10.25 × 8.06 mm
- Punch IV working land: Ø8.50
- KO Pin IV face: Ø8.40, eject only

## FEA method

This is a 2D axisymmetric finite-element stiffness/stress solve using 4-node quadrilateral axisymmetric elements. It calculates stress and yield utilization at each stage.

It is still not a full nonlinear large-strain elastoplastic contact forming simulation. For production approval, run the included Abaqus-style input deck or rebuild the model in a dedicated forming solver.

## Volume screen

Finished ring volume: 207.793 mm³  
Equivalent Ø11.80 solid stock length without scrap: 1.901 mm

Actual cut-off must include slug/pierce/trim/forming allowance.
