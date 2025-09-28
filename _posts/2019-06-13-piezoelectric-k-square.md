---
categories:
- Tutorial
import_date: '2025-09-27'
original_date: '2019-06-13'
tags:
- Lithium Niobate
- Materials
- Piezoelectric
- Simulation
- Reference
title: Piezoelectric K square
toc: true
toc_sticky: True
use_math: true
header:
  cover: /assets/images/imported/piezoelectric-k-square-20190613/image2.png
  overlay_image: /assets/images/imported/piezoelectric-k-square-20190613/image2.png
  show_overlay_excerpt: false
  overlay_filter: 0.5
---

( originally written on 2019-06-13, converted on 2025-09-27. )


This document is still messy, in development.
# TL;DR
Berlincourt is only valid for uniform state and static (?). It's different from the Mason model for a resonant mode. It evaluates how "piezoelectric" the mode/field profile is, but not necessarily strongly coupled to the electrodes.
The energy formula from A. F. Ulitko:
- agrees with simple k\^2 for uniform field
- gives same k\^2 as from Mason's model for a resonant mode.
- haven't figured out how to implement in COMSOL
# Definitions
k square for specific uniform and simple modes: k13, k33 etc.
- see e.g. section 4 of 1987 IEEE standard
Berlincourt: ![Image 50](/assets/images/imported/piezoelectric-k-square-20190613/image50.png)
Mason model for a resonant mode: ![Image 56](/assets/images/imported/piezoelectric-k-square-20190613/image56.png)
Energy formula from A. F. Ulitko: ![Image 67](/assets/images/imported/piezoelectric-k-square-20190613/image67.png)
## From Piazza2017

![Image 12](/assets/images/imported/piezoelectric-k-square-20190613/image12.png)

![Image 38](/assets/images/imported/piezoelectric-k-square-20190613/image38.png)

![Image 53](/assets/images/imported/piezoelectric-k-square-20190613/image53.png)

They said Eq. 6 is also approximated and referred to IEEE 1987 standard.
## From modified BVD (IEEE ultrasonic symp. 2000)

![Image 14](/assets/images/imported/piezoelectric-k-square-20190613/image14.png)

![Image 58](/assets/images/imported/piezoelectric-k-square-20190613/image58.png)

![Image 61](/assets/images/imported/piezoelectric-k-square-20190613/image61.png)

![Image 23](/assets/images/imported/piezoelectric-k-square-20190613/image23.png)

r = C0/C1.
## From P. 52 in Hashimoto
v: acoustic velocity

![Image 22](/assets/images/imported/piezoelectric-k-square-20190613/image22.png)

T: stress
S: strain
E: electric field
D: electric displacement
c\^E: stiffness. T = cS for non-piezoelectric material
epsilon\^S: permittivity
Mechanical wave equation:

![Image 46](/assets/images/imported/piezoelectric-k-square-20190613/image46.png)                    ![Image 32](/assets/images/imported/piezoelectric-k-square-20190613/image32.png)

![Image 48](/assets/images/imported/piezoelectric-k-square-20190613/image48.png)

From the constitutive relation

![Image 20](/assets/images/imported/piezoelectric-k-square-20190613/image20.png)

Acoustic velocity with piezoelectricity

![Image 49](/assets/images/imported/piezoelectric-k-square-20190613/image49.png)

![Image 19](/assets/images/imported/piezoelectric-k-square-20190613/image19.png): electromechanical coupling factor.

![Image 21](/assets/images/imported/piezoelectric-k-square-20190613/image21.png)

![Image 62](/assets/images/imported/piezoelectric-k-square-20190613/image62.png): static capacitance.

![Image 35](/assets/images/imported/piezoelectric-k-square-20190613/image35.png)

Definition of quality factor for series and parallel resonances:

![Image 18](/assets/images/imported/piezoelectric-k-square-20190613/image18.png)               ![Image 4](/assets/images/imported/piezoelectric-k-square-20190613/image4.png)

![Image 11](/assets/images/imported/piezoelectric-k-square-20190613/image11.png)

