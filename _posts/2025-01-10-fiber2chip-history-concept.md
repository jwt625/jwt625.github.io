---
title: "Get light onto a photonic chip: history and concepts"
categories:
  - Tutorial
tags:
    - Photonics
    - Optics
    - Fiber
toc: true
toc_sticky: true
use_math: true
header:
  overlay_image: /assets/images/2025/Photonics_history/photonics_history_cover.png
  cover: /assets/images/2025/Photonics_history/photonics_history_cover.png
  show_overlay_excerpt: false
  overlay_filter: 0.5
---


Light is good. It brings the energy and entropy for life, and it also runs the information around the internet backbone, and carries this little writing to your eyes, both abstractively and literally lol. Light is also naughty, it has many forms, scales, and could go everywhere, so there are a lot of things that need to be done right if you want to tame it for your own good. 

![info_flow_with_light](/assets/images/2025/Photonics_history/info_flow_with_light.png)
*This was actually the second slide from my defense lol. Fits here perfectly excluding the acoustic part.*

What would you expect from this writing? I'm trying to make it as easy to digest and take on as possible, with minimal assumptions on background knowledge, while covering the essense and basics. Most of physics and optics are intuitive to understand (if you try hard enough), and the useful ones always have a daily life analogy, like a Q-switched laser works the same way as how your toilet flushes (ok this example is probably stretching it but you get the point).

You'd be surprised sometimes how oblivious some of the academic or industry experts are about the basics (to be fair many of the basics are far from trivial to understand and straightforward to see behind the complexity), to the extent that occasionally people will come together and review e.g. [what is — and what is not — an optical isolator](https://www.nature.com/articles/nphoton.2013.185). 

One way to get back to the basics is to tell them to more people and broader audience, and this is what I'll try to do here, starting from what is light, how to guide it, why do we want it on a chip, and how to get it onto a chip.
- You'll also find that I could not explain some of the basic concepts well, and some of them would even lead to philosophical discussions. I'd say for now choose your belief and move on, and come back to your doubts when you got time to kill in a nice sunny weekend afternoon.

Lastly, I'm writing this also because I want to collect some of the readings into a more coherent collection, and for fun, so do not take what I wrote here seriously, and always do your own research! Although this is not intended for peer review, please do let me know if you've found errors, what you like and don't like about it! Oh also if you are curious, there is a section for stuff in the [cover image](#cover-image).


# What is light?

## Shaking a point charge

> What's in this section: Maxwell's equation, wave, radiation, polarization

