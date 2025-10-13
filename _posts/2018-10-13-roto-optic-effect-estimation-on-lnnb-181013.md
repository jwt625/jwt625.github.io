---
categories:
- Research
date: '2018-10-13'
header:
  cover: /assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image8.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image8.png
  show_overlay_excerpt: false
original_date: '2018-10-13'
tags:
- Simulation
title: Roto-optic effect estimation on LNNB
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2018-10-13, converted on 2025-10-12. )

# Inspecting model FBH_GA180723_2_ind207.mph
Color: eYY (source of most photoelastic contribution), arrow: disp field

![Image 14](/assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image14.png)

Plotting solid.curlUZ ( = dv/dx-du/dy):

![Image 15](/assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image15.png)

- max curlUZ comparable to max eYY
- regardless of the negative sign of this rotation field in x \< 0 and x \> 0 region, the effect on ![Image 1](/assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image1.png) from the two regions still adds up
solid.curlUY:

![Image 12](/assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image12.png)

# Consider roto-optic effect only from anisotropic refractive index:
Small rotation from ![Image 2](/assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image2.png) is:
I + dR = ![Image 13](/assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image13.png), this matrix is rotating the quantity expressed in the rotated coordinate system back to the global/original coordinate system
Change in permittivity:

![Image 3](/assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image3.png)

For LN, ![Image 4](/assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image4.png), ![Image 5](/assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image5.png)
- i.e., roto-optic effect from anisotropic refractive index only leads to off-diagonal permittivity change and is propto how anisotropic the permittivity is
Function that generates overlap integral expr:
- \expr\ = rto_expr_universal(\n_o\^2, n_o\^2, n_e\^2\, 'solid',\90;90;0\,{'pec','none',''});
COMSOL tells me g from roto-optic effect = 0.7 kHz/sqrt(2).
### Order of magnitude estimation:
- max(![Image 6](/assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image6.png)) and max(![Image 7](/assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image7.png)) are on the same order of magnitude
- for photoelastic effect,   ![Image 8](/assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image8.png)
- for roto-optic effect and this geom config, ![Image 9](/assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image9.png)
- ![Image 10](/assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image10.png)
- ![Image 11](/assets/images/imported/roto-optic-effect-estimation-on-lnnb-181013/image11.png)
- hence g_RTO \<\~ 4% g_PE
- max of curlUz is also further away from the defect/EM field center