---
categories:
- Tutorial
date: '2020-01-28'
header:
  cover: /assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image77.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image77.png
  show_overlay_excerpt: false
original_date: '2020-01-28'
tags:
- Piezoelectric
- Simulation
- Reference
title: Estimating a nanomech resonator with a JJ or tuning it with a SQUID
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2020-01-28, converted on 2025-10-12. )

# parameters
Mechanical mode
- resonance \~ 2 GHz and antiresonance \~ 2.1 GHz
- going to simulate C_g using COMSOL FD for low freq
- I remember doing this a while ago...
- likely the LiSa IDT sim
- Using
- Path: `COMSOL/LN/mechanics/20190222_fromPato_NMR`
- Model: `COMSOL_FR_and_EF_LNY_300nm_lowerFreq_20190222.mph`
- Results (5 min):
- fs = \1e3:1e3:5e3\';
- imagYs = \2.3425E-12
- 4.6851E-12
- 7.0276E-12
- 9.3701E-12
- 1.1713E-11\;
- %%
- imagYs./fs
- C_g = 2.3425 fF
- Going to solve C_m and L_m from the two frequencies and C_g
- L_m \~ 300 nH
- is this too big?
- C_m \~ 19 fF \~ 20 fF
Junction:
- From: Estimating a nanomech resonator with a JJ (PRL, 2012)
- C_J \~ 5 fF
- L_J \~ 7 nH
- ![Image 63](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image63.png)
- ![Image 52](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image52.png) (Bourassa et al)
- Equivalently
- ![Image 8](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image8.png)
- ![Image 22](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image22.png)  (Nigg et al)
- E_J \~ 23 GHz
- With C_J \~ 5 fF, E_C \~ 4 GHz
- ![Image 25](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image25.png)\~ 27 GHz
Estimate chi just using

![Image 66](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image66.png)

L_p \~ L_m, C_p \~ C_m.
E_c \~ 150 MHz.
Get chi \> 1 GHz, must be wrong.
Trying Foster synthesis with Pato's code:
- msg =
-     'Mode 1:
-      f = 1.9998 GHz
-      C = 456.2669 fF
-      L = 13.8819 nH
-      Z = 174.4273 Ohm'
- msg =
-     'Mode 2:
-      f = 22.6011 GHz
-      C = 7.0653 fF
-      L = 7.0186 nH
-      Z = 996.6877 Ohm'
Using C and L from mode 1 would get chi = -3 MHz. Very small.
Is this correct?
- y_fit does not match around 2 GHz
- also this is using E_C = 150 MHz which is from a transmon. It is not the case here.
Maybe worth trying on a WG?
# 20200129, analytic Foster synthesis
Same path and script.
Need to type the derivation.
Frequencies are the same.
The result is
- C1 = 3.128 nF
- L1 = 2.025 pH
- Z1 = 0.0254 Ohm
- this Z1 is very weird
- Z_m from the equiv circuit for the mech mode is 3961 Ohm, much higher
- C2 = 7.085 fF
- L2 = 6.998 nH
- Z2 = 993.85 Ohm
Synthesized Z matches with direct calculated Z:

![Image 20](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image20.png)

However, if we choose the node on the other side of the coupling capacitance, are the results still the same?
- this is equivalent to exchanging C_J \-\-- C_m, and L_J \-\-- L_m
- Going to check tomorrow
- but the junction is only connected to one side
# 20200130, COMSOL external circuit
Motivation:
- if comsol gives different mech eigen freq for different electric BC, it should be real?
- ![Image 42](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image42.png)
- This means we might be able to tune the mech mode freq by tuning the BC

Path: `COMSOL/LN/mechanics/20200130_testPiezoEigen_addExtCircuit`

Connecting the ground and terminals to an external circuit:

![Image 45](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image45.png)

![Image 37](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image37.png)

## Using L1 = 5 nH
- get following errors:
-  - Feature: Eigenvalue Solver 1 (sol1/e1)
- Singular matrix.
-  - Detail: There are 1 void equations (empty rows in matrix) for the variable comp1.cir.L1_self_mflux_didt.
-  at coordinates:  (0,0,0), \...
- There are 1 void equations (empty rows in matrix) for the variable comp1.es.term1.Q0_ode.
-  at coordinates:  (0,0,0), \...
- There are 1 degrees of freedom that do not occur in any equation (empty columns in matrix) for the variable comp1.cir.L1_i.
-  at coordinates:  (0,0,0), ...
- fixed. Wrong selection in External I-Terminal 1 settings
- sol time 3 min
- Needed to solve around 2 GHz, and a lot of fake modes appeared
Seems to work, get 2.145 GHz for L = 0 nH, the short-circuit frequency.
Now trying 10 nH, no change. 1000 nH, no change.
Changed to w_o for L = 1e14 H, unphysical, but do get open-circuit mode:

