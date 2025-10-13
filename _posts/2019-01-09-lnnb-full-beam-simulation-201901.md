---
categories:
- Research
date: '2019-01-09'
header:
  cover: /assets/images/imported/lnnb-full-beam-simulation-201901/image4.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/lnnb-full-beam-simulation-201901/image4.png
  show_overlay_excerpt: false
original_date: '2019-01-09'
tags:
- Lithium Niobate
- Materials
- Simulation
title: Full LNNB simulations
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2019-01-09, converted on 2025-10-12. )

# 20190109. thin AXUC trial
See unitcell sim GD for unitcell design.

Path: `COMSOL/LN/LNNB/20190109_AX_thin`

Parameters:
- P_defect = struct('a', 585e-9, 'w', 1300e-9,'w3',80e-9,\...
-     'amp', 10e-9, 'isFBH',true,'isAX',true,\...
-     'hx', 1895e-9, 'hy', 1004e-9,'thetaN',thetaN, 'thetay',thetay,\...
-     'thetax',thetax,'theta',thetaN,\...
-     'hxN',420e-9,'hyN',2036e-9);
- \% manual mirror from
- \% model_FBUC_piezo_EM_45degLNX_mirror_20181209
- P_mirror = struct('a', 650e-9, 'w', 1300e-9,'w3',80e-9,\...
-     'amp', 10e-9, 'isFBH',true,'isAX',true,\...
-     'hx', 1895e-9, 'hy', 1104e-9,'thetaN',thetaN, 'thetay',thetay,\...
-     'thetax',thetax,'theta',thetaN,\...
-     'hxN',400e-9,'hyN',2036e-9);
Did few updates in build_LNNB_OM
IMPORTANT: cyclic symmetry seems to give the wrong mode profile
- looks like COMSOL treat the cyclic BC more like reflection, not rotation:

![Image 3](/assets/images/imported/lnnb-full-beam-simulation-201901/image3.png)

This does not make sense...Does not agree with what's claimed:

![Image 4](/assets/images/imported/lnnb-full-beam-simulation-201901/image4.png)

I did use copy face for meshing!
this does not make sense!
If simulating the full geom, then it's cyclic symmetric:
- took 55 min, half geom + cyclic sym only took 22 min\...

![Image 5](/assets/images/imported/lnnb-full-beam-simulation-201901/image5.png)

very well confined:

![Image 1](/assets/images/imported/lnnb-full-beam-simulation-201901/image1.png)

However, optics not good enough:
- simulated quality factor \< 50k

![Image 2](/assets/images/imported/lnnb-full-beam-simulation-201901/image2.png)

optics-only model is now working.
# 20190110, LNNB AX optical GA
Path: `COMSOL/LN/LNNB/20190109_AX_thin`

File: `main_LNNB_AX_optics_GA.m`
Started 12:27PM.
Single eval \~ 40 min
Could get Q as high as 700k (within 50 evals)
- but defect cell breathing mode freq too high and crossed with w040