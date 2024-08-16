---
title: "Yapping on ebeam lithography"
categories:
  - Tutorial
tags:
    - Nanofab
    - Lithography
    - Electron
toc: true
toc_sticky: true
use_math: true
header:
  overlay_image: /assets/images/2024/tracer-bild2-2.png
  cover: /assets/images/2024/tracer-bild2-2.png
  show_overlay_excerpt: false
  overlay_filter: 0.5
---


Under construction...

Think about and focus on what you could offer different and extra compared to existing documents.

TODO:
- [x] gather references & documents
- [] pick some cool looking SEMs
- [] think about which part you want to add drawings

# Outline:

## My journey
- History
    - Raith 150 Two (2015 - 2017)
    - JEOL JBX 6300FS (2017 - 2022)
    - Raith Voyager (2022 - 2023)
    - EBPG 5200+ (2023 - 2024)
- Number of sessions (~ 420 total)
    - 2023 - 2024: 60?
    - 2021 - 2022: 109
    - 2019 - 2021: 92 (damn covid)
    - 2018: 89
    - 2017 - 2018: 73
    - pre 2017: sporadic
- Ebeam resist: CSAR, MMA/PMMA, HSQ

## Ebeam basics
- How stable do things need to be
- Why is the column this big
- Where are the electrons going
    - focusing (how is it done)
    - current measurement
    - beam calibration
- Where is the stage going
    - interferometer
    - writefield (WF) size, calibration, stitching
    - subfield (maybe?)
- beam parameters
    - Voltage, current
    - shot pitch
    - dose (DAC rate limit, dose sweep)

## Practical
- What resist to use
    - positive vs. negative
    - adhesion
    - discharge layer
    - selectivity
    - liftoff
- Fracturing (BEAMER)
    - Oh god maybe this should be a different yap-post
    - I should still start to write down things that matters
    - Field control: fixed, manual, different ways to meander, fully manual with layers...
    - multipass
    - PEC
- Mounting your chip
    - front vs. back referenced
    - height measurement (under uscope, in the tool with the LED)
    - multiple chips
- Locating your chip
    - optical microscope / camera assistance
    - using the SEM
- Alignment
    - desired marks (materials, thickness, locations, reusability)
    - how to find the marks (manual & auto, mark params, scan params)
- develop
    - remove discharge layer
    - be wary water + IPA could develop some resist unintentionally
- feedback & optimization
    - dose sweep
- optimize your own workflow
    - better estimation of the exposure time
    - What is the bottleneck? What can be automated?
- TBA...

# References

## Lab resources
1. Caltech KNI lab: [EBPG 5000+: 100 kV Electron Beam Lithography](https://lab.kni.caltech.edu/EBPG_5000%2B:_100_kV_Electron_Beam_Lithography)
2. Stanford [EBL Practical Guide](https://drive.google.com/file/d/1QefNaVA8mRoXeRkXaiWEuVK5TIaO3ECp/view) ([backup](/assets/doc/2024/EBL Practical Guide-Feb 2024.pdf))
3. BEAMER training from GenISys: [Webinar Series - BEAMER Training](https://www.genisys-gmbh.com/webinar-series-beamer-training.html)

## Training videos
4. [JEOL JBX-9300FS EBL (1 of 2) - training video (Georgia Tech - Microelectronics Research Center)](https://www.youtube.com/watch?v=q8h5xYJX-_U)
5. [JEOL JBX-9300FS EBL (2 of 2) - training video (Georgia Tech - Microelectronics Research Center)](https://www.youtube.com/watch?v=SQhP-k8iYWM)


## Papers
1. Altissimo, Matteo. "E-beam lithography for micro-/nanofabrication." Biomicrofluidics 4.2 (2010). [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2917861/)
2. Chen, Yifang. "Nanofabrication by electron beam lithography and its applications: A review." Microelectronic Engineering 135 (2015): 57-72. [link](https://www.sciencedirect.com/science/article/abs/pii/S016793171500101X?via%3Dihub)
3. Gilmour Jr, Alexander S., and A. S. Gilmour. Klystrons, traveling wave tubes, magnetrons, crossed-field amplifiers, and gyrotrons. Artech House, 2011.