![Image 71](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image71.png)

Trying 1 H, likely too small.
- getting large imag freq (1% of the real part), suspicious
## Trying adding capacitor.
- 0.1 fF, same imag freq issue:
- ![Image 40](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image40.png)

![Image 29](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image29.png)

100 fF: Much better and looks like short-circuited:
- the terminal is not exactly 0 V, make sense

![Image 74](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image74.png)

5 fF
- seems to be working

![Image 13](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image13.png)

![Image 17](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image17.png)

1 fF:

![Image 76](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image76.png)

## Going to exclude the metal from the ES sim
### Still giving bullshit results:

![Image 56](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image56.png)

Further changed expr so that the last column should be i*freq:

![Image 16](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image16.png)

- but they are not
# Prediction from the equivalent circuit?
### Adding L
The new freq is given by solving
- k s\^4 + (k w_o\^2 + 1) s\^2 + w_s\^2 = 0
where
- s = i*w
- k = C_m * C_g * L / ( C_m + C_g ), has the unit of 1/w\^2
- w_s and w_o are the short and open circuit eigen frequency
For example, when L = inf, k = inf, w = w_o
Should absorb w_o\^2 into k. Denote k*w_o\^2 as k' and s/w_o as s'.
- C_m*C_g/(C_m+C_g) \~ fF
- need k' \~ 1, i.e., 1/sqrt(C_g*L) \~ w_o
- L \~ 1/C_g/w_o\^2 \~ 2.4 uH
Solving omega:

![Image 24](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image24.png)

![Image 49](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image49.png)

- using old omega_o and omega_s
Approaches omega_o for large k', expected. But why does it go up for small k?

![Image 70](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image70.png)

![Image 30](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image30.png)

From the equiv circuit model, the short and open circuit resonances are not topologically connected by an inductor!
What would happen in COMSOL?
The polarization for the inductor was wrong!!
- Is it a negative inductance then?
### Adding C
- Similarly,
- w = sqrt( (w_s\^2 + k w_o\^2) / (1+k) )
- k = C_m * C_g / ( C_m + C_g ) / C
- k \~ 1 for C \~ C_g \~ 2 fF
- C = 0, k = inf, w = w_o
- C = inf, k = 0, w -\> w_s

![Image 15](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image15.png)

- using old omega_o and omega_s
- what's the order of mag for stray capacitance?
Check Z, agree with above:

![Image 35](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image35.png)

- plotted for C = \1e-15, 2e-15, 5e-15, 10e-15, 20e-15, 50e-15, 100e-15\
## Checking the same circuit in COMSOL
Path: `COMSOL/circuits/20200130_test`

Model: `model54_circuit_add_L_to_mech_20200130.mph`
Added a 2 uH inductor to the mech resonator.
### Voltage drive.
Impedance in dB:

![Image 60](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image60.png)

- which shows the lowered resonant freq
However, the voltage drop across the mech resonator C1 and the coupling C2 is:

![Image 62](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image62.png)

- C1_v is also the voltage ratio between across L1 and across L2
- i.e., most voltage drop is across L2
Similar for current:

![Image 78](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image78.png)

### Current drive

![Image 28](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image28.png)

The \~ 1.85 GHz resonance is now visible.

![Image 61](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image61.png)

Voltage ratio:

![Image 80](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image80.png)

# COMSOL external circuit continued
From COMSOL help on ES sim TERMINAL node:

![Image 46](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image46.png)

Tried, solution makes sense now.
Going to sweep finer freq and compare with the COMSOL circuit model results.
### 20200131, V drive, L = 1 uH
Admittance:

![Image 64](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image64.png)

Displacement:

![Image 27](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image27.png)

- sol time 5 h
Identical to without the inductor. Make sense.
The displacement would also be identical.
### Current drive, L = 1 uH
Remember to change the source from DC to AC.
Does not work. Is it because the es - Terminal and cir - External I-Terminal is taking V from the cir module and put onto the es module, and integrate I from es and feed back to cir. A current source directly connected to the Terminal means V = 0 and thus no motion?
This is awkward, the voltage drive is effectively ignoring the external circuit, and the current drive is not applicable.
Going to try splitting the external L into two L/2 and drive at the center of them.
- still get nothing (zero mech field) with current drive. Why?
- Ohhhhhh, they (disp, V, etc.) are now purely imaginary!
- going to merge the two L
- works, everything for the mech and es is imag
- so sad, I overwrote the 0.5 h freq sweep solutions...
 Sweep done, peak seems different. Going to do twice finer sweep.