People usually start talking about light as electromagnetic wave resulting from Maxwell's equations, with Heaviside's notation ([that got objected by math people at the time and rejected one of his submissions](https://doi.org/10.1063/PT.3.1788)). Let's take a look at [Maxwell's version](https://royalsocietypublishing.org/doi/abs/10.1098/rstl.1865.0008) as he wrote it down in 1865, actually just the quantities and symbols involved:
![maxwell1864-quantities](/assets/images/2025/Photonics_history/maxwell1864-quantities.png)

Hell no, 20 variables and 20 equations. I don't know about you, I cannot deal with equations with more than 20 different symbols, not to mention 20 equations for 20 variables. The takeaway here? Heaviside's [vector calculus](https://en.wikipedia.org/wiki/Vector_calculus) notation is good, and electromagnetism could be really complicated. There are multiple vector fields involved, as well as their distributions and evolutions in **time** and **space**. But as Maxwell mentioned, in many scenarios, only a few equations are required. This is a good way to approach a complex and general problem, find a special & simplified case, for example: a point charge.


So why and how does an accelerating point charge radiate? Let's cheat the math with some more advanced knowledge: special relativity, and more specifically, no information travels faster than light.
- This kind of "cheating" is my favorite & here is another example (in this case cheat trigonometry with a bit advanced math): to prove $$f(\theta) = \sin^2\theta + \cos^2\theta = 1$$, you can take the derivative $$f'(\theta)$$ and find out it's zero, and thus $$f(\theta) = f(0) = 1$$.
- To be more precise, we are defining $\sin$ and $\cos$ as the components of the solution of a first order differential equation for a vector $$ x' = Ax$$, where matrix $$A = \begin{bmatrix}
0 & -1 \\
1 & 0
\end{bmatrix}$$, and with initial condition $$x_0 = \begin{bmatrix}
1 \\
0
\end{bmatrix}$$.
- Why bother with all these? If you are math pilled, you should recognize the Lie group and Lie algebra of a 2D rotation from above, which can also be represented by a complex phasor that is used all the time for a traveling wave. If I ever get to coupled mode theory in a later blog (math for two traveling waves with crosstalk), you'll find it is pretty much this rotation but in 4D.
- Apologize for derailing.. Let's come back to the charge.

Let's say we know the static electric field (E field) of the charge points out straight, which should be the case immediately before and after its velocity gets kicked (acceleration impulse). Special relativity then says this change is moving out at maximum the speed of light, see the animation below.

![charge_kick_field_line.gif](/assets/images/2025/Photonics_history/charge_kick_field_line.gif)
*A nice demo showing the E field line from a moving charge suddenly accelerated from a velocity of 0.5c to 0.6c. [Radiation Pulse from an Accelerated Point Charge](https://demonstrations.wolfram.com/RadiationPulseFromAnAcceleratedPointCharge/). I swear I remember seeing this also in [Feynman lecture](https://www.feynmanlectures.caltech.edu/II_26.html#Ch26-S2) but I cannot find it anymore.*


You might say, why are we jumping ahead and talking about speed of light already while still trying to describe light as a wave? Well I really like this example so I'm going to impose my preference on you lol. But also you could read a lot of more useful information out of this simple example. There is no kink in the field line along the direction of the velocity jump (the acceleration), in other words, if the charge accelerates towards or away from you, you don't get any radiated field. You only get to feel it when the acceleration has a component in the plane perpendicular to your line of sight to it.
- This plane has two degrees of freedom, and this corresponds to the two transverse [polarization](https://en.wikipedia.org/wiki/Polarization_(waves)) degrees of freedom of light.
- There is no longitudinal polarization (longitudinal = field is parallel to the line from the source to you). If you see a "longitudinal" component, it must be from a different source than the one you thought it was from.
- You could have the charge moving back and forth along a line, and you get linearly polarized light. Having it move in a circle, or an ellipse, you get circular or mixed polarization.

Now we could imagine and see the charge gets kicked once, the next step is to keep kicking it back and forth so that we could maintain the outgoing wave. Here is an example:

![charge_em](/assets/images/2025/Photonics_history/charge_em_radiation.gif)
*Animation from [Javalab - Electromagnetic Wave](https://javalab.org/en/electromagnetic_wave_en/).*

You can see the E field is oriented vertically on the equator plane. As you move up or down, the polarization would change correspondingly so that it is always projected to be perpendicular to the line from the source to you, and gone when you are at the north or south pole. Sounds familiar? This is the same far field radiation pattern of an infinitely small dipole antenna, $$\vec E\propto \sin\theta  \cdot \hat\theta$$, where $$\theta$$ is the polar angle, angle from the $$z$$-axis.
- Wondering why I'm talking about polarization so much? It could bring you so much trouble if you are not careful about it. Better get you familiar with it because we will talk about it again and again.
- It is surprising how much you could already intuitively understand from a simple shaking charge (or a dipole). Actually I got an exercise for you to use it a bit more.
- **Exercise 1** (can't believe I'm doing this, putting exercise in my blog lol): use the intuition of the simple shaking charge, explain the [polarization distribution of the blue sky](https://en.wikipedia.org/wiki/Rayleigh_sky_model). *Hint: scattering of light is when light shakes another charge along the direction of the polarization of the incident lightwave.*

![mapdeg](/assets/images/2025/Photonics_history/Mapdeg-ortho.gif)

*The degree of polarization on the celestial sphere ([source](https://en.wikipedia.org/wiki/Rayleigh_sky_model#/media/File:Mapdeg-ortho.gif)). Red is high and black is low.*


Before we move on, there is one more fun thing to think about this simple point charge picture: the above radiation animation properly has a generator attached, as the radiation carries energy away and should slow down the oscillation of the charge, and we'd need energy input to keep it going. Does this mean if it's just a charge attached to a spring and oscillating like a mechanical oscillator, it should experience a damping force from the radiated field? What is breaking the time reversal symmetry here since Maxwell's equation does not have the arrow of time preference?
- Most of the time you could just accept the fact that there will be damping when things radiate, and life goes on fine. Think about this do let you come up with ways to play with how things could radiate.
- One way to answer this is, it is the statistical mechanics of [how the radiator interact with the absorber](https://doi.org/10.1103/RevModPhys.17.157), and the stat mech part is where the arrow of time comes in. Infinite space is also an absorber, just like an infinitely long transmission line is a resistor of its characteristic impedance.
- As a result, if the radiator sees a different environment or different absorbers, its rate of radiation could be totally different (aka [Purcell effect](https://en.wikipedia.org/wiki/Purcell_effect)). This effect is widely used from better emitters (esp. the quantum ones that emit one photon at a time), to improving solar cell efficiency and better lasers.



## How to actually shake the charge(s)

> What's in this section: thermal radiation, spectrum, spectral lines

In the previous section, we showed an oscillating charge, presumably driven by a "function generator". While this is common for lower frequencies, it's a different level of effort to push electronics and oscillators to THz, as one of my friend would like to put it, nature is a low-pass filter: you get self-resonances, skin effect, higher dielectric loss... Anyway doing the shaking at a few hundred THz is hard.

How does nature (as well as us, initially) do it? Heat stuff up! Actually as long as stuff is not at zero temperature, the atoms and electrons are always shaking and exchanging photons.
- Not exactly in the way we described above tho, but let's not get into the quantum stuff for now. 

![Gd_cube](/assets/images/2025/Photonics_history/Gd_cube_thermal.jpeg)

*Here is a thermal image of a cold gadolinium cube.*

Let's get some sense of temperature vs thermal radiation. I won't pretend to be a stat mech expert, so let's take it as a fact that we have these nice fundamental constants that let us convert between different units. Between temperature and frequency? No problem, we'll get the correct unit from Boltzmann constant divided by Planck constant, $$ k_B/h = 2\times10^{10} $$ Hz/K, and it will tell us the thermal radiation frequency or wavelength at given temperature. At room temperature, we get ~ 6 THz, or ~ 45 um. At the surface temperature of our sun, ~ 5800 K, we get ~ 120 THz, or ~ 2.5 um. Naive calculations get us within one order of magnitude, since room-T thermal is more around 10 um, and sun light is more peaked around 500 nm. There is an extra factor of ~ 5 needed from the math of [Planck's law](https://en.wikipedia.org/wiki/Planck%27s_law) of black body radiation. Can't cheat all the way with units, gotta do the hard work to get the "order of unity" factor.

![black_body](/assets/images/2025/Photonics_history/Black_body.svg)
*Black body radiation spectrum ([wikipedia](https://en.wikipedia.org/wiki/Planck%27s_law#/media/File:Black_body.svg)).*

This thermal radiation has been the light source of our daily life for a long time, both outdoor & natural and indoor, until quite recently. It is also used as light source for infrared (IR) spectroscopy, aka [globar](https://en.wikipedia.org/wiki/Globar), because it is literally a glowing bar. In terms of evolution of light source, wikipedia has a nice [Timeline of lighting technology](https://en.wikipedia.org/wiki/Timeline_of_lighting_technology).

In terms of spectrum, even our oldest light source, fire, is already a bit more complicated than black body. There will be emission peaks from molecular vibration modes, and electronic transitions if you sprinkle some elements especially metal elements. These are specific frequencies the atoms or electrons are "shaking" at. Similar [spectral lines from the stars](https://en.wikipedia.org/wiki/Fraunhofer_lines) were observed and really confused people, and explaining them was one of the initial motivation and triumph of quantum mechanics.

![emission_lines](/assets/images/2025/Photonics_history/FlameEmissionSpectroscopy.png)

*The line spectra from the flame emission spectroscopy of several metals ([source](https://keystagewiki.com/index.php/File:FlameEmissionSpectroscopy.png)).*


Thermal light is good and even preferred for a lot of stuff, but it is too generous, it is not "discriminative" enough, in terms of all aspects about light: spectrum, spatial distribution, orientation, duration. In short, it spreads the energy into too many modes.
- We'll get to what is a mode soon (spoiler: what it means won't be very clear and highly depends on the context).

Its entropy is too high, which is destined to be the case as it is "thermal". Meanwhile, low entropy is desired if you want to use light to send information (communication, during which its entropy is increased) or extract information from things (sensing, spectroscopy). 

## And shake them really well: lasers

> What's in this section: boson, stimulated emission, [laser](https://history.aip.org/exhibits/laser/index.html) (this is a really good historical review)

How can we do better and get good low-entropy light? Remember those spectral lines, those might be useful! There is also another blessing for us: light, or photons, are [bosons](https://en.wikipedia.org/wiki/Boson). What do you think being bosons mean? Party? No, it means we are staying together, whenever it is possible, no matter heaven or hell, or superposition of both. I'm taking about this because I like to think about this as one of the fundamental reasons why lasers would work generating a "clean" state of light.

Here is an example of photons being bosons: when you send single photons to a 50:50 [beam splitter](https://www.edmundoptics.com/knowledge-center/application-notes/optics/what-are-beamsplitters/), which is just a half-transparent half-reflective piece of glass at an angle of 45 degree (I thought about making the drawings, but [this blog](https://galileo-unbound.blog/2022/05/08/the-many-worlds-of-the-quantum-beam-splitter/) perfectly captured the two cases I wanted to include here):
- When you send just one photon to one of the two input channels:
- ![single_photon_BS](/assets/images/2025/Photonics_history/quantum1photonbs-1.webp)
- Look we have "modes" again, more on them later.
- Don't be afraid of the symbols, the $$\vert 00 \rangle $$ etc. is just how quantum people count and write number of photons, and the $$a_i$$ ($$a_i^\dagger$$) are used to subtract (add) photons. The beam splitter transforms the "add" operation, and the result is, single photon in, output photon is in a superposition state of the two paths: it could be either in output 1 or output 2, until you measure it.
- Does this seem weird to you? It will start to feel reasonable once you've worked with quantum stuff like this for a while. However, the following still feels weird and even messed up to me, that is, when you send two photons, one for each of the input ports:
- ![two_photons_BS](/assets/images/2025/Photonics_history/hom2.webp)
- Do you see what's going on here? They freaking always get out at the same output port, albeit as a superposition / entanglement of the two output ports. This is weird. It's weird. It's so weird.
- This is what it means to be bosons. You all-in with your fellow bosons.
- **Exercise 2**: what happens when you send a two-photon state to each of the input of the 50:50 beam splitter? What gets out of it? No need to get the coefficients right, just get what are the states that get entangled. *Hint: operators for different modes commute with each other, i.e., $$a_1^\dagger a_2^\dagger = a_2^\dagger a_1^\dagger$$*.

The funny thing is, with all the setup of the bosonic behavior above, the state of light of a laser is not even number states, it is [coherent states](https://en.wikipedia.org/wiki/Coherent_state), and coherent states do not have the above behavior at all (which is also weird and messed up, if you are interested, it's briefly discussed in the blog cited above).
- This "coherent" is related to how "coherent" is used for describing coherence of a signal, but has a very specific meaning in "coherent state".
- It is a big state ("big" as far from origin in phase space) where the uncertainty is isotropic in amplitude and phase, and minimally allowed by quantum mechanics.

![coherent_state](/assets/images/2025/Photonics_history/coherent_state.png)
*A classical signal represented by a phasor $$\alpha$$, with amplitude $$\vert \alpha \vert$$ and phase $$\phi$$, and the corresponding coherent state.*

Ok we are getting distracted again. The point I am trying to make is that, particles that light is made of, aka photons, are bosons, and they like to stick together when you try to mix them. This picture or intuition matches with so called [stimulated emission](https://en.wikipedia.org/wiki/Stimulated_emission), or [Einstrahlung](https://einsteinpapers.press.princeton.edu/vol6-trans/232), the "hypotheses" Einstein used to derive the Planck distribution in a very simple way. So now we just need to use one of those already kind of sharp absorption and emission lines, and somehow make the photons "stick together" more, we would get really good light, we would have a laser. But how?

Turns out we just need two more things:
1. Feedback: to remind the emitters -- the "shaking charges", what it was emitting, so that it emits the same "stuff".
2. Population inversion: light also shake the emitters and gets absorbed. We need more excited emitters than non-excited ones, so that the stimulated emission wins over absorption.

**Feedback**: this part is easy: mirrors. Make two mirrors facing each other, light would bounce back and forth, and keep reminding the emitters to behave properly. Congrats, now you got an [optical cavity](https://en.wikipedia.org/wiki/Optical_cavity) or optical resonator (but you gotta be careful to have a properly working one). This resonator also defines what I mean when I wrote "stuff" above: it means the optical modes supported by the resonator. Oh, modes, I promise more on it in the next section!

![laser-cavity](/assets/images/2025/Photonics_history/Laser_resonator_stability.svg)
*Stability of a laser cavity: have the mirror focus a bit helps relaxing the constraint on how parallel they are. ([source](https://commons.wikimedia.org/wiki/File:Laser_resonator_stability.svg))*

**Population inversion**: this is a bit more involving, since if you drive the vibration/transition resonantly, you would end up getting half and half. Same with temperature, thanks to statistical mechanics and thermal equilibrium, the lower energy states always have more population than the higher energy states, except if the temperature could be somehow "negative". Well that just means the distribution is not at thermal equilibrium.
- A common way to escape from equilibrium is to involve more states with different energy levels, such as three (or more). Let's call them $$g$$, $$e$$, and $$f$$ from lower to higher energy.
- If we shake a thing (e.g. doped chromium in a ruby crystal) up from $$g$$ to $$f$$, and it drops from $$f$$ to $$e$$ real fast (e.g. thru [phonons (crystal lattice vibrations)](https://www.rp-photonics.com/spotlight_2018_04_06.html)), then we could keep shaking the $$g$$ to $$f$$ to $$e$$ without the "half & half" limit. Population (between $$g$$ and $$e$$) inverted!

![laser-cavity-3-level](/assets/images/2025/Photonics_history/SUPR-laser-shirt.png)
*One of my [SUPR](https://photons.stanford.edu/supr) shirt showing the laser cavity with two mirrors on the left and right, and three levels, with an upward arrow representing the $$g$$ to $$f$$ pumping, and a downward arrow for the laser transition. Light bouncing and emitting (thru the right mirror) are drawn as the three horizontal lines.*

Ok we finally get the laser working. Why bother going thru this? Aren't you supposed to be talking about fibers and chips? I dunno, maybe I'm stubborn, maybe I want to show off my skill of yapping. But I do like the journey to reach the point where we can say, "here is a plane wave at frequency $$\omega$$", with confidence we could actually have something close. You don't get a plane wave out of imagination, and perfectly at a single frequency! It took us humans a long journey, a ton of effort ~~and [decades of legal battle](https://history.aip.org/exhibits/laser/index.html)~~, to get such a nice lightwave, albeit still far from a single frequency plane wave. There are always [larger beams](https://opg.optica.org/ol/abstract.cfm?uri=ol-41-4-840) to make, and narrower and stabler lasers to make, and you can do amazing things with them.

![CBC](/assets/images/2025/Photonics_history/CBC-P3120029-2-1.jpg)
*Coherent Beam Combining for [high beam quality and >150 kW of power](https://www.powerphotonic.com/powerphotonics-coherent-beam-combining-module-solves-key-challenges-of-high-energy-lasers/). This is the opposite of fibers and chips, I'm just a fan of big lasers.*

One last thing before we move on, why does a laser output the coherent state of the lasing mode? I still do not have a simple and intuitive microscopic picture for its mechanism after hours of daydreaming. If you have a good explanation, let me know! What I could offer for now is a loose argument for that it has to be the case, only using what we have talked about above:
- The lightwave is constantly exchanging photons with the emitters, while being in "equilibrium". This means its state has to be unchanged by the add/subtract operator $$a^\dagger$$ and $$a$$, i.e., its eigen states. The eigen states of the operators are coherent states.
- The light is also constantly bouncing off the mirrors, some of which gets out of the output mirror. Sounds familiar? This is a beam splitter, although usually not 50:50. If you did the exercise above, you'll find the output of a beam splitter is messy and entangled, and gets worse for "larger" states. Any states that do not get messed up when going thru or bouncing off a beam splitter? Coherent states.


# Watch the light, and guide the light

## Where is the light going?

> What's in this section: diffraction, refraction, reflection, absorption, nonlinearity


## I want it this way, no no this way, yes yes yes, and then this way

> What's in this section: total internal reflection, waveguides, modes, bands


# Finally, get onto the chip


## Ok what do you have on the chip? (historic review)

> What's in this section: thin film light guides, planar lightwave circuits, silicon photonics


## Let me in!

> What's in this section: prism coupling, tapered fiber, grating coupler, butt coupling / edge coupler / inverse taper


(To be continued...)


# Appendix

## Cover image

Here are where the devices and chips in the cover image are from, from left to right:
![photonics_history_cover](/assets/images/2025/Photonics_history/photonics_history_cover.png)

Column 1:
- Colladon1842: [On the reflections of a ray of light inside a parabolic liquid stream](https://web.archive.org/web/20140222223427/http://www.ville-ge.ch/mhs/pdf/aide_colladon.pdf)
- Hopkins1954: [A Flexible Fibrescope, using Static Scanning](https://www.nature.com/articles/173039b0)

Column 2:
- Maiman1960: [HRL Laboratories Celebrates 60th Anniversary of First Laser](https://www.hrl.com/news/2020/05/11/hrl-laboratories-celebrates-60th-anniversary-of-first-laser)
- Berreman1965: [Convective Gas Light Guides or Lens Trains for Optical Beam Transmission](https://doi.org/10.1364/JOSA.55.000239)
- Tien1971: [Light Waves in Thin Films and Integrated Optics](https://doi.org/10.1364/AO.10.002395)
- Soref1986: [All-silicon active and passive guided-wave components for λ= 1.3 and 1.6 µm](https://doi.org/10.1109/JQE.1986.1073057)

Column 3:
- Ilchenko1999: [Pigtailing the high-Q microsphere cavity: a simple fiber coupler for optical whispering-gallery modes](https://doi.org/10.1364/OL.24.000723)
- Cai2000: [Observation of Critical Coupling in a Fiber Taper to a Silica-Microsphere Whispering-Gallery Mode System](https://doi.org/10.1103/PhysRevLett.85.74)
- Waldhäusl1997: [Efficient coupling into polymer waveguides by gratings](https://doi.org/10.1364/AO.36.009383)
- Roelkens2005: [Efficient silicon-on-insulator fiber coupler fabricated using 248-nm-deep UV lithography](https://doi.org/10.1109/LPT.2005.859132)

Column 4:
- Doerr2008: [9 - Planar lightwave circuits in fiber-optic communications](https://doi.org/10.1016/B978-0-12-374171-4.00009-5)
- Murakowski2024: [Ultra-Wideband RF-Photonics Technology for Microwave Spectrometry](https://doi.org/10.1109/JSTARS.2024.3452033)
