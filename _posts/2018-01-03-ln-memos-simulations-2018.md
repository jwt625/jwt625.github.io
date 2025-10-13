---
categories:
- Tutorial
date: '2018-01-03'
header:
  cover: /assets/images/imported/ln-memos-simulations-2018/image108.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/ln-memos-simulations-2018/image108.png
  show_overlay_excerpt: false
original_date: '2018-01-03'
tags:
- Lithium Niobate
- Materials
- Piezoelectric
- Simulation
title: Lithium Niobate MEM optical system
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2018-01-03, converted on 2025-10-12. )

# Theory
Definitions
- ![Image 1](/assets/images/imported/ln-memos-simulations-2018/image1.png): beam length
- ![Image 2](/assets/images/imported/ln-memos-simulations-2018/image2.png): beam width
- ![Image 3](/assets/images/imported/ln-memos-simulations-2018/image3.png): LN layer thickness
- ![Image 4](/assets/images/imported/ln-memos-simulations-2018/image4.png): beam end deflection
- ![Image 5](/assets/images/imported/ln-memos-simulations-2018/image5.png): curvature
- ![Image 6](/assets/images/imported/ln-memos-simulations-2018/image6.png): material coordinates; ![Image 7](/assets/images/imported/ln-memos-simulations-2018/image7.png): global coordinates
- ![Image 8](/assets/images/imported/ln-memos-simulations-2018/image8.png): side-wall tilt angle
- ![Image 9](/assets/images/imported/ln-memos-simulations-2018/image9.png): total displacement-voltage coupling strength (displacement per volt)
Estimations
- estimate curvature from unit-cell: ![Image 10](/assets/images/imported/ln-memos-simulations-2018/image10.png) (need to confirm that it is indeed a "curvature" effect, not simple displacement where ![Image 11](/assets/images/imported/ln-memos-simulations-2018/image11.png))
Aim
- generate large displacement from small voltage
- if aiming at d=100 nm for L=10 um, then C=2000 m\^-1
- 20180105: got ![Image 12](/assets/images/imported/ln-memos-simulations-2018/image12.png) for vertical bender
- 20180105: got ![Image 13](/assets/images/imported/ln-memos-simulations-2018/image13.png) for in-plane bender (d_metal = 100 nm)
Piezoelectric property of LN
- from Weis, R S & Gaylord, T K (1985)
- ![Image 121](/assets/images/imported/ln-memos-simulations-2018/image121.png),![Image 128](/assets/images/imported/ln-memos-simulations-2018/image128.png)
- ![Image 161](/assets/images/imported/ln-memos-simulations-2018/image161.png)
Explicit Effects:

![Image 14](/assets/images/imported/ln-memos-simulations-2018/image14.png)

![Image 15](/assets/images/imported/ln-memos-simulations-2018/image15.png)