- solid.disp is giving zero, but u*conj(u) is not. DO NOT use solid.disp
- sol time 53 min for f = range(1900000000,5000000,2.5e9)
I, V and Y of the nanomech electrodes:

![Image 43](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image43.png)

From equivalent circuit:

![Image 11](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image11.png)

Path: `COMSOL/circuits/20200131_mech_res_equiv`

Model: `model54_circuit_add_L_to_mech_current_drive_20200131.mph`

- showing a different shift
- why???
- C_g is wrong. See the "cross-check" section
Displacement:

![Image 18](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image18.png)

Looks different! Frequency is lower, and max admittance \-\-- max disp
Energies:

![Image 33](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image33.png)

### Force drive, L = 1 uH
Using two Edge Load to squeeze inward:

![Image 69](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image69.png)

![Image 41](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image41.png)

Displacement:

![Image 75](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image75.png)

Terminal properties:

![Image 23](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image23.png)

### Current drive, L = 10 uH

![Image 7](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image7.png)

![Image 50](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image50.png)

Energies in the mech resonator and in the circuit L.

![Image 72](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image72.png)

- very interesting and make sense
- the small mech mode slightly lower than 2.1 GHz is almost not shifted but still excited by the circuit
- Does this agree with the full-circuit mode?
### Force drive, 10 uH

![Image 21](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image21.png)

Displacement:

![Image 51](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image51.png)

Energies:

![Image 38](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image38.png)

## How to interpret the difference between the voltage drive and current drive?
In reality, the whole circuit would be
- mechanically probed?
- capacitively coupled and electrically probed?
### Trying mechanical drive
Working. Almost get confused again because I modified it from the current driven model and the results are plotting imag part and are thus all zero.
Doing fine sweep now. Done. See above.
# 20200130, Marek quantization for two coupled resonator
Read the appendix C of Marek's thesis
- <https://www.research-collection.ethz.ch/handle/20.500.11850/155858>
Seems like the analytic expr is too cumbersome.
Only easy when the two modes are identical.
# 20200131, Coupling to on-resonant LC
Same path.
Model: model54_testPiezo_eigenmode_extLC_FD_curr_drive_20200131.mph
Targeting at the short-circuit resonance freq 2.145 GHz.
Using Z = 300 Ohms
Get
- C = 247.33 fF
- L = 22.26 nH
Seems to work. Going to do finer sweep during dinner.
I, V and Y on the mechanical node
- V is also the same as Z of the node since this is under a current drive towards that node.

![Image 3](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image3.png)

- looks beautiful
Displacement:

![Image 34](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image34.png)

Energies:

![Image 2](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image2.png)

- why are they not identical at the two super-modes??
- Perfect match after dividing the circuit E expression by 4, likely due to the comsol convention that the actual field is ( I + conj(I) )/2 etc.

![Image 39](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image39.png)

![Image 36](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image36.png)

- is the splitting 2g?
- estimated g/2pi = 19.6 MHz
- using ![Image 79](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image79.png)
- what is the condition of this expr?
- From the graph, 2*g /2pi is slightly smaller than 40 MHz, perfect match.
- Also these peaks matches with peaks in Z
## 20200202, Disp/V for the mech part
Path: `COMSOL/LN/mechanics/20200130_testPiezoEigen_addExtCircuit`

Y solely describes the electrical response of the piezoelectric solidmech.
A similar factor could be defined for displacement, since it is in-phase with voltage, let us define Y_mech = max(disp)/V
- Y is probably not a good symbol for this
- calling it X?
The below data is extracted from the extra parallel LC model.

![Image 26](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image26.png)

- sweep_FD_maxDisp_I_V_20200202.mat
- main_20200202.m
- Note that these are plotted with the matlab db function, hence with an extra factor of 2 compared to the manual 10*log10 plots in comsol
- The piezoelectric solidmech properties are not affected by the external circuit.
### Relating X_mech (= disp/V) to OM coupling
Given X_mech, we could directly obtain
- d omega / d V = g0 / x_zp * X_mech
# 20200201, cross-check between piezomech + circuit and equiv-circuit + circuit
For short, calling piezomech + circuit sim as solid-cir sim.

Path: `matlab/20200128_mech_res_plus_JJ`

