---
categories:
- Research
date: '2018-06-01'
header:
  cover: /assets/images/imported/lnnb-full-beam-simulations-1806-1812/image108.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/lnnb-full-beam-simulations-1806-1812/image108.png
  show_overlay_excerpt: false
original_date: '2018-06-01'
tags:
- Lithium Niobate
- Materials
- Piezoelectric
- Simulation
- Reference
title: LNNB full beam simulations 1806 -
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2018-06-01, converted on 2025-10-12. )

## 20180601, radiation pressure coupling for anisotropic media and comsol eval
- For RP evaluation, same dataset propagation problem exist:
- "select -\> mirror -\> join" won't work, can't plot and get zero from integral
- "mirror -\> join" works for plotting and integrals give non-zero value
- also noticed the plot quality degraded after join
- tried old and new rp_expr without flipping sign of the field, agrees not so well
- aniso expr gives \~ 4.6712E-17-4.5174E-18i
- old isotropic expr gives \~ 3.3473E-17-3.2373E-18i
- adding sign flip
- aniso expr gives 3.8229E-17-3.6973E-18i
buildSolveLNNB_piezo function working!
## 20180601, first OM GA
Using GA 180507 mirror cell
Started at 9:42 PM

![Image 90](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image90.png)

![Image 164](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image164.png)

Results
-               a_def: 4.4793e-07
-     angled_sidewall: 0.1920
-         coef_hx_def: 0.6636, hx = 297 nm, ellipse to ellipse = 150 nm
-         coef_hy_def: 0.5350, hy = 587 nm
- optical Q = 2.9e7
- mechanical Q = 6.6e12
- OM evaluations, g_OM/2pi = 490 kHz:
-            intPE: -2.2651e-17 - 7.5902e-20i
-            intRP: -1.3214e-18 - 4.1382e-21i
-        gom2pi_pe: 4.6281e+05
-        gom2pi_rp: 2.6999e+04
-             EMen: 5.1992e-13
-             Qmax: 4.9358e-10
-     meff_Qmax_sq: 3.1051e-34
-             meff: 1.2746e-15
-            q_zpf: 4.4052e-15
- tried computing g_om_rp using old isotropic mode, got \~ 1e4
Stopped 180604 20:50 pm
Go to manual inspect
- see genLNNB_GA_Res_scripts.m
- generated, saved as model_LNNB_GA180601.mph
- optical mode: 2.086 GHz and 2.132 GHz

![Image 174](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image174.png)

![Image 40](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image40.png)