### Berlincourt formula
See Hashimoto P. 63
Internal energy:

![Image 9](/assets/images/imported/piezoelectric-k-square-20190613/image9.png)       ![Image 8](/assets/images/imported/piezoelectric-k-square-20190613/image8.png)

![Image 36](/assets/images/imported/piezoelectric-k-square-20190613/image36.png)         ![Image 30](/assets/images/imported/piezoelectric-k-square-20190613/image30.png)            ![Image 34](/assets/images/imported/piezoelectric-k-square-20190613/image34.png)

- one question: U_m got canceled if I substitute T and D with S and E. What's wrong?
- it's the epsilon, epsilon changed from epsilon\^T to epsilon\^S
- epsilon\^S is larger than epsilon\^T:
- ![Image 37](/assets/images/imported/piezoelectric-k-square-20190613/image37.png)
- Why is U_m written as TdE + EdT, aren't the two the same?
The d in U_m is the piezoelectric tensor.
Constitutive relations:

![Image 47](/assets/images/imported/piezoelectric-k-square-20190613/image47.png)(strain-charge form) or ![Image 22](/assets/images/imported/piezoelectric-k-square-20190613/image22.png) (stress-charge form)

Previous EMC (electromechanical coupling) factor

![Image 10](/assets/images/imported/piezoelectric-k-square-20190613/image10.png)

![Image 3](/assets/images/imported/piezoelectric-k-square-20190613/image3.png)

Or P. 18 in Jaffe:

![Image 7](/assets/images/imported/piezoelectric-k-square-20190613/image7.png)

The appendix A of the book is also useful.
## Appendix A of Jaffe

![Image 27](/assets/images/imported/piezoelectric-k-square-20190613/image27.png)

- f_n: max impedance frequency
- f_m: min impedance frequency
Planar coupling factor k_p:

![Image 39](/assets/images/imported/piezoelectric-k-square-20190613/image39.png)

- sigma\^E: Poisson's ratio (aka cross contraction)
- k_31: transverse coupling factor

![Image 13](/assets/images/imported/piezoelectric-k-square-20190613/image13.png)

- applies to an infinitely thin disk.
- error less than 1% for thickness/diameter \< 0.1
# Eval Berlincourt in COMSOL
path: /user_data/lnsoi/simulation/electromechanics/20190610_LNSOIIDT
First trying COMSOL's global eval for mechanical energies:

![Image 29](/assets/images/imported/piezoelectric-k-square-20190613/image29.png)

- seems weird...
Definitions can be found at COMSOL documentation:

![Image 33](/assets/images/imported/piezoelectric-k-square-20190613/image33.png)

Also what is this???

![Image 6](/assets/images/imported/piezoelectric-k-square-20190613/image6.png)

- further increased epsilon for Al from 10k to 100k:

![Image 54](/assets/images/imported/piezoelectric-k-square-20190613/image54.png)

- how could it be negative?
- Maybe shouldn't simulate the Al in electrostatic
- same weird result...

![Image 15](/assets/images/imported/piezoelectric-k-square-20190613/image15.png)

Tried more equivalent way, more confusing...
- how could it be negative?
- where does the factor of 2 come from?
- from time-averaging (since COMSOL treat it as electrostatic)
- Tested that All components of E and D are real\...

![Image 17](/assets/images/imported/piezoelectric-k-square-20190613/image17.png)

- Is this because that E*D includes T*d*E?
- T*d*E is negative: ![Image 59](/assets/images/imported/piezoelectric-k-square-20190613/image59.png)
## COMSOL energy conventions
EWFD: built a simple Si in Air WG model
- model_54_test_ewfd_20190615.mph

![Image 51](/assets/images/imported/piezoelectric-k-square-20190613/image51.png)

![Image 60](/assets/images/imported/piezoelectric-k-square-20190613/image60.png)

### The previous piezo model
- from model54_piezo_rfl_LNSiWG_IDT_test_integral_20190610.mph
- global eval:

![Image 25](/assets/images/imported/piezoelectric-k-square-20190613/image25.png)

