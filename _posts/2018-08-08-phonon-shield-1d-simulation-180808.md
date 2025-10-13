---
categories:
- Research
date: '2018-08-08'
header:
  cover: /assets/images/imported/phonon-shield-1d-simulation-180808/image8.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/phonon-shield-1d-simulation-180808/image8.png
  show_overlay_excerpt: false
original_date: '2018-08-08'
tags:
- Lithium Niobate
- Materials
- Simulation
title: Phonon shield 1D simulation
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2018-08-08, converted on 2025-10-12. )

# Trying different w1x and w1y, 20180808
model: model_1DPhononShield_20180808.mph

![Image 8](/assets/images/imported/phonon-shield-1d-simulation-180808/image8.png)

![Image 4](/assets/images/imported/phonon-shield-1d-simulation-180808/image4.png)

Resulting bandgap: 1.442 GHz \~ 2.206 GHz
Geometry sweep:
- red background: bands of default parameters shown above
- fname = 'phononBands_1DShield_sweepGeom_180808';
- \~ 6 min per geom

![Image 5](/assets/images/imported/phonon-shield-1d-simulation-180808/image5.png)

Going to use the left most parameters.
Wait, run again with larger theta (19 deg) for w2 (thin) part
- now green is the old data above and blue is the new results with larger sidewall at the tether

![Image 9](/assets/images/imported/phonon-shield-1d-simulation-180808/image9.png)

trying w2 = 75, w1x = 600, looks similar:

![Image 7](/assets/images/imported/phonon-shield-1d-simulation-180808/image7.png)

# 20181025, same geom with 100 nm Al
Model: mechanics/model_1DPhononShield_withMetal_20181025.mph
For w1x = 600, w1y = 650, w2 = 50:

![Image 6](/assets/images/imported/phonon-shield-1d-simulation-180808/image6.png)

Conclusion:
- seems fine in general
- bandgap slightly smaller
# 20181205, same geom with metal for 135 deg LNX
Correction: w1x is 700

![Image 3](/assets/images/imported/phonon-shield-1d-simulation-180808/image3.png)

# 20190225, LNX, Z transverse
file: wtjiang/COMSOL/LN/mechanics/20181205_1DPS_135LNX/model_1DPhononShield_LNX0deg_20190225.mph

![Image 1](/assets/images/imported/phonon-shield-1d-simulation-180808/image1.png)

![Image 10](/assets/images/imported/phonon-shield-1d-simulation-180808/image10.png)

only solved Gamma point
Bandgap: 1.5067 GHz \~ 2.2085 GHz
Update 20190325:
- with w1x = w1y = 650 nm, BG = 1.598 GHz \~ 2.32 GHz
# 20201108, recalc bands of LNX 1DPS
COMSOL/LN/mechanics/20201108_LNX_1DPS
Using the 20190325 model mentioned above.

![Image 2](/assets/images/imported/phonon-shield-1d-simulation-180808/image2.png)

Okay the old numbers are real.