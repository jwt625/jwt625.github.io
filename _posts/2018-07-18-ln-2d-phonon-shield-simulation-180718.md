---
categories:
- Research
date: '2018-07-18'
header:
  cover: /assets/images/imported/ln-2d-phonon-shield-simulation-180718/image8.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/ln-2d-phonon-shield-simulation-180718/image8.png
  show_overlay_excerpt: false
original_date: '2018-07-18'
tags:
- Lithium Niobate
- Materials
- Piezoelectric
- Simulation
title: LN 2D phonon shield simulation
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2018-07-18, converted on 2025-10-12. )

# 20180718, mechanical bands
model : LN/mechanics/model_2DPhononShield_20180718.mph
single eval \~ 15 s

![Image 5](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image5.png)

![Image 20](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image20.png)

- w1: square width
- w2: connection part width
- bandgap: 1.923 GHz \~ 2.13 GHz
script: sweep_MechBands_scripts.m
Calculating w1  =750 nm... bandgap disappeared??

![Image 13](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image13.png)

## 180719, sweep thetas = \0, 5, 10, 15, 20\ deg

![Image 8](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image8.png)

Y cut LN masked by HSQ with hardening:
- sidewall tilt 15 deg \~ 20 deg depending on structure.
- see `fabrication/LNNEMO/SEMs/20180622_LNNB11_postBOE`

This is Z cut, need to redo
# 20190310, redo 2DPS bands on LNX
Path: `COMSOL/LN/mechanics/20190310_2DPS`

Sol time \~ 0.5 min

![Image 6](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image6.png)

Bandgap 1.783 \~ 2.185 GHz:

![Image 3](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image3.png)

Seems like comsol 54 is better at piezoelectrics now, no weird mode away from any band.
Not so good. Trying a wavy design:

![Image 2](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image2.png)

![Image 23](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image23.png)

- 50 nm in                                         30 nm out
Could also do the other way (above right).
Bands:

![Image 21](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image21.png)

![Image 9](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image9.png)

old simple cross-hole one for comparison:

![Image 16](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image16.png)

Give up fancy geom, focus on cross:

![Image 18](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image18.png)

- accidentally overwritten phononBands_2DShield_LNX_wavy_180310.mat.... it's not so good anyway...
This is the best so far:

![Image 14](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image14.png)

![Image 15](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image15.png)

# 20190310, single mode WG first trial
Path: `COMSOL/LN/mechanics/20190310_2DPS`

Geom: ![Image 10](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image10.png)
First trial:

![Image 4](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image4.png)

![Image 7](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image7.png)

WG width doesn't change much about the bands.
Single mode region very small

![Image 1](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image1.png)

![Image 17](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image17.png)

![Image 22](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image22.png)

- data: phononBands_SMWG_LNX_180310.mat
- larger a makes it worse (right, not finished yet (phononBands_SMWG_LNX_180310_a=1000_w=200.mat))
Seems like here not only do we need a bandgap near 2 GHz, but we also need the waveguide at X point to possess a bandgap that has large overlap with the bulk bandgap from the perturbation of attaching it to the half-infinite bulk

![Image 19](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image19.png)

Lamb from X bend down because one of the node move across the tether
Tether at two point: bad idea:

![Image 11](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image11.png)

# 20190311, sweep a for SMWG
Path: `COMSOL/LN/mechanics/20190310_2DPS`

Value of a: linspace(800, 1100, 20)*1e-9
Results:

![Image 12.gif](/assets/images/imported/ln-2d-phonon-shield-simulation-180718/image12.gif)