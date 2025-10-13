---
categories:
- Research
date: '2018-06-23'
header:
  cover: /assets/images/imported/lnnb-unitcell-simulations-1806-1812/image108.png
  overlay_filter: 0.5
  overlay_image: /assets/images/imported/lnnb-unitcell-simulations-1806-1812/image108.png
  show_overlay_excerpt: false
original_date: '2018-06-23'
tags:
- Lithium Niobate
- Materials
- Piezoelectric
- Simulation
title: LNNB unitcell simulations 1806 -
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2018-06-23, converted on 2025-10-12. )

## 20180604, better understanding of zipper unitcell optical modes
Manually changed GA180312 parameters to satisfy geom constraint
Solve time \~ 1 min 20 s
PMC:
Asym TE dielectric mode (1.85e14) and asym TE air mode (2.10e14): Ey:

![Image 124](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image124.png)

![Image 76](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image76.png)

sym TM dielectric (2.04e14) and air (2.067e14) mode: Ez:

![Image 13](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image13.png)

![Image 129](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image129.png)

PEC:
Sym TE dielectric (1.77e14) and air (2.00e14) mode: Ey:

![Image 61](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image61.png)

![Image 100](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image100.png)

Asym TM dielectric (2.14e14) and air (2.17e14) mode: Ez:

![Image 12](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image12.png)

![Image 41](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image41.png)

Select TE & TM based on integration of conj(emw.Ey)*emw.Dy/emw.intWe etc.
Switching to ZXY system in the future.
Write new GA tomorrow!
## 20180623, rectangular hole TE mirror GA
model used for GA: model_unitcell_LN_tilt_rect_180623.mph
Started at 3:56 PM, stopped at 5:54 PM. Bands calculated.
Add smallest hole size constraint to be 300 nm.
Started at 5:56 PM, also started band calc at 6:28 PM
This one seems good enough (which is also used for band calculation):
-                  a: 5.8961e-07
-            coef_hx: 0.5312
-            coef_hy: 0.6433
-             hx_min: 3.0000e-07
-             hy_min: 3.0000e-07
-          maxAspRto: 3
-     minFeatureSize: 5.0000e-08
-                  t: 3.0000e-07
-                  w: 1.0671e-06
-               cost: -0.2089
-             f_band: 4.1117e+13, 41 THz
-              f_mid: 1.9637e+14
Stopped at 7:25 PM
EM Bands and mech bands:

![Image 29](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image29.png)

![Image 89](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image89.png)

### 20181207, revisit with two theta geom and 45 deg alpha (135 deg LNX in-plane rot)
- with 22 deg and 11 deg, EM bandgap move down and shrink: 174.2 \~ 199.6 THz
## 20180705, Y-cut ZXY system fishbone unitcell bands
model: /UnitCell1DCavity/model_FBUC_piezo_EM_20180705.mph
- 1 um width, 400 nm amplitude
- 600 nm lattice const
Second high freq mechanical mode at Gamma point
- Full bandgap exist! Around 3 GHz
- the 6-th mode is a breathing mode

![Image 43](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image43.png)

![Image 24](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image24.png)

w = 800 nm and amp = 300 nm could push breathing mode even higher than the bandgap:

![Image 86](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image86.png)

Lowest two TE modes at 173 and 187 THz, Ey:

![Image 105](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image105.png)

![Image 113](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image113.png)

It has second order transverse mode at 197 THz, Ey:

![Image 56](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image56.png)

Fundamental TM at 215 THz, higher order TM at 233 THz, Ez:

![Image 37](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image37.png)

![Image 39](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image39.png)

Going to check X-cut
- using model: model_FBUC_piezo_EM_nZYX_20180705.mph and model_FBUC_piezo_EM_nZYX_full_20180705.mph
- blue: force y-sym, red: force y-asym, green: full-geom

![Image 123](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image123.png)

## 20180705, Y-cut LNFB mirror cell GA
Need model: /UnitCell1DCavity/model_FBUC_piezo_EM_20180705.mph
Started at 6:52 PM
Terminated before 180706 1:17 AM after 3000 evals

