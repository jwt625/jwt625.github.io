---
categories:
- Tutorial
date: '2018-04-26'
header:
  cover: /assets/images/imported/ln-photonics-literature/image8.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/ln-photonics-literature/image8.png
  show_overlay_excerpt: false
original_date: '2018-04-26'
tags:
- Lithium Niobate
- Materials
title: LN photonics literature
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2018-04-26, converted on 2025-10-12. )

Finesse of Loncar's Monolithic ultra-high-Q lithium niobate microring resonator:
- alpha = 2.7 dB/m
- alpha = 2.7/4.343
- r = 100 um
- L_roundtrip = 2 pi r
- Finesse = 2 pi (1/alpha)/L_rt = 1.6e4
Finesse of a Q \~ 200k nanobeam:
- L_rt = 2*20 um
- T_rt = L_rt/v_g
- kappa = 2 pi 193 THz / 2e5
- Finesse = 2 pi (1/kappa)/T_rt = 3.9e3
# Hanxiao Liang, Qiang Lin, 2017, LN PC 1D, optica
Photonics:
- measured Q \~ 1.09e5
- photorefractive effect \~ 0.64 GHz/aJ, \~ 84 MHz/photon
- simulated Q \~ 6e6, 5.2e5
- photorefraction: \~ 84 MHz/photon
- quenching of photorefraction
Mechanics:
- one mode at 1.003 GHz, Q \~ 1465
- looks like an X point mode
- g_OM \~ 71 kHz
Fabrication:
- sidewalls: 45 deg inside and 75 deg outside:![Image 9](/assets/images/imported/ln-photonics-literature/image9.png)
- 300 nm x-cut on 2 um BOX on Si
- ZEP-520A
- Ar-ion mill
- over-etch to produce fine structure and sidewall smoothness
# D.S. Hines, K.E. Williams, 2002, Patterning of wave guides in LiNbO3 using ion beam etching and reactive ion beam etching

![Image 5](/assets/images/imported/ln-photonics-literature/image5.png)

# Wei C. Jiang, Qiang Lin, 2016, LN disk optomechanics, scientific report
Params:
- mech freq \~ 357 MHz
- m_eff \~ 150 pg
- g_OM \~ 11.6 kHz
Fab:
- Z-cut from NANOLN, 400 nm on 2 um BOX
- \~ 1 um ZEP-520A, bake 170C for 2 min
- JEOL 9500, 300 uC/cm\^2
- ion mill, beam voltage \~ 600 V, etch rate \~ 35 nm/min
# Andrea Guarino, Peter Gunter, 2007, Electro--optically tunablemicroring resonators in lithium niobate, nature
Device looks horrible:

![Image 10](/assets/images/imported/ln-photonics-literature/image10.png)

Parameters:
- R = 100 um
- modulation depth \~ 7 dB
- finesse F \~ 5, Q \~ 4e3, "limited by implantation-induced defects and scattering losses"
- tunability 0.14GHz/V
Fab:
- z-cut LN
- use benzocyclobutene (BCB) to bond sub-micron LN film
# Mian Zhang, Marko Loncar, 2017, Monolithic ultra-high-Q lithium niobate microring resonator, optica

![Image 2](/assets/images/imported/ln-photonics-literature/image2.png)

parameters:
- prop. loss \~ 2.7 dB/m
- Q \~ 1e7
- r = 80 um
- bending loss \~ 9.3 +- 0.9 dB/m
- material intrinsic loss \< 0.\` dB/m
Fab:
- NanoLN, 600 nm X-cut LN on 2 um BOX on Si
- EBL: HSQ with multi-pass
- Ar ion mill tuned to minimize surface redeposition
- 350 nm rib and 250 nm slab
- PECVD clad 1.5 um SiO2
# I. Krasnokutska, A. Peruzzo, 2018, Ultra-low loss photonic circuits in lithium niobate on insulator, optics Express
Results:
- r \~ 80 um, width \~ 1 um
- \~0.4 dB/cm
- sidewall roughness \< 2 nm RMS, sidewall \~ 75 deg
- ![Image 8](/assets/images/imported/ln-photonics-literature/image8.png)
Fab:

![Image 1](/assets/images/imported/ln-photonics-literature/image1.png)

- NanoLN 500 nm Z-cut rib waveguide on 2 um BOX
- EBL:
- eliminate charging: thin 10 nm Cr sputtered prior to spin-coat
- 60 nm Cr e-beam evap, NMP lift-off, thickness optimized for etching process
- CHF3 + Ar, selectivity: metal:LN = 1:7
- PECVD 3 um SiO2 cladding
Things not understand yet:
- "MgO:LNOI, which has 170x higher optical damage threshold than undoped LN"
- what is optical damage?
# Cheng Wang, Marko Loncar, 2017, SHG in nano- structured thin-film LN waveguides, optics Express
Results:
- \~ 3.0 dB/cm
- conversion efficiencies \~ 41% /W/cm\^2
Fab:
- 400 nm X-cut, NanoLN
- 800 nm thick a-Si PECVD
- EBL, RIE Si, then Ar ion LN etch, 80C KOH remove Si
- 3 um PECVD SiO2 cladding

![Image 7](/assets/images/imported/ln-photonics-literature/image7.png)

# Cheng Wang, Marko Loncar, 2014, Integrated high quality factor lithium niobate microdisk resonators, optics express
Results:
- Q \~ 1e5
- SHG efficiency \~ 0.109 /W
- sidewall roughness \< 5 nm RMS
- "Assuming frequency tunability of 0.28 GHz/V and cavity Q \~5 × 10\^4 (common in our devices), as little as 7 V of applied voltage is needed to switch the cavity on- and off-resonance"

![Image 4](/assets/images/imported/ln-photonics-literature/image4.png)

Fab:
- 15 nm Ti deposition prior spin-coat: promote adhesion & conduction during EBL
- HSQ: FOX®-16 by Dow Corning
- "A second blanket electron beam exposure of the resist after development was used to increase the mask hardness, thus enhancing the etching selectivity"
- LN was then dry etched with argon plasma (Ar+) in an electron-cyclotron resonance (ECR) reactive ion etching (RIE) system (NEXX Cirrus 150).
- relatively high RF power (200 W) was used to enable DC bias of \~180 V
- etch rate \~ 30 nm/min, 300 nm of LN could be etched using this approach
- HSQ removal: 2 min 5:1 BOE
# Cheng Wang, Marko Loncar, 2018, Nanophotonic lithium niobate electro-optic modulators, Optics Express

![Image 6](/assets/images/imported/ln-photonics-literature/image6.png)

![Image 3](/assets/images/imported/ln-photonics-literature/image3.png)

                                                        w = 900 nm, h = 400, s = 300, g = 3.5 um
Results:
- EO modulation efficiency 1.8 V cm for MZI
- rate \~ 40 Gbps
- 7 pm/V for micro-ring
- energy confined in LN region is 94%
- extinction ration: 3 dB and 8 dB for racetrack (Q \~ 8000) and MZI
Fab:
- 700 nm X-cut, NanoLN, 2 um BOX
- 800 nm PECVD a-Si hard mask
- HSQ EBL, RIE Si, Ar ion mill at bias \~ 270 V, etch rate \~ 30 nm/min
- LN etch depth \~ 400 nm, 300 nm slab
- Si removal: 30% KOH at 80C
- metal: 15 nm Ti/300 nm Au, e-beam evap, PMMA/MMA lift-off
- 1.5 um PECVD SiO2 cladding
- PMMA masked 5 min BOE, second liftoff for top electrodes
- diced and polished for coupling (5 dB/facet coupling loss)