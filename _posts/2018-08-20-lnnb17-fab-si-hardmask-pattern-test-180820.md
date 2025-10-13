---
categories:
- Research
date: '2018-08-20'
header:
  cover: /assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image8.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image8.png
  show_overlay_excerpt: false
original_date: '2018-08-20'
tags:
- Lithium Niobate
- Materials
title: LNNB17 fab, Si hardmask pattern test
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2018-08-20, converted on 2025-10-12. )

# Goals and plans
## goals:
- get ebeam dose of 200 nm CSAR on SOLNS
- see how's the pattern transfer from Si hardmask through oxide to LN
- see how's the a-Si sidewall from lampoly
- see how's the LN ion mill sidewall from Si hardmask
- test the geom limit of Si hardmask
## plans:
180820:
- grow oxide and a-Si, using two Si chip of same size for calib
- one Si piece only coated with oxide
180821:
- beamwrite on one SOLNS and the SOS (silicon-oxide-silicon)  chip
- lampoly etch on both
- clean & condition
- analysis wafer #1
- SOLNS
- analysis wafer #2 (then hand #1 and #2 to Usha)
- SOS
- dektak both SOLNS and SOS chip
- cleave the SOS chip for SEMing CSAR lampoly sidewall
- also the remaining CSAR thickness
- ion mill the SOLNS chip and half of the SOS chip
180822:
- SEM two SOS pieces (after lampoly before ion mill and after ion mill)
- CSAR, a-Si, oxide thickness
- remaining a-Si/oxide thickness
- SEM SOLNS chip, determine optimal dose and extract patterning limits
- BOE and hot-HF clean, SEM again
- cleave SOLNS and SEM cross section
# SOLNS chip prep
woollam the five LNY pieces I currently have
p4 from a while ago:
- 312.7 nm
- MSE = 67
From the last four-pieces-thinning:
p2: 317.0 nm, MSE = 68
p3: 326.5 nm, MSE = 67
p4: 336.5 nm, MSE = 68
Going to ion mill fp1-p4 and fp2-p2 by 15 nm.
- 1 min 15 s
- Done
Diced one k-test wafer for accompanying ccp-dep
- using SPR220-3 and laurell-R
- not perfect
- quite some came off the tape during the dicing
run ccp-dep SiN 1 min with carriers loaded.
- run SiN350-T, 1 min
to dep oxide and Si:
- want 70 nm oxide
- want \~ 350 nm Si
- coat both fp1-p4 and fp2-p2, from now on rename them as LNNB17-a and LNNB17-b

![Image 24](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image24.jpg)

- 1 min SiO350-0
- take out one calib Si piece, measure oxide thickness
- 75.0 nm, MSE = 41
- from SEM of sp5-03, \~ 60 nm
- 8 min JKSi-0
- save this JKSi-0 as WJSi-0
- measure the other calib Si piece.
- oxide thickness fixed at 75 nm
- a-Si 322.9 nm, MSE = 86.4
- from SEM of sp4-02 and sp5-03, 30 \~ 50 nm thicker than this, i.e., 353 \~ 373 nm

![Image 19](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image19.jpg)

# Beamwrite, 20180821
Dose sweep layout:
For SOLNS:
- LNNBGeomTestAry1_NBs_zigzags.dxf
- extension: 650 by 1600
- layout x pitch = 800 um
- 7 doses: 240 : 20 : 360
- base dose 300
- 240              260           280           300            320              340         360
- 0.8000    0.8667    0.9333    1.0000         1.0667    1.1333    1.2000
- GMs_180821.dxf, dektak marks included
- trenches_180821.dxf, length 3500
- two doses: 280 (0.9333), 320 (1.0667)
- y pitch = 100
For SOS:
- GMs_180821.dxf, dektak marks included
- trenches_180821.dxf
- dose: 280, 300, 320
- 0.9333, 1, 1.0667
- y pitch = 200
Actually pretty fast, hence write the same pattern also for SOS.
# lampoly and ion mill:
From lampoly etch rate, for 373 nm, main etch time = (373-213)/4.54 = 35.24 s
- I'll use 36 s main etch time
- done
## SEM of SOS after lampoly:

![Image 8](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image8.png)

![Image 2](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image2.png)

![Image 10](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image10.png)

![Image 11](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image11.png)

![Image 18](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image18.png)

From a-Si and SiO ion mill:
- assume 60 nm SiO ⇒ t2 = 4.38 min
- 300 nm LN ⇒ t3 = 25 min
- 29.38 min required in total. Will be shorter than this because lampoly also etched a small amount of oxide
- Let's use \~\> 32 min
- a-Si could hold for at least t1 = 353/13.2 = 26.74 min, at most 373/13.2 = 28.26, I don't know the 220 nm CSAR ion mill rate. Hopefully its etch rate is \> 30 nm/min so that a-Si is still almost gone even masked by remaining CSAR.
- I'll use 33 min
- 5 * 6 min + 3 min
- started at 0:40 am
## SEM of SOLNS after ion mill:
Horrible.

![Image 20](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image20.png)

![Image 9](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image9.png)

![Image 17](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image17.png)

![Image 21](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image21.png)

![Image 6](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image6.png)

![Image 3](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image3.png)

![Image 4](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image4.png)

conclusion:
- seems like LN not fully etched through
- ran out of mask
Possible reason:
- oxide and a-Si grown on LN is different
- lampoly on SOLNS failed
- LNY is hard to etch
TODO:
- cleave SOLNS and SEM cross section
- also ion mill the SOS piece
- if similar, then even lampoly etch looks good, a-Si is a bad mask
- if better, two possibilities: lampoly etch failed on SOLNS or Si is easier to etch
- try an LNX piece
Done ion milling the SOS piece with the same 33 min recipe. (180822)
Going to SEM, 180822 evening.
## SEM of SOS after ion mill:
What happened???

![Image 22](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image22.png)

![Image 23](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image23.png)

![Image 14](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image14.png)

# Same beamwrite again on LNNB17-b, 180822
Using the new bottle of CSAR 62.09
Done.
Same lampoly (36 s main etch) done. Looks ordinary.
## SEM after lampoly:

![Image 12](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image12.png)

![Image 16](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image16.png)

![Image 13](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image13.png)

Cleaved into two halves.
Did 15 min ion mill on the left piece.
## SEM after 15 min ion mill:

![Image 15](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image15.png)

![Image 5](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image5.png)

![Image 1](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image1.png)

## conclusion: a-Si cracks, doesn't get etched homogeneously.
Hence the cracked edges on LNNB17a SOLNS is also explained, they were transferred from these cracked a-Si.
Solution:
- change ion mill recipe, i.e., smaller angle
- Going to try 3 deg tilt on 0824.
- I guess this is unlikely to change it. The mask is poor and fragile near edges.
- The SOS chip also shows the mask got etched much faster from edge inward.
- or
- anneal a-Si to get p-Si (polycrystalline silicon):
- <https://aip.scitation.org/doi/abs/10.1063/1.342851>

![Image 7](/assets/images/imported/lnnb17-fab-si-hardmask-pattern-test-180820/image7.png)

- going to get trained on alwin 610 rapid thermal annealer
- could do the RTA on SOS and SOLNS-b pieces that are not ion milled yet.
- LN might crack