![Image 127](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image127.png)

![Image 109](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image109.png)

Results:
-                  a: 6.1539e-07
-           coef_amp: 0.8453, amp = 275.099 nm
-             f_goal: 1.9341e+14
-     minFeatureSize: 1.0000e-07
-                  t: 3.0000e-07
-                  w: 6.5089e-07
-               cost: -0.1480
-             f_band: 1.6071e+13, 16.1 THz
-              f_mid: 1.9149e+14
f_TM = 217 THz
bands:

![Image 27](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image27.png)

![Image 134](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image134.png)from old geom: ![Image 24](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image24.png)

Breathing mode at 3.5 GHz, hopefully could be pressed down to \~ 3GHz into the symmetric bandgap.
Also, there's a very large (\~ 1 GHz) asym bandgap between the 6-th and 7-th band.
## 20180706, same fishbone UC GA with 150 nm and 200 nm geom constraint
Running same GA with minFeatureSize constraint = 150 nm instead of 100 nm
File: gaParams_LNFB_TEmirror_150nm_180706.mat
Results:
-                  a: 5.8590e-07
-           coef_amp: 0.7857, amp = 279.8 nm
-             f_goal: 1.9341e+14
-     minFeatureSize: 1.5000e-07
-                  t: 3.0000e-07
-                  w: 7.1213e-07
-               cost: -0.1500
-             f_band: 1.4000e+13, 14.0 THz
-              f_mid: 1.9327e+14
Band calculating (180706 11:50 PM)\...
Done.

![Image 91](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image91.png)

![Image 75](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image75.png)

Running same GA with minFeatureSize constraint = 200 nm
File: gaParams_LNFB_TEmirror_180706.mat
Finished. Results:
-                  a: 5.7759e-07
-           coef_amp: 0.7200, amp = 286.16 nm
-             f_goal: 1.9341e+14
-     minFeatureSize: 2.0000e-07
-                  t: 3.0000e-07
-                  w: 7.9494e-07
-               cost: -0.1354
-             f_band: 1.0852e+13, 10.8 THz
-              f_mid: 1.8990e+14
Bands TBA. Calculating (180707 1:07 AM)

![Image 112](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image112.png)

![Image 47](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image47.png)

## 20180707, geom sweep with band calculation for FBUC
Finished.
Data: sweepGeom_LNFBUC_bands_180707.mat

![Image 121](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image121.png)

![Image 38](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image38.png)

![Image 48](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image48.png)

![Image 79](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image79.png)

## 20180707, new FBH (fishbone-hole) unitcell design & GA
Idea: use hole to increase bandgap and transform to fishbone type defect cell
Model:

![Image 45](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image45.png)

![Image 104](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image104.png)

![Image 66](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image66.png)

First calculation already yield TE bandgap 180.0 \~ 207.6 THz, fundamental TM = 219 THz
- parameters used:
- a = 615.4 nm
- wmin = 600 nm
- wmax = 1400 nm
- amp = (wmax - wmin)/4 = 200 nm
- theta = 20 deg
- hx = 369.2 nm (coef_hx = 0.6)
- hy = 980 nm (coef_hy = 0.7)
Calculating mechanical bands... Very promising. Sym bandgap 3.142 \~ 4.456 GHz

![Image 111](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image111.png)GA geom mech bands:![Image 80](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image80.png)

Going to run GA. GA mech bands above left, 4 GHz bandgap disappeared. Bandgap around 2 GHz larger: \1.3324e+09 2.1632e+09\. Original 4 GHz bandgap is now \~ 7 GHz
Results:
-                  a: 5.5762e-07
-            coef_hx: 0.5918
-            coef_hy: 0.6890
-             f_goal: 1.9341e+14
-     minFeatureSize: 8.0000e-08
-                  t: 3.0000e-07
-               wmax: 1.2465e-06
-               wmin: 9.1900e-07
-                 hx: 3.2998e-07
-                 hy: 8.5887e-07
-                amp: 8.1880e-08
-                  w: 1.0828e-06
-                  d: 2.1135e-07+
-             f_band: 3.3698e+13, 33.7 THz
-              f_mid: 1.9806e+14
## 20180720, piezoelectric polarization of unitcell and pze coupling simulation
Explicit form:

![Image 1](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image1.png)

![Image 2](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image2.png)

![Image 3](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image3.png)

Above is in crystal coordinates!
Agree with sims:
- on Y-cut (ZXY) nanobeam where NB // Z:
- breathing mode: ![Image 4](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image4.png),
- dominant polarization is ![Image 5](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image5.png), which is global Pz

![Image 77](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image77.png)

- on X-cut (nZYX) nanobeam where still NB // Z
- breathing mode is ![Image 6](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image6.png),
- dominant polarization is ![Image 7](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image7.png), which is global Py

![Image 74](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image74.png)

### pze coupling simulation, X-cut:
First good news:
model: UnitCell1DCavity/model_FBHUC_180707_piezoDrive_180720.mph

![Image 135](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image135.png)

![Image 17](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image17.png)

Voltage profile:

![Image 70](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image70.png)

![Image 101](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image101.png)

![Image 136](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image136.png)

Why there's a large Ex component??

![Image 18](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image18.png)

db(Y11):
Finer freq sweep using matlab:

![Image 25](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image25.png)

wide range and fit (180724):

![Image 118](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image118.png)

#### network synthesis
- C0 = 1.7759e-16 F
- g calculated using another resonator/qubit with ![Image 8](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image8.png)fF and freq 2.5 GHz.
- 2.36 GHz is the breathing mode.
              g_list (Hz)         freq                    C                    L                         Z
    \_\_\_\_\_\_\_\_\_\_    \_\_\_\_\_\_\_\_\_\_    \_\_\_\_\_\_\_\_\_\_    \_\_\_\_\_\_\_\_\_\_    \_\_\_\_\_
    7.9433e+06       8.5e+08    2.3796e-15    1.4733e-05    78685
    2.3859e+06    1.0425e+09     3.577e-14    6.5158e-07     4268
    1.0077e+07      2.36e+09    4.3041e-15    1.0567e-06    15668
### Y-cut:
Not able to get finer Y11 resolution even refine the frequency (\~\< 0.00001 GHz)!

![Image 59](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image59.png)

wider sweep and fit using synthesize_Y:

![Image 92](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image92.png)

#### Network synthesis:
- coupling is assuming another resonator/qubit with ![Image 8](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image8.png)fF and freq 2.5 GHz.
- C0 = 1.7748e-16 F
- grey color: modes that are not effectively coupled, gs for them are wrong.
              g (Hz)                  freq                    C                    L                    Z
    \_\_\_\_\_\_\_\_\_\_    \_\_\_\_\_\_\_\_\_\_    \_\_\_\_\_\_\_\_\_\_    \_\_\_\_\_\_\_\_\_\_    \_\_\_\_\_\_\_\_\_\_
    8.7087e+06      8.55e+08    1.9434e-15     1.783e-05         95785
    2.1022e+07    1.0593e+09    1.2667e-16     0.0001782    1.1861e+06
    2.7615e+07    2.1899e+09    2.5655e-16    2.0588e-05    2.8328e+05
    8.3491e+06    2.3927e+09    6.4776e-15    6.8305e-07         10269
    1.0636e+07      2.48e+09    4.0391e-15    1.0196e-06         15888
    2.7925e+07    2.6227e+09    3.6476e-16    1.0096e-05    1.6636e+05
The breathing mode is at 2.39 GHz.
The two strongly coupled modes both have large PpzeY component:
left: ![Image 9](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image9.png). Right: ![Image 10](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image10.png)
Keep in mind that the crystal system is ZXY

![Image 60](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image60.png)

![Image 68](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image68.png)

