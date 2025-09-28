---
categories:
- Tutorial
date: '2025-09-27'
original_date: '2018-04-28'
tags:
- Lithium Niobate
- Materials
- Piezoelectric
- Simulation
- Reference
title: Lithium Niobate properties
toc: true
toc_sticky: True
use_math: true
header:
  cover: /assets/images/imported/ln-properties/image25.png
  overlay_image: /assets/images/imported/ln-properties/image25.png
  show_overlay_excerpt: false
  overlay_filter: 0.5
---

( originally written on 2018-04-28, converted on 2025-09-27. )


# Material coordinates and symmetries
From Weis and Gaylord, Appl. Phys. A, 1985
Right: S. Sanna, W. Schmidt, PRB, 2010

![Image 77](/assets/images/imported/ln-properties/image77.png)

![Image 25](/assets/images/imported/ln-properties/image25.png)

## LNX chip and pieces orientation:
X-cut:

![Image 103](/assets/images/imported/ln-properties/image103.png)

![Image 67](/assets/images/imported/ln-properties/image67.png)

If
- nanobeams perpendicular to wafer flat
- nanobeam along x axis in COMSOL
Then
- rotated system and resulting material coordinates (called coordA):
- also call this nZYX, which means negative crystal Z along x and crystal Y along y
- ![Image 52](/assets/images/imported/ln-properties/image52.png)

![Image 42](/assets/images/imported/ln-properties/image42.png)

## Chris's LNX nanobeam orientation: YZX

![Image 115](/assets/images/imported/ln-properties/image115.png)

![Image 64](/assets/images/imported/ln-properties/image64.png)

## LNX 45 deg, 20181031

![Image 82](/assets/images/imported/ln-properties/image82.png)

![Image 28](/assets/images/imported/ln-properties/image28.png)

## LNY chip orientation (Y-cut)

![Image 73](/assets/images/imported/ln-properties/image73.png)

with X perp. to the NB:
- call this ZXY coordinate (which means crystal Z along x and crystal X along y)
- ![Image 60](/assets/images/imported/ln-properties/image60.png)

![Image 94](/assets/images/imported/ln-properties/image94.png)

- equiv to (pi/2, pi/2, 0)
- nanobeams (crystal Z) perp to long edge, i.e., long edge parallel to wafer flat
## old bender NB coordinate:
- careful! all old simulations (most 2018 April and pre-April sims) are with this coordinate!
# Permittivity, refractive index
From Weis and Gaylord, Appl. Phys. A, 1985

![Image 88](/assets/images/imported/ln-properties/image88.png)

![Image 44](/assets/images/imported/ln-properties/image44.png)

Superscript T: unclamped (low freq), S: clamped (high freq)
# Elasticity
From Weis and Gaylord, Appl. Phys. A, 1985

![Image 1](/assets/images/imported/ln-properties/image1.png)

![Image 38](/assets/images/imported/ln-properties/image38.png)

![Image 47](/assets/images/imported/ln-properties/image47.png)

In COMSOL:
- manually typed for PML, model: model_GA_20180413_mechSolved_PML_20180430

![Image 31](/assets/images/imported/ln-properties/image31.png)

- when scripting, COMSOL's convention for 6x6 symmetric D matrix:
- {D11, D12, D22, D13, D23, D33, ..., D56, D66}
From K. K. Wong, properties of LN:

![Image 79](/assets/images/imported/ln-properties/image79.png)+

![Image 51](/assets/images/imported/ln-properties/image51.png)

## Symmetry of c_ij and s_ij:
From John Nye, Properties of crystals, P. 136

![Image 68](/assets/images/imported/ln-properties/image68.png)

![Image 34](/assets/images/imported/ln-properties/image34.png)

# Electro-optic effect
From K. K. Wong, properties of LN

![Image 58](/assets/images/imported/ln-properties/image58.png)

![Image 118](/assets/images/imported/ln-properties/image118.png)

![Image 101](/assets/images/imported/ln-properties/image101.png)

![Image 104](/assets/images/imported/ln-properties/image104.png)

![Image 113](/assets/images/imported/ln-properties/image113.png)

![Image 53](/assets/images/imported/ln-properties/image53.png)

