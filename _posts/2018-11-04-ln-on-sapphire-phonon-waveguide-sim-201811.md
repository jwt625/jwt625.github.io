---
categories:
- Research
date: '2018-11-04'
header:
  cover: /assets/images/imported/ln-on-sapphire-phonon-waveguide-sim-201811/image8.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/ln-on-sapphire-phonon-waveguide-sim-201811/image8.png
  show_overlay_excerpt: false
original_date: '2018-11-04'
tags:
- Simulation
title: LN on Sapphire phonon waveguide sim
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2018-11-04, converted on 2025-10-12. )

[20181104, first try](#20181104-first-try)
[20181105, adding LN slab](#20181105-adding-ln-slab)

Path: `COMSOL/LN/mechanics`

# 20181104, first try

![Image 9](/assets/images/imported/ln-on-sapphire-phonon-waveguide-sim-201811/image9.png)

Default crystal orientation (i.e., same as global coord)
Fundamental mode very well confined.

![Image 4](/assets/images/imported/ln-on-sapphire-phonon-waveguide-sim-201811/image4.png)

10*log10(disp):

![Image 3](/assets/images/imported/ln-on-sapphire-phonon-waveguide-sim-201811/image3.png)

on a vertical cut line:

![Image 1](/assets/images/imported/ln-on-sapphire-phonon-waveguide-sim-201811/image1.png)

TODO
- band structure
- running (181105 11:30 AM)
- add LN slab
- use the correct cut for LN (maybe a minor effect on the modes?)
bands
- with fake manual symmetry:
- ![Image 10](/assets/images/imported/ln-on-sapphire-phonon-waveguide-sim-201811/image10.png)
- full geom (black):
- ![Image 2](/assets/images/imported/ln-on-sapphire-phonon-waveguide-sim-201811/image2.png)
# 20181105, adding LN slab
Model: `COMSOL/LN/mechanics/model_LiSa_slabWG_full_181105.mph`

Start using l = 200 nm, i.e., k_F = pi/l \~ 1.5e7
Trying t_slab = 200 nm LN slab (should be close to what we currently have), mode still very well confined:

![Image 5](/assets/images/imported/ln-on-sapphire-phonon-waveguide-sim-201811/image5.png)

![Image 8](/assets/images/imported/ln-on-sapphire-phonon-waveguide-sim-201811/image8.png)^[a](#cmnt1)[b](#cmnt2)[c](#cmnt3)[d](#cmnt4)[e](#cmnt5)[f](#cmnt6)^

Decay rate along z (blue) and y (green), for lowest freq mode:

![Image 6](/assets/images/imported/ln-on-sapphire-phonon-waveguide-sim-201811/image6.png)

Decay along z, different modes (1st, 5th, 10th, 15th, 20th):

![Image 7](/assets/images/imported/ln-on-sapphire-phonon-waveguide-sim-201811/image7.png)

decay along y, different modes (1st, 5th, 10th, 15th, 20th):
- 20 th is no longer confined

![Image 11](/assets/images/imported/ln-on-sapphire-phonon-waveguide-sim-201811/image11.png)

<!-- Internal discussion:
[a] Is this mode mostly longitudinal?
Here's this paper we talked about
https://www.osapublishing.org/oe/abstract.cfm?uri=oe-19-9-8285
We'll probably see similar as that paper, just need to inject sufficient power.

[b] (If the mode is mostly longitudinal, there's some simple expression only containing p12 that determines the interaction rate.)

[c] Just added the profile

[d] Is not so clear to me sorry, could you perhaps plot norm(u_z)/norm(u) with z along the waveguide?

[e] I'm also not sure. The profile looks like a horizontally polarized transverse mode, but volint of abs(eXX) is the largest. (X parallel to the WG)

[f] You can open and play with the model if you have time.
-->