### Sweeping geometry to see scalings, 180725
Parameters:
- t_metals = \50e-9:25e-9:200e-9\;
- d_metals = \50e-9:25e-9:400e-9\;
- params1 = genParamStructs('t_metal', t_metals, 'd_metal',150e-9);
- params2 = genParamStructs('t_metal', 100e-9, 'd_metal', d_metals);
- freqs = \0.005:0.005:3\;
- getImagY11s = @(model)(mphsweepPZEfreq(freqs, model));
Started at 4:06 PM
Results see below.
## 20180722, NB UC with elliptical hole, 22 deg hole sidewall and 15 deg outer sidewall

![Image 35](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image35.png)

Results:
-                  a: 5.3646e-07
-             f_goal: 1.9341e+14
-     minFeatureSize: 5.0000e-08
-                  t: 3.0000e-07
-               wmax: 9.6126e-07
-               wmin: 9.6126e-07
-                 hx: 2.6799e-07
-                 hy: 8.5491e-07
-                amp: 0
-                  w: 9.6126e-07
-                  d: 5.3176e-08   (min feature size)
-               cost: -0.1900
-             f_band: 2.2173e+13, 22.2 THz
-              f_mid: 1.9568e+14
Tried manually select band center and TM1, got same results as from GA.
50 nm might be too small for the electrode alignment, trying FBH design.
Results:
-                    a: 5.9583e-07
-            coef_hx: 0.5893
-            coef_hy: 0.8620
-             f_goal: 1.9341e+14
-     minFeatureSize: 8.0000e-08
-                  t: 3.0000e-07
-               wmax: 1.2033e-06
-               wmin: 9.7239e-07
-                 hx: 3.5111e-07
-                 hy: 1.0373e-06
-                amp: 5.7738e-08
-                  w: 1.0879e-06
-                  d: 1.4014e-07
-               cost: -0.2243
-             f_band: 3.1922e+13
-              f_mid: 1.8840e+14
but the mechanical bandgap is not good:
band_Mech = \1.172e9, 1.804e9\;![Image 120](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image120.png)
only up to 1.8 GH
Examed old FBH GA from 180707, it's actually still pretty good with new sidewalls:
- TE bandgap 178.5 \~ 208.5 THz, i.e., 30 THz at 193.5 THz, first TM at 222 THz
- phonon bandgap 1.481 \~ 2.151 GHz ![Image 85](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image85.png)
## 20180724, FBH UC for breathing mode at given freq and optical bandgap at 193 THz
GA scheme:
- get X-point TE and TM band edge as usual
- get Gamma-point mechanical modes, check breathing or not
Or should I just use the same mirror cell and do the hole-displace-y trick?
Do this in the future.
## 20180806, PZE copling geom sweep results
### sweep metal thickness:

![Image 125](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image125.png)

Circuit parameters:

![Image 97](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image97.png)

![Image 126](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image126.png)

### sweep electrode separation:

![Image 130](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image130.png)

![Image 83](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image83.png)

![Image 32](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image32.png)

## 20180821, Unitcell from GA180707 with 5 deg theta_out and 10 deg theta
Mechanical bandgap: 1.306GHz \~ 2.196 GHz
optical bandgap: 183.4 THz \~ 227.9 THz

![Image 62](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image62.png)

![Image 98](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image98.png)

## 20181031, FBH unitcell with full geom for LNX 135 deg (45deg in-plane)
model created.
semi-symmetry selection strategy:
Optics:
- semi-TE: vol int of
- conj(ewfd.Ey) * ewfd.Dy / ewfd.intWe / 4
- semi-TM: similarly
mechanics:
- evaluate u*y, v*y and w*y and normalize by max(disp), V_NB and w_NB:
- ![Image 108](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image108.png)
- sweeping band structure to see if it works or not. See sweep_EMBand_script.m
- results TBA
- not so good, trying abs(v) * (abs(y) \< 1e-9)
- better, still not good enough
- trying to generate sym y geom and then mirror, then do abs(v) on the y = 0 surface
- not good
- tried integrating eXY, eYY etc., not good.
- The best is compare v*(x\>0)*(z\>0)*(y\>0) and v*(x\>0)*(z\>0)*(y\<0)
mech bands:
- blue: semi-symy
- red: semi-asymy
- green: hybrid

