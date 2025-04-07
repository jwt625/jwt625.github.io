---
title: "How to (not) excite a wavelength-scale acoustic/mechanical waveguide"
categories:
  - Tutorial
tags:
- Acoustic_waves
- Piezoelectricity
- Nanofab
toc: true
toc_sticky: True
use_math: true
header:
  cover: /assets/images/2025/mech_wave_transduction/White1965-SAW.png
  overlay_image: /assets/images/2025/mech_wave_transduction/White1965-SAW.png
  show_overlay_excerpt: false
  overlay_filter: 0.5
---

This is meant to be a short rant, as well as share the lesson I learnt from my colleagues about why it is tricky to make a good taper for mechanical waves (and they also wrote about it): you need to be careful about how is the mechanical mode guided / confined. Mechanical waves are a bit more weird than em waves. Hopefully it would also be useful for some folks.

So... where should I start? That's simple: why do we care about mechanical waves first, and why a waveguide, and why a wavelength-scale mechanical waveguide?

You might remember sound wave in air is a bit more than 300 m/s, which is SIX orders of magnitude slower than light. It turns out it is not that different in solids, and surfaces of solids: few thousands meters per second to sometimes a bit more than 10,000 m/s. Let's say 3,000 m/s, which is FIVE orders of magnitude slower than light. Why are you boasting about it being slow? Well, slow means its wavelength is much shorter than the corresponding electromegnetic waves at the same frequency. Hmm, isn't this making it more annoying to play with? Yes, but it also makes the devices much smaller. You could make smaller resonators, smaller filters, and even smaller amplifiers (maybe).

