---
title: "Infinera 1.6T DWDM DP-64QAM Silicon Photonic Chip Analysis"
categories:
  - tutorial
tags:
- Photonic_integrated_circuit
- DWDM
- Coherent_transceiver
- DBR_laser
- InP
- Waveguide
- Spot_size_converter
- Polarization_rotator
- IQ_modulator
- Phase_modulator
- Amplitude_modulator
- Monitor_photodetector
- Semiconductor_optical_amplifier
- MMI
- Injection_locking
- Optical_QPSK
- Stealth_dicing
toc: true
toc_sticky: True
use_math: true
header:
  cover: /assets/images/2026/20260516_20260521_long_thread/20260516_054502_0.jpg
  overlay_image: /assets/images/2026/20260516_20260521_long_thread/20260516_054502_0.jpg
  show_overlay_excerpt: false
  overlay_filter: 0.5
---




this is a photonic integrated circuit chip from a 1.6T DWDM transceiver module by Infinera (2 wavelengths x 2 polarizations (DP-64QAM) x 96 GBaud), and I'll make some guess on what is going on on this PIC.

before I start, you can zoom in onto the edges and see the facets were cleaved... (the year was already ~2020) 
![20260516_054502_0.jpg](/assets/images/2026/20260516_20260521_long_thread/20260516_054502_0.jpg)
- (image credit: [https://siliconpr0n.org/map/infinera/1p6tbpspic/single/infinera_1p6tbpspic_evilmonkeyz_mx_am10x.jpg](https://siliconpr0n.org/map/infinera/1p6tbpspic/single/infinera_1p6tbpspic_evilmonkeyz_mx_am10x.jpg))
- the video is [Photonic Integrated Circuits - Inside an Infinera 1.6Tb/s PIC module](https://www.youtube.com/watch?v=zM60Vs7GhVA), should've bought some photonics stocks when I first saw this video.. 

# Lasers
first of all, it is pretty easy to find the lasers, you know there should be at least two for the transmit, and at least two for the receive (need LO because it is coherent). And it is DWDM, so you definitely need to tune the lasers by tuning the DBR mirrors. after some quick staring, you'll realize the left half of the chip is for transmit, and the right half is for receive, and there are four lasers in total, each with DBR mirrors on the two ends. No redundancy, one laser broken and you are screwed. you can also see the little InP coupons are transfered onto the chip.
![20260516_063702_0.jpg](/assets/images/2026/20260516_20260521_long_thread/20260516_063702_0.jpg)
![20260516_063702_1.jpg](/assets/images/2026/20260516_20260521_long_thread/20260516_063702_1.jpg)


output waveguide with spot size converters, TE and TM are the two polarizations.
![20260516_064408_0.jpg](/assets/images/2026/20260516_20260521_long_thread/20260516_064408_0.jpg)

# Modulation
you can follow the two ends of the laser to find TE and TM input to the modulation region. There is an additional phase modulator inside the laser. I cannot find any polarization rotator on the chip, my best guess is it is rotated and combined off chip. So everything on-chip would be TE, likely simplifies a lot of stuff. There are four paths needed for IQ modulation, thus each "polarization" gets 1x2 split twice, and each path seems to have its own amplitude (shorter because it is absorptive, I1A, I2A etc.) and phase (longer because it is thermal, I1P, I2P etc.). The actual fast modulation is near the top, right next to the wirebonded differential pairs. The slow amplitude and phase tuning lines are jumped on the chip multiple times with wirebonds to reduce crossover of electrical routings for reasons.
![20260516_065712_0.jpg](/assets/images/2026/20260516_20260521_long_thread/20260516_065712_0.jpg)
![20260516_065712_1.jpg](/assets/images/2026/20260516_20260521_long_thread/20260516_065712_1.jpg)
![20260516_065712_2.jpg](/assets/images/2026/20260516_20260521_long_thread/20260516_065712_2.jpg)


## Monitoring
after the fast modulators, the four paths for each polarization gets combined once into two arms, with monitor photodetectors tapped on each one of them (TEIM, TEQM, TMIM, TMQM), and then combined again and tapped again (TECPD, TMCPD). And the final combined outputs go thru their corresponding SOAs (semiconductor optical amplifiers), and to their output facets. They are all made with similar InP coupons. The PDs have curved tapered waveguide terminations to dump the residual light.
![20260516_070527_0.jpg](/assets/images/2026/20260516_20260521_long_thread/20260516_070527_0.jpg)
![20260516_070527_1.jpg](/assets/images/2026/20260516_20260521_long_thread/20260516_070527_1.jpg)


# Receivers
the receiver side has one more port in addition to the 2 wavelength x 2 polarizations, which is called WLL. My best guess is for injection locking of the LO lasers. It seems to get split, amplified, and goes into the two LO lasers. I'm still confused how are they using one WLL port for two wavelengths.
![20260516_071651_0.jpg](/assets/images/2026/20260516_20260521_long_thread/20260516_071651_0.jpg)


the dummy is removed around the MMIs and detectors, not sure why. You can see the CMP dishing causing fringes in the open areas. The MMIs also all have extra dummy ports, my best guess for them is for improving local symmetry. The Is and Qs are out at different location to get the magical phases you need for the I and Q receivers. [Optical QPSK transceiver]( https://optics.ansys.com/hc/en-us/articles/360042819033-Optical-QPSK-transceiver)
![20260516_073033_0.jpg](/assets/images/2026/20260516_20260521_long_thread/20260516_073033_0.jpg)
![20260516_073033_1.jpg](/assets/images/2026/20260516_20260521_long_thread/20260516_073033_1.jpg)


# some overall observations
- isolation trenches everywhere, surrounding wirebond pads and between the polarizations, around the four receiving channels etc. 
- many jump pads on the chip to minimize crossover between electrical routings and optical routings. Wherever they cross, the electrical routings' width is reduced, unless it is right before monitor PDs. 
- enough space for probing for all the knobs, and they were all used multiple times.


I take back the oroginal tweet, it's most likely laser stealth diced. Looks too clean to be cleaved.


found a nice diagram for coherent transmit and receive system 
- Ye2025: [Simplified Transceivers for Short-Reach Coherent-Lite Systems]( https://doi.org/10.1109/JLT.2025.3581121)
![20260521_063140_0.jpg](/assets/images/2026/20260516_20260521_long_thread/20260521_063140_0.jpg)
- (however few arrows are off lol)