![Image 33](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image33.png)

![Image 62](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image62.png)

I don't understand mechanics.
Selecting using all u, v and w information

![Image 23](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image23.png)

Should compare with fake enforced symmetry
I want to see the mode shape from Gamma to X.
- use matlab mphplot, save fig and png
- done. rerun band sweep while saving mode profiles
EM bands also running.
- semi-TE and TM classification working well
- ![Image 107](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image107.png)
### 20181207, 45 deg (135 deg in-plane rotation):
## 20181107, LN FBH mirror cell GA, for 250 nm
Started 11:40PM.
Converged after overnight GA.

![Image 69](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image69.png)

manually choose 2908 in the sorted index.
- manually checked TM0 \> TE1 by more than 1 THz
Results:
- ALL_P(inds(2908))
-  =
-   struct with fields:
-                  a: 5.7244e-07
-            coef_hx: 0.5864
-            coef_hy: 0.8622
-             f_goal: 1.9341e+14
-     minFeatureSize: 8.0000e-08
-                  t: 2.5000e-07
-               wmax: 1.1620e-06
-               wmin: 9.7032e-07
-                 hx: 3.3570e-07
-                 hy: 1.0019e-06
-                amp: 4.7918e-08
-                  w: 1.0662e-06
-                  d: 1.2629e-07
-               cost: -0.1968
-             f_band: 3.5841e+13
-              f_mid: 2.0396e+14
Geometry looks like this:

![Image 28](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image28.png)

TE0:

![Image 34](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image34.png)

TE1

![Image 63](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image63.png)

## 20181108, bands of GA 181107
sym mech bandgap: \1.129, 1.789\ GHz
TE bandgap: \186.04, 221.89\ THz

![Image 57](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image57.png)

![Image 11](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image11.png)

I should do a +-10% perturbation on all geom parameters to see how they affect the bands.
Should I try to get higher mech bandgap freq?
Very hard to push breathing mode \~ 2.47 GHz down into bandgap. Should try to push up the 4th mech band of the mirror cell.
Checking GA 180707 again, change t to 250 nm and scale other geom params to shift band mid to \~ 197 THz
- used the wrong 'a' hence wrong 'k', but the X point is still included
- sym mech bandgap: \1.253, 1.887\ GHz, "breathing" band much closer to bandgap edge
- TE bandgap: \180.8, 213.8\ THz, f_band = 33 THz

![Image 115](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image115.png)

![Image 88](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image88.png)

Use this for 250 nm OM GA.
## 20181201, FBH mirror cell mech bands with different in-plane rotation
Path: `COMSOL/LN/UnitCell1DCavity/FBH/20181201_FBH_mechBands_sweepRotation`

Started 4:15 PM
file corrupted.
 rerun with 40 kF and 9 theta:

![Image 78](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image78.png)

hopeless, too hard to interpret.
TODO:
- plot gamma point mode vs. theta
- compare with rotated elasticity matrix
### compare 0, 45 deg and 135 deg in-plane rotation bands.

![Image 53](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image53.png)

One thing: confirm elasticity is larger along y for -45 deg:
- NOT TRUE
- main terms in elasticity is the same at \\pm 45 deg
20181205, manual FBH mirror bands:

![Image 94](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image94.png)

Not as good as GA 180722
## 20181207, naming the lowest few gamma point modes
model:
- UC1D/FBH/model_FBHUC_full_LNX135deg_GA180723_defect_modified_181206.mph
Flappy0 (\~0.83 GHz):

![Image 19](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image19.png)

![Image 15](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image15.png)

![Image 96](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image96.png)

Shear0 (0.88 GHz):

![Image 21](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image21.png)

![Image 20](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image20.png)

![Image 114](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image114.png)

Breathing (2.13 GHz):

![Image 122](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image122.png)

![Image 99](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image99.png)

![Image 51](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image51.png)

Flappy1 (1.97 GHz):

![Image 65](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image65.png)

![Image 42](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image42.png)

![Image 64](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image64.png)

Shear1 (3.38 GHz):