- mechanical mode (there's a lot of high Q modes)

![Image 56](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image56.png)

![Image 115](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image115.png)

![Image 64](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image64.png)

Feedback
- difference between breathing mode exist or not is too sharp (ratio = g_OM)
- normalize g_OM
- geom error punishment too strong, change from c = 1 to c = 0
## 20180604, second OM GA, still with same fixed mirror cell (from GA 180507), better cost function
Restart with more initial population
Still not good, no good optics
## 20180606, LNNB OM GA with defect cell optical mode check
Started 12:03 PM
180607, 9:47, still seems bad, no good optics yet (Q \< 100), is it in the range of 30 eigvals?
Maybe better to solve at average freq of X-point defect and band-mid
Stopped 9:58 AM, add variable target freq for EM sol
Restart at 180607, 10 AM
Got one with gom2pi \~ 800 kHz (ind = 151)
Verify rp and pe eval with Si NB!
Stopped 180613, 3PM
Results:
-               a_def: 4.9415e-07
-     angled_sidewall: 0.1920
-         coef_hx_def: 0.6528, hx = 323 nm
-         coef_hy_def: 0.5924. hy = 651 nm
-              f_goal: 1.9477e+14
-      minFeatureSize: 1.5000e-07
-            N_mirror: 18
-        N_transition: 16
-                   t: 3.0000e-07
-                   w: 1.0980e-06
-            intPE: 5.5878e-17 - 2.0959e-16i
-            intRP: 4.2629e-18 - 1.6030e-17i
-        gom2pi_pe: 7.6628e+05
-        gom2pi_rp: 5.8598e+04
-             EMen: 5.6764e-13
-             Qmax: 9.3606e-10
-     meff_Qmax_sq: 9.2996e-33
-             meff: 1.0613e-14
-            q_zpf: 1.5449e-15
coupling +- \~ 10% uncertainty, just from repeating the same geom.
Looks like the fundamental TE mode, at 193.4 THz

![Image 111](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image111.png)

![Image 80](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image80.png)

Fundamental breathing mode at 2.08 GHz

![Image 163](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image163.png)

![Image 48](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image48.png)

### 20180613, OM code verified
Code included in genLNNB_GA_Res_scripts.m
model: model_SiNB_180607.mph
photoelastic term agree within \~ 0.02%
radiation pressure term off by a factor larger than 15.
### 20180614, photoelastic contribution from each term
model: OMGA180607
script: wtjiang/COMSOL/LN/LNNB/check_LNNB_PEInt_script.m
photoelastic tensor of LN for reference:
p11 = -0.026;   p12 = 0.09;     p13 = 0.133;    p14 = -0.075;
p31 = 0.179;    p33 = 0.071;    p41 = -0.151;   p44 = 0.146;
pmat = \p11     p12     p13     p14     0       0;\...
        p12     p11     p13     -p14    0       0;\...
        p31     p31     p33     0       0       0;\...
        p41     -p41    0       p44     0       0;\...
        0       0       0       0       p44     p41;\...
        0       0       0       0       p14     (p11-p12)/2\;
Plotting contributions from different single pe component, normalized by abs val of total pe coupling.

![Image 28](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image28.png)

Conclusion:
- p11 and p13 dominant, each contributed \~ 45%, \~ 90% in total, p12 is the next largest
- luckily they add up, because the breathing mode has large S11 and relative large S33 with different sign
- p14 contribution is expected to be less than p41's, which is already very small in the fig above
Uncertainty of PE coefficients:
- <https://aip.scitation.org/doi/full/10.1063/1.3238507>
- see also the LN properties GD
## 20180614, OM GA after g_total bug fix and with 100 nm geom constraint
Hopefully HSQ would enable smaller structure
Use 100 nm smallest feature constraint
Started 5:28 PM
Stopped, 180623 2:50 PM
Switching to rectangular holes.
## 20180623, LNNB OM GA with rectangular holes,
Inspect at 11 AM 180624, highest g_pe \~ 700 kHz, lower than before, symmetry-reduction not taken into account.
Might be missing the EM mode when f_em_defect is relatively high
- e.g., for f_defect = 1.846e14, f_mode = 1.817e14, already the first mode in all solved modes
- considering subtracting 3 THz for f_goal.
Seems the GA can't find lower cost

![Image 35](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image35.png)

![Image 25](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image25.png)

Going to stop and change f_goal, 180625, 11:05 AM
Modes:

![Image 75](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image75.png)

![Image 165](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image165.png)

![Image 127](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image127.png)

![Image 147](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image147.png)

Mech looks more confined, maybe should go to higher f_em (and lower f_mech?)
Also, imaginary part larger than real part for g_pe and g_rp, should inspect the modes again, maybe save the model/mode profile during the GA run.
### checking phase of interaction with and without PML
With PML:
- int_pe = -3.9792E-18-3.2523E-19i
- int_rp = -4.5149E-18-3.7734E-19i
without PML:
- ind_em = 16
- ind_mech = 16
- data can't propagate to join dataset again, can't plot ewfd data from mirror-then-join dataset, which worked before. Plotting from mirror dataset works.
- going to delete all dataset and then rerun the sol
- ind_mech = 17, ind_em = 16
- still zero??? why???
- 180626: tried regenerating the whole model without mechanical PML, still got all zero interaction integrations, checked in GUI that it's because of the same dataset problem. WHY? Doesn't make sense. The only change is that the geom domains related to mech PML is removed. The mech dataset is working inside the join datasets.
change the method: inspect the phase of various components and and integral arguments
arg(u) from GA180607:
- ![Image 88](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image88.png)
- arg(v) and arg(w)

![Image 134](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image134.png)

![Image 53](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image53.png)

- arg(el11), arg(el22), arg(el33)

![Image 124](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image124.png)

![Image 83](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image83.png)

![Image 107](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image107.png)

- they are either -3.0539 or 0.087689, which is exactly the arg of all components of g_pe (= 3.0545), negative sign from some conjugation?
- the phase is binary until getting close to the PML
from GA 180625:
- arg(u) and arg(v):

![Image 45](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image45.png)

![Image 137](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image137.png)

- arg(el11) etc.

![Image 65](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image65.png)

![Image 81](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image81.png)

![Image 41](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image41.png)

- corresponded pe and rp integral arguments:

![Image 67](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image67.png)

![Image 133](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image133.png)

- all phases above are either -2.7100 or 0.43159
- the phase of g_pe and g_rp is 2.7073 and 2.7100, which is exactly the negative vals of the phase of the mechanics up to a conjugation
- also checked for another mechanical mode, the phase is random and agree with the phase of g_pe & g_rp up to 99.5%
## 20180625, rect LNNB OM GA, modified f_goal and ga_checkDup
Started at 11:34 AM
Already got g_pe \~ 600 kHz (symmetry not taken into account), where
- f_goal = 194.8 THz, f_em = 193.0 THz, Q \~ 7e6
- f_mech = 1.86 GHz
Still running, use the design in model model_LNNB_GA180625_180628.mph for beamwrite LNNB13
f_mech = 2.1141e9

![Image 130](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image130.png)

f_em = 187 THz

![Image 141](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image141.png)

![Image 68](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image68.png)

OM coupling, need to be divided by sqrt(2), also g_rp not reliable:
- Eval OM coupling of EM 10 and Mech 39\...
-         g_pe = 2pi*513.00kHz  =\> 2pi*362.7 kHz
-         g_rp = 2pi*114.97kHz
-         g_om = 2pi*627.98kHz
- Eval OM coupling of EM 10 and Mech 47\...
-         g_pe = 2pi*506.61kHz
-         g_rp = 2pi*186.05kHz
-         g_om = 2pi*692.66kHz
Stopped at 180703 00:43 AM, optimal the same as above.
## 20180706, LNNB fishbone geom GA
Using 100 nm geom constraint mirror cell design (GA 180705)
Finished building model.
Modes rarely fall into bandgaps.
Need to define cost for geom with which the cost function won't proceed to generate and solve the whole NB, because it happens so often at the beginning. Simply giving zero to all the cases is bad. Need to guide the GA to find modes within bandgap.
- tried \~ 70 instances and none of them hit both bandgaps

![Image 176](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image176.png)

DOF for EM = 1095066. Sol time 24.5 min (with another band simulation running).
Should use PMC for x=0 sym plane!
Tried one instance with optical mode within bandgap:

![Image 122](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image122.png)

![Image 87](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image87.png)

Not so effective, maybe a lot of mirror cells are required.
DOF of mechanics = 828500
Going to try smaller transition cell and more mirror cell.
Could also combine FB with hole-type mirror cell, but holes are hard to pattern.
Can't find the case where both EM and mech modes are in bandgap
Best result:

![Image 138](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image138.png)

![Image 182](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image182.png)

-           a_def: 5.9533e-07
-        coef_amp_def: 0.7665
-              f_goal: 1.8748e+14
-      minFeatureSize: 1.0000e-07
-            N_mirror: 17
-        N_transition: 15
-                   t: 3.0000e-07
-               w_def: 6.0099e-07
- UC evals:
-         f_TE1: 1.9148e+14
-          V_uc: 5.3725e-20
-        f_mech: 3.9508e+09
## 20180707, FBH nanobeam trials and GA
Just made the mesh work by meshing all LNNB surface with free triangular first.
Using manual mirror, defect cell from GA yesterday:

![Image 112](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image112.png)

![Image 139](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image139.png)

Solving EM, DOF = 1556386. There's GA and sweepCOMSOLParams running at the same time. Sol time = 42 min.
Q not good. Should use PMC at x=0.
Solving mechanics at 4 GHz. DOF = 1323225. Sol time 33 min, no breathing mode, maybe too far from 4 GHz
### Trial 180708, manual mirror cell, mech bandgap around 4 GHz
P_defect  = struct('a', 520e-9, 'w', 820e-9, 'amp', 260e-9, 'isFBH',true,\...
    'hx', 0e-9, 'hy', 0e-9);
P_mirror = struct('a', 615.4e-9, 'w', 1000e-9, 'amp', 200e-9, 'isFBH',true,\...
    'hx', 369.2e-9, 'hy', 980e-9);
Results:
- optical Q \~ 5.4e4, low

![Image 29](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image29.png)

![Image 104](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image104.png)

![Image 43](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image43.png)

- OM evals:
- Eval OM coupling of EM 15 and Mech 8\...
-         g_pe = 2pi*247.08kHz
-         g_rp = 2pi*289.92kHz
-         g_om = 2pi*536.99kHz
- Eval OM coupling of EM 15 and Mech 9\...
-         g_pe = 2pi*218.87kHz
-         g_rp = 2pi*365.25kHz
-         g_om = 2pi*584.11kHz
- Eval OM coupling of EM 15 and Mech 14\...
-         g_pe = 2pi*329.02kHz
-         g_rp = 2pi*507.00kHz
-         g_om = 2pi*836.00kHz
- Used the wrong boundary condition for the expression generation! Interaction above is wrong! But the correct values should still be similar.
### Trial 180709, mirror cell from FBH GA 180707, mech bandgap around 2 GHz
Have to really push the breathing mode of FB unitcell down to 2 GHz
Main motivation: increase width so that the mode is better confined along the transverse direction.
P_defect  = struct('a', 510e-9, 'w', 1200e-9, 'amp', 500e-9, 'isFBH',true,\...
    'hx', 0e-9, 'hy', 0e-9);
\% mirror cell from FBH GA 180707
P_mirror = struct('a', 557.6e-9, 'w', 1083e-9, 'amp', 81.9e-9, 'isFBH',true,\...
    'hx', 330e-9, 'hy', 859e-9);
Results
- optical Q = 6.7e4, still not confined well comparing to traditional NB

![Image 175](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image175.png)

![Image 50](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image50.png)

![Image 140](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image140.png)

- Eval OM coupling of EM 15 and Mech 33\...
-         g_pe = 2pi*118.35kHz
-         g_rp = 2pi*52.30kHz
-         g_om = 2pi*170.65kHz
- Eval OM coupling of EM 15 and Mech 42\...
-         g_pe = 2pi*107.74kHz
-         g_rp = 2pi*71.89kHz
-         g_om = 2pi*179.62kHz
Hopeless, Q is always lower than 1e5. Coupling also weaker because el11 dominant the stress.

![Image 49](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image49.png)

![Image 42](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image42.png)

- highest Q \~ 9.7e4
Going to also let defect cells have holes.
## 20180709, GA 180607 on X-cut
DOF = 2551657, not enough memory (COMSOL shows memory \> 65 G in the GUI, only \~ 45 G given)
Reduced mesh, DOF = 1078022. Solved in 23 min

![Image 37](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image37.png)

![Image 168](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image168.png)

Q_m = 26760
### Using old ZXY expr:
Eval OM coupling of EM 6 and Mech 48\...
        g_pe = 2pi*759.63kHz
        g_rp = 2pi*149.49kHz
        g_om = 2pi*909.12kHz
details:
-            intPE: 1.5169e-16 + 4.1040e-17i
-            intRP: 2.9868e-17 + 8.0143e-18i
-        gom2pi_pe: 7.3326e+05 + 1.9839e+05i
-        gom2pi_rp: 1.4438e+05 + 3.8742e+04i
-             EMen: 5.6764e-13
-             Qmax: 1.8044e-09
-     meff_Qmax_sq: 4.9775e-33
-             meff: 1.5288e-15
-            q_zpf: 4.0752e-15
### Using nZYX (X-cut) system:
Eval OM coupling of EM 6 and Mech 48\...
        g_pe = 2pi*426.07kHz
        g_rp = 2pi*341.99kHz
        g_om = 2pi*84.09kHz
details:
-            intPE: -8.5079e-17 - 2.3024e-17i
-            intRP: 6.8313e-17 + 1.8389e-17i
-        gom2pi_pe: -4.1128e+05 - 1.1130e+05i
-        gom2pi_rp: 3.3023e+05 + 8.8894e+04i
-             EMen: 5.6764e-13
-             Qmax: 1.8044e-09
-     meff_Qmax_sq: 4.9775e-33
-             meff: 1.5288e-15
-            q_zpf: 4.0752e-15
The radiation pressure code is definitely wrong, it should be the same for both system.
Maybe because the ewfd solution is not updated even after I changed the mesh?
### ewfd updated:
Eval OM coupling of EM 13 and Mech 48\...
        g_pe = 2pi*427.58kHz
        g_rp = 2pi*84.61kHz
        g_om = 2pi*342.97kHz
Details:
-            intPE: 6.0914e-17 + 1.6529e-17i
-            intRP: -1.2075e-17 - 3.1935e-18i
-        gom2pi_pe: 4.1266e+05 + 1.1198e+05i
-        gom2pi_rp: -8.1801e+04 - 2.1634e+04i
-             EMen: 4.0504e-13
-             Qmax: 1.8044e-09
-     meff_Qmax_sq: 4.9775e-33
-             meff: 1.5288e-15
-            q_zpf: 4.0752e-15
### ewfd updated & nZYX expr:
Eval OM coupling of EM 13 and Mech 48\...
        g_pe = 2pi*185.46kHz
        g_rp = 2pi*82.41kHz
        g_om = 2pi*103.05kHz
Details:
-            intPE: -2.6424e-17 - 7.1567e-18i
-            intRP: 1.1722e-17 + 3.2531e-18i
-        gom2pi_pe: -1.7901e+05 - 4.8482e+04i
-        gom2pi_rp: 7.9409e+04 + 2.2038e+04i
-             EMen: 4.0504e-13
-             Qmax: 1.8044e-09
-     meff_Qmax_sq: 4.9775e-33
-             meff: 1.5288e-15
-            q_zpf: 4.0752e-15
## 20180709, LNNB FBH GA, mirror from GA180707 defect cells have holes
Inspecting hero parameters (ind = 213):
P_mirror (from GA):
-         a: 5.5760e-07
-         w: 1.0830e-06
-       amp: 8.1900e-08
-     isFBH: 1
-        hx: 3.3000e-07
-        hy: 8.5900e-07
P_defect (ind = 213):
-         a: 4.8071e-07
-         w: 1.3442e-06
-       amp: 2.7751e-07
-     isFBH: 1
-        hx: 3.5196e-07
-        hy: 5.4875e-07
N_trans = N_mirror = 15
Results (sol time 32.2 min):
- Optical Q max = 2.50e+07, f = 194.55THz
- Eval OM coupling of EM 3 and Mech 31\...
-         g_pe = 2pi*416.83kHz
-         g_rp = 2pi*560.77kHz
-         g_om = 2pi*977.60kHz
- Eval OM coupling of EM 3 and Mech 41\...
-         g_pe = 2pi*132.38kHz
-         g_rp = 2pi*276.60kHz
-         g_om = 2pi*408.98kHz
- g_rp is wrong since the hole-sidewalls are not selected for rp evaluation
Built, solved, saved as model_LNNB_FBH_GA180709.mph
Modes:

![Image 125](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image125.png)

![Image 85](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image85.png)

ewfd.normE is 50 dB smaller when 5 um away.
f_mech = 1.9027 GHz

![Image 128](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image128.png)

![Image 126](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image126.png)

### Try reducing N_trans to 10:
Optical Q degraded to 3.5e5, not so bad.
OM evals:
- Eval OM coupling of EM 1 and Mech 15\...
-         g_pe = 2pi*324.37kHz
-         g_rp = 2pi*318.76kHz
-         g_om = 2pi*641.40kHz
- Eval OM coupling of EM 1 and Mech 39\...
-         g_pe = 2pi*414.65kHz
-         g_rp = 2pi*653.59kHz
-         g_om = 2pi*1065.47kHz
Modes look similar to above.
Also tried manually push up the TE freq of the defect cell, Q not improving.
## 20180716, ind 270 of GA 180709
Used for LNNB14
Modes:

![Image 160](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image160.png)

![Image 142](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image142.png)

![Image 155](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image155.png)

![Image 183](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image183.png)

## 20180716, electrode spacing sweep for GA 180607
script: LN/LNNB/sweep_LNNB_electrode.m

![Image 86](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image86.png)

15 um spacing still gives a Q \~ 490 k

![Image 105](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image105.png)

### 180719, same simulation for GA 180709
- Q \~ 61k for d_metal = 16 um
- Q \~ 411k for 18 um, which is used for LNNB14
## 20180717, fishbone-hole OMGA with 50 nm min feature size and 10 transition cells
Also made the mesh of the defect UC model coarser.
Started 12:55 PM.
Restarted on 0718 with partially fixed surface selection.
TBA
In general, Q not high, always \< 1e6
## 20180722, Elliptical hole design revisited with 20 deg sidewall tilt
From LNNB14 measurement, could get Q \~ 380k on Y cut
180723, actually use FBH design, since 50 nm min feature size mirror cell is too hard for electrode alignment.
Maximal NB width is fixed.
Sidewall angle from LNNB14 SEM: 22 deg for holes and 12 deg for outer sidewall
Results (on 180726, file: gaParams_LNNB_full_OM_FBH_20180723_2.mat)
- ind = 207
- defect parameters:
-             a: 4.4977e-07
-             w: 1.1695e-06
-           amp: 3.8655e-08
-         isFBH: 1
-            hx: 3.3364e-07
-            hy: 8.1096e-07
-         theta: 0.3840
-     theta_out: 0.2094
- f_em = 200.3 THz
- f_mech = 2.115 GHz
- Q_em = 4e6
- coupling: (need to be divided by sqrt(2) )
-         g_pe = 2pi*952.13kHz
-         g_rp = 2pi*65.27kHz
-         g_om = 2pi*886.87kHz
Strain components: el11 (eyy) and |Ey|\^2:

![Image 177](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image177.png)

el22 (ezz) and el33 (exx):

![Image 145](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image145.png)

![Image 148](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image148.png)

Rough ratio between el11, el22 and el33 = 10:-1:-2
## 20180724, PZE coupling in LNNB, the picture
Explicit form:

![Image 1](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image1.png)

![Image 2](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image2.png)

![Image 3](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image3.png)

In LNNB cases:
- on Y-cut (ZXY) nanobeam where NB // Z:
- breathing mode: ![Image 4](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image4.png),
- dominant polarization is ![Image 5](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image5.png), which is global Pz

![Image 119](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image119.png)

- on X-cut (nZYX) nanobeam where still NB // Z
- breathing mode is ![Image 6](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image6.png),
- dominant polarization is ![Image 7](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image7.png), which is global Py

![Image 136](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image136.png)

## 20180906, LNNB mechanics on YZX coordinate
Naively run old ellipse design on YZX, no breathing mode.

![Image 72](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image72.png)

## 20180910, check radpress on model_LNNB_FBH_GA180723_2_ind207
Old results:
-         g_pe = 2pi*952.13kHz
-         g_rp = 2pi*65.27kHz
-         g_om = 2pi*886.87kHz
Using code I wrote:
- surface integration gives -2.0176E-17-1.3395E-18i
- surface integration with isotropic approximation: -7.2505E-17-4.8137E-18i
- iso-approx. is 3.6 times larger, but still not large enough to bring down g_tot
Double check OM code verification on 20180606:
- directly loaded existing model_SiNB_180607
- solved, evaluation clean
- results from interaction_si:
- pereal =  -2.8526e+20
- rpreal =   2.2901e+18
- dominated by PE?
- now save and load again
- volint: -1.1733E-6, from matlab: -1.173313656e-06
- surfint: 9.4197E-9
- using expr from pe_expr_universal for volint
- volint: -1.173289085e-06
- going to set back to old expr to make sure it's actually changing and changing back
- ![Image 99](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image99.png)
- it does change back.
- conclusion, g_PE for Si NB works
- Going to use pe_expr_universal.m for LN, instead of pe_expr_LN.m
- old expr from pe_expr_LN gives volint = 2.9432E-16+1.9854E-17i
- using \0, -90, 180\ as Euler angle if messed up the crystal orientation, volint = -5.6928E-16-3.8413E-17i, even larger
- Two functions generate exactly same string:
- ![Image 114](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image114.png)
- Remaining possibilities that pe_expr_LN or pe_expr_universal could be wrong: mirroring and rotation. (or the crystal orientation is wrong)
- going to figure out how to rotate p tensor instead of rotating fields.
## 20180911, check the SiNB fully using LN code.
SiNB model will be generated fully based on LN code, g_OM will be calculated in the same way that g_OM of LNNB was calculated, and to be compared to interaction_si.m
Script: LN/LNNB/check_SiNB_180911.m
The unitcell parameters are not from cubic interpolation (see below), going to directly use params from old code generate_slab_holes_nanobeam.m.

![Image 47](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image47.png)

Made new function with minor modification comparing to LNNB case.
Mode comparison:
- frequency matches well, difference \~\< 1%
- mechanical profile slightly different, maybe because the x symmetry is not enforced.
- directly measured geometry in COMSOL, seems identical.

![Image 21](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image21.png)

![Image 31](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image31.png)

![Image 97](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image97.png)

![Image 184](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image184.png)

After refining mesh, mechanical mode look closer, frequencies of both modes are also closer to Si NB results. Results TBA
### From interaction_si (two independent run with same geom, results identical):

![Image 103](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image103.png)

![Image 118](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image118.png)

### From SiNB_fromLNNB (with extra sqrt(2) ):
           intPE: -1.6389e-06 - 8.8496e-09i
           intRP: 1.0997e-07 - 5.3080e-26i
       gom2pi_pe: -7.6202e+06 - 4.1148e+04i
       gom2pi_rp: 5.1132e+05 - 2.4680e-13i
            EMen: 1.6279e-13
            Qmax: 6.8767
    meff_Qmax_sq: 4.8992e-15
            meff: 1.0360e-16
           q_zpf: 4.3123e-15
After converting to Hertz and remove extra sqrt2:

![Image 60](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image60.png)

after correcting factor of 2 for s4 \~ s6:

![Image 158](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image158.png)total g_OM = 858.5 kHz

### Conclusion:
photoelastic component generally agree, difference might be from mesh/mechanical mode profile.
radiation pressure component off by \~ a factor of 10.
Remaining possible error for g_OM on LNNB: rotation.
### Checking GA 180723_2 after corrected 2pi in eval_LNNB_OM.m
- overestimating q_zpf hence overestimating g by sqrt(2*pi) \~ 2.51
- after this correction, g should be \~ 251 kHz
- sim running:
-         g_pe = 2pi*379.92kHz
-         g_rp = 2pi*20.91kHz
-         g_om = 2pi*359.01kHz
- if using isotropic approx. for g_rp, and adding missing factor of 2 for s4 \~ s6 in pe_expr:
-         g_pe = 2pi*387.42kHz
-         g_rp = 2pi*88.29kHz
-         g_om = 2pi*299.13kHz
I do think it's hard/impossible to get g \> 500 kHz on LNNB, based on experiment on GaAs nanobeam:
- (K.C. Balram, \..., K. Srinivasan, Moving boundary and photoelastic coupling in GaAs optomechanical resonators, 2014) they measured g \~ 1 MHz on GaAs NB
- GaAs has higher index = 3.35 at 1550 nm
- GaAs has larger PE components (from R.W.Dixon, Photoelastic Properties of Selected Materials..., 1967):

![Image 46](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image46.png)

## 20180918, rotating the PE tensor back to the global coordinates and don't rotate the EM fields:
Still using model = mphload(\pwd '/LNNB/model_LNNB_FBH_GA180723_2_ind207.mph');
- Eval OM coupling of EM 3 and Mech 6\...
-         g_pe = 2pi*380.17kHz
-         g_rp = 2pi*93.57kHz
-         g_om = 2pi*286.60kHz
- sqrt(2) from symmetry not divided.
Seems agreeing with rotating the field.
Going to get in-plane rotation curve for LNY from COMSOL:
- approximating the mechanics using solution from non-rotated orientation
- sqrt(2) from symmetry already divided.

![Image 159](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image159.png)

Photoelastic tensor components:

![Image 135](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image135.png)

![Image 62](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image62.png)

![Image 24](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image24.png)

![Image 89](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image89.png)

With PE tensor from ASA (see below), slightly lower.

![Image 123](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image123.png)

### Next: rotate the elasticity matrix to see how different it is after 45 deg (wrong)
No extra 2s for Voigt notation of elasticity tensor c
LNX:
wrong:![Image 63](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image63.png)
corrected:

![Image 91](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image91.png)

LNY (need double check, WTJ, 20181207):

![Image 120](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image120.png)

## 20180919, in-plane rotation of LNX (wrong, to be updated)

![Image 101](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image101.png)

![Image 179](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image179.png)

But this is with PE tensor from Yariv, Yeh, P 326
Going to try PE tensor from A. S. Andrushchak et. al, JOURNAL OF APPLIED PHYSICS 106, 073510 (2009).
- slightly smaller

![Image 113](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image113.png)

![Image 150](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image150.png)

![Image 146](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image146.png)

- this seems too large.
At 45 deg in-plane rotation:

![Image 149](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image149.png)

45 degree on LNX:
- p22' = (p11+p33+p13+p31+4*p44-2*p14-2*p41)/4 = 0.304
on LNY:
- p22' = (p11+p33+p13+p31+4*p44)/4 = 0.223
### Comparing LN photoelasticity to Si:
PE tensor of Si (from Jasper's thesis)

![Image 26](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image26.png)

- reduction from lower index \~ (2.2 / 3.5)\^4 \~ 0.156
- increase from large p22' is only a factor of 2 or 3
- hence highest g might be on the order of \~ 400 kHz
## 20180925, adding manual imag part to LN elasticity to make the mech Q as measured
Using model = mphload(\pwd '/LNNB/model_LNNB_FBH_GA180723_2_ind207.mph');
function: set_imag_cE(model, Q)
- want a frequency factor (1+1i/(2Q))
- solution: add a factor (1+1i/Q) to all elasticity components.
Trying Q = 4e3, seems working, mode shape the same:
- get Q = 4254

![Image 58](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image58.png)

Trying Q = 4e4
- get Q \~ 4.254e4, very repeatable and scales perfectly.
Trying freq domain with artificial loss + piezoelectric drive:
- just using a slab shape electrode, not the reality, but should have minor effect on the mode.
- x design (electrodes in both mirror region and the E field is along global x):
- ![Image 129](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image129.png)
- mode Q stays the same after adding electrode
- mode freq change \< 0.1% after adding artificial loss and adding electrodes
- real(Y11) and db(imag(Y11)):

![Image 71](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image71.png)

![Image 157](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image157.png)

The driven disp field is very much the mechanical mode:

![Image 109](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image109.png)

- For 1V, Qmax \~ 0.4 nm near resonance
Then
- ![Image 8](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image8.png)GHz/V
- what does this mean? Modulation depth?

![Image 70](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image70.png)

- then for ![Image 9](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image9.png)GHz, ![Image 10](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image10.png), not a small number? Should I be able to see the higher sidebands?
At DC:

![Image 110](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image110.png)

### Trying y design electrode...
- DOF increased from 1167k to 2278k
- sol time 1h

![Image 108](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image108.png)

Not coupled at all:

![Image 69](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image69.png)

### Going to try y design on X cut, 180927
Mode looks similar, freq slightly lower, indeed asymmetric wrt. y
- Q \~ 27.2k

![Image 23](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image23.png)

freq domain results:

![Image 22](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image22.png)

Re(Y):

![Image 152](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image152.png)

- two orders of mag higher than re(Y) from Y cut x design
db(imag(Y)):

![Image 132](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image132.png)

TODO:
- sweep hole y displacement
- extract Qm, Y, max(disp)
## 20181012, roto-optic effect
Inspecting model FBH_GA180723_2_ind207.mph
Color: eYY, arrow: disp field

![Image 117](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image117.png)

Plotting solid.curlUZ ( = dv/dx-du/dy):

![Image 156](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image156.png)

- max curlUZ comparable to max eYY
- regardless of the negative sign of this rotation field in x \< 0 and x \> 0 region, the effect on ![Image 11](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image11.png) from the two regions still adds up
solid.curlUY:

![Image 33](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image33.png)

#### Consider roto-optic effect only from anisotropic refractive index:
Small rotation from ![Image 12](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image12.png) is:
I + dR = ![Image 144](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image144.png), this matrix is rotating the quantity expressed in the rotated coordinate system back to the global/original coordinate system

![Image 13](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image13.png)

For LN, ![Image 14](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image14.png), ![Image 15](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image15.png)
Function: \expr\ = rto_expr_universal(\n_o\^2, n_o\^2, n_e\^2\, 'solid',\90;90;0\,{'pec','none',''});
COMSOL tells me g from roto-optic effect = 0.7 kHz.
### Order of magnitude estimation:
- ![Image 16](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image16.png) and ![Image 17](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image17.png) are on the same order of magnitude
- for photoelastic effect,   ![Image 18](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image18.png)
- for roto-optic effect and this geom config, ![Image 19](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image19.png)
- ![Image 20](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image20.png)
- hence g_RTO \<\~ 4% g_PE
- max of curlUz is also away from the defect center
## 20181031, LNNB full geom, no symmetry
Done. Images TBA

![Image 39](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image39.png)

![Image 32](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image32.png)

Trying to solve it
- DOF of eigenfreq of EMFD: 8119220

![Image 171](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image171.png)

Amir ran the sim on his desktop computer. WTJ trying to open it.
Newer COMSOL needed, installed COMSOL 5.4
COMSOL 5.4 matlab server freeze when evaluating OM interaction.
Use COMSOL 5.0 for matlab GA.
The LN crystal coordinates were wrong!
- Euler angle -pi/4, pi/2, pi/2
- should be pi/4, pi/2, pi/2
## 20181103, LN zipper NB optical Q GA
Started at 181104 12:36 AM
Got COMSOL assertion error sometimes.
Highest Q so far is 790k.
Evaluation pretty long:

![Image 94](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image94.png)

Moved to LNPED teamdrive zipper cavity google doc.
## 20181108, LNNB FBH 250 nm OM GA
Using :
\% mirror cell from FBH GA 180707 modified: model_FBHUC_GA180707_scale_250nm_181108.mph
P_mirror = struct('a', 585.5e-9, 'w', 1137e-9, 'amp', 86e-9, 'isFBH',true,\...
    'hx', 346.5e-9, 'hy', 902e-9,'theta',theta, 'theta_out',theta_out);
wmax = P_mirror.w + 2*P_mirror.amp;
Started at 2:12PM.
Get some mechanics during the weekend:
- mechanical mode at 1.85 GHz, 37 MHz from bandgap edge.
- optical mode at 185.67 THz, \~ 4.5 Hz from bandgap edge. Optical Q \~ 200 k
20181126, 9:50 AM:

![Image 153](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image153.png)

- killed
## 20181127, LNNB FBH GA with fewer cells
Updates:
- use N_trans = 8 and N_mirror = 12
- new f_em goal and f_mech goal:
First tried same defect as from GA 180723
Far field:

![Image 54](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image54.png)

- old:

![Image 93](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image93.png)

Log scale:

![Image 52](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image52.png)

old:

![Image 61](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image61.png)

Mechanical leakage mode the same:

![Image 106](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image106.png)

old:

![Image 84](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image84.png)

Going to check the full LNX 45deg sim:

![Image 36](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image36.png)

![Image 30](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image30.png)

This is roughly k = pi/a/2.5 of the mirror cell:

![Image 170](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image170.png)

![Image 92](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image92.png)

Looks pretty hard to excite:

![Image 166](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image166.png)

TODO:
- use full NB and -45 deg on LNX
Stopped by accident because files moved.
- optical Q \~ 150k
- g \~ 280 kHz
## 20181129, LNNB to WG
path: COMSOL/LN/LNNB/20181129_NB2WG

![Image 180](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image180.png)

## 20181205, real breathing modes on LNX 135 deg and modes around 1.9 GHz on LNX 135 deg (135 is the COMSOL Euler angle alpha -\> in-plane rotation 45 deg)
Mode at 1.9176 GHz on LNX 135 deg, should be what I'm really measuring:

![Image 181](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image181.png)

![Image 185](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image185.png)

It's not a gamma point mode, that's why the coupling is weak
2.2 GHz mode:
- gamma point
- not breathing

![Image 173](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image173.png)

### 20181207, checking defect cell
Defect at 135 deg:
Breathing mode (?) at 2.136 GHz and the above mode at 2.1395 GHz (difference 35 MHz):

![Image 151](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image151.png)

![Image 57](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image57.png)

![Image 98](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image98.png)

![Image 27](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image27.png)

probably because these two modes are too close?
Manually tune them away:
- UC1D/FBH/model_FBHUC_full_LNX135deg_GA180723_defect_modified_181206.mph
- breathing mode at 1.969 GHz and flap0 mode at 2.028 GHz (difference 60 MHz)

![Image 74](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image74.png)

![Image 178](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image178.png)

![Image 44](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image44.png)

![Image 55](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image55.png)

- but this is 45 deg in-plane rotation
going to check same geom but 135 deg in-plane rotation:
- not near-degenerate, but it's at \~ 2.3 GHz, outside of the bandgap.
Breathing mode at \~ 2.15 GHz (higher order):
- from model solved on Amir's computer

![Image 38](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image38.png)

- leaky.
Doesn't measure anything around 2.1 GHz
### LNX 45 deg (135 in-plane rotation), no breathing mode:
1.789 GHz

![Image 66](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image66.png)

1.8235 GHz:

![Image 82](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image82.png)

1.88 GHz:

![Image 100](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image100.png)

1.955 GHz:

![Image 161](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image161.png)

2.1134 GHz (from now on plotting solid.eYY):

![Image 131](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image131.png)

2.1766 GHz:

![Image 143](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image143.png)

Do have few devices with modes around 2.2 GHz (LNNB24TD77O1):

![Image 59](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image59.png)

but coupling very weak.
Question: why I didn't see breathing mode even on LNY?
## 20181208, manual defect
Path: `COMSOL/LN/LNNB/20181208_manualDefect`

Manually push the breathing mode of the defect down to 2.14 GHz on LNX with 135 deg in-plane rotation.
No breathing mode.
1.97 GHz defect UC flappy mode goes to 2.02 GHz fundamental NB flappy mode:
- color is eYY
- mirror UC flappy mode at 2.2 GHz
- UC to NB shifted up 50 MHz

![Image 102](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image102.png)

No hope to get large g from this mode because of symmetry:
- eYY on cross section:

![Image 76](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image76.png)

Why no breathing mode again?
- mirror UC breathing mode freq 2.625 GHz might be too high that the resulting NB breathing mode is outside the bandgap
- going to solve NB mechanics around 2.4 GHz
- also going to play with mirror
### NONONONO, I found the breathing mode, very lossy:
plotting eYY:
- 2.13 GHz, imag part \~ 1 MHz

![Image 78](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image78.png)

Q \~\< 1000!

![Image 51](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image51.png)

Again leaking via the asym band across the bandgap:

![Image 116](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image116.png)

Also tried manual mirror, in the same folder, from unitcell sim manual mirror on 20181208, running...
Same, leaking NB breathing mode:

![Image 34](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image34.png)

## 20181209, LNNB with axe UC
Path: `COMSOL/LN/LNNB/20181209_AX`

First trial not good, Shear1 too close to Breath on defect cell.
Tried to further push up Shear1, now \~ 200 MHz above Breath
Breathing mode exist and is well confined:

![Image 167](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image167.png)

- 4.28 GHz

![Image 73](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image73.png)

![Image 121](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image121.png)

Trying to solve the optics
- DOF = 3603440
- could start but takes forever
YOU STUPID, YOU COULD USE CYCLIC BOUNDARY CONDITION
From COMSOL doc:

![Image 162](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image162.png)

Tried using cyclic boundary condition for the mechanics, worked
- sol time reduced from 17 min to 4 min
- difference between w/ and w/o symmetry is only 20 MHz

![Image 79](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image79.png)

![Image 77](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image77.png)

eYY at the defect:

![Image 169](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image169.png)

However, there is no this boundary condition for the optics
- tried using periodic BC w/ k = 0, but it's wrong
- ![Image 96](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image96.png)
- solution also doesn't make sense
Trying enforced x and y sym for optics,
- wrong, but hopefully accurate up to 95%
- DOF = 1333k
- Solution time (Study 1): 3127 s. (52 minutes, 7 seconds)
- Saved file: model_AX2_LNNB_rotSym_optics_20181209.mph
Q not so good (50k), probably because PML too close?

![Image 95](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image95.png)

ewfd.Weav:

![Image 154](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image154.png)

db(normE):

![Image 172](/assets/images/imported/lnnb-full-beam-simulations-1806-1812/image172.png)