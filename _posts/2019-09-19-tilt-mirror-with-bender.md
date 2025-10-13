---
categories:
- Research
date: '2019-09-19'
header:
  cover: /assets/images/imported/20190919-tilt-mirror-with-bender/image8.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/20190919-tilt-mirror-with-bender/image8.png
  show_overlay_excerpt: false
original_date: '2019-09-19'
tags:
- Simulation
title: Tilt Mirror
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2019-09-19, converted on 2025-10-12. )

Use Z-cut LN to generate vertical displacement and tilt a mirror.
# 20190919, first trial
Path: `COMSOL/LN/BeamBender/20190919_TiltMirror`

Model: `model54_piezo_tiltMirror_20190919.mph`
Simplest naive model, no geom trick:

![Image 16](/assets/images/imported/20190919-tilt-mirror-with-bender/image16.png)

- DOF = 278 k
- 40 s sol time
- 10 um by 10 um plate
\~ 4 nm vertical disp for 10 um bender, as expected. The nice thing is that the tangential of the plate matches with both bender, thus no elastic loading.
- tilt angle \~ arctan(8 nm/ 10 um) \~ 1e-3 rad \~ 0.057 deg...
- too small
- 20 V -\> \~ 1 deg, too small
Since the bender displacement propto L\^2, angle propto disp/L hence propto L
## Geometric trick
Going to reduce the bender anchor point separation on the plate.
model54_piezo_tiltMirror_GeomTrick_20190919.mph

![Image 6](/assets/images/imported/20190919-tilt-mirror-with-bender/image6.png)

Hmm, the axis also moved. Only a minor improvement.
But this means that the direction of the tilt is engineerable.
No, this is because the min separation is still \~ L

![Image 11](/assets/images/imported/20190919-tilt-mirror-with-bender/image11.png)

- Bender L = 20 um, max disp \~ 11 nm

![Image 15](/assets/images/imported/20190919-tilt-mirror-with-bender/image15.png)

![Image 1](/assets/images/imported/20190919-tilt-mirror-with-bender/image1.png)

- L = 40 um, max disp 14 nm, increasing very slowly.
- the bender is getting weak
## Trying to fix the rotation axis, does not help:

![Image 4](/assets/images/imported/20190919-tilt-mirror-with-bender/image4.png)

Because the tangential * (anchor separation) does not match the expected bender displacement.
Holy shit! a zigzag could do this tangential conversion! Magic!
We just want a twist/angle, not a displacement!
## Look back to zigzag model, but now for Z-cut.

![Image 3](/assets/images/imported/20190919-tilt-mirror-with-bender/image3.png)

![Image 14](/assets/images/imported/20190919-tilt-mirror-with-bender/image14.png)

- model54_LN_slabUnitcell_vertiBend_zigzag_20190919.mph
- sol time 2.5 min
- LN thickness is 500 nm! Will be larger for thickness 300 nm
- electrodes are also gold, going to change to Al
The displacement is small, but the twist accumulates. The twist is exactly what we need!
- the tangential is \~ 2*bender end disp/L, and linearly grow with \# of benders.
- E.g. in the above sim, single bender theta \~ 4 nm/ 10 um, total theta \~ 16 nm/10 um
- Single bender theta grows linearly with L
- Total theta grows linearly with total L.
- To get \~ 1 rad / V, means we need \~ 200 * 10 um \~ 2 mm total length...
- 100 um might be possible, then it's
- 10 * 10 um bender
-  \~ 0.23 deg / V
- 30 * 30 um bender -\> \~ 2 deg / V
## Comparison to DMD
DMD needs \~ 24 V for switching +- 12 deg:
Pixel size \~ 12 um
Switch time \~ 20 us
numbers from
-  <https://www.youtube.com/watch?v=N4aUU3-PKQ4>
- <https://www.spiedigitallibrary.org/conference-proceedings-of-spie/4985/0000/Emerging-digital-micromirror-device-DMD-applications/10.1117/12.480761.full>
- <https://www.jku.at/fileadmin/gruppen/204/Dateien/Lehre/Mikrosystemtechnik/5.2.pdf>
- <https://ieeexplore.ieee.org/abstract/document/704274>
- they could also do grey scale using time-domain duty cycle
## TODO:
add the second zigzag and the mirror plate
# 20190920, full Z-cut zigzag + mirror
same dir.
model54_LN_vertiBend_zigzag_mirror_20190920.mph

![Image 13](/assets/images/imported/20190919-tilt-mirror-with-bender/image13.png)

- DOF = 2718 k
- sol time 9 min

![Image 5](/assets/images/imported/20190919-tilt-mirror-with-bender/image5.png)

Hmm not as expected. Is the wiring correct?
- ![Image 8](/assets/images/imported/20190919-tilt-mirror-with-bender/image8.png)
- no, wrong! The field is mirrored, hence bending direction flipped, but same bending desired.
## Redo ground and terminal selection, separate top and bottom zigzags
- model54_LN_vertiBend_zigzag_mirror_diferentTerminalSel_20190920.mph
- this is 10 * 10 um
- Great, as expected:

![Image 10](/assets/images/imported/20190919-tilt-mirror-with-bender/image10.png)

![Image 7](/assets/images/imported/20190919-tilt-mirror-with-bender/image7.png)

![Image 17](/assets/images/imported/20190919-tilt-mirror-with-bender/image17.png)

![Image 2](/assets/images/imported/20190919-tilt-mirror-with-bender/image2.png)

- two 10 * 10 um zigzags, 0.57 deg / V
- if we do 20 * 20 um, then 2.3 deg / V expected
Running eigen-mode now.
- DOF 2201 k, why smaller?
- sol time 9 min
First two eigen modes, 120 kHz and 300 kHz
- the fundamental one is moving the mass center of the mirror and is this much slower.

![Image 12](/assets/images/imported/20190919-tilt-mirror-with-bender/image12.png)

![Image 9](/assets/images/imported/20190919-tilt-mirror-with-bender/image9.png)

Moving this doc to LNPED drive and maintain it there.