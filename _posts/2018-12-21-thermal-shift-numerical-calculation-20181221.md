---
categories:
- Research
date: '2018-12-21'
header:
  cover: /assets/images/imported/thermal-shift-numerical-calculation-20181221/image8.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/thermal-shift-numerical-calculation-20181221/image8.png
  show_overlay_excerpt: false
original_date: '2018-12-21'
tags:
- Technical
title: Thermal shift numerical calculation
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2018-12-21, converted on 2025-10-12. )

Write a script:
- take a temperature
- give the
# Quadratic thermal shift
Path: `matlab/LNNB/thermal_optic`

What I'm doing:
Solve
- ![Image 1](/assets/images/imported/thermal-shift-numerical-calculation-20181221/image1.png)
- hot detuning: ![Image 2](/assets/images/imported/thermal-shift-numerical-calculation-20181221/image2.png)
Parameters controllable in experiment:
- ![Image 3](/assets/images/imported/thermal-shift-numerical-calculation-20181221/image3.png)
- cold detuning ![Image 4](/assets/images/imported/thermal-shift-numerical-calculation-20181221/image4.png)
Measured in experiment:
- maximum shift
- hot detuning ![Image 5](/assets/images/imported/thermal-shift-numerical-calculation-20181221/image5.png)
Numerical results with measured parameters:
- alpha/2pi = 34 Hz/n\^2 is used

![Image 8](/assets/images/imported/thermal-shift-numerical-calculation-20181221/image8.png)

Comparison of optical scan:
- using real measured P_in
- line: measurement. Dots: numerical

![Image 6](/assets/images/imported/thermal-shift-numerical-calculation-20181221/image6.png)

Comparison of hot detuning vs. cold detuning measurement:
- dataset: TD67_VNA_lowP_wlmin_1532.0_wlmax_1536.0_atten_5.53_20181219T133913
- script: `measurements/20181216_LNNB24_lowT_drag/plot_steplaser_noFSW.m`
- big dots: measurement. Small dots: numerical

![Image 7](/assets/images/imported/thermal-shift-numerical-calculation-20181221/image7.png)