# 8 mm Steel Collar — FEA-Style Forming Animation

This folder contains a screening animation generator for the 14B tooling stack:

- Die Insert IV final cavity: Ø10.25 × 8.06 mm
- Punch IV final bore land: Ø8.08 × 8.05 mm
- KO Pin IV face: Ø7.95 mm
- Finished collar limits: J max Ø10.31 mm, K max 8.13 mm

## Important status

This is a **kinematic axisymmetric FEA-style surrogate**, not a validated nonlinear elastoplastic contact FEA solve. Use it for tool-review communication and early screening only. Production release should still use physical trials or a validated forming solver.

## Output interpretation

- Highest relative stress/strain is expected at:
  - Punch nose / bore forming land
  - Die IV entry into final sizing land
  - Outer wall contact during OD calibration
- KO Pin IV must remain an ejector only. Do not let it resize the bore.

## Run

```bash
python fea_surrogate_8mm_collar_animation.py
```

Outputs are written to `outputs/`.

## Volume screen

Final ring volume: 251.795 mm³  
Equivalent Ø11.80 solid stock cut length: 2.304 mm

Use actual forming allowance, trimming, and piercing scrap before setting production cut-off.
