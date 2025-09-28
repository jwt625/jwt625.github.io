---
categories:
- Tutorial
date: '2025-09-27'
original_date: '2019-09-03'
tags:
- Piezoelectric
- Simulation
title: Piezoelectric eigen mode sim with different ES boundary on metal
toc: true
toc_sticky: True
use_math: true
header:
  cover: /assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image2.png
  overlay_image: /assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image2.png
  show_overlay_excerpt: false
  overlay_filter: 0.5
---

( originally written on 2019-09-03, converted on 2025-09-27. )


# Pato's nanomech resonator model
Path: /user_data/wtjiang/COMSOL/LN/mechanics/20190222_fromPato_NMR
model: COMSOL_FR_and_EF_LNY_300nm_lowerFreq_20190222.mph

![Image 15](/assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image15.png)

![Image 1](/assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image1.png)

- V = 0 on both electrodes
Metal is NOT included in the ES sim and hence related property not used:

![Image 12](/assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image12.png)

![Image 11](/assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image11.png)

# Test toy model
Path: /user_data/wtjiang/COMSOL/LN/mechanics/20190903_testPiezoEigen
The toy model is just  a 1 um * 1 um * 300 nm Y-cut floating LN block with two metal stripes, surrounded by an r = 1.5 um air ball:

![Image 6](/assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image6.png)

Using manual metal electrostatic property:

![Image 16](/assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image16.png)

- high relative permittivity -\> E \~ 0
- this is not necessary, you could also exclude the metal from the ES sim and select all corresponding metal surfaces when setting the ground/terminal boundary condition
## Floating metal (voltage terminal and ground not added):

![Image 3](/assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image3.png)

![Image 4](/assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image4.png)

Sol time 24 s.
## Terminal and ground added
Voltage terminal with V = 1:

![Image 8](/assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image8.png)

![Image 2](/assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image2.png)

- V = 0 in eigen mode solution, even 1 is specified.
- Eigen frequency lower than floating/open electrode boundary condition.
If the terminal is set to Charge type with Q_0 = 0 C:

![Image 9](/assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image9.png)

![Image 13](/assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image13.png)

Both mode profile and frequency agree with floating metal!
## Freq domain sweep
Single freq sol time 11 s.
Running 2e9:1e6:3e9, going to take \~ 2.8 h.

![Image 5](/assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image5.png)

Comparing the frequency:

![Image 10](/assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image10.png)

k\^2 can be evaluated by two eigen mode simulations

![Image 7](/assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image7.png)

In the above case, k\^2 = 20.7%
## Conclusion
The eigen mode sim with terminal and ground boundary condition on the metal make sense.

![Image 14](/assets/images/imported/piezoelectric-eigen-mode-sim-with-different-es-boundary-on-metal/image14.png)

For voltage type terminal, the voltage setpoint is ignored by COMSOL. The terminal and ground are treated as shorted. In the parallel LC model for the mechanical resonance with a series coupling capacitor (as in Pato's PRA paper), the eigen mode frequency is the lower one (resonance, Z = 0, between L1 and C0 + C1) and corresponds to infinite |Y|
For charge type terminal, the terminal and ground are treated as open. The eigen mode frequency is higher and is the anti-resonance (Y = 0, between L1 and C1). This is the mode that the qubit/MW resonator is coupled to. The simulated voltage between the electrodes should correspond to the voltage across the whole circuit, which is equal to the voltage across L1 and C1 at anti-resonance (?).