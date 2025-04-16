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

# Why do we need big transducers?

Hint: the [cover image](https://doi.org/10.1063/1.1754276).

The short answer is [impedance matching](https://en.wikipedia.org/wiki/Impedance_matching). More specifically, (almost) everyone uses a 50 Ohms transmission line for RF and microwave, and it is hard to achieve a 50 Ohms impedance with a small transducer.

Why is it hard to get to 50 Ohms with a small transducer? I actually have a relatively simple explanation when I was scratching my head thinking about how to explain this for my thesis defense. We need a simple method to estimate the impedance of a transducer, and the basic concept of impedance actually leads us the way:
- What is [impedance](https://en.wikipedia.org/wiki/Electrical_impedance)? The EEs reading this blog should be familiar with the impedance of a capacitor $$Z_C = 1/(i\omega C)$$, and of an inductor $$ Z_L = i\omega L $$. A resistor's impedance would be the same as its resistance.
- You could immediately recognize that if an element does not dissipate / consume energy, its impedance would be fully imaginary. How does a piezoelectric transducer "consume" energy, or more accurately, convert electrical energy to acoustic energy? It shows different dielectric constant with different mechanical boundary conditions.

![piezo-coupling-illustration](/assets/images/2025/mech_wave_transduction/piezo-coupling-illustration.png)

Here is a figure from one of my favorite standard ([1987 - IEEE Standard on Piezoelectricity](https://doi.org/10.1109/IEEESTD.1988.79638), [also here](/assets/doc/2025/00026560-IEEE-1987-standard-piezoelectricity.pdf)) on how to do mechanical work with piezoelectric materials, illustrated in (b). You have two lines with different slopes between D and E field, which correspond to the two different dielectric constant for fixed and free mechanical boundary conditions. And the shaded area between the two straight lines give you the mechanical work you extracted by charging and discharging this piece of piezoelectric material at different mechanical boundary conditions.

Now time for some hand-wavy math. We know the capacitance of a parallel capacitor, and thus its admittance (inverse of impedance): 

<div style="text-align: center;">
$$Y = i\omega C = i\omega \frac{\epsilon_0 \epsilon_\text{r} A}{d},$$
</div>
where $$A$$ is the area, and $$d$$ is the separation between the parallel plates. Now we have two different dielectric constant if the material is piezoelectric, and the difference gives us an estimation for the real part of the admittance:

<div style="text-align: center;">
$$G \sim \omega \frac{\epsilon_0 (\epsilon^\text{T}_\text{r}-\epsilon^\text{S}_\text{r}) A}{d}.$$
</div>

Now we could plug in some actual numbers to calculate the conductance.
- for a small piece of [lithium niobate (LN)](/assets/doc/2025/gaylord1985-bf00614817.pdf), which is a pretty good piezoelectric material, assume we would like a little chunk of it at the wavelength-scale for ~ 1 GHz mechanical waves, $$A \sim 1~\text{um}^2$$, $$d \sim 1~\text{um}$$, and $$\epsilon^\text{T}_\text{r} \sim 80$$, $$\epsilon^\text{S}_\text{r} \sim 40$$. We get $$G\sim 1/(450~\text{k}\Omega)$$.
- That is an insanely high impedance, and more than 99.9% of the power will be reflected.
- From the conductance formula, you could immediately see ways to improve it: increasing the area $$A$$, decrease the gap size $$d$$, and find materials with higher dielectric constant and higher dielectric constant difference (piezoelectricity). Higher dielectric constant is directly linked to stronger piezoelectric effect, as well as other effects such as electro-optic effect (see [Anderson2025](https://arxiv.org/abs/2502.15164)).
- Another knob available is the bandwidth of the transducer, making it higher Q or narrow bandwidth let's you bump up the peak conductance. It is easier to impedance match to a narrower bandwidth. Sounds like the [Bode-Fano Limit](https://web.ece.ucsb.edu/~long/ece145a/zmatch.pdf), right? (I have not thought much about the actual link here yet)

Here is an [actual example](https://link.aps.org/accepted/10.1103/PhysRevApplied.15.014039): 
![mayor2020-fig2](/assets/images/2025/mech_wave_transduction/Mayor2020-fig2.png)
- let's eyeball the area of this transducer, which is the ridge area that is covered by the IDT (interdigital transducer) electrodes, roughly 3 um x 10 um.
- The transducer has a Q of 400 or a bandwidth of ~ 10 MHz.
- These two factors bring down the ~450 kOhm number to ~38 Ohm, decently matched.

Let's find another example, here is a [film bulk acoustic resonator (FBAR)](https://spectrum.ieee.org/design-and-optimization-of-fbar-filters-to-enable-5g):
![fbar](/assets/images/2025/mech_wave_transduction/onscale-fbar.webp)
![fbar-xsec](/assets/images/2025/mech_wave_transduction/onscale-fbar-xsec.webp)
- It is made of aluminum nitride (AlN), which has lower dielectric constants and lower piezoelectric constants, let's say 10x smaller than LN. The area is 50 um x 50 um, and thickness is 1 um.
- The formula gives a real impedance of ~1800 Ohms. So making it a few percent of fractional bandwidth could roughly match it to 50 Ohms.
- Note that 50 um x 50 um is much larger than wavelength-scale.

Please be wary that the above order of magnitude calculation is extremely simplified, and good enough to serve the purpose of showing why we need big transducers. There is a lot more about how to properly model and understand piezoelectric transducers. You can read more in [Dahmani2020](https://doi.org/10.1103/PhysRevApplied.13.024069), as well as more generally [Butterworth-Van Dyke circuit](https://ieeexplore.ieee.org/document/922679), and the one I prefer: [Foster network synthesis](https://web.archive.org/web/20180719090643id_/https://link.aps.org/accepted/10.1103/PhysRevA.94.063864).

One more thing, I have mentioned [interdigital transducer (IDT)](https://en.wikipedia.org/wiki/Interdigital_transducer) without explaining it. The idea is simple. Remember at the beginning we talked a lot about how the E&M waves and the acoustic waves have orders of magnitude different velocity? If you make a parallel plate capacitor to transduce the mechanical wave, it will excite the bulk acoustic resonance like in the FBAR filter above, and won't excite acoustic waves that are traveling along the surface. The travelling wave would have alternating sign of amplitude, and cancels between the electrodes. To make then not cancel? Shape the electrodes with the same periodicity so that the E field flips sign and match with how the acoustic wave amplitude flips its sign, and you get an IDT.


# Tapering the width of a mechanical waveguide
([see also](https://x.com/jwt0625/status/1905499644958048363))

Ok now we understand the transducer need to be have a big enough area to support the impedance matching and bandwidth required, i.e., make it wider, and longer.

To excite a wavelength-scale waveguide with width comparable to the mechanical wavelength, the IDT region needs to be connected to the waveguide somehow, and the naive choice of a straight taper could get you in trouble.


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

Here is an example of a focusing IDT exciting a wavelength scale waveguide ([Peairs2020](https://doi.org/10.1103/PhysRevApplied.14.061001)):
![Peairs2020](/assets/images/2025/mech_wave_transduction/Peairs2020.png)

I'll finish my rant with, don't trust the waveguide S21 if you don't see the waveguide being released/separated from the bulk substrate, or making bends. The S21 could be well from the surface acoustic waves (SAW) instead of actually being guided in the narrow waveguide.


# Examples of how to not excite a tiny mechanical waveguide

(Hopefully no one reads my blog lol)

![Forsch2020](/assets/images/2025/mech_wave_transduction/Forsch2020.png)
- see that big IDT, and the small arrays of wavelength-scale structures near the bottom? The efficiency from the microwave shooting onto the IDT, to mechanical vibrations in one of the structures is about $$10^{-8}$$. (see [Forsch2020](https://www.nature.com/articles/s41567-019-0673-7) and also [here](https://arxiv.org/pdf/1812.07588))


![Ding2024](/assets/images/2025/mech_wave_transduction/Ding2024.png)
- This one looks like a 20+ um wide IDT with straight taper into a sub-um suspended waveguide. S21 about -50 dB. 
- They showed a version with an unreleased waveguide that has S21 approaching -20 dB, which I suspect it is mostly from the surface acoustic waves that are not in the sub-um waveguide (see [Ding2024](https://link.aps.org/accepted/10.1103/PhysRevApplied.21.014034))


![Deng2025](/assets/images/2025/mech_wave_transduction/Deng2025.png)
- This IDT is 100+ um wide and tapered to a ~4 um wide waveguide, and they measured an insertion loss of 10 dB from the taper. I'd suspect this taper loss is an upper bound (e.g. there's some SAW contributing to the S21) until they bend the waveguide by 90 degree.
- They even say the taper loss "can be further optimized by reducing the tapering angle", no please don't make it even slower. They do get the "adopting a focused IDT design" part. (see [Deng2025](https://arxiv.org/abs/2503.18113))


Conclusion? Be wary of $$\pm$$30 dB engineers/engineering. If you found one, help them be +30 dB instead of -30 dB.