![Image 16](/assets/images/imported/piezoelectric-k-square-20190613/image16.png)

- according to COMSOL doc, Wh_tot is the same as Ws_tot is prestress = 0, and is
- ![Image 68](/assets/images/imported/piezoelectric-k-square-20190613/image68.png)
- integrated mechanical energy

![Image 24](/assets/images/imported/piezoelectric-k-square-20190613/image24.png)

![Image 41](/assets/images/imported/piezoelectric-k-square-20190613/image41.png)

- integrated ES energy

![Image 66](/assets/images/imported/piezoelectric-k-square-20190613/image66.png)

![Image 65](/assets/images/imported/piezoelectric-k-square-20190613/image65.png)

- integrate es.Wav gives the same result as es.Weav
- the actual fields are not static, i.e., going to divide es.intWe by 2
- one question about this es.intWe is that dunno if it includes E*d*T or not\...
- don't know why E * D etc. are not working\...
- piezoelectric mutual energy (E*d*T/2)

![Image 64](/assets/images/imported/piezoelectric-k-square-20190613/image64.png)

![Image 1](/assets/images/imported/piezoelectric-k-square-20190613/image1.png)

### By changing from stress-charge to strain-charge coupling, all above evaluations changed by \~ 2%
Results for 0.1 GHz freq change \< 1%
E * D etc. are still negative...
## COMSOL material properties conventions:

![Image 42](/assets/images/imported/piezoelectric-k-square-20190613/image42.png)

- d and e are both 3 by 6
- Seems like COMSOL's e is much more accurate than d:
- d = {0\C/N\, -2.1e-011\C/N\, -1e-012\C/N\,
- 0\C/N\, 2.1e-011\C/N\, -1e-012\C/N\,
- 0\C/N\, 0\C/N\, 6e-012\C/N\,
- 0\C/N\, 6.8e-011\C/N\, 0\C/N\,
- 6.8e-011\C/N\, 0\C/N\, 0\C/N\,
- -4.2e-011\C/N\, 0\C/N\, 0\C/N\}
- e = {0\C/m\^2\, -2.53764\C/m\^2\, 0.193644\C/m\^2\,
- 0\C/m\^2\, 2.53764\C/m\^2\, 0.193644\C/m\^2\,
- 0\C/m\^2\, 0\C/m\^2\, 1.30863\C/m\^2\,
- 0\C/m\^2\, 3.69548\C/m\^2\, 0\C/m\^2\,
- 3.69594\C/m\^2\, 0\C/m\^2\, 0\C/m\^2\,
- -2.53384\C/m\^2\, 0\C/m\^2\, 0\C/m\^2\}
- epsilonr11 etc. are not used for LN. epsilonrS11 is used instead, and refers to the material coordinate.
- For Si and Al, it's es.epsilonrxx etc. As a result, if plotting epsilonrxx etc., only Si and Al domain have values:
- ![Image 26](/assets/images/imported/piezoelectric-k-square-20190613/image26.png)
- When plotting es.epsilonrS11 etc., only LN domain has value, and correspond to the component in the global system! e.g., epsilonrS22 = 29.16 while epsilonrS11 = epsilonrS33 = 43.6
- WARNING: solid.epsilonrS11 etc. also works for LN domain, but is in local system (solid.epsilonrS33 = 29.16)
- solid.epsilonrXX etc. works for LN, in global system (solid.epsilonrYY = 29.16)
- es.epsilonrYY is the same, LN only, global system.
- ![Image 45](/assets/images/imported/piezoelectric-k-square-20190613/image45.png)
- For strain and stress, pretty sure eXY etc. are in global system and el12 etc. are in material/local system. Although they don't look exactly the same (e.g. between eXY and el23, which is the case in COMSOL 5.0\...)
- for stress, sxy etc. are in the global system, and sl12 etc. are in the material/local system
- I understand why! The global and local coordinate systems are the same for Al and Si, that's why eXY and el23 are different in Al and Si, they should only be the same for LN. Totally make sense. You stupid.
- when scripting, COMSOL's convention for 6x6 symmetric D matrix:
- {D11, D12, D22, D13, D23, D33, ..., D56, D66}
- elasticity:
- cEg11 etc. only support LN, and are in global system (cEg22 = 243 GPa)
- even support cEg21 (unlike D21 etc. is not allowed)
- D11 etc. works for all materials and are in material system (D33 = 243 GPa for LN)
- cE11 etc. only works for LN and are in material system (cE33 = 243 GPz)
- coupling matrix:
- see <https://docs.google.com/document/d/1v15M8Tta7OC2Jg4JfoSGLQ5nPUOMZ4h_vZngcF3KyV8/edit#> for material properties
- eES11 seems like material system (eES22 = 2.54, eES33 = 1.31)
- eESgX1, seems like global system (eESgX1 = 2.54, eESgY2 = 1.31, eESgZ3 = 0)
- although I'm going to use our own rotated d tensor in the global system (cross checked with Raphael)
## Strategy
### v1
Using all components in global system:
For elastic energy:
- strain-stress product. This includes T*d*E!
- convention: real fields are (conj(solid.eXX) + solid.eXX)/2 etc.
- expr = (conj(solid.eXX)*solid.sx+conj(solid.eYY)*solid.sy+conj(solid.eZZ)*solid.sz+2*conj(solid.eYZ)*solid.syz+2*conj(solid.eXZ)*solid.sxz+2*conj(solid.eXY)*solid.sxy)/4
- accurately equal to solid.Wk_tot, roughly equal to solid.Wh_tot
- Manually integrate kinetic energy gives identical result:
- expr = solid.rho*(conj(solid.u_tX)*solid.u_tX+conj(solid.u_tY)*solid.u_tY + conj(solid.u_tZ)*solid.u_tZ)/2/2
- or
- expr = solid.rho*solid.omega\^2*(conj(u)*u+conj(v)*v+conj(w)*w)/2/2
- gives identical results
For electric energy
- E*D, this includes T*d*E!
For mutual energy
- use rotated d tensor
- tested rotated d tensor. See user_data/lnsoi/simulation/electromechanics/20190610_LNSOIIDT/test_d_tensor_script.m
Finally, subtract T*d*E from T*S and D*E, and evaluate k\^2 = Um\^2/Ue/Ud
- DOES NOT WORK, k\^2 seems very wrong
- see test_eval_Berlincourt.m
- got 1.6%, 2.44%, 5.1% for the three frequencies (0.1, 4.7249, 5.2178 GHz)
### v2
Manually evaluate

