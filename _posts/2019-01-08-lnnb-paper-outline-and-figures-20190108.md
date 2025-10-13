---
categories:
- Research
date: '2019-01-08'
header:
  cover: /assets/images/imported/lnnb-paper-outline-and-figures-20190108/image8.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/lnnb-paper-outline-and-figures-20190108/image8.png
  show_overlay_excerpt: false
original_date: '2019-01-08'
tags:
- Piezoelectric
- Simulation
title: Outline and figures
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2019-01-08, converted on 2025-10-12. )

# TODO 20190301
In the SI, make it clear that we don't know the cause of the n_escape.
About quadratic thermal-optical shift
- it's not simply loss from SHG photons
- no apparent change in the linewidth
- it's the portion of lost photons that get absorbed?
Mention the added sentences in the sim paragraph.
# TODO
update Figures:
- make Fig1 (a) and (b) larger
- done
- add labels to SEM? (LN, Al, etc.)
- remake Fig. S4
- done
- add fig in SI for on-chip EOM fit
- done
- simulation of OM interaction
- done
Setup the story
Why is this important and interesting
- cavity optomechanics enables application ranging from sensing to quantum information science
- piezoelectric coupling between nanomechanical resonator and superconducting circuits enables coupling and quantum control of phonons, and also transducing, storing and processing of quantum information.
why is this hard
- different piezoelectric materials have been exploit for optomechanics (AlN, GaAs, GaP)
How the difficult is solved and what's the new physics:
Details:
- put the X of the X-point in latex eq. env.
- add more about LN fab, why is it hard, what people have done.
## 1. Design of nanobeam and mode profile

![Image 10](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image10.png)

- mechanical mode profile TBA
Should we mention that it's originally designed for Y-cut? (fabricated on both X-cut and Y-cut)
- (a, b, c) geometry optical and mechanical band structure of mirror cell with defect cell mode
- (d, e) geometry and mechanical bands of 1D phonon shield
- (f, g) full nanobeam optical and mechanical mode profile
- (h) SEM of real device (and OM coupling vs. theta (in SI))
## 2. Measurement setup and optical modes
- (a) measurement setup
- (b) one example optical scan and zoomed-in optical mode + fit (inset)
- (c) histogram of optical quality factor
- (c) thermal optical shift, including loglog of WL vs. power, T0 vs. power and n_c vs. power?
## 3. EIT/EIA & mechanical lasing

![Image 6](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image6.png)

- (a) wide and narrow (inset) VNA sideband sweep
- (b) fit results of (a) vs. power/detuning (room T, low T with & without PS)
- (c) power spectrums of not-lasing to lasing transition
- (d) lasing power spectrum results: linewidth vs. intracavity photon number, temperature vs. intracavity photon number (also include low power backaction measurement?)
- plot the fit independently
## 4. piezoelectric drive

![Image 20](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image20.png)

- (a) wide ZNB scan, along with the mechanical bandgap
- (b) zoom-in ZNB scan showing the mechanical response
- (c) FSW scan showing the mechanics at the same frequency
# Questions:
- nonlinear thermal-optical shift in the article or in SI?
- what journal are we aiming at?
- should we talk about gamma_i vs. n_c?
# In SI:
## Anisotropic photoelastic coupling (Almost done)
- (a) dependency of photoelastic p22 vs. crystal cut and orientation
- (b) simulated g vs. crystal orientation with measurements
- (c) optical and mechanical quality factor vs. theta
- Path: `measurements/20181126_LNNB24/plot_modes.m`
- ![Image 12](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image12.png)
Need to add g0 measurements from LNNB24
- no, not as good
### Simulated g0:
- Path: `COMSOL/LN/LNNB/FBH/20190115_recheckCoupling`

![Image 15](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image15.png)

## Quadratic thermal optical shift (Done)
- (a) scans with different power (and fits using quadratic thermal shift?)
- (b) loglog plot of WL shift vs. input power
- (c) VNA sideband sweep showing cavity linewidth not changing
- (d) T0 vs power
- (e) n_c vs power

Path:
- `measurements/20181216_LNNB24_lowT_drag`
- `plot_optical_power_sweep.m`

![Image 5](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image5.png)

## Thermal relaxation rate (Done)
Path: `LNNB24_lowT_drag`

Files:
- `plot_near_escape_all.m`
- `plot_thermal_fit_res.m`
- (a) maybe a simple illustration showing how slow amplitude modulation could probe the slow nonlinear optical effect
- (b) low freq VNA response and fit
- (c) relaxation rate vs. intracavity photon number
Relaxation rate with different power and detuning:

![Image 16](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image16.png)

I derived why it's n_c dependent.
I don't understand why it's linear
- I figured it out!
Understood. See SI.
## Kappa vs nc
- folder: LNNB24_lowT_drag
- plot_kappa_vs_nc.m
## Microwave to mechanical conversion efficiency (Done)
- show the mechanical thermal motion + coherent drive tone
# Details
Subfigures will be assembled in
- `manuscripts/20190114_LNNB/figures`
- going to use inkscape for editing
## Fig. 1 (done)
Still need to confirm which mode is the actual mechanical mode

Path: `COMSOL/LN/UnitCell1DCavity/FBH/20190114_recalc_bands_180707`

Bands on Y-cut

Images saved in:
- `COMSOL/LN/UnitCell1DCavity/FBH/20190114_recalc_bands_180707/plot`
- UC geom generated by COMSOL + ignore faces & edges + material appearance (need to enable rendering it in Options -\> preference)

![Image 7](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image7.png)

![Image 13](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image13.png)

![Image 18](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image18.png)

1DPC:

![Image 8](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image8.png)

![Image 9](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image9.png)

## Fig. 2 (done)
1.  Setup, finished.
2.  optical scan:
    1.  Path: `measurements/20181216_LNNB24_lowT_drag`
    2.  Script: `plot_optics.m`
3.
## Fig. 3 (done)
low power EIT data:
- Path: `measurements/20181212_LNNB24_lowT`
- Fitting script: `plot_EIT_individual_181213.m`
- plotting: plot_EIT_fits.m

![Image 2](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image2.png)

![Image 17](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image17.png)

not sure if we want to show the fit results of low power EIT measurements for different power.
Going to use phase only and make the zoom-in plot an inset.
high power EIA & lasing data:
- Path: `measurements/20181216_LNNB24_lowT_drag`
- Fitting script: `plot_steplaser_VNA_FSW.m`
- plotting: plot_for_paper.m
FSW spectrum:
- Cooperativity = 0.55, 0.92, \>1 (from same power but different detuning)

![Image 3](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image3.png)

- low power backaction fit results:
- Path: `measurements/20190115_LNNB24_backactionSummary`

![Image 11](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image11.png)

EIT/EIA fit results (with all different detuning and power):
- fitted g0/2pi = 124 kHz
- also the "intrinsic linewidth":

![Image 4](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image4.png)

![Image 1](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image1.png)

High power PSD fit results (different power plotted together):
- do we want to show these or not?
- this total linewidth is a mixture of detuning (gamma_OM depends on it) and mode mixing

![Image 14](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image14.png)

![Image 19](/assets/images/imported/lnnb-paper-outline-and-figures-20190108/image19.png)

## Fig. 4 (done)
Path: `measurements/20180912_LNNB18_roomT_wirebonded`