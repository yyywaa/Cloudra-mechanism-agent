# HI1_E3 provided guess provenance — ts_guess_c2o25_220.xyz

## What this file is
Geometric pre-organisation seed (relaxed-scan frame with r(C2–O25) = 2.1996 Å) for the durable TS run
of HI1_E3 (iminium–aldolate hydrolysis). It is a **coordinate artifact only**:
it carries no barrier information and the source scan energies are NOT used as evidence.

## Source (native log, unmodified)
- job 963, input: /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/preorg_v2/scan_c2o25_316_220.gjf
  (sha256 60a25746b3abd96e2af6628a08e126f603f1f526363354a27cb28a49d2602b5e)
  route: # opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)
  scan card: B 2 25 S 3 -0.320000   (1-based working order)
- log: /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/preorg_v2/scan_c2o25_316_220.log
  sha256 e535fb2f1bc5b7259aaed18ba7f391290bfec3e4f07ce39cf146238ed63c27cf  (3,914,230 B)
  "Normal termination of Gaussian 16 at Thu Oct 15 23:38:46 2026."  (log line 58635)
  4 scan points, 4 x "Stationary point found" (log lines 5136 / 13935 / 24919 / 57436)
- scan point values r(C2-O25): 3.15959 / 2.83959 / 2.51959 / 2.19959 Å
- last scan point converged constrained coordinate, raw line:
  log:57346  " ! R7    R(2,25)                 2.1996         -DE/DX =    0.0151              !"
- last SCF of the job, raw line:
  log:56970  " SCF Done:  E(RB3LYP) =  -939.307665339     A.U. after    7 cycles"
  (reported for audit only; NOT used as a barrier or reference energy)

## Extraction
- format_converter(input_format=log -> output_format=xyz) : "extracted final frame (frame 3)"
- guess xyz: /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/preorg_v2/ts_guess_c2o25_220.xyz
  sha256 640405ff9b4f59c234fd966fadd1689c7717feb924fc7b4fd40b18a72e1a2bec  (41 atoms, 2 comment lines + 41 atom lines)
- atom order verified identical to the I2 reference minimum /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/I2_optfreq/I2_min_v5.xyz
  (sha256 9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b): same element sequence, 41 atoms.

## Measured key distances (Å) in this guess  [value in I2 minimum for comparison]
- r(C2–O25)  = 2.1996   [3.1596]   <- the scanned, pre-organised coordinate
- r(C2–N4)   = 1.3051   [1.2994]   iminium C=N
- r(O25–H26) = 0.9675   [0.9664]
- r(O25–H27) = 0.9963   [0.9895]
- r(H26···N4) = 3.5905  [4.0064]   (water H not yet oriented to the proline N)
- r(H27···O10) = 1.6746 [1.7171]   (water H hydrogen-bonded to carboxylate O10)
- r(O28–H24) = 0.9882   [0.9842]   (aldol O carries H24)
- r(O11···H24) = 1.7218 [1.7915]   (carboxylate O11 deprotonated)
- r(C1–C29) = 1.5637, r(C29–O28) = 1.4068, r(C9–O10) = 1.2561, r(C9–O11) = 1.2519

## Protonation-state note (declared vs measured)
The deposited I2 reference minimum (0 imaginary frequencies, job 961) is the tautomer
aldol-OH + carboxylate + spectator water, whereas the source-declared HI1_I2 SMILES is
alkoxide + COOH (identical heavy-atom graph, identical total charge, one proton H24 apart).
This guess inherits the measured tautomer. The durable run declaration is documented in
gold_finish_20261015/HI1/E3/STATUS.md (section F) together with the evidence-driven decision record.

## How it is used
ts_prepare input.guess = {kind: "provided", xyz_path: <this directory>/ts_guess_c2o25_220.xyz,
evidence_refs: [<this file>]}. The scan itself is a pre-organisation step only.