![Image 103](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image103.png)

![Image 44](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image44.png)

![Image 36](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image36.png)

Flappy2 (3.76 GHz):

![Image 93](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image93.png)

![Image 46](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image46.png)

![Image 133](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image133.png)

Tidal0 (4.26 GHz):

![Image 30](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image30.png)

![Image 58](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image58.png)

![Image 55](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image55.png)

Shear2 (4.29 GHz):

![Image 71](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image71.png)

![Image 81](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image81.png)

![Image 14](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image14.png)

Flappy3 (4.97 GHz)
Shear3 (5.45 GHz)
Flappy&Shear mixed (5.93 GHz)
Tidal1 (6.1 GHz):

![Image 128](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image128.png)

Higher freq modes are harder to classify (edge modes etc.)
For mirror cell (GA180722, 135 deg in-plane rot LNX), it has very similar modes:
- Shear0 (0.92 GHz)
- Flappy0 (1 GHz)
- Flappy1 (2.2 GHz)
- Tidal0 (2.3 GHz)
- breathing (2.6 GHz)
- Shear1 (2.8 GHz)
- Flappy2(3.5 GHz)
- Tidal1 (3.97 GHz)
- Shear2 (4.27 GHz)
- edge modes (4.51 GHz, 4.64 GHz, \...)

![Image 53](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image53.png)

Target:
- clean mechanics around breathing mode
- push up F1 and T0
- large TE optical bandgap around 193 THz
## 20181208, manual mirror
Reduce w to push up F1.

![Image 132](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image132.png)

Bands, 135 deg LNX (45 deg in-plane), 45 deg LNX running...:

![Image 106](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image106.png)

Further trying to pushing S0 at X point down:
- by using larger hole
- ![Image 52](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image52.png)

![Image 40](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image40.png)

![Image 82](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image82.png)

## 20181208, FBH mirror GA 180722 X point mode classification
- See [WJ - LNNB unitcell mechanical modes 20181109.pdf](/assets/doc/2025/WJ - LNNB unitcell mechanical modes 20181109.pdf)
- and also: `COMSOL/LN/UnitCell1DCavity/FBH/20181207_FBH_mirrorGA180722_45deg_mechBands/modeprofile`
## 20181209, FB mirror with elliptical shape
Path: `COMSOL/LN/UnitCell1DCavity/FB/20181209_mechbands`

Model: `model_FBUC_piezo_EM_45degLNX_20181209.mph`
mech bands:
Very promising:

![Image 116](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image116.png)

### Add elliptical holes to increase TE optical bandgap:
- TE bandgap increase from \~ 16 THz to \~ 28 THz
- also helps pushing down the breathing mode of the defect down into the full mech bandgap

![Image 110](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image110.png)

New mech bandgap:
- model_FBUC_piezo_EM_45degLNX_mirror_20181209.mph
- bandgap \~ 500 MHz at \~ 4 GHz
- now I need to push up the breathing mode at 3.43 GHz to \~ 4 GHz
- old one on the right

![Image 31](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image31.png)

![Image 116](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image116.png)

### New geom on 20181210, pushing up Breath:
- model_FBUC_piezo_EM_45degLNX_mirror_testGeom_20181210
- bands: sweep_mechBands_FB_45degLNX_mirror_181210_2.mat
- right: old geom from yesterday

![Image 16](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image16.png)

![Image 26](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image26.png)

![Image 31](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image31.png)

Further pushup Breath:
- sweep_mechBands_FB_45degLNX_mirror_181210_3.mat

![Image 102](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image102.png)

![Image 50](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image50.png)

## 20181229, AX UC optical GA
Path: `COMSOL/LN/UnitCell1DCavity/FB/20181229_AX_OpticalGA`