Script: `main_20200131.m`
Y - f does not match with simulation???

![Image 1](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image1.png)

- blue: COMSOL piezomech only
- red: parallel LC
- yellow: BvD
parallel LC matches with BvD.
Is it because C_lowFreq is off?
Going to try different low freq capacitance.
Using 0.4 fF instead of 2.2 fF as simulated from COMSOL at 1 \~ 5 kHz
- you stupid, you forgot to divide 2pi when calculating this C_lowFreq

![Image 65](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image65.png)

## Comparing adding L
Equiv circuit only models at

Path: `COMSOL/circuits/20200131_mech_res_equiv`

Model: `model54_circuit_add_L_to_mech_current_drive_20200201.mph`
- sol time 1s
### L = 1 uH
From above solid-cir sim:

![Image 43](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image43.png)

Cir only:

![Image 12](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image12.png)

### L = 10 uH

![Image 7](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image7.png)

![Image 9](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image9.png)

Resonant freq off by more, likely because of the equiv model is not as accurate.
Redo the above with the correct C_g:

![Image 5](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image5.png)

## Resonant coupling to parallel LC
solid-cir result from above:

![Image 3](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image3.png)

- green: total impedance at the port
- red: admittance of the piezoelectric mechanical model
equiv-cir:

![Image 59](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image59.png)

- Node 1 is inside the solid mech mode. L1 and C1 are L_m and C_m
- C2 is C_g
- C3 and L2 are the on-resonant external parallel LC
- question remaining: in the cir model, the left LC and right LC have different parallel resonant frequency
### Energies:
solid-cir:

![Image 36](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image36.png)

- note: these solid-cir results are still using the manual C_g = 0.4 fF
- more accurate C_g = 0.352 fF
equiv-cir:
Left LC and "mechanics" (C_g + right LC)

![Image 31](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image31.png)

All elements:

![Image 53](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image53.png)

![Image 58](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image58.png)

- energies in left L and left C match better with each other
- why?
- also why energies in left L and C are both zero at the bare frequency?
- this is also observed in the solid-cir simulation result
- is this because the current drive is on the left node?
- going to change it to the right node
- ![Image 47](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image47.png)
- Yes. it is exchanged. Make sense, this is the only thing that breaks the symmetry.
- At left LC's original parallel resonance, Y = 0.
- right LC's parallel resonance is \~ 2.4 GHz, different
# 20200204, coupling two mech resonator electrically
Path: `COMSOL/LN/mechanics/20200204_electrically_coupled_PNC`

Using two identical NMR, tried current drive at the center node, hence could only drive the symmetric mode.
Force drive on one of them:

![Image 67](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image67.png)

Seems like it passed a zero point between the two modes.
- A pi phase jump happened at 1.9475 GHz
- but no jump at 1.7325 GHz
- what are these two frequencies?
I, V and Y:

![Image 6](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image6.png)

![Image 19](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image19.png)

- suspicious
- Y on the two ES terminals no longer match with the single NMR case.
- likely because of the force drive. In previous sim with force drive, the Y curve is also different.
- why?
Going to add parasitic inductance between them and drive electrically (current).
- nay, complicated and arbitrary
## Equiv circuit
Path: `COMSOL/circuits/20200131_mech_res_equiv`

Model: `model54_circuit_two_coupled_mech_current_drive_20200204.mph`

![Image 32](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image32.png)

Current drive, equivalently "internal" of one mech mode.

![Image 68](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image68.png)

![Image 44](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image44.png)

Resonant freqs as expected.

![Image 55](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image55.png)

What's wrong with the mech drive?
Need to test just a single simple model, maybe with a large resistor in the circuit.
- the external circuit also constraints the I=V relationship
Log disp from just one NMR:
- model54_testPiezo_eigenmode_single_FD_force_drive_20200204.mph

![Image 14](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image14.png)

- Why? force drive is softening the mode?
- Going to do finer sweep
Finer freq:

![Image 4](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image4.png)

![Image 54](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image54.png)

![Image 73](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image73.png)

Around 1.95 GHz:
Plotting imag deformation: ![Image 10](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image10.png)
Real deformation: ![Image 77](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image77.png)
Why?
Around 1.73 GHz:
imag: ![Image 57](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image57.png)
real: ![Image 48](/assets/images/imported/estimating-a-nanomech-resonator-with-a-jj-or-tuning-it-by-bc/image48.png)
I don't get this. Force and displacement should have either 0 of pi phase difference?
- is the 1e12 Ohm resistance doing anything?