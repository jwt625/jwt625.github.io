---
layout: single
title: "Silicon photonics and co-packaged optics: what is inside the box?"
categories:
  - Tutorial
tags:
  - Photonics
  - Silicon_photonics
  - Co-packaged_optics
  - Optical_interconnect
  - Data_center
  - Networking
toc: true
toc_sticky: true
use_math: true
header:
  overlay_image: /assets/images/2025/20251219_CPO/intel-oci-chip-pencil.webp
  cover: /assets/images/2025/20251219_CPO/intel-oci-chip-pencil.webp
  show_overlay_excerpt: false
  overlay_filter: 0.5
---

This tutorial is a general introduction to silicon photonics and co-packaged optics, based on materials I gathered over the years as well as some [teardown images](/teardown/100G-200G-400G-800G/) I have.

![Photonic and electronic hardware prototype](/assets/images/2025/20251219_CPO/photon-electron-hardware.webp)
- Intel 2017 CWDM silicon photonics transceiver, photo taken by [@sokol_cc](https://x.com/sokol_cc)
- I believe I have convinced at least a dozen ish people to buy this intel transceivers lol 
- I also have written a more low level intro on silicon photonics in this tutorial: [Selected Basics of Silicon Photonics](/tutorial/SiPho/)

A lot of things we take for granted are running on photons and electrons. People with personal blogs usually think about AWS, Grafana, postgres, and all the software in between, but underneath all of these are currents, voltages, and light.

For example, how are you seeing this page? It is stored somewhere in one of github's datacenters, sent through the internet backbone and multiple internet exchange points, received by your laptop, and finally shown by a giant array of LEDs that converts electrical currents into photons. There are dozens maybe hundreds of electrical-to-optical and optical-to-electrical conversions along the way. When some of them broke, you get longer github outages.

![Electrical and optical conversions across a cloud communication path](/assets/images/2025/20251219_CPO/network-conversions.webp)
*The exact number of conversions depends on the path.*

# We have been doing this for a while

To be exact, from almost 150 years ago, when Alexander Graham Bell and Charles Sumner Tainter built the photophone. That experiment already had the components we use in optical transceivers today.

The source was sunlight. Bell reflected it from a metal membrane and spoke toward the membrane, so his voice changed the amount of reflected light. A few hundred meters away, the light landed on selenium, a semiconductor whose resistance changed with illumination. A battery and telephone receiver then converted the light signal back into electrons and sound. He was sending voice through light in 1880.

![Bell and Tainter's photophone](/assets/images/2025/20251219_CPO/photophone-comparison.webp)
*The photophone sent voice over a beam of light roughly 145 years before this writing. Illustrations collected via the [Photophone overview](https://en.wikipedia.org/wiki/Photophone).*

Since then, we have pushed optical communication bandwidth in several ways. First we pushed the modulation rate: how quickly we can change some property of light to encode information. Then we added wavelength-division multiplexing (WDM), which is a fancy way of saying we shove more wavelengths into the same fiber. We also added spatial-division multiplexing (SDM), i.e., using more modes, cores, or more often just more fibers.

![Fiber-optic network capacity scaling](/assets/images/2025/20251219_CPO/winzer-fiber-network-scaling.jpeg)
*Source: Winzer et al., [“Fiber-optic transmission and networking: the previous 20 and the next 20 years”](https://doi.org/10.1364/OE.26.024190) (2018).*

The bad news is that communication is still not catching up with compute. Large AI models and accelerators are scaling much faster than the bandwidth of individual network links, so we end up adding more networking equipment and spending more power on moving data.

![Total SerDes shipments by application](/assets/images/2025/20251219_CPO/ieee-total-serdes-shipments.jpg)
*Serdes shipment, the volume is growing and so does the speed. Source: Weckel et al., [IEEE 802.3 Ethernet for AI assessment](https://www.ieee802.org/3/ad_hoc/E4AI/public/25_0327/weckel_e4ai_01_250327.pdf) (2025).*

![Compute and interconnect scaling](/assets/images/2025/20251219_CPO/compute-vs-interconnect-scaling.webp)
*This is a bit of a graph crime because the y-axis is arranged to separate the curves visually. The useful point is the widening gap between compute demand and interconnect scaling. Figure from Cheng et al., [“The rise of optical interconnects in data center systems”](https://doi.org/10.1364/OE.555476).*

![Aggregate optical bandwidth for high-performance computing and AI systems](/assets/images/2025/20251219_CPO/taubenblatt-hpc-ai-optical-bandwidth.jpg)
*Aggregate optical bandwidth for high-performance computing and AI systems, catching up quick with total internet bandwidths in the past. Source: Taubenblatt, [“Optical Interconnects for High-Performance Computing”](https://doi.org/10.1109/JLT.2011.2172989) (2012); extended by me and GPT-5.6.*

How do we catch up with the scaling of compute and of the big AI models and their interconnects and bandwidths need? Like said before, we need faster speed per lane, more wavelengths lanes, and more physical lanes. We need to shrink the conversions, make them faster and cheaper, and shink how we route light around.


# What is photonics?

![NVIDIA co-packaged-optics photonic switch and optical subsystem](/assets/images/2025/20251219_CPO/nvidia-cpo-photonic-switch.webp)

Photonics basically means **circuits for light**. In an electronic circuit, we use copper to route currents and voltages. In a photonic circuit, we use waveguides and other optical components to route and manipulate light.

A long time ago, people showed that light could bounce inside a water jet through total internal reflection. That was a very early demonstration that light could be guided.

![Colladon's water-jet light-guiding experiment](/assets/images/2025/20251219_CPO/colladon-water-jet.webp)
*Colladon's light-guiding experiment from the 1840s.*

After the invention of the laser, people gained a much cleaner and more controllable source of light. In the 1960s and 1970s, as always, researchers at Bell Labs showed that you can put a prism real close to a chip, and you could couple a free-space beam into a thin film on the chip. Now the light was traveling on the plane of a chip rather than through free space, using the same exact idea of total internal reflection. People called this integrated optics.

![Prism coupling into a thin-film optical waveguide](/assets/images/2025/20251219_CPO/thin-film-prism-coupling.webp)
*The thin-film/prism geometry from Tien's early work on [light waves in thin films and integrated optics](https://doi.org/10.1364/AO.10.002395).*

Later, those films were patterned into wires called waveguides, by doping the thin film along the desired paths and thus changing the refractive index locally. Light could be confined inside the waveguides, split, combined, filtered, and routed around a planar chip. By the 1990s and 2000s, planar lightwave circuits were already being used throughout the fiber-optic internet backbone.

![Planar lightwave circuit used in optical networking](/assets/images/2025/20251219_CPO/roadm-planar-lightwave-circuit.webp)
*A later planar lightwave circuit with patterned waveguides and free-space optical components. See Doerr's overview of [planar lightwave circuits in fiber-optic communications](https://doi.org/10.1016/B978-0-12-374171-4.00009-5).* They probably labeled the heaters wrong, and what a gross gluing for the heaters.

And more recently since early 2000s, we switched the material from glass to silicon itself, which is transparent for the light used (~1.5 um), and has much higher refractive index of ~3.5 instead of ~1.5, so the circuits can be made much smaller, and potentially at a much larger scale using process relatively compatible with CMOS industry, and thus riding the Moore's law curve, or so we wish, and it is yet to fully plan out. And the following example transceiver from intel is based on such silicon photonic circuits.

<div style="display: flex; flex-direction: row; align-items: center; gap: 10px;">
  <a href="https://doi.org/10.1109/JLT.2008.922149" style="width: 50%;"><img src="/assets/images/2025/20240830_20250427/20250114_024106_3.jpg" alt="Comparison of electronic-IC and photonic-IC component-count scaling" style="width: 100%; height: auto;"></a>
  <a href="https://doi.org/10.1038/s41467-024-44750-0" style="width: 50%;"><img src="/assets/images/2025/20240830_20250427/20250114_024106_4.jpg" alt="Scaling of monolithic and heterogeneous photonic integrated circuits" style="width: 100%; height: auto;"></a>
</div>
*The gap might be more than 50 years: today's silicon photonics looks roughly like electronic ICs in the 1970s. Left: Kaminow, [“Optical Integrated Circuits: A Personal Perspective”](https://doi.org/10.1109/JLT.2008.922149) (2008), with the figure credited to Rod Tucker. Right: Shekhar et al., [“Roadmapping the next generation of silicon photonics”](https://doi.org/10.1038/s41467-024-44750-0) (2024). [More context in the original thread](https://x.com/jwt0625/status/1916022570316664918).*

# How to send bits with light

An Intel 100G CWDM4 silicon-photonics transceiver from around 2017 is a great example. It is old enough that you can buy one on eBay for about four bucks, they are so cheap that I have a few dozens at home as gifts. And it contains all the basic components: lasers, modulators, photodetectors, drivers, amplifiers, control electronics, and an optical multiplexer. (and circulators but thats going a bit too deep.)

There are four optical channels, and each channel carries 25 Gb/s. Four wavelengths are combined into one fiber to make a 100G link.

![Annotated Intel 100G silicon-photonics transceiver](/assets/images/2025/20251219_CPO/intel-100g-transceiver-annotated.webp)
*Four 25-Gb/s optical channels are multiplexed into a 100G link. The module is roughly 18 mm long. Architecture labels follow Robert Blum's [Intel silicon-photonics overview](https://epic-photonics.com/wp-content/uploads/2021/12/Robert-Blum-Intel.pdf).* FOUR BUCKS WOULD YOU BELIEVE IT!

The architecture is basically the same as Bell's photophone: source, modulation, transmission, and detection. Now we go thru each one of them real quick.

## Source: lasers

The source is a semiconductor laser. The short version for how lasers work is that there are electronic states at different energies inside a semiconductor. When carriers transition between them, photons are emitted, just like all atoms do. Put the gain medium inside an optical cavity and you get a laser.
- The sooner you start learning how lasers work, the longer it takes, so I will stop here.
- quiz: do you get a laser if you put a normal flame from a normal fire between two mirrors?

The important system point is that lasers are often the failure points, and silicon itself is a poor light emitter (Silicon has indirect bandgap unless you are a freak and put silicon under a lot of stress, and indirect bandgap means light need to absorb some lattice vibration to emit, much harder than direct bandgap.). A silicon-photonics process therefore needs either III-V material integrated with the silicon waveguides or an external laser coupled into the chip.
- it is worth a whole other blog to talk about various laser integration techniques and why they almost all suck in different ways. For another day.
- there are also rich kids who make photonic circuits on indium phosphide wafers, the most popular semiconductor laser materials. By paying more as well as working with more retarded foundries (they hand cleave/mechanically cleave the dies instead of making facets and dicing until maybe 2020, insert sivers patent here), you get to put active components onto the same chip, lasers, amplifiers, modulators, detectors... Although it might sound simple, it usually involves regrowth of the quantum well and the junctions, and is a pain in the ass in its own way.

![Fraunhofer HHI 100-channel InP spectrometer PIC](/assets/images/2025/20251219_CPO/fraunhofer-100-channel-inp-spectrometer.jpg)
*Here is a InP PIC, a  100-channel spectrometer  from Fraunhofer HHI, [HIPPIOS](https://www.hhi.fraunhofer.de/abteilungen/hybride-integration-und-sensorik/projekte/archiv/hippios.html).*


![Cross-section of an InP photonic-integrated-circuit platform](/assets/images/2026/20250712_20260714/20260711_174715_0.jpg)
*Doesn't this look fun? And now imagine a grad student doing this by hand.*

![A lithography stage from a 243-step InP photonic-integrated-circuit process](/assets/images/2026/20250712_20260714/20260711_185040_0.jpg)
*An InP PIC platform cross-section and one lithography stage; by this point, the flow has completed only 74 of 243 steps. Figures from Docter et al., [“The 243 Steps of Making Photonic Integrated Circuits in InP”](https://alexandria.tue.nl/openaccess/Metis244709.pdf) (2010).*


![Lumentum laser-chip fabrication equipment operating on a wafer](/assets/images/2025/20251219_CPO/lumentum-cleaver.png)
*Glorious production scale mechanical cleaving by Lumentum. Frame at approximately 0:31 from NVIDIA, [“NVIDIA Spectrum-X Ethernet Photonics | Now in Full Production”](https://www.youtube.com/watch?v=CNM6Mmqrfeg&t=31s).*


In the Intel transceiver, six small InP coupons are visible near the source section. I initially thought they are four lasers and two redundant lasers. But one friend told me they are four lasers plus two monitor photodiodes.. So they actually did not build in redundancy.


![Laser and monitor-photodiode region inside the Intel 100G CWDM4 transceiver](/assets/images/2025/20251219_CPO/intel-100g-laser-source-teardown.webp)

An integrated laser reduces coupling loss and makes the optical engine more self-contained. An external laser is easier to replace when the laser fails, but it adds fiber coupling and connectors. Both approaches show up in CPO designs, but the ones shipping or near shipping today all have disaggregated lasers.

Fun fact, I used to make fun of disaggregated lasers when I was young and naive, thinking that integrating everything is the future and what a funny way to (not) admit defeat by calling it disaggregated.


## Modulation

Once the laser is turned on, it gives continuous optical power, which carries no information. We need to turn the light on and off (and potentially many other ways).

Some transceivers directly modulate the laser current, some put the modulator onto the same laser dies (EML). Silicon-photonics transceivers and CPO usually use a separate modulator. A simple way to picture it is as an optical switch. Continuous-wave light comes in, an electrical signal controls the switch, and modulated light comes out.

![Modulator region inside the Intel 100G CWDM4 transceiver](/assets/images/2025/20251219_CPO/intel-100g-modulator-teardown.webp)
*the big blob on top of the SiPho chip is the driver for the modulators. It needs to swing a few volts, and also pull up the voltage for a much larger capacitance of the modulator compared to logic circuits. This is with old school MZM hence the length of the chip.*

![Electro-optic intensity-modulation concept](/assets/images/2025/20251219_CPO/electro-optic-modulation-concept.webp)

There are many ways to build this switch: Mach-Zehnder modulators, microrings, electro-absorption modulators, and others. Everyone has a favorite because they trade off voltage, capacitance, bandwidth, optical loss, area, temperature sensitivity, and fabrication tolerance, and the most commonly, what they already know about how to do it.

![Lightmatter comparison of MZM, SiGe/Ge EAM, and microring modulators](/assets/images/2025/20251219_CPO/lightmatter-modulator-comparison.webp)
*here is a table from lightmatter phraising MRM. From hot chips 2025*

![Celestial AI comparison of MZI, ring, and electro-absorption modulators](/assets/images/2025/20251219_CPO/celestial-ai-modulator-comparison.webp)
*here is a very similar table from celestial trash talking MRM and worshipping EAM, from the same hot chips 2025 session. Also I just noticed why are they showing periodic poling for MZI hmm..*



The eye diagrams below are basically extremely fast observability plots. Instead of a metric arriving once per second, tens of billions of symbols arrive every second and are overlaid. Timing error spreads the transitions horizontally. Voltage noise and distortion spread the levels vertically. The cleaner the opening between states, the lower the expected error rate.

![NRZ and PAM4 eye diagrams](/assets/images/2025/20251219_CPO/nrz-pam4-eye-diagrams.webp)
*Two-level NRZ and four-level PAM4 eye diagrams from Blum's Intel overview.*

NRZ has two states and therefore carries one bit per symbol. PAM4 has four amplitude levels and carries two bits per symbol:

$$R_\text{bit}=R_\text{symbol}\log_2(M).$$

For example, 100 Gb/s PAM4 is roughly a 50-GBd-class signal before overhead. Symbol rate is in baud, data rate is in bit/s, and the analog bandwidth of the modulator is in hertz. They are related but not the same number.

The optical carrier itself is much faster. Light near 1550 nm has a frequency around 193 THz. The 50-GBd modulation is an envelope riding on top of that carrier, much like Wi-Fi data rides on a 2.4, 5, or 6 GHz RF carrier.

A faster modulator increases the bandwidth of one lane. More total bandwidth can also come from more bits per symbol, more wavelengths, and more fibers. More levels require better signal-to-noise ratio and usually more DSP and forward-error correction.

## Detection

At the other end, the receiver, a photodetector converts optical power into electrical current. More light produces more current; less light produces less current.

![Receiver and photodetector region inside the Intel 100G CWDM4 transceiver](/assets/images/2025/20251219_CPO/intel-100g-receiver-teardown.webp)
*Photodiodes (under the prism on the right) and TIA chip from intel 100G CWDM4 transceiver.*

The rest of the system wants a clean digital voltage, so a transimpedance amplifier (TIA) converts that small current into a voltage. Signal conditioning, clock/data recovery, DSP, and error correction then recover the bitstream. These are not my expertise, I just know these words.

![Photodetector and receiver signal-conditioning chain](/assets/images/2025/20251219_CPO/photodetection-concept.webp)

The detector itself is only one part of the receiver power. The TIA, ADC in DSP-heavy architectures, equalizer, clock recovery, and FEC all run at the full lane rate.

Quiz: is the bandwidths for the photodetectors and TIAs the higher the better? What about the modulators?


## Multiplexing and demultiplexing

We have four lasers and four modulation channels in the 100G example, but we want all four wavelengths in one fiber. The thing that shoves them into the same waveguide/fiber is called the multiplexer. At the receiver, a demultiplexer separates them again.

The intuition is similar to the rainbow from a CD or DVD. A periodic structure sends different wavelengths in different directions. If you run it in reverse, light arriving at several angles can be combined into one output waveguide. Thats one way to make a mux/demux on a chip, you make an on-chip grating.

![Diffraction grating separating wavelengths by angle](/assets/images/2025/20251219_CPO/diffraction-grating-concept.webp)

![Optical multiplexer region inside the Intel 100G CWDM4 transceiver](/assets/images/2025/20251219_CPO/intel-100g-optical-mux-teardown.webp)
*The intel transceiver again, you can vaguely see a curved surface (actually a curve in top view) near the bottom right, that's an echelle grating. Four waveguides shooting onto it from the left, and one output waveguide on the right.*

On an integrated chip, this can be done with echelle gratings, arrayed-waveguide gratings, microrings, or cascaded filters/MZIs.

<div style="display: flex; flex-direction: row; align-items: center; gap: 10px;">
  <a href="https://doi.org/10.1109/JSTARS.2024.3452033" style="width: 50%;"><img src="/assets/images/2024/spiral_AWG.png" alt="NIST spiral arrayed-waveguide-grating chip for microwave spectrometry" style="width: 100%; height: auto;"></a>
  <a href="https://arxiv.org/abs/2504.12917" style="width: 50%;"><img src="/assets/images/2025/20240830_20250427/20250421_154847_0.jpg" alt="Conventional arrayed-waveguide gratings fabricated in thin-film lithium tantalate" style="width: 100%; height: auto;"></a>
</div>
*Left: an extreme NIST spiral AWG developed for space-based microwave spectrometry, where sub-1-GHz resolution between adjacent wavelength channels required about 1 ns of delay, or a 9 cm path-length difference, thus the small to big spirals; Murakowski et al., [“Ultra-Wideband RF-Photonics Technology for Microwave Spectrometry”](https://doi.org/10.1109/JSTARS.2024.3452033) (2024). Right: more conventional AWGs, with two free-propagation regions joined by an array of incrementally lengthened waveguides; Hulyal et al., [“Arrayed waveguide gratings in lithium tantalate integrated photonics”](https://arxiv.org/abs/2504.12917) (2025).*

# Co-packaged optics: less copper, more fiber

What we have looked at so far is a silicon photonics pluggable transceiver. I'd like to quickly mention that most pluggables shipped are VCSELs and EMLs based ones instead of SiPho, and SiPho is more relevant for co-packaged optics.

![VCSEL short-reach transceiver shipment forecast](/assets/images/2025/20251219_CPO/ieee-vcsel-sr-volume-forecast.jpg)
*Source: [IEEE 802.3 200 Gb/s over multimode fiber CFI](https://www.ieee802.org/3/ad_hoc/ngrates/public/calls/25_0717/CFI_200GMMF_R3_250717.pdf) (2025).*

![EML-based pluggable optical transceiver](/assets/images/2025/20250117_20250127_long_thread/20250122_043517_3.jpg)
*A zoom-in shot of an EML-based pluggable optical transceiver, near the EML. (Innolight 200G QSFP56 FR4 1310 nm)*

The pluggable optical module sits at the front panel, while high-speed copper traces connect it to the switch ASIC. Those traces can be tens of centimeters long after including the package, PCB, and connectors. All these different electrical components cause loss, reflections and interferences, and good luck getting all the up-to-date S parameters from a dozen different vendors.

![Electrical path through a 400 Gb/s package](/assets/images/2025/20251219_CPO/ieee-400g-package-electrical-path.jpg)
*I want to carry the bits through the quiet murmur of a Broadcom PHY, watch the driver shake out the electrons, cross the little copper bridges of CoWoS with them, descend through forests of microbumps, and wander along the green terraces of Ajinomoto substrate. I want to follow them through BGA fields, watch them gather themselves at every via, at the polished gates of Samtec and Amphenol, through every reflection, loss, and trembling discontinuity, until, at last, they arrive cleanly at your receiver, the equalizer restores their shape, the clock finds their rhythm, and I can watch your eye open. Source: Sakai et al., [IEEE 802.3 400 Gb/s per-lane package study](https://www.ieee802.org/3/400GPL/public/2605/sakai_400GPL_01a_2605.pdf) (2026).*

Co-packaged optics moves the optical engines (OEs) right next to the switch ASIC (and in the future GPU/CPU/inference ASIC/memory. idk about TPU, google seems to hate CPO). The long electrical path becomes a very short package-level connection, and fiber carries the signal for the remaining distance.

![Pluggable optics, near-package optics, and co-packaged optics](/assets/images/2025/20251219_CPO/pluggable-npo-cpo-comparison.webp)
*The electrical reach shrinks as optical conversion moves from the faceplate toward the ASIC. Figure from Cheng et al., [Optics Express 33, 24190 (2025)](https://doi.org/10.1364/OE.555476).*

This does not mean everything becomes one homogeneous chip, people have a fancier name for it called EPIC (electronic-photonic IC). A CPO package contains a switch ASIC, electrical interface dies, photonic integrated circuits, drivers, TIAs, control electronics, fiber attach, and connections to internal or external lasers. The current generation of CPO is also imposters, the OEs are on organic substrate instead of the silicon interposers. Their bandwidths are not high enough to challenge the interposer real estate from high bandwidth memories (HBM).

Moving the optical engines closer offers several advantages:

- The copper path is shorter, so less power is spent driving and equalizing it.
- More lasers, wavelengths, and fibers can fit around the ASIC.
- Optical and electrical I/O density can be higher than a faceplate full of pluggables.
- Some retiming and DSP may be simplified, reducing power and latency.
- More assembly can eventually move into semiconductor and advanced-packaging processes. Semiconductor foundries are usually more competent than packaging and assembling houses

It also creates a reliability, yield, and maintenance problem. A failed pluggable can be pulled from the front of a switch. A failed optical engine inside a CPO package is not so easy to replace. Fiber attach, laser reliability, thermal management, yield, test strategy become part of the switch design. Known good die, known good OE, known good CPO, and finally known good CPO switch. I wish I know more people in the trenches of the yield grind so they could spare me some bad dies and bad OEs for fun.


# Copper versus fiber: some numbers

![Cisco Finisar 400G DR4 optical transceiver](/assets/images/2025/20251219_CPO/cisco-finisar-400g-dr4.webp)

## Propagation and bandwidth

Copper here means a high-speed PCB trace, an RF/coaxial cable etc. One easy order-of-magnitude number is that a representative RF cable around 25 GHz can lose half of its signal power after roughly one meter. The exact number depends heavily on the cable and connectors, and loss becomes worse as frequency increases.

This is why we do not use one passive high-speed copper link to go tens or hundreds of meters. The signal would be gone without repeaters, retimers, or a much lower data rate.

Fiber is in a completely different propagation regime, if it is worth a Nobel price it better be really good.. Corning specifies up to 0.18 dB/km attenuation at 1550 nm for SMF-28 fiber. That corresponds to roughly 3 dB loss, or losing half the optical power, after about 17 km. Inside a data center, the loss along a normal fiber is 100% negligible compared with coupling, connectors, splitting, and the conversions at the ends (if it is not negligible then you messed it up maybe with too many tight bends).

![Fiber-channel loss budget](/assets/images/2025/20251219_CPO/ieee-fiber-channel-loss-budget.jpg)
*Here's some connector insertion losses in a typical intra data center optical link. Source: Stone et al., [IEEE 802.3 400 Gb/s per-lane fiber-path study](https://www.ieee802.org/3/400GPL/public/260630/stone_400GPL_01a_260630.pdf) (2026).*

<div style="display: flex; flex-direction: row; align-items: center; gap: 10px;">
  <img src="/assets/images/2025/20251219_CPO/fiber-attenuation-vs-wavelength-itu.png" alt="Single-mode fiber attenuation versus wavelength" style="width: 50%; height: auto;">
  <img src="/assets/images/2025/20251219_CPO/fiber-dispersion-vs-wavelength-itu.png" alt="Single-mode fiber chromatic dispersion versus wavelength" style="width: 50%; height: auto;">
</div>
*Here is why we use 1.3 um and 1.5 um for fiber communication, for their low dispersion and propagation loss, accordingly. Hence all short reach datacom is running around 1.3 um. Source: ITU-T, [Optical fibres, cables and systems](https://www.itu.int/dms_pub/itu-t/oth/0B/04/T0B040000282C01PDFE.pdf).*

![A 1978 copper bundle and a fiber carrying comparable bandwidth](/assets/images/2025/20251219_CPO/copper-bundle-vs-fiber-1978.webp)
*A very physical comparison from a [1978 Bell System film](https://www.youtube.com/watch?v=gf2J3HTYUHE): a copper bundle and the much smaller fiber replacing its aggregate capacity. Go watch this video it is good.*

The optical carrier around 1550 nm is about 193 THz, leaving enormous optical bandwidth for many wavelength channels. But not with one modulator runs at ~100 THz tho. It means the carrier spectrum gives us much more room to scale with wavelength multiplexing than a single electrical channel. Here is an extreme example:

![O/E/S/C/L/U-band transmission setup for a 402.2-Tb/s single-fiber link](/assets/images/2025/20240822_20250825/20250824_092253_0.jpg)
*The experimental setup behind a 402.2-Tb/s transmission demonstration over one fiber, combining channels across the O, E, S, C, L, and U bands. Puttnam et al., [“402 Tb/s GMI Data-Rate OESCLU-Band Transmission”](https://doi.org/10.1364/OFC.2024.Th4A.3) (2024).*

There are still good reasons to use copper. It is cheap and direct: connect an electrical transmitter to an electrical receiver and there is no laser, modulator, photodiode, or optical connector in between. Lower latency as well. Even active copper is more competitive than doing the electrical-optical conversion and using fibers in many cases, and thus Credo's valuations.


## Latency

![Illustrative latency versus distance for copper and optical links](/assets/images/2025/20251219_CPO/latency-vs-distance.webp)
*These are rough curves. Actual numbers depend on the SerDes, retimers, DSP/FEC, routing, and protocol.*

A direct-attach copper link can have the smallest fixed delay because it avoids electro-optical conversion and the DSPs involved. A pluggable optical link adds relatively fixed delay in the transmitter, receiver, DSP, and extra on-module propagation.

CPO can reduce that fixed cost because the photonic engine is much closer to the switch ASIC and may need less electrical signal conditioning, which is where most of the latency savings are from. It does not remove the propagation delay of fiber, and it does not guarantee lower end-to-end latency for every architecture.

## Energy

There are many components and many ways to draw the boundary around an energy number. Whenever someone says their architecture is the best, check which components they included.

The three numbers to keep together are power, bandwidth, and energy per bit:

$$P=E_\text{bit}R_\text{bit}.$$

If a 1-Tb/s interface consumes 5 pJ/bit, it uses 5 W. That small-looking number becomes large after multiplying across every link in a cluster.

![Representative component contributions to short-reach link energy](/assets/images/2025/20251219_CPO/optical-link-energy-breakdown.webp)

The useful ballparks in the figure are around 10–20 pJ/bit for a complete short-reach optical link today and roughly 1–5 pJ/bit as an optical-I/O/CPO target. But ask what is included:

- laser wall-plug efficiency;
- modulator plus driver, not just the device capacitance;
- microring heaters and control loops;
- photodetector, TIA, ADC, DSP, clock recovery, and FEC;
- one-way versus aggregate bidirectional bandwidth;
- operating temperature, loss budget, and error rate.

![Comparison of NVIDIA's clock-forwarded DWDM optical link with prior NRZ DWDM links](/assets/images/2025/20251219_CPO/sota-DWDM-nvidia.png)
*Here is a nice 2026 Nvidia demo showing you how they break down the energy per bit. Song et al., [“A 32 Gb/s/λ 256 Gb/s/Fiber Half-Rate Bandpass-Filtered Clock-Forwarding DWDM Optical Link in a 3D-Stacked 7 nm EIC/65 nm PIC Technology”](https://doi.org/10.1109/ISSCC49663.2026.11409081) (ISSCC 2026).*

Electrical signaling has a strong length dependence. A simple picture is charging and discharging the capacitance of a copper trace, with energy on the order of $CV^2$. A longer and lossier channel needs more drive, equalization, or retiming.

![Communication energy increases as electrical links cross larger physical boundaries](/assets/images/2025/20251219_CPO/interconnect-energy-vs-distance.webp)
*Order-of-magnitude ranges based on Miller's [attojoule-optoelectronics review](https://doi.org/10.1364/JOSAB.34.000A01).*

Optics pays most of its energy at the two conversion endpoints. Once the light is in ordinary fiber, it goes kilometers, and optics win long-distance communication. It is now moving closer and closer to the chip as electrical bandwidth becomes harder to scale, and speed of light sounds cool.

# How to read the CPO bandwidth numbers

I promise you only need to multiple numbers, scalar numbers, not even matrices.

Intel's optical compute interconnect chiplet is a useful example.

![Intel optical compute interconnect chiplet next to a pencil eraser](/assets/images/2025/20251219_CPO/intel-oci-chip-pencil.webp)

![Intel OCI electrical IC, photonic IC, and fiber-array interface](/assets/images/2025/20251219_CPO/intel-oci-eic-pic-fiber.webp)

They used eight fiber pairs and eight wavelengths per fiber, for 64 optical lanes. Each lane carried 32 Gb/s in each direction. This gives roughly 2 Tb/s in one direction or **4 Tb/s aggregate bidirectional** bandwidth. Intel reported 5 pJ/bit. This thing is about ten times smaller than the old 100G pluggable examples we looked into above, while carrying about forty times the aggregate bandwidth. See the [Optics & Photonics News overview](https://www.optica-opn.org/home/industry/2024/june/intel_showcases_optical-interconnect_chiplet/).

Here is another configuration from Ranovus and MediaTek: eight fibers, eight wavelengths per fiber, and 100 Gb/s per channel:

$$8\times8\times100\ \text{Gb/s}=6.4\ \text{Tb/s}.$$

![Ranovus optical engines with external- and internal-laser configurations](/assets/images/2025/20251219_CPO/ranovus-external-internal-laser.webp)

![Ranovus optical engines co-packaged around a MediaTek ASIC](/assets/images/2025/20251219_CPO/ranovus-optical-engines-on-asic.webp)

They showed both internal- and external-laser versions and quoted 4 pJ/bit including the laser. Put eight 6.4-Tb/s optical engines around an ASIC and you get a 51.2-Tb/s switch-level number. See the [Ranovus/MediaTek OFC 2024 announcement](https://ranovus.com/wp-content/uploads/2024/03/Ranovus-CPO-3.0-MediaTek-announcement-March-20-2024-Final.pdf).

Whenever you see a very large bandwidth number, expand it back into lane rate, wavelengths, fibers, and directions. Also check whether the energy number describes a modulator, an optical engine, or the complete link.

Notice the total bandwidths is barely not making 1 TB/s? HBM4 is ~ 2 TB/s. Plus the yield and reliability, thats why these optical engines do not get to go on interposers yet.


# How to make your own

![Flip-chip bonder operating over a semiconductor wafer](/assets/images/2025/20251219_CPO/flip-chip-bonder-wafer.webp)

Don't.

Okay the short version is that you need to do a lot of begging. First, beg the software companies for access to their tools. Then beg a foundry for its process development kit. Later, beg a cleanroom or packaging house for time.

## Design the components and circuit

With electronics, you can often put a multimeter probe onto a node and measure the voltage. I wish photonics were that easy. Even a device whose only job is to split one input waveguide into two outputs depends on several dimensions, interference, reflection, wavelength, polarization, and fabrication errors.

![Simulated optical field in a compact waveguide splitter](/assets/images/2025/20251219_CPO/waveguide-splitter-simulation.gif)
*Simulated optical field in a multimode interference (MMI) splitter*
- quiz: what happens when you run the 1x2 MMI splitter backward with the two inputs out of phase with each other?

Component design commonly uses FDTD, FEM, eigenmode solvers, and coupled-mode models. Tools include Ansys Lumerical, COMSOL, Flexcompute Tidy3D, and Photon Design. Once the components work, they are connected at circuit level using tools such as Synopsys OptSim, Lumerical INTERCONNECT, Luceda IPKISS, or GDSFactory. I promise you'll always forget something in your circuit level simulations, whether it is backreflection, other modes, or stray light. It will get better over time, you will learn your mistakes, but it will never match your measurement.


![A photonic circuit assembled from reusable components](/assets/images/2025/20251219_CPO/photonic-circuit-layout.webp)

I'm not gonna talk about the EIC design, thats 10 other blogs someone else need to write. I guess also no mention of laser design, thats another 10 blogs for the experts.


## Get the foundry PDK

Next, beg and sign an NDA with a foundry and get its PDK. A photonic PDK is similar in spirit to an SDK, except it describes a manufacturing process: layers, dimensions, tolerances, design rules, validated components, and compact models.

![Examples of silicon-photonics foundries and platforms](/assets/images/2025/20251219_CPO/silicon-photonics-foundries.webp)

After laying everything out, review the design many, many, many times. A photonic chip has layers that route light and other layers that route electrical signals. Waveguide bends and crossings, RF paths, phase errors, heaters, pads, fiber coupling, test structures, and packaging keepouts all interact. Check out the [Infinera 1.6T DWDM DP-64QAM chip die-shot analysis](/tutorial/infinera-DP-64QAM/) and see if you can explain all the subtle decisions.

![A dense silicon-photonics layout that must be reviewed before tapeout](/assets/images/2025/20251219_CPO/intel-photonic-ic-layout.webp)
*A 1.6-Tb/s silicon-photonics PIC layout from Blum's Intel overview.*

Once you send the design to a foundry, you may wait half a year to learn about a mistake, and you pay quite a lot for that lesson.

## Fabrication

A multi-project wafer shares mask and wafer cost across many designs. Depending on the process, area, packaging, and whether this is an MPW or custom run, an R&D tapeout can range from tens of thousands of dollars to more than a million. The wait can vary from a quarter or two to a year. Oh and the chips come back in, well, chips, not wafers, so no easy additional wafer scale backend or packaging steps.

![Tower Semiconductor 2026 MPW schedule, including PH18M and PH18DA 0.18 µm silicon-photonics runs](/assets/images/2025/20251219_CPO/tower-2026-MPW.png)
*Tower Semiconductor's [2026 MPW schedule](https://towersemi.com/wp-content/uploads/2026/03/MPW-Schedule_External_03_10_2026_AC.pdf), including the PH18M and PH18DA 0.18 µm silicon-photonics shuttle runs.*

![AIM Photonics process cross-section](/assets/images/2025/20251219_CPO/aim-photonics-process-cross-section.webp)

![Illustration of a photonic-process etch step](/assets/images/2025/20251219_CPO/aim-photonics-process-etch.webp)
*Process illustrations from the [AIM Photonics MPW program](https://www.aimphotonics.com/mpw).*

If you are developing a new process instead of using an established PDK, debugging and stabilizing it can take years. If you know what you are doing and have access to an academic cleanroom, you can make a simple chip much faster, but that is very different from a qualified high-volume process.

## Laser integration and packaging

After the photonic chip is fabricated, it still has to be integrated with lasers, electronic ICs, drivers, TIAs, fibers, electrical interconnect, thermal hardware, and a PCB or larger package.

![Laser integration visible inside a silicon-photonics transceiver](/assets/images/2025/20251219_CPO/laser-integration-teardown.webp)

There are many steps to stack the dies and route signals between them. Fiber alignment, attach accuracy, adhesives, solder, underfill, thermal expansion, contamination, test access, known-good-die, burn-in, and rework all affect yield and reliability.

(written by codex:) This is why CPO is not only a photonics problem. It is also an advanced-packaging, manufacturing, and test problem. The switch vendor may design the architecture and ICs, while foundries make the chips, packaging houses assemble the optical engines, and system manufacturers build and qualify the switch.


# What CPO changes for data centers

![Meta data-center fiber pathways](/assets/images/2025/20251219_CPO/ieee-meta-fiber-pathways.jpg)
*We have a lot of fibers inside and between data centers. Source: Stone et al., [IEEE 802.3 400 Gb/s per-lane fiber-path study](https://www.ieee802.org/3/400GPL/public/260630/stone_400GPL_01a_260630.pdf) (2026).*

Practically, the two biggest reasons, power and reliability.

At large cluster scale, removing pluggable transceivers and long electrical channels can save megawatts. That power can be used for more GPUs. The cooling load also falls by the same electrical power, although in practice the saved power will probably be filled with more compute and turned into heat anyway.

Transceivers and their connections are also frequent failure points in backend networks. CPO removes many individual pluggable modules and one connector interface per link. The vendor pitch is that the switch should remain as reliable as a conventional switch and that a replaceable external laser module should fail less often than the switch itself. Although the current external laser source form factor ELSFP is stupid, but nvidia is moving them into the switch box anyways..


CPO can also simplify physical deployment. Instead of installing a pluggable transceiver and then the fiber, the fiber connects directly to the switch.

The honest answer is probably that production behavior has to be measured (which meta has some publications). Moving optics into the switch removes some failure modes but creates a different repair model.

![Optical cabling in an IBM Power 775 supercomputer rack](/assets/images/2026/20241104_20260628/20260621_161815_3.jpg)
*Fibers go burrrr (Partially populated optical cabling in an IBM Power 775 rack). Source: Taubenblatt, [“Optical Interconnects for High-Performance Computing”](https://doi.org/10.1109/JLT.2011.2172989), Fig. 10; previously used in [OFS #105]({% post_url 2026-06-29-weekly-OFS-105 %}#optical-interconnect-volume-growth-for-ai).*


# Recap and miscellaneous

## Recap

![NVIDIA co-packaged-optics photonic switch and optical subsystem](/assets/images/2025/20251219_CPO/nvidia-cpo-photonic-switch.webp)

Photonics means circuits for light. The basic components are lasers, modulators, photodetectors, multiplexers, demultiplexers, drivers, TIAs, and DSP.

CPO moves the optical I/O closer to the switch or compute ASIC. The main physical reason is that copper bad bad, but copper is cheap. Sorry, it is that electrical signaling becomes harder and more energy-intensive with distance and data rate, while fiber has very low propagation loss and enormous wavelength bandwidth. 

The total bandwidth is still just the product of a few understandable numbers:

$$R_\text{total}=R_\text{lane}\times N_\lambda\times N_\text{fiber}\times N_\text{direction}.$$

And the power is

$$P=E_\text{bit}R_\text{bit}.$$

The hard part is making all the lasers, modulators, detectors, electronics, fiber interfaces, packaging, cooling, test, and sales strategy work together at useful yield and reliability. And figure out which part is consuming how much of your power, link, financial, and mental health budget.

I did not go into the whole engineering aspects about MRM, the nonlinearities, the thermal control, the analog-mixed signal hell.. If you know these pains, you should write up a blog!

I also did not even mention VCSELs ~~and micro LEDs~~, another day!


## Near-packaged optics and length of the link

I did not talk about ner-package optics, in short it is a compromise and attempt to still shrink and reduce the electrical propagations and interfaces, by putting the EO conversion on the board instead of as aggressive as CPO (onto the organic substrate), and VCSELs are leading the charge.

![200 Gb/s VCSEL link over 60 m of OM4 fiber](/assets/images/2025/20251219_CPO/ieee-200g-vcsel-60m-om4.jpg)
*Source: Rodes et al., [IEEE 802.3 200 Gb/s over multimode fiber](https://www.ieee802.org/3/200GMMF/public/Plenary_Nov_11-2025/rodes_200gmmf_01_2511.pdf) (2025).*

However VCSELs are mostly multimode, and they use multimode fiber to make the fiber alignment easier. As a result, the modal dispersion (different modes propagating at different speed) could interfere your symbols and limit the baud rate. In contrast, SiPho based CPOs are running on single mode silicon photonic waveguide and single mode fibers, and can go hundreds of meters and further. Current CPO solutions are thus all for scale-out, which loosely mean interconnects between racks. (I guess we should also talk about scale-up and scale-out..)

<div style="display: flex; flex-direction: row; align-items: center; gap: 10px;">
  <img src="/assets/images/2025/20251219_CPO/ieee-data-hall-fiber-link-lengths.jpg" alt="Data-hall fiber-link length distribution" style="width: 50%; height: auto;">
  <img src="/assets/images/2025/20251219_CPO/ieee-smf-zero-dispersion-distribution.jpg" alt="Single-mode fiber zero-dispersion wavelength distribution" style="width: 50%; height: auto;">
</div>
*Source: Kuschnerov et al., [IEEE 802.3 Ethernet for AI optical-link study](https://ieee802.org/3/ad_hoc/E4AI/public/25_1023/kuschnerov_e4ai_01_251023.pdf) (2025).*




## Startups


# References and further reading

- Robert Blum, Intel, [*High Volume Silicon Photonics for Optical I/O and Other Next Generation Applications*](https://epic-photonics.com/wp-content/uploads/2021/12/Robert-Blum-Intel.pdf) ([local PDF backup](/assets/doc/2025/20251219_CPO/robert-blum-intel-high-volume-silicon-photonics.pdf)), 2022.
- Cheng et al., [*The rise of optical interconnects in data center systems*](https://doi.org/10.1364/OE.555476), *Optics Express*, 2025.
- Stewart Wills, [*Intel Showcases Optical-Interconnect Chiplet*](https://www.optica-opn.org/home/industry/2024/june/intel_showcases_optical-interconnect_chiplet/), *Optics & Photonics News*, 2024.
- Ranovus and MediaTek, [6.4-Tb/s CPO 3.0 announcement](https://ranovus.com/wp-content/uploads/2024/03/Ranovus-CPO-3.0-MediaTek-announcement-March-20-2024-Final.pdf) ([local PDF backup](/assets/doc/2025/20251219_CPO/ranovus-mediatek-cpo-3-ofc-2024.pdf)), OFC 2024.
- David A. B. Miller, [*Attojoule Optoelectronics for Low-Energy Information Processing and Communications*](https://doi.org/10.1364/JOSAB.34.000A01), *JOSA B*, 2017.
- Corning, [SMF-28 Ultra optical-fiber specifications](https://www.corning.com/media/worldwide/coc/documents/Fiber/product-information-sheets/PI-1424-AEN.pdf) ([local PDF backup, 2014 revision](/assets/doc/2025/20251219_CPO/corning-smf-28-ultra-specifications.pdf)).
- AIM Photonics, [Silicon Photonics Multi-Project Wafer program](https://www.aimphotonics.com/mpw).
- ASE, [Silicon Photonics advanced-packaging overview](https://ase.aseglobal.com/silicon-photonics/).
- Umesh Shainer, NVIDIA, [*Scaling AI Factories with Co-Packaged Optics*](https://hc2025.hotchips.org/assets/program/conference/day2/HC25_NVIDIA_Shainer_v4.pdf) ([local PDF backup](/assets/doc/2025/20251219_CPO/umesh-shainer-nvidia-scaling-ai-factories-with-cpo-hot-chips-2025.pdf)), Hot Chips 2025.


# Revision history

- **2026-08-22:** Added figures and sources on network scaling, fiber characteristics, InP photonics, electrical paths, VCSEL links, NPO, and data-center fiber deployment; reorganized the recap and miscellaneous material.