Few updates:
- add geom-check for neg-holes not fully through outer edge
- tried different TM2BE and bandgap center tolerance
20190105, still running
Stopped.
Model:
- model_AXUC_piezo_EM_45degLNX_20190104_GARes_small_a.mph
Optical band:
-                  a: 5.7619e-07
-                 hy: 1.2341e-06
-                hyN: 1.7952e-06
-                  t: 3.0000e-07
-        thres_TM2BE: 2.0000e+12
-        tol_bandmid: 4.0000e+12
-                  w: 5.3508e-08
-                 hx: 2.7409e-06
-                hxN: 3.3000e-07
-             f_band: 3.4059e+13
-              f_mid: 2.0037e+14

![Image 137](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image137.png)

Trying calculating overlapping integral between gamma and X point modes:

![Image 90](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image90.png)

![Image 22](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image22.png)

![Image 95](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image95.png)

![Image 131](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image131.png)

- blue: find gamma from X
- dashed red: find X from gamma
Not exactly correct.
Actually seems correct, it's not necessary that the gamma and X point of one band looks similar.
Comparison between bands and fixed (blue) or free (dashed red) BC:

![Image 54](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image54.png)

### Mode identification working, can now plot mech bands vs. gem params:
- {        'a',              'hx',        'hxN',             'hy',                  'hyN',                'w'}

![Image 73](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image73.png)

- five segments along x are param sweep of
- {        'a',              'hx',             'hxN',             'hy',                  'hyN',                'w'}
- top: mech bands. Black is breathing mode band
- bot: optical bands
Error happens for uy2_X and wy3_X
### 20190108, also varying thickness.
Manual params:
-       a: 6.3000e-07
-      hx: 1.8947e-06
-     hxN: 4.3200e-07
-      hy: 1.1104e-06
-     hyN: 2.0360e-06
-       w: 7.8687e-08
-       t: 2.6000e-07
Bands:
- much larger curlUYy2 - wy4 anticrossing bandgap
- red band inside the cYy2 - wy4 bandgap is the tether mode
- note uy4-gamma already at lower freq than cYy2_gamma
- there's hope to further push breathing mode (vy1) into cY020 - w040 bandgap

![Image 72](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image72.png)

Geom sweep around this design:
- load('sweep_geom_GARes_medium_a_thinner_20190108.mat')
- {'a',                'hxN',                        'hy',                'w',                        't'};

![Image 117](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image117.png)

- t is the most effective param to bring down w040, agree with intuition
Thinner!
- model = mphload('model_AXUC_piezo_EM_45degLNX_20190106_GARes_medium_a_thinner');
- fname = 'model_AXUC_piezo_EM_45degLNX_20190106_GARes_medium_a_thinner_180109';
-       a: 6.5000e-07
-      hx: 1.8947e-06
-     hxN: 4.0000e-07
-      hy: 1.1040e-06
-     hyN: 2.0360e-06
-       w: 8.0000e-08
-       t: 2.1000e-07

![Image 87](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image87.png)

![Image 67](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image67.png)

                                                {'a',           'hxN',                'hy',        'w',          't'};
- breathing mode is the bandgap edge!
- optical bandgap: 189.7 THz \~ 222 THz (32 THz at 206 THz), TM0 at 223 THz
I also got a defect with TE0 at 211 THz, gamma point v010 at 3.28 GHz and no mode crossing!
- ![Image 119](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image119.png)
- tether mode at 3.5 GHz \~ 3.67 GHz
- gamma w040 at 3.16 GHz
I feel ready to try out the full nanobeam.
varying thickness GA res:
- model_AXUC_piezo_EM_45degLNX_20190109_GARes
-             f_band: 3.1969e+13
-              f_mid: 1.9419e+14
-       a: 6.5115e-07
-      hx: 2.9272e-06
-     hxN: 3.6612e-07
-      hy: 1.4038e-06
-     hyN: 2.9125e-06
-       w: 5.3768e-08
-       t: 2.2942e-07

![Image 84](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image84.png)

![Image 49](/assets/images/imported/lnnb-unitcell-simulations-1806-1812/image49.png)

Sweeping geom... Done.                       {'a',                   'hxN',             'hy',        'w',          't'};
- w040 too close to v010 at gamma point, can't get a very pure breathing defect
- this a (650 nm) is also too large
### 20180114, fixing thickness at 210 and rerun GA.