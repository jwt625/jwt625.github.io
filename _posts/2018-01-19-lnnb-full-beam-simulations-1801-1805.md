---
categories:
- Research
date: '2018-01-19'
header:
  cover: /assets/images/imported/lnnb-full-beam-simulations-1801-1805/image63.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/lnnb-full-beam-simulations-1801-1805/image63.png
  show_overlay_excerpt: false
original_date: '2018-01-19'
tags:
- Piezoelectric
- Simulation
- Reference
title: LNNB full beam simulations 1801 - 1805
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2018-01-19, converted on 2025-10-12. )

## 20180113, LN 1D beam cavity with 30deg sidewall tilt
geometry: single defect cell
- using default parameters:

![Image 29](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image29.png)

![Image 15](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image15.png)

Bound em and mech mode (only one each):

![Image 8](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image8.png)

![Image 13](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image13.png)

Next:
- need more input from fabrication, i.e., actual side-wall tilt angle
- does it make sense to do unit cell & nanobeam optimization now?
- unit cell bands for different symmetry
- MEM frequency tuning
### 20180119, increase N_trans to 10
Q increased from \~ 2050 to 31339.
## 20180115 & 16, OM interaction in LN nanobeam cavity
Fixed unit cell generation method, now having same side wall tilt in both x and y direction for holes.
Interaction calculation: see photoelastic_LN.m and pe_expr_LN.m for detail.
Photoelastic tensor:

![Image 48](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image48.png)

Method:
- ignoring anisotropic refractive index for both moving boundary and photoelastic effect
- rotate E field to material local frame for photoelastic calculation
- carry out matrix multiplication with comsol strings instead of manually obtaining final expression
Trial results:
- model = build_LNNB_cavity_tilt('N_transition',6,'N_mirror',7,'LNmeshsize',3);
- ![Image 1](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image1.png)
- ![Image 2](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image2.png)
- ![Image 3](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image3.png)
## 20180118, Placing a LN WG near LN NB

![Image 65](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image65.png)

![Image 28](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image28.png)

Sweeping the distance between the WG and the NB
- running, 10 min each

![Image 4](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image4.png) depends more strongly on the distance than ![Image 5](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image5.png)

- bare Q \~ 2050 (without the WG) (PML too close)
Next:
- extract WG induced kappa for bound mode:

![Image 56](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image56.png)

- change WG structure, e.g., to a full mirror cell NB
## 20180221, Full LNNB GA with 500 nm thickness and 15deg tilt
Started at 11:30 AM
Using fixed mirror cell from GA20180218
Single evaluation cost \~50 min
Stopped at 9:20AM, 20180222
Started GA 20180222
Stopped on 20180226
Results
-           a_def: 4.2938e-07
-     coef_hx_def: 0.7000
-     coef_hy_def: 0.6997
-          f_goal: 1.9341e+14
-               t: 5.0000e-07
-               w: 9.6100e-07
-            Q: -5.8374e+04
## 20180314, LNNB full GA, 13deg, 300 nm
Using mirror cell from GA20180206
20180316, 10.51pm, still running
Manually stopped, 20180320
Not useful, limited by fab
## 20180322, LNNB full beam GA, 15deg, 300 nm, with geom constraint
Started 11:33 AM
Stopped 11:07PM, 20180326
Results
-              a_def: 4.7574e-07
-        coef_hx_def: 0.5737
-        coef_hy_def: 0.7305
-             f_goal: 1.9341e+14
-     minFeatureSize: -1
-           P_mirror: \1×1 struct\
-                  t: 3.0000e-07
-                  w: 9.9400e-07
-               cost: -1.9391e+04
or
- P_defect =
-      a: 4.7574e-07
-      w: 9.9400e-07
-     hx: 2.7295e-07
-     hy: 7.2607e-07
- P_mirror =
-      a: 5.4200e-07
-      w: 9.9400e-07
-     hx: 1.9300e-07
-     hy: 6.3500e-07
Resulting smallest geom feature:
- hole to edge: 134 nm
- hole to hole: 205 nm
- aspect ratios: mirror: 3.29, defect: 2.66
## 20180411, LNNB GA, 15 deg, 300 nm, geom constraint, also change N_trans and N_mirror
Also increased simulation domain size and PML size
Started 20180411 9:32AM
- single evaluation takes \~ 50 min
Stopped at 12:15 PM, 20180413
- highest Q \~ 1.35e7
## 20180413, LNNB full GA with mirror cell GA180412
Started at 12:11 PM, 20180413
GA180411 for LNNB full beam still running, highest Q \~ 1.35e7
- going to stop GA180411
- stopped, see there
WRONG again! Forget to fix wrong ellipse hole sidewall tilt for full NB simulation
- 7:50PM, going to stop
- rerun with name gaParams_LNNB_full_15tilt_300nm_20180413_2
- Q \>\~ 4e7
180418 9:50 PM, Still running
- using following parameters for beamwrite on 180419:
-              a_def: 4.6718e-07
-        coef_hx_def: 0.4395, hx = 205.3256 nm
-        coef_hy_def: 0.6652, hy = 615.98 nm
-           N_mirror: 18
-       N_transition: 16
-                  t: 3.0000e-07
-                  w: 9.2600e-07
-               cost: -4.3254e+07
## 20180418, LN Wedge NB GA
Mirror cell from GA20180417
Example geometry:

![Image 50](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image50.png)

Started 180418 3:11PM
Stopped 180418 evening, too slow and not enough memory to run two full beam GA at the same time.
## 20180427, modes of GA 180413
Mode 1 and mode 3 solved.
Solving mode 2, 3:00 PM, already finished at 3:27 PM
- Solution time (em): 1660 s. (27 minutes, 40 seconds)
Solving mode 4, 3:30 PM
- 27 min 6 s
Mode 1:

![Image 25](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image25.png)

- f = 198.22 THz, Q = 43.254 million, lambda = 1512.4 nm
Mode 2:

![Image 12](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image12.png)

- f = 190.90 THz, Q = 11.535 million, lambda = 1570.4 nm
Mode 3:

![Image 47](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image47.png)

- f = 185.52 THz, Q = 655.27 k, lambda = 1616.0 nm
Mode 4:

![Image 44](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image44.png)

- f = 181.46 THz, Q = 19.97 k, lambda = 1652.1 nm

![Image 6](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image6.png)

### Mechanical modes near 2GHz:
1.865 GHz:

![Image 43](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image43.png)

1.895 GHz:

![Image 45](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image45.png)

1.935 GHz:

![Image 21](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image21.png)

1.974 GHz:

![Image 61](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image61.png)

2.017 GHz:

![Image 32](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image32.png)

## 20180430, piezoelectric simulation of full beam geom GA 180413
Model: `COMSOL/LN/LNNB/model_GA_20180413_piezo_20180429.mph`

x-Symmetric modes:
All this kind:

![Image 55](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image55.png)

2.134 GHz:

![Image 26](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image26.png)

![Image 58](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image58.png)

2.088 GHz:

![Image 66](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image66.png)

![Image 57](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image57.png)

2.062 GHz:

![Image 41](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image41.png)

![Image 35](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image35.png)

2.033 GHz

![Image 38](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image38.png)

![Image 60](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image60.png)

2.010 GHz, looks similar
## 20180430, mechanics of full beam geom GA 180413 with Si PML
Model: `COMSOL/LN/LNNB/model_GA_20180413_mechSolved_PML_20180430.mph`

Geometry and typical leakage:

![Image 37](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image37.png)

![Image 52](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image52.png)

- it's more useful to plot log(solid.disp)
PML coefficient:
- (1+i* ( ( (x-x0)\^2+y\^2 +(z-z0)\^2 ) \> r_pml\^2 ) * s_pml * (((x-x0)\^2+y\^2 +(z-z0)\^2 ) - r_pml\^2)/c_pml\^2)
- r_pml = 5e-6, s_pml = 1, c_pml = 1e-5
- PML domain: r = 10 um
Resulting Q for first three symmetric modes:
- 7.1e13, 2e12, 2e10
- too high, PML too strong? Actually already tried weakening the PML, but Q gets even higher. too weak?
- corresponded frequency: 2.029, 1.983, 1.940 GHz
Asym modes also solved, see model_GA_20180413_mechSolved_asym_PML_20180430.mph
Added top thin-film LN PML on 180501, changes of Q:
- 4.59e13, 8.47e11, disappeared
Wrong! Need full geometry and use coordA instead!
See LN properties for definition of coordA
## 20180503, full beam mechanics, no symmetry plane
Model: wtjiang/COMSOL/LN/LNNB/model_GA_20180413_mechSolved_PML_noSym_20180503.mph
DOF = 1087 k, Sol time = 19 min, \# of modes to look for = 60
Fundamental mode Q \~ 2200, leaky:

![Image 9](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image9.png)

Second order mode Q \~ 8k
Conclusion:
- need cross phonon shield to do optomechanics
But above is with coordB (for bender)
For coordA (x cut LN, Z along -x):
- Fundamental at 2.014 GHz and first order at 1.994 GHz
- Q = 7.27e4 and 8.33e6 respectively

![Image 49](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image49.png)

![Image 46](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image46.png)

![Image 27](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image27.png)

![Image 53](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image53.png)

Still wrong, should use piezoelectric
## 20180507, sidewall tilt correction from SEM LNNB05
Goal: correct dependence of sidewall tilt versus hx & hy
- make an interpolation of theta_x, theta_y vs. hx, hy
- theta_x(hx, hy) and theta_y(hx, hy), linear interpolate data from SEM LNNB0
- theta_x for positive and negative x direction is actually different, ignore for now.
- this might also be from the HF etch of LN
- but I only have data on two straight lines in the (hx, hy) plane, can't use matlab's interp2 etc.
- Plan A: If sharp bottom hole corner doesn't happen (see unitcell sim doc), regard theta_x independent of hy, etc.
- i.e., if s \> a\^2/b, use theta_x and theta_y of the closest point on the line to (hx, hy)
- if s \< a\^2/b, use theta_x from the closest hx value and theta_y from the closest hy value.
- if size larger than threshold (for example hx and hy of mirror cell), theta saturate at minimum value \~ 10 deg.
- turns out to be bad
- plan B: find nearest measured size and use that tilt angles regardless of sharp or not
- turns out not working so well
- ![Image 10](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image10.png)
- ![Image 7](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image7.png)
- still not able to capture the sharp increase of ty
- need to correct the mismatch or scaling between design and fab
- after scaling down the hole size:
- ![Image 24](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image24.png)
- looks okay
- plan B Still bad, see GA 20180508
- plan C, fit tx with cubic (not shown) and ty with x\^4:
- ![Image 16](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image16.png)
- for simplicity, use x\^4 for both tx and ty
## 20180508, full LNNB EM sim (¼ of the real beam) with SEM correction from LNNB05
i.e., geom as close as the actual LNNB05 nanobeam as possible
Model: LNNB/model_LNNB05_20180508.mph
Q much worse than the designed case: 7.56e5

![Image 59](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image59.png)

- but this is still coordB (for bender, y cut)
- Using coordA (x cut, z direction along NB), calculating... (2:46 PM)
- Done. 3:26 PM

![Image 34](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image34.png)

- Q \~ 8.86e5
## 20180508, full LNNB (¼ only) optical Q optimization with interpTilt
Started \~ 4:20 PM
Bad, highest Q \< 1e4
Because sidewall from interpolation (well, actually not interpolation, just find the closest measured size) is jumpy hence leads to scatter at that hole
Stopped 5:42 PM, 20180509
Results:

![Image 31](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image31.png)

![Image 11](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image11.png)

Max Q only 8k
## 20180509, full LNNB (¼) optical Q optimization with x\^4 smooth variable sidewall angle
Started 6:35 PM
Forget to change the filename! GA180508 got overwritten!!!!
Idiot! You also didn't change the coord system!!! Why are you keep simulating and optimizing in the wrong material coordinate???
Corrected, restarted at 20180510 12:23 AM.
Still quite low, \< 1e4
Turns out to be that you are using the wrong mirror cell!

![Image 51](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image51.png)

while from mirror cell GA:

![Image 14](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image14.png)