From Weis and Gaylord, Appl. Phys. A, 1985:

![Image 80](/assets/images/imported/ln-properties/image80.png)

There's one sign difference (r13) comparing to K. K. Wong?
- comparing to piezoelectric matrix, I trust Weis and Gaylord

![Image 96](/assets/images/imported/ln-properties/image96.png)

![Image 81](/assets/images/imported/ln-properties/image81.png)

Question: how the primary effect compare to converse piezoelectric + photoelastic effect?
Answer in Weis and Gaylord, Appl. Phys. A, 1985:
- This secondary linear electro-optic effect is the result of the applied electric field causing a strain in the crystal through the converse piezoelectric effect. This electrically induced strain then causes a change in the crystal's refractive index through the photoelastic effect
## Magnitude of second order E-O effect
- ![Image 2](/assets/images/imported/ln-properties/image2.png)
- ![Image 3](/assets/images/imported/ln-properties/image3.png)

![Image 91](/assets/images/imported/ln-properties/image91.png) while r_mat: ![Image 71](/assets/images/imported/ln-properties/image71.png)

- largest component \~ 1.3e-11 m/V
- largest first-order component \~ 3e-11 m/V
- comparable
## Electro-optic coupling

![Image 4](/assets/images/imported/ln-properties/image4.png)

![Image 5](/assets/images/imported/ln-properties/image5.png)

For LN, ![Image 6](/assets/images/imported/ln-properties/image6.png)

![Image 7](/assets/images/imported/ln-properties/image7.png)

# Piezoelectric and converse piezoelectric
From Weis and Gaylord, Appl. Phys. A, 1985:

![Image 8](/assets/images/imported/ln-properties/image8.png)

![Image 9](/assets/images/imported/ln-properties/image9.png)

![Image 36](/assets/images/imported/ln-properties/image36.png)

![Image 46](/assets/images/imported/ln-properties/image46.png)

![Image 41](/assets/images/imported/ln-properties/image41.png)

From K. K. Wong, properties of LN:

![Image 39](/assets/images/imported/ln-properties/image39.png)

![Image 95](/assets/images/imported/ln-properties/image95.png)

![Image 84](/assets/images/imported/ln-properties/image84.png)

![Image 100](/assets/images/imported/ln-properties/image100.png)

In COMSOL:
- Coupling matrix eES = {0, -2.53764, 0.193644, 0, 2.53764, 0.193644, 0, 0, 1.30863, 0, 3.69548, 0, 3.69594, 0, 0, -2.53384, 0, 0} \C/m\^2\
- i.e., convention for 3x6 matrix eES is
- {e11, e21, e31, e12, e22, ..., e26, e36}
# Photoelastic effect

![Image 10](/assets/images/imported/ln-properties/image10.png)

From Weis and Gaylord, Appl. Phys. A, 1985:

![Image 70](/assets/images/imported/ln-properties/image70.png)

![Image 93](/assets/images/imported/ln-properties/image93.png)

Primary effect is direct photoelastic, a secondary effect exist: piezoelectric + linear electro-optic effect.
In lithium niobate, the secondary effect is significant in the determination of the values of p13 and p33. The relationships between the measured coefficients and those describing the primary effect are: p13(pri)=p13(meas)-0.043, and p13(pri) = p13(meas) - 0.154
From K. K. Wong, properties of LN

![Image 111](/assets/images/imported/ln-properties/image111.png)

From A. S. Andrushchak et. al, JOURNAL OF APPLIED PHYSICS 106, 073510 (2009):

![Image 65](/assets/images/imported/ln-properties/image65.png)

## Photoelastic coupling

![Image 11](/assets/images/imported/ln-properties/image11.png)

For LN, ![Image 12](/assets/images/imported/ln-properties/image12.png)

![Image 13](/assets/images/imported/ln-properties/image13.png)

## Rotation of photoelastic tensor:
see [Rotation of photoelastic and piezoelectric tensor](/tutorial/rotation-of-photoelastic-tensor-and-piezoelectric/)
# Photorefractive effects
Aka optical damage: optically induced change of the refractive indices.
Caused by photoexcited carriers, transported along the polar axes, being trapped.
From K. K. Wong:

![Image 90](/assets/images/imported/ln-properties/image90.png)

High resistivity of LN -\> Small current flow cause a high space charge field -\> modified the refractive indices via the electro-optic effect. This change is reversible.
## From F. Jermann et. al, Photorefractive properties of congruent and stoichiometric lithium niobate at high light intensities, JOSA B, 1995:
- pumped at 514.5 nm and probed at 632.8 nm

![Image 78](/assets/images/imported/ln-properties/image78.png)

measured by light-induced birefringence change:

![Image 62](/assets/images/imported/ln-properties/image62.png)

which decays as ![Image 61](/assets/images/imported/ln-properties/image61.png)because of photoconductivity ![Image 50](/assets/images/imported/ln-properties/image50.png)
Saturate val of birefringence change, and photoconductivity:

![Image 85](/assets/images/imported/ln-properties/image85.png)

![Image 89](/assets/images/imported/ln-properties/image89.png)

For Fe doped LN, the same OOM, \~ 50% higher.
From Boyd, nonlinear optics, P525:

![Image 30](/assets/images/imported/ln-properties/image30.png)

# Photovoltaic effect
Mostly for wavelength \~\< 500 nm
# Pyroelectric effect
From Huihui Lu et. al 2013:

![Image 37](/assets/images/imported/ln-properties/image37.png)

![Image 116](/assets/images/imported/ln-properties/image116.png)

From Weis & Gaylord:

![Image 117](/assets/images/imported/ln-properties/image117.png)

![Image 99](/assets/images/imported/ln-properties/image99.png)

But this is at 25 deg C
From Savage 1966:

![Image 55](/assets/images/imported/ln-properties/image55.png)

From Mostafa et. al, 2006, heating Z-cut LN to 120C could expose ZEP.
# Radiation pressure coupling for anisotropic media
Decompose the energy density expression ![Image 14](/assets/images/imported/ln-properties/image14.png) into ![Image 15](/assets/images/imported/ln-properties/image15.png) and ![Image 16](/assets/images/imported/ln-properties/image16.png)
In the surface local coordinate system (t1, t2, n), where t1 and t2 are tangential components and n is the norm of the surface
In the local surface coordinate system, denote ![Image 17](/assets/images/imported/ln-properties/image17.png), then ![Image 18](/assets/images/imported/ln-properties/image18.png). As long as ![Image 19](/assets/images/imported/ln-properties/image19.png)(which is always the case), we can solve ![Image 20](/assets/images/imported/ln-properties/image20.png) in terms of ![Image 21](/assets/images/imported/ln-properties/image21.png) and ![Image 16](/assets/images/imported/ln-properties/image16.png), and the energy expression is written with continuous field components, and the step function in ![Image 22](/assets/images/imported/ln-properties/image22.png) gives a delta function after differentiation, and the volume integral becomes a well-defined surface integral.
The above is wrong! I have a new method TBA. For rp components of the OM interaction, still using isotropic approx.
# TBA: Acoustic waves
TBA:
# Thermal properties
This section mainly from K. K. Wong.
## Thermal expansion
# Nonlinear optics
## General nonlinear optics (Boyd, nonlinear optics)

![Image 87](/assets/images/imported/ln-properties/image87.png)

Second order nonlinear effects:

![Image 56](/assets/images/imported/ln-properties/image56.png)

# Thermodynamics of equilibrium properties
20181005
Mainly from John Nye, Physical properties of crystals

![Image 86](/assets/images/imported/ln-properties/image86.png)

![Image 29](/assets/images/imported/ln-properties/image29.png)

Principle effects:
- temperature change -\> entropy change: ![Image 63](/assets/images/imported/ln-properties/image63.png)
- E field change -\> electric displacement field change:

![Image 66](/assets/images/imported/ln-properties/image66.png)

- stress change -\> strain change (s: elastic compliance): ![Image 54](/assets/images/imported/ln-properties/image54.png)
Coupled effects:
- lines between points that are not both at the same corner.
- e.g., thermal expansion, piezocaloric effect, thermal pressure
All effects are related, it's important to specific measurement condition. E.g., for elastic compliance, the value under isothermal and adiabatic condition differ by \~ 1%
For strong interaction between different crystal properties, second order effect might be important to consider, e.g., pyroelectric effect from T -\> D and secondorder effect throught T -\> strain -\> D.
Thermodynamic relation:

![Image 35](/assets/images/imported/ln-properties/image35.png)

![Image 107](/assets/images/imported/ln-properties/image107.png)

There are too many. Go read the book.
## Magnitude of effects

![Image 27](/assets/images/imported/ln-properties/image27.png)

# Patterning
Ion milling:
- depend strongly on the residual partial pressure in the chamber, O2 cause metal oxidised or ashing of resist
Why no good chemistry: Li doesn't form volatiles with Br or Cl.
# HF clean/etch
From Investigation of pyroelectric electron emission from monodomain lithium niobate single crystals, Physica B, 2006:

![Image 57](/assets/images/imported/ln-properties/image57.png)

Z axis parallel to NB, chip annealed before the fab:
- from /user_data/wtjiang/fabrication/LNNEMO/SEMs/20181004_LNNB22Y_postHotHF

![Image 83](/assets/images/imported/ln-properties/image83.png)

![Image 26](/assets/images/imported/ln-properties/image26.png)

From
- Microstructuring of lithium niobate using differential etch-rate between inverted and non-inverted ferroelectric domains

![Image 48](/assets/images/imported/ln-properties/image48.png)

From LNNB24 post HF:

![Image 72](/assets/images/imported/ln-properties/image72.png)

![Image 59](/assets/images/imported/ln-properties/image59.png)

# Single domain crystal vs polycrystalline
From Physical-Acoustics-Principles-and-Methods_vol1, P. 218

![Image 33](/assets/images/imported/ln-properties/image33.png)

![Image 40](/assets/images/imported/ln-properties/image40.png)

# Convention of 2s
In general, this is the price you pay by writing higher rank tensor with some symmetry to artificial matrix and still want the eqn. to look like multiplication between actual matrices.
- extra 2 and 4 for compliance (s)
- extra 2 for strain (S or epsilon) and piezoelectric d
- no extra 2 or 4 for stress (T or sigma), elastic stiffness (c) and piezoelectric e
IEEE 1987 standard on piezoelectricity is the best!:

![Image 119](/assets/images/imported/ln-properties/image119.png)

![Image 49](/assets/images/imported/ln-properties/image49.png)

## Auld:

![Image 102](/assets/images/imported/ln-properties/image102.png)

No extra 2 for c.
## Andrew Cleland, Foundation of nanomechanics
P. 178
Stress:

![Image 24](/assets/images/imported/ln-properties/image24.png)

![Image 98](/assets/images/imported/ln-properties/image98.png)

Strain:

![Image 109](/assets/images/imported/ln-properties/image109.png)

![Image 105](/assets/images/imported/ln-properties/image105.png)

![Image 43](/assets/images/imported/ln-properties/image43.png)

## Yariv, Yeh, Optical waves in crystals
### Electro-optics:

![Image 69](/assets/images/imported/ln-properties/image69.png)

## John Nye, Properties of crystals
### Elasticity (P. 134)

![Image 112](/assets/images/imported/ln-properties/image112.png)

![Image 74](/assets/images/imported/ln-properties/image74.png)

![Image 76](/assets/images/imported/ln-properties/image76.png)

### Piezoelectricity (P. 114):

![Image 75](/assets/images/imported/ln-properties/image75.png)

![Image 106](/assets/images/imported/ln-properties/image106.png)

![Image 108](/assets/images/imported/ln-properties/image108.png)

![Image 92](/assets/images/imported/ln-properties/image92.png)

# Relations between piezoelectric constitutive equations
From IEEE 1987 standard:

![Image 45](/assets/images/imported/ln-properties/image45.png)            ![Image 32](/assets/images/imported/ln-properties/image32.png)

![Image 97](/assets/images/imported/ln-properties/image97.png)          ![Image 110](/assets/images/imported/ln-properties/image110.png)

Relations between the coefficients:

![Image 114](/assets/images/imported/ln-properties/image114.png)

![Image 23](/assets/images/imported/ln-properties/image23.png)

# Reference
Main: Gaylord.
Found a new source on 20200127: <https://ieeexplore.ieee.org/abstract/document/171403>