Here is a random surface acoustic wave (SAW) filter from Kyocera with 1.3 dB insertion loss around 1.2 GHz, that is only 1.1 mm x 0.9 mm x 0.6 mm. ([SF11-1192M5UUA1](https://ele.kyocera.com/en/product/saw-device/saw_filters/sf11/sf11-1192m5uua1/))
<div style="display: flex; justify-content: space-between;">
    <img src="/assets/images/2025/mech_wave_transduction/SF11.png" alt="SAW-SF11" style="max-width: 48%;"/>
    <img src="/assets/images/2025/mech_wave_transduction/SF11-1192M5UUA1_DS-S21.png" alt="SAW-S21" style="max-width: 48%;"/>
</div>

Look how clean this S21 curve is!!

Ok back to the point, which is, the electromagnetic waves around this frequency would have a wavelength of 0.3 m, way way bigger than these devices. Even with some crazy high dielectric constant ceramics, it would still be ~> 10 mm. Hence small size is one big motivation for dealing with mechanical waves and resonances. In addition to SAW, there are also [bulk acoustic waves (BAW)](https://www.qorvo.com/innovation/technology/baw), and [FBAR](https://en.wikipedia.org/wiki/Thin-film_bulk_acoustic_resonator). (Please pronounce them as saw and baw, instead of S-A-W or B-A-W.)
- there are a few other advantages, including they have higher quanlity factors, can be used for sensing because they are sensitive to contact, mass etc., and could be more robust or more stable.
- the acoustic wavelength at 1 GHz would be ~ 3 um, why is this SAW filter still much much bigger than the acoustic wavelength? Well it takes a bit more than the length of a single bullet-point to explain, so a quick answer will be provided in the next section.


Next, why a waveguide, and a wavelength-scale waveguide? As the name suggests, you could guide the wave, and thus you could do more fun stuff such as bending the waves around, make it circulating in a ring/racetrack, make directional couplers, have more spatial channels without diffraction, all the usual waveguide stuff. 

![Mayor2020](/assets/images/2025/mech_wave_transduction/Mayor2020.png)
- here is a wavelength-scale mechanical waveguide and racetrack resonator my friends and I made ([see](https://ntt-research.com/wp-content/uploads/2022/09/Gigahertz-phononic-integrated-circuits-on-thin-film-lithium-niobate-on-sapphire1.pdf))
- We "cheated" and used relative transmission, shame on us. (we did not cheat for the S21 in Fig. 3)

Making the waveguide wavelength-scale (or even subwavelength scale) further helps concentrating the energy, and is useful for nonlinear applications, and quantum applications, where things scale faster with power density or field amplitude, or when you are limited to be playing with single [phonons](https://www.britannica.com/science/phonon) (this is a highly simplified explanation of why quantum applications need smaller modes).
- One [recent example](https://arxiv.org/abs/2503.09946) is the observation of acoustic [Purcell effect](https://en.wikipedia.org/wiki/Purcell_effect) of a color-center coupled to a nanomechanical resonator
- See the $$Q/V$$ factor from the Purcell effect? The smaller your resonator is, and the higher Q it is, the stronger the effect.
![Joe2025](/assets/images/2025/mech_wave_transduction/Joe2025.png)

# Why do we need big transducers

Hint: the [cover image](https://doi.org/10.1063/1.1754276).

(To be continued)


# Tapering the width of a mechanical waveguide
([see also](https://x.com/jwt0625/status/1905499644958048363))

<div style="display: flex; justify-content: space-between;">
    <img src="/assets/images/2025/mech_wave_transduction/mode_anime_free_20250327.gif" alt="taper-free" style="max-width: 48%;"/>
    <img src="/assets/images/2025/mech_wave_transduction/mode_anime_soft_fixed_20250327.gif" alt="taper-fixed" style="max-width: 48%;"/>
</div>

The above two animations are the fundamental mechanical shear mode in a 2D waveguide toy model, and how the mode evolve when you make the waveguide wider. The modes for the narrowest and widest cases are included here so you could see them actually moving.


The left one has free boundary conditions, and as you make the waveguides wider, the mode stays at the boundaries. If you put the IDT at the center of the wide waveguide, it is not going to excite the mode well. As a result, it won't be able to excite the narrow waveguide mode well.


<div style="display: flex; justify-content: space-between;">
    <img src="/assets/images/2025/mech_wave_transduction/mode1_narrow_dde_free_20250327.gif" alt="taper-free" style="max-width: 48%;"/>
    <img src="/assets/images/2025/mech_wave_transduction/mode1_wide_dde_free_20250327.gif" alt="taper-fixed" style="max-width: 48%;"/>
</div>


Then how does an rf horn antenna for em waves work? Because the metal boundary is a "hard" or "fixed" boundary for the em waves.

I did the exact same for the second case above, where the mechanical wave is "clamped" by materials with higher acoustic velocity. Now when you make the waveguide wider, the mode would actually stay inside instead of at the edge because the edge is no longer softer, and it will fill the whole waveguide.


<div style="display: flex; justify-content: space-between;">
    <img src="/assets/images/2025/mech_wave_transduction/mode1_narrow_dde_soft_fixed_20250327.gif" alt="taper-free" style="max-width: 48%;"/>
    <img src="/assets/images/2025/mech_wave_transduction/mode1_wide_dde_soft_fixed_20250327.gif" alt="taper-fixed" style="max-width: 48%;"/>
</div>



In this case, you can fill the wide waveguide with IDT and it will excite the narrow waveguide well after you taper down the waveguide width.



Here is one example of the second case, where the boundary is hard. The acoustic wave is confined by the SiN layer to the openings, because "the acoustic velocity (index) of SiN is greater (smaller) than that of LN". Thus the straight taper performed quite decent, they got 10% S21 when the device is cold, which is >30% single sided including the taper. That's pretty good given the IDT is not unidirectional.
![Shao2020](/assets/images/2025/mech_wave_transduction/Shao2022.jpeg)
- Shao2022: [Electrical control of surface acoustic waves](https://doi.org/10.1038/s41928-022-00773-3)


There are some examples of wide IDTs with poor efficiency into a narrow waveguide mode if you got good eyes.

Here is a more technical description of what's happening in the gif. When you make the waveguide wider, the fundamental shear that you might be trying to excite will become almost degenerate with the first order shear, and they'll both become the "edge" modes of the wide waveguide, and have poor overlap with a wide IDT.

To get around this, a longer and slower taper won't help. You could stop when the waveguide have not got too wide, or have a non-adiabatic taper, i.e., a focusing IDT.
![Dahmani2020](/assets/images/2025/mech_wave_transduction/Dahmani2020.png)
- Dahmani2020: [Piezoelectric Transduction of a Wavelength-Scale Mechanical Waveguide](https://doi.org/10.1103/PhysRevApplied.13.024069)


I'll finish my rant with, don't trust the waveguide S21 if you don't see the waveguide being released/separated from the bulk substrate, or making bends. The S21 could be well from the surface acoustic waves instead of actually being guided in the narrow waveguide.


# Examples of how to not excite a tiny mechanical waveguide


(To be continued)


