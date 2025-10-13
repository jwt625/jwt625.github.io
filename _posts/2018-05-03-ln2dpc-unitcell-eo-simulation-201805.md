---
categories:
- Research
date: '2018-05-03'
header:
  cover: /assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image48.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image48.png
  show_overlay_excerpt: false
original_date: '2018-05-03'
tags:
- Lithium Niobate
- Materials
- Piezoelectric
- Simulation
title: Lithium niobate 2D photonic crystal unitcell E-O simulations
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2018-05-03, converted on 2025-10-12. )

# Goals
Obtain optical Q due to metal loss
Obtain electro-optic coupling rate
Obtain mechanical loss rate from piezoelectric effect in driven case
# Model setup
Physics:
- ewfd, half the unitcell, floquet boundary
- electrostatic (es), half the unitcell
- piezoelectric, full geom
- including solid mechanics + electrostatic (es2)
- floquet boundary for solid mechanics
- zero charge boundary for electrostatic
## Electro-optic coupling

![Image 1](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image1.png)

![Image 2](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image2.png)

For LN, ![Image 3](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image3.png)

![Image 4](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image4.png)

![Image 5](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image5.png)

![Image 29](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image29.png)

Values:![Image 30](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image30.png)
Derivation and n, k for Al: <https://sandbox.open.wolframcloud.com/app/objects/b16a5678-3f92-412c-a042-0f4d004c5ab9>
## 2D simple slab mechanics
More detail in [WJ - EtchFlip Theory and estimation](https://docs.google.com/document/d/13FAgJA0bsfEBpeMdyAB4H_5aIpuA0Fx4lUMMOTqyrGI/edit?usp=sharing)
#### Dynamics
- ![Image 6](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image6.png)
- ![Image 7](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image7.png), where ![Image 8](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image8.png)
- eigenvalues:![Image 37](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image37.png)
- ![Image 9](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image9.png)
For LN, E \~ 200 GPa, v \~ 0.4, rho = 4700 for simple estimation
- ![Image 10](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image10.png) where t and w in unit \m\
- t = 300 nm, w = 9 um, ![Image 11](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image11.png)MHz
# 20180503, photon bands, first try
Model: `COMSOL/LN/Unitcell2DPC/model_LN2DPC_ewfd_UC_20180503.mph`

Geometry:
sys2:

![Image 32](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image32.png)

DOF = 653692
Single evaluation 7 min 42s, too slow.
Reduce N from 5 to 4, DOF = 480594, still cost 6 min 4 s
Use swept for Si slab, reduced DOF to 290756, does not converge??
Same mesh scheme, coarser, DOF = 225636, 1 min 52 s
Using beamwrite parameter (right: bands of LNNB mirror):

![Image 40](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image40.png)

![Image 18](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image18.png)

Run with N = 5 and solve for 30 eigenvals
- average eval time = 100s
- N = 4 (blue) and N = 5 (red)

![Image 24](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image24.png)

TE even: ![Image 27](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image27.png)
# 20180504, photon bands of all four symmetry
Same model as yesterday, ewfd only.
Selecting highlighted solvals using regional Weav integration
All symmetries: (0: even, 1: odd)

![Image 20](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image20.png)

# 20180504, ewfd + es + piezo, EO coupling first try
Model: `COMSOL/LN/UnitCell2DPC/model_LN2DPC_ewfd+es_UC_20180504_fast.mph`

Metal parameter: ![Image 23](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image23.png), ![Image 36](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image36.png), such that

 ![Image 46](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image46.png) = ![Image 42](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image42.png) from Jeremy's paper

Geometry: Aluminum highlighted

![Image 48](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image48.png)

Solve time: es \~ 30s, ewfd \~ 4 min
Electrostatic: Color: es.Ex

![Image 33](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image33.png)

![Image 17](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image17.png)

ewfd: Q \<\~ 1e5

![Image 21](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image21.png)

## E-O coupling strength:
from eo_expr_LN, for mode above

![Image 12](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image12.png) Hz  \~ 2 GHz

- Emen = ![Image 13](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image13.png)
- 2 GHz is from 1 V on metal and 0 V on x-symmetry plane, i.e., 2 V bias
- ![Image 14](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image14.png) GHz
For 1uV, ![Image 15](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image15.png)
Rough estimate:
- for E \~ 1V/1um, r33 = 32 pm/V
- ![Image 16](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image16.png), upper bond
Try mirror along x and adding mechanics...
## Mechanics using piezoelectric also working
solve time \~ 2 min

![Image 47](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image47.png)^[a](#cmnt1)[b](#cmnt2)^![Image 39](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image39.png)

Frequency: left = 28 MHz, right = 70 MHz.
Simple slab estimation gives ![Image 11](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image11.png)MHz, stiffness weakened by holes.
# 20180505, piezo freq domain with mechanical PML
First of all, frequency domain without PML:
imag(Y11) across one mechanical resonance:

![Image 28](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image28.png) real(Y11) = 0 because lossless.

Adding PML... still maintaining periodicity
- PML factor: (1+i* (x \> x0) * ( ( (x-x0)\^2+y\^2 +(z-z0)\^2 ) \> r_pml\^2 ) * s_pml * (((x-x0)\^2+y\^2 +(z-z0)\^2 ) - r_pml\^2)/c_pml\^2+i* (x \<-x0) * ( ( (x+x0)\^2+y\^2 +(z-z0)\^2 ) \> r_pml\^2 ) * s_pml * (((x+x0)\^2+y\^2 +(z-z0)\^2 ) - r_pml\^2)/c_pml\^2)

![Image 25](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image25.png)

why some solutions don't look like periodic?
- E.g.:
- color: log(solid.disp) ![Image 45](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image45.png)
- found problem: mesh not properly copied
- Now fundamental mode at 26.1 MHz
- ![Image 31](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image31.png)

![Image 19](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image19.png)

Sweeping frequency now.
- Y11, real and imag:
- ![Image 35](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image35.png)

![Image 38](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image38.png)

# 20180505, sweep WG-metal separation, recording Q and g
Script: `COMSOL/LN/UnitCell2DPC/sweep_LN2DPC_geom_scripts.m`

Running, 1:37PM
Dunno when finished, only know it's before 3PM
Looks working: (d_metal in um)
- ![Image 34](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image34.png)

![Image 41](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image41.png)

- selected according to the Q, suspectively for the TM modes
- use frequency to select!
- why some drops? Mode jump when selecting using Q
Finer sweep and save more data & timeStamps
- error encountered
- wrong comsol node name, fixed

![Image 44](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image44.png)

This increasing g doesn't make sense. Probably mode jumped. Luckily all gs are calculated.
Finer sweep:

![Image 43](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image43.png)

![Image 22](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image22.png)

![Image 26](/assets/images/imported/ln2dpc-unitcell-eo-simulation-201805/image26.png)

- this gV going up wrt. d_metal doesn't make sense
Manually try N = 5 & d_metal = 5 um
- f_2V=195e12/2*5.43e-19 /(7.44e-14/2)=1.4e9 Hz , gV = 0.7 GHz
- Q \~ 2.6e7
Manual N = 5, d_meatl = 4.5 um
- f_2V=195e12/2*5.9e-19 /(7.3e-14/2)=1.58e9 Hz , gV = 0.79 GHz
- Q \~ 1.36e7
Manual N = 5, d_metal = 4.25 um
- f_2V=195e12/2*6.53e-19 /(7.57e-14/2)=1.68e9 Hz , gV = 0.85 GHz
- Q \~ 1.77e6
Manual N = 4, d_metal = 4 um
- f_2V=195e12/2*6.18e-19 /(6.84e-14/2)=1.8e9 Hz , gV = 0.9 GHz
- Q \~ 3e5
BUG FIX: rotation for interaction calculation was wrong, but almost only a sign change in interaction strength.
- e.g., for 4.25um d_metal, numerator value changed from 6.5336e-19 to -6.5324e-19.
- UPDATE: old rotation is actually correct.

<!-- Internal comments:
[a] what are the frequencies for this?
[b] 28MHz and 70MHz, will compare to simple estimation soon.
-->