- neglecting d31
- Ex: zx shear strain (d15) and xy shear strain (-2*d22)
- Ey: x normal strain (-d22), y normal strain (d22) and yz shear strain (d15)
- Ez: z normal strain (d33)
- Ez and d33 is the cleanest effect
- ![Image 16](/assets/images/imported/ln-memos-simulations-2018/image16.png) is the best candidate to generate bending
Calculated max d33 direction: [link](https://sandbox.open.wolframcloud.com/app/objects/0d741600-74bb-43e8-aff8-f7ffe3086f14)
## Zig-zag in-plane bender (50 nm in 10*10 um\^2) theory estimation
20180106

![Image 155](/assets/images/imported/ln-memos-simulations-2018/image155.jpg)

![Image 144](/assets/images/imported/ln-memos-simulations-2018/image144.png)

Parameters:
- ![Image 17](/assets/images/imported/ln-memos-simulations-2018/image17.png): deflection angle of a simple beam
- ![Image 18](/assets/images/imported/ln-memos-simulations-2018/image18.png)
- ![Image 2](/assets/images/imported/ln-memos-simulations-2018/image2.png): unit cell width
- ![Image 19](/assets/images/imported/ln-memos-simulations-2018/image19.png): number of zig-zag unit cell
- ![Image 20](/assets/images/imported/ln-memos-simulations-2018/image20.png), zig-zag structure length
- ![Image 21](/assets/images/imported/ln-memos-simulations-2018/image21.png): deflection angle of single unit cell
- ![Image 22](/assets/images/imported/ln-memos-simulations-2018/image22.png): radius of the whole structure (![Image 23](/assets/images/imported/ln-memos-simulations-2018/image23.png) ?)
- ![Image 24](/assets/images/imported/ln-memos-simulations-2018/image24.png): total deflection of zig-zag structure
Estimation (displacement-related parameters are all for 1 Volt):
- from beam bender simulation, ![Image 25](/assets/images/imported/ln-memos-simulations-2018/image25.png) for ![Image 26](/assets/images/imported/ln-memos-simulations-2018/image26.png)
- assuming unit cell width ![Image 27](/assets/images/imported/ln-memos-simulations-2018/image27.png)
- for 10 unit cell, ![Image 28](/assets/images/imported/ln-memos-simulations-2018/image28.png)
- ![Image 29](/assets/images/imported/ln-memos-simulations-2018/image29.png)
- ![Image 30](/assets/images/imported/ln-memos-simulations-2018/image30.png)
- approximation need: w \<\< L
Direct calculation from analytic model (no approximation): ![Image 31](/assets/images/imported/ln-memos-simulations-2018/image31.png)(see [detail](https://sandbox.open.wolframcloud.com/app/objects/bf0e1d2d-de2b-4765-96ad-7bbd617e5bfa))
Comparison to simulation:
- ![Image 32](/assets/images/imported/ln-memos-simulations-2018/image32.png) from single arm simulation
- 1-unit-cell: predicted ![Image 33](/assets/images/imported/ln-memos-simulations-2018/image33.png), simulated ![Image 34](/assets/images/imported/ln-memos-simulations-2018/image34.png)
- 3-unit-cell: predicted ![Image 35](/assets/images/imported/ln-memos-simulations-2018/image35.png), simulated ![Image 36](/assets/images/imported/ln-memos-simulations-2018/image36.png)
- 5-unit-cell: predicted ![Image 37](/assets/images/imported/ln-memos-simulations-2018/image37.png), simulated ![Image 38](/assets/images/imported/ln-memos-simulations-2018/image38.png)
- a factor of \~2 disagreement
- corrected: ![Image 10](/assets/images/imported/ln-memos-simulations-2018/image10.png), not ![Image 39](/assets/images/imported/ln-memos-simulations-2018/image39.png), ![Image 40](/assets/images/imported/ln-memos-simulations-2018/image40.png)
- ![Image 41](/assets/images/imported/ln-memos-simulations-2018/image41.png)
- ![Image 42](/assets/images/imported/ln-memos-simulations-2018/image42.png)
## Reflectional grating estimation (20180110)
Objective: observe displacement from color change
Setup: light incide at angle ![Image 43](/assets/images/imported/ln-memos-simulations-2018/image43.png), observe vertically:

![Image 44](/assets/images/imported/ln-memos-simulations-2018/image44.png)

For first order grating and reasonable width, ![Image 45](/assets/images/imported/ln-memos-simulations-2018/image45.png)um
For fixed incident angle
- ![Image 46](/assets/images/imported/ln-memos-simulations-2018/image46.png)
- For 1V: ![Image 47](/assets/images/imported/ln-memos-simulations-2018/image47.png)
- For visible light ![Image 48](/assets/images/imported/ln-memos-simulations-2018/image48.png), ![Image 49](/assets/images/imported/ln-memos-simulations-2018/image49.png)
For fixed incident wavelength
- ![Image 50](/assets/images/imported/ln-memos-simulations-2018/image50.png), large angle prefered, i.e., ![Image 51](/assets/images/imported/ln-memos-simulations-2018/image51.png), or higher order grating
- For ![Image 52](/assets/images/imported/ln-memos-simulations-2018/image52.png)deg, ![Image 53](/assets/images/imported/ln-memos-simulations-2018/image53.png)deg
## Photo-elastic contribution of LN nanobeam ![Image 54](/assets/images/imported/ln-memos-simulations-2018/image54.png)
Photoelastic effect: ![Image 55](/assets/images/imported/ln-memos-simulations-2018/image55.png)
For a general permittivity: ![Image 56](/assets/images/imported/ln-memos-simulations-2018/image56.png)
Do calculation in material coordinate:
- Euler angle from global frame to mat frame: ![Image 57](/assets/images/imported/ln-memos-simulations-2018/image57.png)
- Electric field components in mat frame:
- ![Image 58](/assets/images/imported/ln-memos-simulations-2018/image58.png)
- be careful that the transformation of component is inverse (and transpose if distinguishing covariant and contravariant) of the transformation for base vectors. They look the same here because of the special angles
Rotation of field to material frame
20180115\~17: finished code for photoelastic in LN, see
- Optomechanics/integrals/interaction/pe_expr_LN.m
## Electrostriction in LN
20180123, WTJ
Main ref: [Tailoring optical forces in waveguides through radiation pressure and electrostriction](https://www.osapublishing.org/oe/abstract.cfm?uri=oe-18-14-14439)
General electrostriction effect:

![Image 59](/assets/images/imported/ln-memos-simulations-2018/image59.png)

Isotropic (as approximation for LN): ![Image 60](/assets/images/imported/ln-memos-simulations-2018/image60.png)
Elasticity: ![Image 61](/assets/images/imported/ln-memos-simulations-2018/image61.png)
Final ![Image 62](/assets/images/imported/ln-memos-simulations-2018/image62.png) for LN:
- ignoring p11, p12, p14 & p33
- ignoring s12, s13, s14
- Detail calculation [here](https://sandbox.open.wolframcloud.com/app/objects/779a2789-222f-4ecc-8ce7-a752cfe22c85)

![Image 120](/assets/images/imported/ln-memos-simulations-2018/image120.png)

- too small, need double check
- typically ![Image 63](/assets/images/imported/ln-memos-simulations-2018/image63.png) in LN piezo bender under 1 V
Ez of Fundamental TE mode is a good candidate:

![Image 134](/assets/images/imported/ln-memos-simulations-2018/image134.png)

![Image 127](/assets/images/imported/ln-memos-simulations-2018/image127.png)

- which generates ![Image 64](/assets/images/imported/ln-memos-simulations-2018/image64.png) and ![Image 65](/assets/images/imported/ln-memos-simulations-2018/image65.png) distribution
- which means x-cut or y-cut LN
- disadvantage: |Ez|\^2 is an order smaller than |Ex|\^2
## THEORY of curvature bender
WTJ, 20180223
Why this stupid theory takes you so long? Are you really thinking?
Effect: ![Image 16](/assets/images/imported/ln-memos-simulations-2018/image16.png), ![Image 66](/assets/images/imported/ln-memos-simulations-2018/image66.png)
For homogeneous field, ![Image 67](/assets/images/imported/ln-memos-simulations-2018/image67.png), where ![Image 68](/assets/images/imported/ln-memos-simulations-2018/image68.png) is the length along x direction.
Consider a rectangle on x-z plane with size ![Image 68](/assets/images/imported/ln-memos-simulations-2018/image68.png) and ![Image 69](/assets/images/imported/ln-memos-simulations-2018/image69.png) under ![Image 70](/assets/images/imported/ln-memos-simulations-2018/image70.png) with ![Image 71](/assets/images/imported/ln-memos-simulations-2018/image71.png), its right end will bend to positive z-axis by ![Image 72](/assets/images/imported/ln-memos-simulations-2018/image72.png), where ![Image 73](/assets/images/imported/ln-memos-simulations-2018/image73.png) is the central angle of the curved rectangle. For simplicity, assume ![Image 74](/assets/images/imported/ln-memos-simulations-2018/image74.png) at ![Image 75](/assets/images/imported/ln-memos-simulations-2018/image75.png). ![Image 76](/assets/images/imported/ln-memos-simulations-2018/image76.png) is the radius of the arc.
Up to first order:
- ![Image 77](/assets/images/imported/ln-memos-simulations-2018/image77.png)
- ![Image 78](/assets/images/imported/ln-memos-simulations-2018/image78.png)
Subtract the above two equations:
- ![Image 79](/assets/images/imported/ln-memos-simulations-2018/image79.png)
- therefore ![Image 80](/assets/images/imported/ln-memos-simulations-2018/image80.png)

![Image 81](/assets/images/imported/ln-memos-simulations-2018/image81.png)

Only one parameter from the material, amazing.
Verified by simple simulation, deviation within 0.5% (although the simulation is designed to verify this)
### General case
- ![Image 82](/assets/images/imported/ln-memos-simulations-2018/image82.png)
- approximate all other S components as zero
- ![Image 83](/assets/images/imported/ln-memos-simulations-2018/image83.png)
- ![Image 84](/assets/images/imported/ln-memos-simulations-2018/image84.png)
- ![Image 85](/assets/images/imported/ln-memos-simulations-2018/image85.png) hence ![Image 86](/assets/images/imported/ln-memos-simulations-2018/image86.png)
# Simulations
## 20180103, LN-on-SiO2 vertical bender (bad)
Use d33 effect
Vertical bender requires two layers of different materials
- use 200 nm LN on 200 nm SiO2
Part of LN needs to be removed to break symmetry
Simulate one unit cell + one extra ground electrode
Geometry:
- periodic along y
- electrode width = 2 um
- gap between electrode = 2 um
Potential and displacement:

![Image 129](/assets/images/imported/ln-memos-simulations-2018/image129.png)

![Image 184](/assets/images/imported/ln-memos-simulations-2018/image184.png)

Result:
- 1V Curvature C = 1.33 m\^-1
- much larger than results from [10.1038/ncomms10078](http://www.nature.com/doifinder/10.1038/ncomms10078) (C \<\< 0.01)
- linearly depends on voltage (where in the above paper it's voltage square)
Conclusion:
- hard to use in-plane E field and d33 for vertical bend
## 20180104, LN arc vertical bender, \~2 nm vertical bend within 8um (simple beam is better)
Only using Lithium Niobate.
A combination of all piezoelectric effects.
Geometry:
- arc radius r = 3 um, width w = 600 nm, thickness t = 200 nm
- electrode width w_metal = 200 nm
Electric potential and resulting displacement:

![Image 166](/assets/images/imported/ln-memos-simulations-2018/image166.png)

![Image 151](/assets/images/imported/ln-memos-simulations-2018/image151.png)

Max z displacement = 1.67 nm
Scaling (from param sweep):
- ![Image 87](/assets/images/imported/ln-memos-simulations-2018/image87.png) (change w by changing electrode distance)
- for r = 10 nm, max disp \~ 20 nm:
- ![Image 125](/assets/images/imported/ln-memos-simulations-2018/image125.png)
- maximum exist for thickness t:
- ![Image 187](/assets/images/imported/ln-memos-simulations-2018/image187.png)
- expected to be square wrt. \# of concatenation (it looks like a curvature effect, not simple displacement)
## 20180104, LN beam in-plane bender, \~1.5 nm disp. for L=10 um
Material coordinate: x3 = - y, x2 = z (y-cut)
Dominant effect:
- S11: non-zero Ez component (E2 in mat. coord.) under the electrodes with opposite direction, hence opposite S11 effect under the two electrode
Geometry:
- simple LN beam, w = 600 nm, t = 200 nm, L = 10 um
- electrode width 200 nm
Electric potential and displacement:

![Image 132](/assets/images/imported/ln-memos-simulations-2018/image132.png)

![Image 175](/assets/images/imported/ln-memos-simulations-2018/image175.png)

Max y displacement: 1.98 nm
Reduced to 1.45 nm after adding top Au electrode (t_metal = 200 nm) to solid mech
Scaling (from param sweep):
- ![Image 88](/assets/images/imported/ln-memos-simulations-2018/image88.png) (change w by changing electrode distance)
- thickness t: optimal around 500 nm:
- ![Image 131](/assets/images/imported/ln-memos-simulations-2018/image131.png) (expected to drop if further increase t)
Dominant effect verification:
Add electrodes on LN bottom to enhance Ez, should lead to much larger disp.:

![Image 119](/assets/images/imported/ln-memos-simulations-2018/image119.png)

Resulting curvature: ![Image 89](/assets/images/imported/ln-memos-simulations-2018/image89.png)(1V), ![Image 90](/assets/images/imported/ln-memos-simulations-2018/image90.png) if reduce electrode separation to 100 nm
Dynamics (20180108):
- fundamental vertical mode: 2.00 MHz
- fundamental in-plane mode: 2.57 MHz
## 20180105, LN beam vertical bender (2 nm vert. disp. in L=10 um)
Material coordinate = global coordinate (z-cut)
Non-zero strain:
- S11 = d22 Ey
- S22 = -d22 Ey
- S23 = -d15 Ey
Combination of the three effects:
- A: different x contraction due to Ey vertical distribution
- z bend along x
- B: different y contraction due to Ey vertical distribution
- -z bend along y (negligible)
- C: yz shear from S23
- A is the dominant effect (see below)
Electric potential and displacement:

![Image 164](/assets/images/imported/ln-memos-simulations-2018/image164.png)

![Image 178](/assets/images/imported/ln-memos-simulations-2018/image178.png)

5 nm 1V vertical displacement with 10 um beam
Reduced to 2 nm after adding to Au electrodes (t_metal = 200 nm) in solid mech.
Scaling from param sweep
- ![Image 91](/assets/images/imported/ln-memos-simulations-2018/image91.png) (change w by changing electrode distance)
- optimal t exist \~ 200 nm
- ![Image 142](/assets/images/imported/ln-memos-simulations-2018/image142.png)
Determine the dominant effect: Use side electrodes instead of surface electrode, i.e., Ey const. along z direction.
- Result: homogeneous x & y (small) contraction and yz shear:

![Image 185](/assets/images/imported/ln-memos-simulations-2018/image185.png)

![Image 183](/assets/images/imported/ln-memos-simulations-2018/image183.png)

Further enhancing the effect by adding bottom electrodes can get ![Image 92](/assets/images/imported/ln-memos-simulations-2018/image92.png) for d_electrode = 100 nm
## 20180105, LN slab vertical bender unitcell, disp. 0.5 nm with L=5 um
Geometry: periodic along y
- t = 200 nm, t_etch = 150 nm, w_etch = 200 nm
- w_metal = 200 nm, d_metal = 100 nm, t_metal = 200 nm
Potential and displacement:

![Image 148](/assets/images/imported/ln-memos-simulations-2018/image148.png)

![Image 123](/assets/images/imported/ln-memos-simulations-2018/image123.png)

disp. ![Image 93](/assets/images/imported/ln-memos-simulations-2018/image93.png)
Curvature: ![Image 94](/assets/images/imported/ln-memos-simulations-2018/image94.png)
Adding top Au electrode:
- disp. reduced to ![Image 95](/assets/images/imported/ln-memos-simulations-2018/image95.png) for a full etch:

![Image 157](/assets/images/imported/ln-memos-simulations-2018/image157.png)

## 20180106, scaled LN slab vertical bender (for Photolitho, 40 nm disp. in 0.3 mm length)
Geometry:

![Image 163](/assets/images/imported/ln-memos-simulations-2018/image163.png)

Displacement:

![Image 160](/assets/images/imported/ln-memos-simulations-2018/image160.png)

Curvature: ![Image 96](/assets/images/imported/ln-memos-simulations-2018/image96.png)
Can be enhanced if using thinner electrode and LN slab
## 20180106, LN zig-zag in-plane bender (8 nm for 1 unit cell, linear wrt. \# of unit cell)
See theory for idea and estimation
Unit cell size \~ 1.1 um by 11 um
1 unit cell potential and disp. (max 5.66 nm):

![Image 167](/assets/images/imported/ln-memos-simulations-2018/image167.png)

![Image 180](/assets/images/imported/ln-memos-simulations-2018/image180.png)

- increase to ![Image 97](/assets/images/imported/ln-memos-simulations-2018/image97.png) 8 nm , ![Image 98](/assets/images/imported/ln-memos-simulations-2018/image98.png) for t = 500 nm
- ![Image 99](/assets/images/imported/ln-memos-simulations-2018/image99.png), agree with theory
- dynamics:
- in-plane modes: f0 = 1.98 MHz, f1 = 2.02 MHz
- out-of-plane modes: f2 = 2.36 MHz, f3 = 2.40 MHz
- f4 (16 MHz) and above demonstrate complicated twist
3 unit cell potential and disp. (max 17.0 nm):

![Image 176](/assets/images/imported/ln-memos-simulations-2018/image176.png)

![Image 159](/assets/images/imported/ln-memos-simulations-2018/image159.png)

- increase to ![Image 97](/assets/images/imported/ln-memos-simulations-2018/image97.png)25.1 nm , ![Image 100](/assets/images/imported/ln-memos-simulations-2018/image100.png)for t = 500 nm
- ![Image 101](/assets/images/imported/ln-memos-simulations-2018/image101.png), agree with theory
- dynamics:
- ![Image 172](/assets/images/imported/ln-memos-simulations-2018/image172.png)

![Image 174](/assets/images/imported/ln-memos-simulations-2018/image174.png)

![Image 149](/assets/images/imported/ln-memos-simulations-2018/image149.png)

![Image 126](/assets/images/imported/ln-memos-simulations-2018/image126.png)

- f0: 655 kHz, in-plane bend mode
- f1: 705 kHz, out-of-plane bend mode
- f2: 740 kHz, combination of y and z (mainly y)
- f3: 868 kHz, y twist
- f4 & f5: higher in-plane modes
Expected to get Dx and Dy \~ 50 nm for 10 unit cells (area \~ 10 by 10 um)
- \~ 80 nm for t = 500 nm
If further increase the \# of unit cell to 5:
- f0: 333 kHz, out-of-plane bend mode
- f1: 340 kHz, in-plane bend mode
- f2: 445 kHz, y-y-mode
- f3: 524 kHz, y-axial-mode
- f4: 1.08 MHz, higher in-plane mode
- ![Image 182](/assets/images/imported/ln-memos-simulations-2018/image182.png)

![Image 186](/assets/images/imported/ln-memos-simulations-2018/image186.png)

![Image 177](/assets/images/imported/ln-memos-simulations-2018/image177.png)

![Image 152](/assets/images/imported/ln-memos-simulations-2018/image152.png)

## 20180108, simplified mechanics for LN zig-zag in-plane bender eigen modes
Simplification: ignore gap between two gold electrodes
Comparison between calculated 1, 3 & 5 unit cell mode frequencies:
- 1 unit cell (MHz): with gap: 1.98, 2.02, 2.36, 2.40; simplified: 1.87, 1.91, 2.31, 2.34
- 3 unit cells (kHz): with gap: 655, 705, 740, 868; simplified: 616, 694, 724, 852
- 5 unit cells (kHz): with gap: 333, 340, 445, 524; simplified: 320, 346, 422, 515
- simplified model frequency accuracy \~ 95%
9-unit-cell (![Image 102](/assets/images/imported/ln-memos-simulations-2018/image102.png)10.8 um, ![Image 103](/assets/images/imported/ln-memos-simulations-2018/image103.png)11 um) modes from simplified model:
- f0 to f3 (kHz): 127, 128, 235, 287
- first four mode profiles the same as in 5-unit-cell case
- f4 = 493 kHz is a higher order mode
Conclusion:
- four types of modes
- roughly ![Image 104](/assets/images/imported/ln-memos-simulations-2018/image104.png)
## 20180110, LN trapezoid WG mode analysis
Parameters: waveguide top width w = 1 um, thickness t = 500 nm, sidewall tilt angle 15 deg
TE mode exist for 500 nm thickness.

![Image 165](/assets/images/imported/ln-memos-simulations-2018/image165.png)

![Image 170](/assets/images/imported/ln-memos-simulations-2018/image170.png)

If t = 250 nm, only one TE mode

![Image 122](/assets/images/imported/ln-memos-simulations-2018/image122.png)

## 20180117, side-wall tilt in-plane bender, single beam generate displacement \~10 nm/V
Idea: evaporate metal directly onto side-wall (if possible)
Advantage:
- no alignment if using the same layer of resist for metal lift-off
- larger effect
- extensible to zig-zag structure without crossover
disadvantage:
- z-cut LN
Using tilt angle ![Image 105](/assets/images/imported/ln-memos-simulations-2018/image105.png)deg
Electrostatic potential and displacement:

![Image 139](/assets/images/imported/ln-memos-simulations-2018/image139.png)

![Image 150](/assets/images/imported/ln-memos-simulations-2018/image150.png)

Displacement will be reduced after taking the stiffness from the metal electrode into consideration, which will be roughly reduced by a factor of 2
## 20180118, trapezoid waveguide taper bands

![Image 133](/assets/images/imported/ln-memos-simulations-2018/image133.png)

![Image 162](/assets/images/imported/ln-memos-simulations-2018/image162.png)

Left: left WG width/total WG width = 0.1 or 0.9; right: left WG width/total WG width = 0.5\
bands and normalized index sensitivity (percent/nm):

![Image 145](/assets/images/imported/ln-memos-simulations-2018/image145.png)

![Image 124](/assets/images/imported/ln-memos-simulations-2018/image124.png)

Results:
- single WG mode transform to symmetric mode (blue), which has high sensitivity in two-mode region
- if used as a directional coupler, ![Image 106](/assets/images/imported/ln-memos-simulations-2018/image106.png)
- if using the symmetric mode for one of the two arms of a MZI
- ![Image 107](/assets/images/imported/ln-memos-simulations-2018/image107.png)
- ![Image 108](/assets/images/imported/ln-memos-simulations-2018/image108.png)
- sensitivity in general \~ 0.01%/nm, limited by gap, gap limited by sidewall tilt
## 20180205, LN zigzag horizontal bender 200 nm LN thickness

![Image 154](/assets/images/imported/ln-memos-simulations-2018/image154.png)

![Image 130](/assets/images/imported/ln-memos-simulations-2018/image130.png)

## 20180223, horizontal gap LNOI WG, bad idea
Model: `COMSOL/LN/optics/model_ewfd_2D_LNOI_gapWG_20180222.mph`

Geometry: Air + LN wedge WG + air slot + SiO2

![Image 117](/assets/images/imported/ln-memos-simulations-2018/image117.png)

## 20180223, simple bender theory verification
Model: `COMSOL/LN/BeamBender/model_LN_piezoElec_testCurvTheory-20180223.mph`

Effect: ![Image 16](/assets/images/imported/ln-memos-simulations-2018/image16.png)
Setup:
- ![Image 109](/assets/images/imported/ln-memos-simulations-2018/image109.png)
- z-cut, apply Ey, vertical bender
- directly set surface potential at ![Image 110](/assets/images/imported/ln-memos-simulations-2018/image110.png) and ![Image 111](/assets/images/imported/ln-memos-simulations-2018/image111.png) to linearly vary from 1 to -1 along z
- Theory (very simplified): ![Image 112](/assets/images/imported/ln-memos-simulations-2018/image112.png)m
Electric potential and displacement:

![Image 158](/assets/images/imported/ln-memos-simulations-2018/image158.png)

![Image 143](/assets/images/imported/ln-memos-simulations-2018/image143.png)

![Image 113](/assets/images/imported/ln-memos-simulations-2018/image113.png), agree with simulation up to 99.5%

If double the thickness, ![Image 114](/assets/images/imported/ln-memos-simulations-2018/image114.png) reduced by half as expected (and quite accurate), despite the a stronger change in mechanical stiffness:
If reduce width to 50%, displacement increased by a factor of 2.

![Image 168](/assets/images/imported/ln-memos-simulations-2018/image168.png)

![Image 141](/assets/images/imported/ln-memos-simulations-2018/image141.png)

## 20180302, horizontal zigzag bendersingle arm GA

![Image 118](/assets/images/imported/ln-memos-simulations-2018/image118.png)

Results:
- d_metal \~ 60 nm
- t_metal \~ 80 nm (should be smaller)
- gap \~ 50 nm
- t_LN \~ 250 nm
- w_metal \~ 56 nm
- displacement: 27 nm (L = 10 um)
- corresponded
- curvature C = 540 m\^-1
- unitcell width w = 2*(2*w_metal + d_metal + gap) \~ 500 nm
- square-shape zigzag endpoint displacement ![Image 115](/assets/images/imported/ln-memos-simulations-2018/image115.png)
## 20180303, horizontal zigzag GA, LN thickness fixed at 300 nm

![Image 137](/assets/images/imported/ln-memos-simulations-2018/image137.png)

Results:
- displacement \~ 27 nm
- all dimension tends to smallest except metal thickness
## 20180303, vertical bender unitcell GA, with two-step etch
LN domain & electric potential:

![Image 181](/assets/images/imported/ln-memos-simulations-2018/image181.png)

![Image 135](/assets/images/imported/ln-memos-simulations-2018/image135.png)

L = 10 um
Displacement \~ 11 nm
## 20180303, vertical bender GA

![Image 140](/assets/images/imported/ln-memos-simulations-2018/image140.png)

Results
-       d_metal: 5.3559e-08
-             t: 9.8672e-08
-       t_metal: 5.1436e-08
-        w_etch: 7.4548e-08
-       w_metal: 6.4642e-08
-          displacement: 77 nm
## 20180606, two single-arm bender + one NB
model : LN\\BeamBender\\model_LN_zigzag_NB_20180606.mph
Suppose to bend towards y, but locked by the bender-NB joint:

![Image 138](/assets/images/imported/ln-memos-simulations-2018/image138.png)

- 1V disp: max(v) = 0.19 nm, max(w) = 0.63 nm
Try to reduce joint cross section
- with 150 nm wide joint:
- ![Image 136](/assets/images/imported/ln-memos-simulations-2018/image136.png)

![Image 153](/assets/images/imported/ln-memos-simulations-2018/image153.png)

- 1V disp: max(v) = 1.75 nm, max(w) = 0.655 nm
- single arm alone, no NB: 1V max(v) = 3.73 nm
Parallel bender-NB-bender:

![Image 173](/assets/images/imported/ln-memos-simulations-2018/image173.png)

- 1V disp: max(v) = 0.93 nm
- increased to 0.97 nm if metal thickness reduced from 200 nm to 100 nm, not critical
## 20180922, sweep LNY in-plane rotation
script: LN/BeamBender/sweep_LN_BeamBender_InPlaneRot.m

![Image 171](/assets/images/imported/ln-memos-simulations-2018/image171.png)

Maximum: 14.7 deg, 165.3 deg (= 180 - 14.7)
The asymmetry wrt. 90 deg should be structural (the zigzag shape breaks the symmetry).
## 20181114, dn/dx for slot ridge waveguide
model: optics/model_ewfd_2D_slotRWG_20181113.mph
Mode profile:

![Image 147](/assets/images/imported/ln-memos-simulations-2018/image147.png)

neff vs gap:

![Image 156](/assets/images/imported/ln-memos-simulations-2018/image156.png)

dn/dx \~ 1.5e-4 / nm

![Image 116](/assets/images/imported/ln-memos-simulations-2018/image116.png)

## 20181115, electrostatic zigzag
Using SOI geometry parameters
Cross section

![Image 169](/assets/images/imported/ln-memos-simulations-2018/image169.png)

Displacement:

![Image 146](/assets/images/imported/ln-memos-simulations-2018/image146.png)

\~ 0.5 nm/V\^2 for L = 10 um
Need cross-over for zig-zag
displacement \~ L\^3.7 (close to uniformly loaded beam)

![Image 179](/assets/images/imported/ln-memos-simulations-2018/image179.png)