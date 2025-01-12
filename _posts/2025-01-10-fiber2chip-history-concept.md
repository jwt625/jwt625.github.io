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

You'd be surprised sometimes how oblivious some of the academic or industry experts are about the basics (to be fair many of the basics are far from trivial to understand and straightforward to see behind the complexity), to the extent that occasionally people will come together and review e.g. [what is — and what is not — an optical isolator](https://www.nature.com/articles/nphoton.2013.185). One way to get back to the basics is to tell them to more people and broader audience, and this is what I'll try to do here, starting from what is light, how to guide it, why do we want it on a chip, and how to get it onto a chip.

Lastly, I'm writing this also because I want to collect some of the readings into a more coherent collection, and for fun, so do not take what I wrote here seriously, and always do your own research! Although this is not intended for peer review, please do let me know if you've found errors, what you like and don't like about it! Oh also if you are curious, there is a section for stuff in the [cover image](#cover-image).


# What is light?

People usually start talking about light as electromagnetic wave resulting from Maxwell's equations, with Heaviside's notation ([that got objected by math people at the time and rejected one of his submissions](https://doi.org/10.1063/PT.3.1788)). Let's take a look at [Maxwell's version](https://royalsocietypublishing.org/doi/abs/10.1098/rstl.1865.0008), actually just the quantities and symbols involved:
![maxwell1864-quantities](/assets/images/2025/Photonics_history/maxwell1864-quantities.png)

Hell no, 20 variables and 20 equations. 

![charge_em](/assets/images/2025/Photonics_history/charge_em_radiation.gif)
[Javalab - Electromagnetic Wave](https://javalab.org/en/electromagnetic_wave_en/)

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