You probably need to take a rest.^[a](#cmnt1)^
## 20180509, full beam piezo with mechanical PML + ¼ beam ewfd with optical PML ready to solve!
Can't run when GA180509's still running.
Below: mesh, solid mechanics, electrostatic, EM field freq domain

![Image 64](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image64.png)

![Image 63](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image63.png)

![Image 30](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image30.png)

![Image 62](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image62.png)

## 20180510, rerun GA180509 with correct P_mirror
Started 11:24 PM
Didn't write down stop time. Should be in the morning of 20180514

![Image 36](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image36.png)

![Image 39](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image39.png)

Results:
-              a_def: 4.7584e-07
-        coef_hx_def: 0.5197, hx = 247 nm, ellipse to ellipse = 228 nm
-        coef_hy_def: 0.6382, hy = 701 nm, ellipse to beam edge = 199 nm
-             f_goal: 1.9341e+14
-     minFeatureSize: 1.5000e-07
-           N_mirror: 18
-       N_transition: 16
-                  t: 3.0000e-07
-                  w: 1.0980e-06
-               cost: -3.1693e+08
COMSOL can't mesh this solution
Use second smallest cost sol: same coef_hx and coef_hy
-              a_def: 4.9635e-07, hx = 258 nm, ellipse to ellipse = 238 nm
-        coef_hx_def: 0.5197, hy = 701 nm, ellipse to beam edge = 199 nm
-        coef_hy_def: 0.6382
-             f_goal: 1.9341e+14
-           N_mirror: 18
-       N_transition: 16
-                  t: 3.0000e-07
-                  w: 1.0980e-06
-               cost: -2.8216e+08
Actually using wrong sidewall tilt for the beam
## 20180515, rerun GA 180510 with 11 deg beam sidewall tilt
Started at 11:31 PM
mat file accidentally saved in measurement folder: measurements/20180512_LNNB08
Remember to copy it out! Done.
### Stopped 20180521 6 PM
Results:

![Image 22](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image22.png)

![Image 19](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image19.png)

-               a_def: 4.6373e-07
-     angled_sidewall: 0.1920
-         coef_hx_def: 0.4681, hx = 217.07 nm, hole sep. = 246.66 nm
-         coef_hy_def: 0.6566, hy = 720.95 nm, hole to beam edge = 188.53 nm
-              f_goal: 1.9341e+14
-      minFeatureSize: 1.5000e-07
-            N_mirror: 18
-        N_transition: 16
-                   t: 3.0000e-07
-                   w: 1.0980e-06
-                cost: -4.6346e+08
Checking model:
Can't mesh, try random perturbation... Worked.
Trying full model with piezoelectric... seems worked, solving. DOF \~ 2.58 M, sol time 59 min
### Piezoelectric mechanics, 20180522
One mode with Q \~ 118 k

![Image 67](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image67.png)

![Image 40](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image40.png)

### ewfd, 20180522
DOF \~ 1.425 M, sol time \~ 20 min
## 20180521, piezoelectric mechanics, first try, LNNB05 geom
Model: model_ewfd_piezo_LNNB_20180521_mechSolved.mph
original mesh leads to 3.10M DOF to solve, occupied all 62 GB memory, not really able to run.
Reduce mesh (increase)
Solved, \~ 45 min, debug mechanical PML
Results:
- all mechanical Q \< 20k

![Image 20](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image20.png)

![Image 54](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image54.png)

![Image 17](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image17.png)

Going to check mirror cell again. See mirror cell sim 20180503. No full bandgap.
The mode does not look symmetric or anti-symmetric.

![Image 18](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image18.png)

## 20180522, mechanics on Y-cut LNNB, X perp. to NB
Solving geom GA180515, 6:16 PM, DOF 2.58 M, sol time 49 min
- model: model_ewfd_piezo_GA20180515_ycut_solved.mph
Results:
- Q \~ 1.4e9

![Image 42](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image42.png)

![Image 33](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image33.png)

- X-point mode, want Gamma point. You should setup the optomechanical coupling calc asap
Solving geom LNNB05, 8:13 PM, DOF 2.21 M,
- model: model_ewfd_piezo_LNNB_20180521_ycut_mechSolved.mph
- Q \~ 140 k and 313 k (for two nearly degenerate modes at 2.033e9)
- localized in mirror cell region
- doesn't make sense
- now looks symmetric perp. to y:

![Image 23](/assets/images/imported/lnnb-full-beam-simulations-1801-1805/image23.png)

## 20180522, coupling calculation with piezoelectric full mechanics
Model: model_ewfd_piezo_GA20180515_solved.mph
Mirroring the ewfd dataset and do the proper sign flips in the expr generation function.
Still gives absolute zero?
- try evaluating volume max of the numerator expr., comsol crashed
- can't even plot ewfd from the joint dataset? why? solid still could be plotted
- comsol always crashes (tried 3 times) when solid solution is the first data set in the "join dataset", why?
- error msg:
- \#
- \# A fatal error has been detected by the Java Runtime Environment:
- \#
- \#  SIGSEGV (0xb) at pc=0x00007f2d324ab4a6, pid=28812, tid=139829094373120
- \#
- \# JRE version: Java(TM) SE Runtime Environment (7.0_67-b01) (build 1.7.0_67-b01)
- \# Java VM: Java HotSpot(TM) 64-Bit Server VM (24.65-b04 mixed mode linux-amd64 compressed oops)
- \# Problematic frame:
- \# C  \libc.so.6+0x14d4a6\  \_\_nss_passwd_lookup+0x92d6
- \#
- \# Failed to write core dump. Core dumps have been disabled. To enable core dumping, try \"ulimit -c unlimited\" before starting Java again
- \#
- \# An error report file with more information is saved as:
- \# [error log file]
- \#
- \# If you would like to submit a bug report, please visit:
- \#   http://bugreport.sun.com/bugreport/crash.jsp
- \# The crash happened outside the Java Virtual Machine in native code.
- \# See problematic frame for where to report the bug.
- \#
- after trying "ulimit -c unlimited":
- \#
- \# A fatal error has been detected by the Java Runtime Environment:
- \#
- \#  SIGSEGV (0xb) at pc=0x00007f0939ae04a6, pid=6170, tid=139674739787520
- \#
- \# JRE version: Java(TM) SE Runtime Environment (7.0_67-b01) (build 1.7.0_67-b01)
- \# Java VM: Java HotSpot(TM) 64-Bit Server VM (24.65-b04 mixed mode linux-amd64 compressed oops)
- \# Problematic frame:
- \# C  \libc.so.6+0x14d4a6\  \_\_nss_passwd_lookup+0x92d6
- \#
- \# Core dump written. Default location: [core dump location]
- \#
- \# An error report file with more information is saved as:
- \# [error log file]
- \#
- \# If you would like to submit a bug report, please visit:
- \#   http://bugreport.sun.com/bugreport/crash.jsp
- \# The crash happened outside the Java Virtual Machine in native code.
- \# See problematic frame for where to report the bug.
- \#
- Aborted (core dumped)
- If making join dataset using ewfd dataset before mirroring, then works
- also works using dataset mirrored once and then join
## 20180526, coupling calculation with piezoelectric full mechanics, y-cut
Plan:
- Y-cut with global y symmetry (NB along x)
- simulate half beam for piezoelectric mechanics
- simulate ¼ beam for optics
- mirror optics sol and join with mechanics sol
model: model_ewfd_piezo_GA20180515_ycut_solved_20180525.mph
- using Z-X system
Optics the same as nZ-Y system, which make sense. DOF \~ 1.34 M, sol time \~ 20 min
- estimate
- int = n_LN\^4*epsilon0 * E * p * S * E * Volume
        \~ 2.2\^4*9e-13 * (2e8)\^2 * 0.1*0.001 * 1e-6*0.5e-6*0.3e-6
        \~ 84 * 1e-6*0.5e-6*0.3e-6 \~ 1e-17
(from comsol max(expr) \~ 100, comparable to estimated 84)
       from COMSOL, int = 9.4e-19
- EMen = D*E*Volume \~ (2e8)\^2 * 2.2\^2 * 9e-13 * 5e-6*0.5e-6*0.3e-6 \~ 1e-13
- from COMSOL EMen = 3.1e-13 (only ¼ beam)
- Qmax = 4.8e-10 from COMSOL
- m_eff = 2.6e-13 kg
- Q_zpf = 3.1774e-16
- g_pe \~ 180 Hz, seems too small
Forget to change Euler angles for the expr
- even lower after fixing this bug
First breathing mode with high Q optics (\>1e6)
- manually increase hx to make Gamma point breathing modes in defect cell
- use manually developed defect cell and GA 180507 mirror cell to make NB
- optical Q still okay, \> 1e6
- finished PE interaction calculation, g*2*pi = 167 kHz
Need to rewrite RP interaction expr and eval codes...
New coupling GA scheme:
- Goal: high optical Q + Gamma-point breathing mode in mech bandgap
- varying all mirror cell and defect cell params at the same time
- independent sims of mirror and defect cell
- mirror cell TE bandgap reward factor: (df_TE \> 15 THz) * (df_TE - 15 THz)
- mirror cell TM
::: c22
[a](#cmnt_ref1)yes
:::