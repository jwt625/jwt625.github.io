---
categories:
- Research
date: '2018-01-11'
header:
  cover: /assets/images/imported/lnnb-unitcell-simulations-1801-1805/image8.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/lnnb-unitcell-simulations-1801-1805/image8.png
  show_overlay_excerpt: false
original_date: '2018-01-11'
tags:
- Piezoelectric
- Simulation
- Reference
title: LNNB unitcell simulations 1801 - 1805
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2018-01-11, converted on 2025-10-12. )

## 20180109, LN 1D beam cavity unit cell optical band

![Image 25](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image25.png)

![Image 24](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image24.png)

## 20180111, LN 1D Beam cavity unit cell phonon band

![Image 27](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image27.png)

Bandgap exist
## 20180112, LN 1D beam unit cell bands, sidewall 20 deg tilt, using rotated coord for LN
Geometry (approximate hole sidewall by eccentric cone) and coord:

![Image 17](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image17.png)

![Image 9](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image9.png)

![Image 26](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image26.png)

TE (left) and TM (right) bands:

![Image 32](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image32.png)

![Image 23](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image23.png)

Mechanics (left y sym, right y anti-sym):

![Image 11](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image11.png)

![Image 6](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image6.png)

Defect geom:

![Image 21](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image21.png)

![Image 13](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image13.png)

defect breath mode: 2.16 GHz
defect dielectric mode: 196 THz
## 20180120, mirror & defect unit cell GA
Mirror cell:
- cost c = - ( f_band - abs(f_mid - f_goal) +\...
- \%               min(f_TE1 - f_TM2, 50THz) )/f_mid
- Search for larger TE band-gap centered at 193 THz
            a: 5.8441e-07
      coef_hx: 0.4502
      coef_hy: 0.7931
       f_goal: 1.9341e+14
            t: 2.6935e-07
            w: 8.0903e-07
         cost: -0.2260
       f_band: 2.2393e+13
        f_mid: 1.9342e+14
Defect cell:
- cost c = abs(f_TE1 - P.f_goal)/1e12 * P.coef_hx * P.coef_hy;
            a: 5.2479e-07
      coef_hx: 0.5186
      coef_hy: 0.3572
       f_goal: 1.9341e+14
            t: 2.7000e-07
            w: 8.1000e-07
         cost: 2.2893e-05
## 20180205, unitcell GA with 200 nm LN thickness
Stopped.
-             a: 5.9383e-07
-       coef_hx: 0.2363
-       coef_hy: 0.2196
-        f_goal: 1.9341e+14
-             t: 2.0000e-07
-             w: 8.2106e-07
-        f_band: 3.3706e+12
-         f_mid: 1.9309e+14
## 20180206, NB mirror cell GA with 300 nm, 15 deg tilt

![Image 22](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image22.png)

Tilt angle is changed in the comsol model.
Result:
-             a: 5.8436e-07
-       coef_hx: 0.4539
-       coef_hy: 0.7990
-             t: 3.0000e-07
-             w: 9.7134e-07
-        f_band: 3.1531e+13
-         f_mid: 1.9342e+14
## 20180218, NB mirror cell GA with 500 nm, 15 deg tilt

![Image 15](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image15.png)

Results:
-             a: 4.8482e-07
-       coef_hx: 0.4412
-       coef_hy: 0.8000
-        f_goal: 1.9341e+14
-             t: 5.0000e-07
-             w: 9.6107e-07
-        f_band: 2.7086e+13
-         f_mid: 1.9341e+14
## 20180307, zipper LNNB mirror cell GA
Results
-             a: 5.8196e-07
-       coef_hx: 0.5588
-       coef_hy: 0.6384
-        disply: 5.0052e-07
-        f_goal: 1.9341e+14
-             t: 2.1334e-07
-             w: 9.7657e-07
-          cost: -0.0683
-        f_band: 1.9127e+13
-         f_mid: 1.9304e+14
-     timestamp: 7.3713e+05
Inspect in comsol model, two zipper NB is not separated!
Criteria for disply is wrong!!! Rerun on 20180312:
Stopped on 20180314 afternoon, results to be updated.
-             a: 6.8382e-07
-       coef_hx: 0.6855
-       coef_hy: 0.6870
-        disply: 5.1028e-07
-        f_goal: 1.9341e+14
-             t: 2.7184e-07
-             w: 6.1334e-07
-        f_band: 2.6674e+13
-         f_mid: 1.9341e+14
- but, ellipse-to-beam edge to small
## 20180320, LNNB mirror cell GA with smallest feature constraints
Constraints:
- (w - hy)/2 \> 150 nm
- (a - hx)/2 \> 150 nm
Running, 20180320, 5:27 PM
Stopped, 20180222, 11:08 AM
Results
-                  a: 5.4199e-07
-            coef_hx: 0.3559
-            coef_hy: 0.6390
-             disply: 0
-             f_goal: 1.9341e+14
-     minFeatureSize: 1.5000e-07
-                  t: 3.0000e-07
-                  w: 9.9423e-07
-               cost: -0.2048
-             f_band: 2.1745e+13
-              f_mid: 1.9382e+14
## 20180403, zipper LNNB unit cell, 300 nm, 15 deg, geom constraint
Started 10:47PM
Finished before 20180404 9:21 PM
Results:
-           a: 7.7530e-07
-            coef_hx: 0.5669
-            coef_hy: 0.3777
-             disply: 6.0814e-07
-             f_goal: 1.9341e+14
-          maxAspRto: 3
-     minFeatureSize: 1.5000e-07
-       minPillarSep: 3.0000e-07
-                  t: 3.0000e-07
-                  w: 8.4579e-07
-             f_band: 5.2673e+12
-              f_mid: 1.9122e+14
f_band so small!
## 20180409, LN mirror cell bands, geom from GA180403
Results weird.