![Image 36](/assets/images/imported/piezoelectric-k-square-20190613/image36.png)         ![Image 30](/assets/images/imported/piezoelectric-k-square-20190613/image30.png)            ![Image 34](/assets/images/imported/piezoelectric-k-square-20190613/image34.png)

I trust the E*d*T from v1, but I don't know why it's negative or whether it's supposed to be negative...
Solved the model again with strain-charge form.
For Ue,
- using solid.sEg11 (global), LN only, sEg21 etc. allowed
- similar to cEg11 etc.
- for metal + Si, S*T should be fine? Going to check that it agree with T*sE*T, or S*c*S
- confirmed conj(S)*T/4 = conj(S)*c*S/4
- using COMSOL's D_ij for c matrix
- both not equal to rho*conj(v)*v/4 or rho*omega\^2*conj(u)*u/4
- ![Image 63](/assets/images/imported/piezoelectric-k-square-20190613/image63.png)
- Going to just use S*T for non-LN domain mechanics
For Ud,
- using isotropic air and Si
- going to use es.epsilonrxx for both Si and air
- using solid.epsilonrTgXX (global) etc. for LN domain
- solid.epsilonrTgYX etc. are allowed
- generate epsilon manually is much faster and simpler
- Done. See getRotated_epsilonrT_LNXY.m
- need two volint
#### Results
See
- model54_piezo_rfl_LNSiWG_IDT_test_integral_strainCharge_20190615.mph
- and
- test_eval_Berlincourt.m
For comparison,
- U_e + U_m should be equal to S*T
- U_d + U_m should be equal to E*D
- Results:
- E*D match well:![Image 2](/assets/images/imported/piezoelectric-k-square-20190613/image2.png)
- relative mismatch \~ 1e-12
- S*T relative mismatch: \~1 for 0.8 GHz, 0.01% for 4.72 GHz and 3.1% for 5.2 GHz
k square:
- got very close results to v1...
- ![Image 57](/assets/images/imported/piezoelectric-k-square-20190613/image57.png)
- not sure for the first column (0.8 MHz)
### Old:
For LN domain:
- elasticity:
- stiffness: cEg11 etc. from COMSOL
- strain: eXY
- piezoelectric constitutive
- using rotated d from Wolfram + MATLAB
For isotropic material (Si + Al)
- elasticity:
- stress: sx, sxy, \...
- compliance from E and v (see below)
- or just use strain and stress
- or use kinetic energy
# Using different electrostatic boundary condition in COMSOL
20190620
Using floating potential and connect to an external resistor. Trying 1 M Ohm and 0 Ohm.
Eigen mode simulation
- 1 M Ohm: bandgap edge modes: 4.7312 GHz and 5.2164 GHz
- 0 Ohm: no difference\...
Now trying to apply a prescribed disp and do FD sim.
# 20190903, update on ES boundary condition
See also <https://docs.google.com/document/d/1po74C6RYo9cgR3MS6ebrOZZBP_NZEOO7nmalX2lCs0c/edit?usp=sharing>
It turns out that for eigen mode simulation in COMSOL
- voltage type terminal -\> short circuit
- charge type terminal -\> open circuit
Now we could try the energy formula EMCC:

![Image 43](/assets/images/imported/piezoelectric-k-square-20190613/image43.png)

![Image 31](/assets/images/imported/piezoelectric-k-square-20190613/image31.png)

However, for eigen mode simulation, the absolute energy does not make sense.
# Elasticity of isotropic material
From Ding H., Chen W.
Shear modulus: ![Image 28](/assets/images/imported/piezoelectric-k-square-20190613/image28.png)
Elastic stiffness and compliance:

![Image 55](/assets/images/imported/piezoelectric-k-square-20190613/image55.png)

![Image 5](/assets/images/imported/piezoelectric-k-square-20190613/image5.png)

The above agree with [wikipedia](https://en.wikipedia.org/wiki/Poisson%27s_ratio#Isotropic_materials):

![Image 40](/assets/images/imported/piezoelectric-k-square-20190613/image40.png)

and also this:
- from <http://web.mit.edu/16.20/homepage/3_Constitutive/Constitutive_files/module_3_with_solutions.pdf>

![Image 52](/assets/images/imported/piezoelectric-k-square-20190613/image52.png)

From Auld vol. 1 P. 363:

![Image 44](/assets/images/imported/piezoelectric-k-square-20190613/image44.png)

# Reference
\Ken-Ya_Hashimoto\\_Rf_Bulk_Acoustic_Wave_Filters_for communication
Bernard Jaffe - Piezoelectric-Ceramics
\Ding_H.,\_Chen_W.,\_Zhang_L.\\_Elasticity_of_Transversely Isotropic Materials
\B_A_Auld\\_Acoustic_fields_and_waves_in_solids
D. A. Berlincourt, D. R. Curran, and H. Jaffe, \"Piezoelectric and piezomagnetic materials and their function in transducers,\" in: Physical Acoustics (edited by W. P. Mason), Vol. i, Part A, Academic Press (1964).
Chang, S. H., N. N. Rogacheva, and C. C. Chou. \"Analysis of methods for determining electromechanical coupling coefficients of piezoelectric elements.\" IEEE transactions on ultrasonics, ferroelectrics, and frequency control 42.4 (1995): 630-640.
W. P. Mason, Piezoelectric Crystals and Their Applications to Ultrasonics, Van Nostrand Reinhold.
- I can't find it
# TODO
Read A. F. Ulitko, theory of electromechanical energy conversion in nonuniformly deformable piezoceramics.
Read about Mason model