![Image 7](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image7.png)

## 20180412, previous mirror cell GA geometry wrong! Side wall for ellipse is generated in a wrong way
Was using hxBot = hx-t*tan(theta), should be hxBot = hx-2*t*tan(theta)
Fixed in model model_unitcell_LN_tilt_20180320_mirror and in this GA
Started 180412 9:10PM, GA180411 still running.
Stopped 180413 10:01AM. Results: Going to sweep band structure.
Geometry saved as model_unitcell_LN_tilt_mirror_GA20180412.mph

![Image 19](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image19.png)

![Image 12](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image12.png)

-                  a: 5.7586e-07
-            coef_hx: 0.5767
-            coef_hy: 0.6028
-          maxAspRto: 3
-     minFeatureSize: 1.5000e-07
-       minPillarSep: 3.0000e-07
-                  t: 3.0000e-07
-                  w: 9.2607e-07
-             f_band: 2.7945e+13, comparing to 21.7 THz in GA180320
-              f_mid: 1.9348e+14
Feature sizes (measured in COMSOL):
- ellipse edge to beam edge: 184 nm
- ellipse edge to ellipse edge: 122 nm * 2
- aspect ratio: hy/hx = 279 nm * 2/332 nm = 1.68
Phonon bands (calculated on 20180425)

![Image 31](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image31.png)

![Image 14](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image14.png)

## 20180413, GA for 775 nm mirror, hat structure
Geometry:

 ![Image 8](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image8.png)

Started 1:11 PM, 20180413
Stopped 20180414 afternoon
Bandgap too small, only \~ 4 THz
## 20180417, LN wedge NB mirror cell GA
For adding electrode and integrating with wedge WG
Geometry:

![Image 29](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image29.png)

Varying all geom params: hx, hy, w, a, t, t_slab
Started 180417 10:47 AM
Need larger power on bandgap
Stopped, 6:30 PM
- bandgap too small, \~ 10 THz
Restart with fixed thickness t = 300 nm and t_slab = 100 nm
- new cost function, no punishment if f_mid is within f_goal +- 5 THz
- fname = 'gaParams_LNWNBUnitcell_TEmirror_180417_2';
- Stopped 20180418 morning
- Bands:

![Image 16](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image16.png)

![Image 30](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image30.png)

Results:
-                  a: 5.0453e-07
-            coef_hx: 0.5215, hx = 263.11
-            coef_hy: 0.6691, hy = 658.3543
-                  t: 3.0000e-07
-             t_slab: 1.0000e-07
-                  w: 9.8394e-07
-             f_band: 1.7563e+13
-              f_mid: 1.8853e+14
## 20180501, sharp bottom hole corner because of sidewall tilt
See <https://sandbox.open.wolframcloud.com/app/objects/dcd0ffda-f605-41be-a54a-975af269a689>
Parameters:
- s: shift of hole edge due to sidewall tilt
- a, b: semi-axis, convention: b \> a
Condition for sharp corner:
- s \> a\^2/b
Bottom hole curve:

![Image 18](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image18.png)

## 20180503, phonon bands of GA180412 mirror cell in coordA, comparing solution using piezoelectric and pure mechanics
For definition of coordA, see LN properties GD
Unclear:
- not able to set floquet periodic boundary condition in electrostatic
- two options: continuous or zero charge
Piezoelectric with continuous boundary condition for electrostatics
Piezoelectric with zero charge boundary conld for ES:
Pure mechanics:

![Image 5](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image5.png)

![Image 28](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image28.png)

![Image 10](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image10.png)

All together (right: x-axis zoomed):

![Image 20](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image20.png)

![Image 3](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image3.png)

Conclusion:
- pure mechanics gives lower freqs, which make sense because piezoelectric effect effectively increase the stiffness
- not sensitive to boundary condition for piezoelectric sim
- zero charge should be the correct one to use after discussing with Pato
- observed at least one anticrossing between originally "symmetric" and "antisymmetric" bands
## 20180507, TE mirror with interpolated hole sidewall tilt, beam sidewall tilt 10 deg
Started 12:58 AM, 20180508
Stopped 11:34 AM, 20180508

![Image 2](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image2.png)

Results:
-                  a: 5.7640e-07
-            coef_hx: 0.5023, hx = 290 nm, hole separation 287 nm
-            coef_hy: 0.7097, hy = 779 nm, hole-edge separation 159 nm
-             f_goal: 1.9341e+14
-                  t: 3.0000e-07
-                  w: 1.0980e-06
-             f_band: 3.3244e+13, 33 THz
-              f_mid: 1.9170e+14
Bands:

![Image 4](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image4.png)

## 20180525, phonon bands of GA 180507 mirror cell, Y-cut, piezo
Going to compute half geometry both sym, asym, and full geometry, then compare, should be identical
Almost perfect (blue: half, sym; red: half, asym; black dotted: full geom):

![Image 1](/assets/images/imported/lnnb-unitcell-simulations-1801-1805/image1.png)

Why there's imperfection for the highest band?