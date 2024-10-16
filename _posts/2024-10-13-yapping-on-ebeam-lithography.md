---
title: "Yapping on ebeam lithography"
categories:
  - Tutorial
tags:
    - Nanofab
    - Lithography
    - Electron
toc: true
toc_sticky: true
use_math: true
header:
  overlay_image: /assets/images/2024/ebeam/jeol_jbx-6300_61255172.jpg
  cover: /assets/images/2024/ebeam/jeol_jbx-6300_61255172.jpg
  show_overlay_excerpt: false
  overlay_filter: 0.5
---


The cover of this blog was the JEOL JBX 6300FS at Stanford [SNSF](https://snsf.stanford.edu/). I love it. Here is the evolution of JEOL JBX series.

![JEOL_JBX_history](/assets/images/2024/ebeam/JEOL_JBX_history.jpg)
*History of JEOL JBX. From [Application note: Development of JBX-A9, Electron Beam Lithography System](https://www.jeol.com/solutions/applications/details/se2024-01.php)*

*DISCLAIMER: I'm writing this blog for fun. You should always question the numbers and practices here, and consult your colleagues, ebeam staff, and the references here for your own judgement.*

# What is EBeam litho

Ebeam lithography, as the name suggests, is using electron beams for lithography. [Lithograph](https://en.wikipedia.org/wiki/Lithography) has a pretty old history, and involves a mask or print plate, materials to be printed (started with oil), and a physical or chemical process to shape the print using the mask. It is a powerful technique at the time to mass produce drawings and maps, and later photos (photography).

![Hands](/assets/images/2024/ebeam/Hands-SantaCruz-CuevaManos-P2210651b.jpg)
*Hands, stenciled at the [Cave of the Hands](https://en.wikipedia.org/wiki/Cueva_de_las_Manos)*

When people start to think about how to reduce the size of electronic circuits in the 1950s, they adopted photographic technique (using optics to shrink and project the pattern, expose and develop the [photoresist](https://en.wikipedia.org/wiki/Photoresist) just like in photography) and thus coined the term [photolithography](https://en.wikipedia.org/wiki/Photolithography). Circuit designers would draw the circuit layout on a big canvas, that would later [tapeout](https://en.wikipedia.org/wiki/Tape-out) (it is still called tapeout to this date even physical tape is no longer involved) and be shrinked into a [photomask](https://en.wikipedia.org/wiki/Photomask), and shrinked again by the photolitho system onto the wafer. The quest for shrinking the size of electronic circuits and transistors has been on a non-stop march, and shorter wavelengths are needed because of refractive limit of the resolution. But you know what has a much shorter wavelengths? Electrons!

Let's quickly estimate typical "wavelengths" of electrons in an electron beam. Assuming 10 kV of acceleration, that makes its speed roughly $$0.2 c$$, where $$c$$ is the speed of light. This is without relativistic correction, which will be $$10\%$$ or $$ 20\%$$ so let's ignore it. The corresponding momentum is $$ 5\times 10^{-23}~\text{kg}\cdot\text{m/s} $$ (hmm this is suspiciously close to Boltzmann constant... whatever), and these electrons's [de Broglie wavelength](https://en.wikipedia.org/wiki/Matter_wave) would be $$ 1.2\times 10^{-11}~\text{m} $$ or 12 pm. If we were to get light with wavelength this small, they would be called [gamma rays](https://en.wikipedia.org/wiki/Gamma_ray). 

Another way to think about the wavelength or resolution ability of these tens of kV electrons is, 1 eV photons are around 1 um wavelength, so 10 keV photons would be 0.1 nm wavelength, pretty close to the calculation above. The reason why no one uses gamma rays for photolitho is probably they are hard to generate, and photons do not interact with each other except indirectly via atoms or nonlinear dielectrics, or high enough energy to have quantum electrodynamics shit going. People are already using mirrors for 13.5 nm photon EUV photolitho instead of lenses because of transmission loss, and those mirrors have crazy specs (the YouTube channel Asianometry has a series of videos (e.g.: [ASML's High-NA EUV Lithography: A 2024 Update](https://www.youtube.com/watch?v=UdcFpjgCnP8)) about EUV and they are very informative). Gamma rays would mostly just pass through things, and happily ionizing stuff along the way.

Ok back to ebeam. Electrons are used for many things even before [its discovery](https://www.britannica.com/science/atom/Discovery-of-electrons) in 1897, before which electron beams would only be called [cathode rays](https://en.wikipedia.org/wiki/Cathode_ray). They are nice in many ways, it is "free" (heat up a metal enough and electrons would run out of it, see thermionic emission), it is charged, which means it's easy to manipulate with electric and magnetic field, and it interacts with stuff like generating fluorescence light. Thus the cathode ray tube for display, and scanning electron microscopy for seeing small stuff. As I learnt recently, some ebeam litho equipments actually work more like a display, and it's called shaped beam.


![ebeam_evolution](/assets/images/2024/ebeam/ebeam_litho_evolution.png)
*From [Pfeiffer2010](/assets/doc/2024/EBL_paper/pfeiffer2010.pdf)*


The first use of ebeam for direct write lithography is more than 60 years old, and it has evolved into many different kinds for different purposes. Here we will focus on just some common aspects of ebeam litho, and tools that I have used which are all single pixel Gaussian beam, from Raith 150 Two, to JEOL JBX 6300FS (my favorite!), Raith Voyager, and most recently Raith EBPG 5200+.


![ebpg_histpry](/assets/images/2024/ebeam/EBPG_history.png)
*History of EBPG. From [Yale: Electron-Beam Lithography Training » History](https://nano.yale.edu/history)*




# Ebeam specs and why

I think many people, me included, do not appreciate the performance or requirements of ebeam lithography (EBL) enough. Before we get into the details, let's get a taste of the way I would love more people to be doing and looking at things: order of magnitude estimations. Let's take the example of how to deflect the electron beam.


## How do we deflect the electron beam

The answer is simple: there are four fundamental forces, and we really only have one option: electric field and/or magnetic field.


Let's try to estimate how much electric field or magnetic field we need to deflect the electrons by some reasonable angle. 
- It is funny to me that the wikipedia article on [electrostatic deflection](https://en.wikipedia.org/wiki/Electrostatic_deflection) does not have a single voltage number in it (at the time of the writing: 20240924). 
- For electric field, it is simple: it should be comparable to $$ V_a \cdot \tan\theta $$, where $$V_a$$ is the acceleration voltage, and $$\theta$$ is the deflection angle. Hence for small deflection of a ~20 kV beam, it should be a couple hundred volts to a few kV. 
- For magnetic field, it depends on the radius of the trajectory which is limited by the size of the machine, and let's say it is $$ r = 0.1~\text{m}$$. The resulting magnetic field $$B = mv/e/r \approx 5~\text{mT} = 50~\text{G}$$ (assuming speed of 0.3c or 30 keV acceleration). Hmm this magnetic field is actually pretty close to the target for a few coils I winded lol, so I could straight tell you that you need ~2000 turns with a current of ~100 mA.

![image45.png](/assets/images/2024/ebeam/image45.png)
*The coil I winded for tuning superconducting resonators in a dilfridge. It uses NbTi wire from [Supercon Inc.](https://www.supercon-wire.com/)*

Well actually before we move on, let's also estimate how much mass we need to deflect the beam with gravity lol. Assuming the same force and radius, we have $$e v  B = GMm/r^2$$, and voila, $$M =$$ 7e24 kg. Mass of the earth is 6e24 kg. Damn why are they so close. If we want this mass to fit inside the radius of the ebeam trajectory, it would be only 10x larger than the Schwarzschild radius.

It is funny why it is close to the Schwarzschild radius, and that is because 20 keV electrons are close to a speed of 0.3c, and you could get Schwarzschild radius by just assuming light is a classical particle (mistake 1) and the gravity field/force is Newtonian (mistake 2): $$ m c^2/r = GMm/r^2 $$. And because there are two mistakes, you get an extra factor of 2 (this is not how it actually works): $$ r_s = 2GM/c^2 $$.

Ok this is derailing too much, let's focus back to the EBL specs.


## What are the specs?

These are the EBPG5200 specs, from the Unviersity of Manchester ([link](https://research.manchester.ac.uk/en/equipments/raith-ebpg5200-100kv-e-beam-lithography-system-aka-vistec)):
- Electron Source: Thermal Field Emission
- Acceleration Voltage: 20, 50, and 100 kV
- Beam Current: 0.1 to 200 nA
- Maximum Clock Rate: 50 MHz
- Main Field Beam Deflection: 20 bit DAC
- Maximum Write-Field Size: 1 mm x 1 mm
- Minimum Theoretical Spot Size: 2.2 nm
- Stage Travel Range: 210 mm x 210 mm
- Thermal Stability: < 50 nm / h (Open Loop)
- Footprint: < 20 m^2
- Minimum Feature Size: 6 nm
- Stitching and Overlay Accuracy: < 12 nm
- Wafer Writing: Holders for 3”, 4”, 6”, and 8” Wafer Writing
- Photomask Writing: Holders for 5” and 6” Mask Plate Writing

Similar Specs from [JEOL JBX-6300FS](https://www.jeol.com/products/semiconductor/ebx/JBX-6300FS.php)
- Electron gun: ZrO/W Shottky type
- Acceleration Voltage: 25 kV (option), 50 kV, 100 kV
    - A newer model [JBX-8100FS](https://www.jeol.com/products/semiconductor/ebx/JBX-8100FS.php) has 200 kV option
- 5 nm min pattern, 2 nm beam diameter, 0.125 nm DAC resolution, 0.6 nm laser interferometer resolution
- Max field size 
- 19 bit DAC, 50 MHz scan speed
- Maximum Write-Field Size: 2 mm x 2 mm
- Stage Travel Range: 190 mm x 170 mm
- Stitching and Overlay Accuracy: <= $$\pm9$$ nm
- Hold up to 150 mm (6 in) wafer
- Automatic beam adjustment, dose correction and position correction


Overwhelming? They are all fun to understand and some of these numbers are crazy. Let's go thru them one by one.


## Electron source and emission


I don't know much about this part. Need to read more and add more later.

One fun thing I learnt recently is that, for high current stuff, the emission could be explosive arounf sharp features, and corrode the emitter. The advantage is that the emission current density can be much higher and in the range of $$10^6\sim10^8$$ A/cm^2.

![emission_types](/assets/images/2024/ebeam/emission_types.png)
![explosive_emission](/assets/images/2024/ebeam/explosive_emission.png)
(From thesis [Relativistic magnetron with diffraction output and split cathode](https://digitalrepository.unm.edu/ece_etds/528/))


## Why higher voltage?

The beam is better. Here are two examples I ran by tweaking the comsol charged particle tracing example a bit. It solves for how the ebeam will diverge from interacting with its own E and B field.

![ebeam_physics](/assets/images/2024/ebeam/ebeam_divergence_physics.PNG)

The first solution shows the ebeam trajectories with 1e8 m/s beam or 30 kV, and the second solution shows a 2e8 m/s beam, or 175 kV (notice how nonlinear this velocity vs voltage is because of relativity. Try it yourself at [this calculator](https://www.ou.edu/research/electron/bmz5364/calc-kv.html).). I did not bother to change the current or size of the beam, but the point of having higher acceleration voltage is very clear.

![ebeam_trajectory_1e8](/assets/images/2024/ebeam/trajectory_3A_v=1e8.PNG)
*Divergence of ebeam trajectory with 30 kV acceleration voltage.*

![ebeam_trajectory_2e8](/assets/images/2024/ebeam/trajectory_3A_v=2e8.PNG)
*175 kV acceleration, much smaller divergence*

Ok now let's see if we could do this with pen and paper instead of a fancy simulation. The logic is as follows: current density gives how much coulumb repulsion there is, and from how much time the beam has between it exits the electro-optics system and hitting the chip, we could calculate how much it has moved laterally. Warning, the following calculation is non-relativistic and probably off by a factory of order of unity.
- Current of the beam is $$ I = eV\rho \pi (D/2)^2 $$.
- Electric field for an electron at the edge of the beam: $$ E = \frac 1{2\epsilon_0}\rho e D/2 $$.
- The amount of change on the beam diameter is $$ \Delta D = \frac 1 2 \frac{eE}{m} (L/v)^2 $$, where $$L$$ is travel length from the deflection/focusing field to the sample. 
- As a resut, if we keep the current of the beam constant, the amount of expansion of the beam $$ \Delta D = \frac{e}{2\pi m \epsilon_0} I L^2 v^{-3} D^{-1}$$.
- This looks scary, let's see if the dimensions and rough order of magnitude works out (btw I use [numbat.dev](https://numbat.dev/) for this kind of calculations. Highly recommnd.). Typical ebeam current is 1 nA with a diameter of 10 nm. The electron speed is 1e8 m/s. Assume $$L = 0.1$$ m. I'm getting $$\sim 3$$ um for $$\Delta D$$. This sounds much bigger than the actual beam size... Maybe the magnetic field is not negligible, and most importantly the focus should be already at the sample.
- In any case, the $$v^{-3}$$ dependency is likely general.


![beam_expansion_estimation.PNG](/assets/images/2024/ebeam/beam_expansion_estimation.PNG)
*This is [numbat.dev](https://numbat.dev/), ladies and gentlemen.*


Actually talk is cheap, why not do the velocity sweep in COMSOL and check the simulated beam size? I did, here is the result:
![velocity_sweep](/assets/images/2024/ebeam/charged_particle_tracing_20241014.png)
- Hmm it is actually not $$v^{-3}$$, welp, let's blame relativity and move on with our life.



## Beam current, higher? Lower?

The rule of thumb for current is, and as you could see from derivation in the previous section, the smaller it is, the smaller the beam could be focused, and it scales linearly (if I did not make any mistake deriving it).

On the other hand, the major motivation to go to higher current beam is the exposure time. Life is short, and ebeam is expensive. Let's say Alice has a 10 mm by 10 mm chip (p.s. do not use square or near-square chips for anisotropic materials), and she is writing 0.1% of the chip area just like most people doing hands on fab (wasting most of the materials most of the time). The dose for Alice's resist is around 1000 uC/cm^2. From these and the current, Alice could easily calculate how much time the beam needs to be on to expose all the resist in all the area.


![exposure_time_estimation.PNG](/assets/images/2024/ebeam/exposure_time_estimation.PNG)

17 minutes! Not bad! That is only $177 on Stanford SNSF's EBPG5200 if Alice is an industry user (indirect cost included, see [Rates](https://snsf.stanford.edu/labmembers/rates)). However, both the time and the cost could very quickly climb up when Alice starts to expose say 1% of her chip, and use some novel resist that needs 3x higher dose, and trying to write five chips in one go. Boom, that is 150x more. So be smart and use higher current when you can, and always run the estimation especially now EBPG's `cebpg` or `cjob` came with an exposure time estimation which even takes into account the calibration and load/unload. I'd recommend you still do your own homework, and plan accordingly, so you don't need to panic when seeing an ETA of 5 hours in front of the ebeam computer.

One thing to be aware about higher current beam (we are talking about the 100 nA + ones) is, they might not be used often, and could be out of calibration, so off that the calibration itself might not run properly. So be prepared to tune the beam yourself, or switch to a lower one until the calibration runs properly.



## DAC clock rate and shot pitch / spot size

I am not a digital guy, and am not equipped to appreciate the clock rate of a 20 bit DAC. What I could do here is to point out the limit or tradeoff between DAC rate, dose, and shot pitch or spot size. In short, the time a single shot need, is dose times the area, divided by the current, and it cannot be shorter than the rate the DAC could steer the beam. 
- $$ \frac 1 {\text{DAC rate}} \sim \frac{\text{dose}\times \text{shot pitch}^2 /4 }{ \text{beam current}} $$.

For our 50 MHz DAC rate from the spec, that is ~ 20 ns. If we are exposing 1000 uC/cm$$^2$$ with 1 nA at 8 nm shot pitch, the dwell time neede is 160 ns, and we are safe. But if you switch to a 10 nA beam, you'd need a larger shot pitch.



## DAC resolution

So how good is a 20 bit DAC, and why do we need it? 20 bit is $$2^{20} \approx 10^6$$,  that is a dynamic range of 60 dB.
For comparison, for reading out voltages, an oscilloscope typically has 8 to 10 bit, and prefer to have a higher sampling rate (e.g. [Tektronix MSO](https://www.tek.com/en/datasheet/2-series-mso-mixed-signal-oscilloscope-datasheet)).
At slower sampling rate, and for analog output, [NI DAQ](https://www.ni.com/pdf/product-flyers/multifunction-io.pdf) has 16 ~ 18 bit at around 1 MS/s. And for sensitive measurement such as lock-in amplifiers, you can find 14 ~ 16 bit at ~ 200 MS/s (e.g. Zurich Instruments [HF2LI](https://www.zhinst.com/ch/en/products/hf2li-lock-in-amplifier#specifications)).
Someone who's an expert on DAC/ADC should make a tradeoff and price chart of all these specs.

Back to DAC for ebeam, a dynamic range of 60 dB roughly means that we could have $$10^6$$ shots along x and y within a single write field. That is, how many distinct spots can we have before we have to move the stage.
For a spot or step size of ~ 4 nm, that means the write field can be as big as ~ 4 mm (in principle). The max write field size on EBPG5200 is indeed 1 mm x 1 mm. You are writing a terapixel image onto your chip with the ebeam, and doing it one pixel at a time, and ~ 50 millions per second.
- I would like to point out that I recently learnt that shaped beam, or electron projection lithography (EPL) has been improving, and they can do a few gigapixels per second by late 1990s, and a million beams in parallel. (See [Pfeiffer2010](/assets/doc/2024/EBL_paper/pfeiffer2010.pdf) and [Petric2009](https://pubs.aip.org/avs/jvb/article-abstract/27/1/161/467317/REBL-A-novel-approach-to-high-speed-maskless))

![EBL_throughput_pixel_per_sec_pfeiffer2010.PNG](/assets/images/2024/ebeam/EBL_throughput_pixel_per_sec_pfeiffer2010.PNG)

- One challenge there is sending data to the digital pattern generator (DPG), which "needed throughput with only 1 Tbit/s of compressed data sent to the DPG". ([Petric2009](https://pubs.aip.org/avs/jvb/article-abstract/27/1/161/467317/REBL-A-novel-approach-to-high-speed-maskless))



## Stability

Why is stability important? Here is an example of bad stability (writefield stitching), and maybe another one about dose/current drift if I could find an SEM for it. Basically anything that is being precisely controlled and could affect the properties of the beam (current/dose, size/focus, and position).

![LNNB19](/assets/images/2024/ebeam/20180920_LNNB19_top_dev6_001.PNG)
*You can see two writefield stitching error in this SEM.*

Let's estimate how much change do we need to shift the beam by ~100 nm, which would be too much in many devices.
- For the field that deflects the ebeam, this is ~10x the beam spot size. Since the DAC dynamic range is 60 dB, this means a stability of $$10^{-5}$$.
- For the stage positioning, let's see how much temperature variation would lead to a change of 100 nm for a 200 mm stainless steel cassette/holder.
    - Steel (and many common metals) have a CTE of $$1\sim 2 \times 10^{-5}$$, a 100 nm deformation out of 200 mm is $$ \sim 10^{-6} $$, thus the temperature stability has to be ~ 0.1 C.

How long would it take the cassette to thermalize after you have inevitably touched it and heated it up?
- This depends on how the cassette is held, the path for heat dissipation could be as short as the thickness of the cassette (10 mm), or as long as the size of it (100 mm).
- [Thermal diffusivity](https://en.wikipedia.org/wiki/Thermal_diffusivity) is very handy for time scale estimation for thermalization. All you need to remember is it has a unit of length squared over time, thus 10x longer thermalization path would take 100x longer time.
- I'm actually not sure if the cassette is made of steel or aluminum. Let's use aluminum since it has higher thermal diffusivity of $$\sim 100~\text{mm}^2/\text{s}$$. As a result, it takes 1 s to 100 s for the heat to diffuse, and you probably would want to wait 10x of that for it to be within 1% of the original temperature difference (0.1 C of the 10 C temperature change from your finger).


How about the magnets used in the electro-optic system?
- This is because different current and writefields use different aperture and different settings on the magnets. Whenever you select and switch to a different beam, the system would demagnetize and then put it back.
- I do not have a good answer.
- The practice on the JEOL was to do the beam change at the beginning of everything, and thus when you have finished mounting and loading etc., there's a good chance it is 15 min later.
- On EBPG, the default wait time is 60 s.


## How does the ebeam tool know it is in a good state?

There are mainly the following states that need to be good
- properties of the beam: current/dose, size/focus, and position
    - current: measured by the Faraday cup. If the tool is dumb like Raith voyager, you'd need to remember to manually ask the tool to automatically calculate the dwell time for your target dose
    - size/focus: this will be covered in the calibration section. In short, it scans the beam off a marker or a sharp edge, and optimize the sharpness of the scan signal
    - position: also more in the calibration section. The tool points the beam to existing markers, use the beam to find the marker position, and thus correcting where the beam is pointing.
- position of the stage: measured with [laser inteferometers](https://www.ligo.caltech.edu/page/what-is-interferometer).
- relative position between the stage and the beam: this is also called writefield stitching: the tool will move around the stage, and thus moving around a marker. The beam will then point around accordingly and look for the same marker, This links the position of where the stage is going and where the beam is going.




# Practical stuff

Ok hopefully I have yapped enough about the specs of the ebeam tool. The following will be practical stuff that I'd be talking you through if you are shadowing me through an ebeam session. It will probably be boring to read... I'll just do it and see how I could improve it with fancy photos and stupid drawings.

## Design 

So you have something you want to make with ebeam? Have you thought about no? Make sure you really need ebeam because it is expensive, usually takes longer (30 min or more of preparation time vs. ~ 10 min), and more annoying to do. If your mean feature size is more than one or two microns, consider photolitho. If you have access to a maskless photolitho tool, then it is a no brainer. If not, then you might want to use ebeam to just save the wait time for your photomask.

Ok, design, design... The first thing I could think of is, it is likely you'll have another layer after your ebeam patterns. No matter what you are trying to do, ebeam features are probably too small for interfacing with the macroscopic world, and you'll need some photolitho metal pads for contacting your probe, or even just some markers and labels to see your devices. Think about how the ebeam pattern is going to interface the photolitho patterns, and how are you going to find them in the maskless or mask aligners.


Think about the locations and clearance for your chip. How are you going to mount your chip on the sample holder, how big is the shadow from the clamp on the holder, what is the orientation of your device and your chip in the design, and in the ebeam tool.


Think about how is the beam and the stage are going to move on your chip to write your patterns or devices, how the writefield is going to be arranged on your patterns. Avoid unnecessary crossing of sensitive structures over the writefield boundaries. If you cannot avoid it, think about how to make the adjacent writefields also adjacent in time during the exposure, e.g., how is the writefield order, meander x or y, or floating, or manually assigned. If the writefield is fixed on a grid, is your device on the same grid or interger multiple of it? This is a iterative process with the fracturing, as well as actually finish the layer and check the structures. Think about it more in advance could probably save you a few runs.


## Fracturing

About fracturing, you should really check out GenISys's own [BEAMER training](https://www.genisys-gmbh.com/webinar-series-beamer-training.html) materials, there are way more details there. BEAMER could also do booleans, transforms, arrays, assign dose factors etc. These are relatively straight forward and won't be covered here, just go play.

In short, fracturing is breaking your pattern into more primitive shapes that the ebeam tool would be more readily fill them with shots. And then arrange these fractured patterns into writefields, and tell the ebeam tool where are the writefields, and which field to write first.

Since there are plenty of training materials out there, I figure I'd mention stuff that is harder to encounter but very handy
- The extract node actually has many features, the most often used one is extract by layer, but you could also extract by cell, extract certain region etc. Very useful when you figure out you need to hack something but do not have time to rerun your cad script to generate a new DXF or GDSII.
- There are many ways to change the dose (dose factor), and they could stack properly. For example, you could have a PEC (proximity effect correction), and then dose sweep that whole PEC pattern.
- There are many ways to change the writefield arrangement, as well as the write order within a writefield. Make sure you play with them and see the result in beamer if it's relevant for your pattern. The extreme case for this is, you could even breakup a single device into multiple layers, and manually assign the order to be following the layers.
- There are also ways you could play with how writefields are stitched together: overlapping & sharing the dose, interleaving etc.
- Be careful with the dose for [multipass](https://www.genisys-gmbh.com/multipass-techniques.html). The tool does not know if you are doing multipass or not (at least not yet), and you have to take care of reducing it.
- Be clear about the origin of your pattern. It is the leading cause of a failed aligned beamwrite.
- You could have multiple import and multiple export nodes, handy for  merging multiple designs and playing with different final fracturing settings.
- ALWAYS CHECK THE FINAL OUTPUT/EXPORT. I have many horror stories of some wrong settings messing up a beamwrite that could be caught by checking the output in beamer, such as not selecting the layer for manual writefield, and that layer (usually squares that enclose patterns you want to keep within a single writefield) got exposed by the beam, overwritting the actual patterns.

I feel like there are plenty more. I'll add to this list over time when things occur to me or if you have stuff to add, let me know.


### Proximity effect correction (PEC)

(See also GenISys [Part 2 – Dose PEC Algorithm and Parameter](https://www.genisys-gmbh.com/part-2-dose-pec-algorithm-and-parameter.html))

When the electron shoots into the resist, it scatters around multiple times, and effectively giving a volumetric distribution of dose. This distribution is called the point spread function (PSF), and it blurs out the pattern you are trying to expose. Proximity effect correction (PEC) is the attempt to correct this effect.

![tracer-bild2-2.png](/assets/images/2024/tracer-bild2-2.png)
*Simulation of the scattering path of electrons.*

I used to not be a believer in PEC, but I still do it manually almost every beamwrite, assigning a lower dose factor to larger areas. At some point the types of different manual dose just became too much work, I tried it, and realized I did not appreciate the basis of how it works. How I convinced myself that PEC could work is because the resist development is a nonlinear process:
- If the development is linear, then there is no way to have a single shot that is missing in a big exposed area to be resolved. You will always get resist strength or thickness that represents the dose after getting smoothed by the PSF.
- If the development is extremely nonlinear (resist thickness jump from 0 to max at the threshold dose), then you could slowly decrease the dose, such that the threshold  is at the edge of the missing single shot, and such an amazing resist would make such crazy feature possible
- In reality, the effectiveness of PEC is somewhere in between these two extreme scenarios. You will be able to clear finer patterns that would otherwise be imppossible without PEC, but it also has limits, and that depends on how accurate the PSF, and how good the resist and its development is etc.

A few comments:
- I only have experience with dose PEC, but [shape PEC](https://www.genisys-gmbh.com/shape-pec.html) exists
- The PSF usually have two length scales, and PEC usually only attempt to correct the long range one (backscatter, mostly sensitive to accel. voltage and substrate material). The short range one would take much more compute to "de-convolute" it
- Whenever you change the PEC parameters, you'll likely need a dose sweep. Scaling the PEC doses such that the big area end up having the same dose as before is a good starting point.



## Ebeam resist

My first exposure of ebeam resist is with [MMA](https://en.wikipedia.org/wiki/Methyl_methacrylate)/[PMMA](https://en.wikipedia.org/wiki/Poly(methyl_methacrylate)) double layer for Josephson junctions (JJ) ([Dolan bridge](https://en.wikipedia.org/wiki/Niemeyer%E2%80%93Dolan_technique)). It was such a long time ago and I did not have much "cleanroom consciousness" on what was important and what needed improvement. Later on I happened to need to make them again.

![JJ_20200225_D1_45deg_020.jpg](/assets/images/2024/ebeam/JJ_20200225_D1_45deg_020.jpg)
*Here is a JJ made with MMA/PMMA Dolan bridge. You could see the aluminum from the second angled evap hit the sidewall of the lower layer resist, and left a vertical flap standing after liftoff.*

When I got started at Stanford cleanroom, the first process I shadowed and learnt was using [CSAR](https://www.allresist.com/portfolio-item/e-beam-resist-ar-p-6200-series-csar-62/) to mask silicon etch on silicon-on-insulator (SOI) substrate. It was a great choice for starters, as the dose is low ($\sim 300~\text{uC/cm}^2$, exposure would be fast) and pretty robust, the development is also short (sub one minute) and pretty robust. The only annoyance is the cleaning after the plasma etch.
You could find a lot of SEM images of pattered silicon photonics, so here I wanted to show you that you could also use CSAR for liftoff (which to be honest you could probably also find a lot of SEM of).

![20180216_dose_11_dev_1_1.jpg](/assets/images/2024/ebeam/20180216_dose_11_dev_1_1.jpg)
*One of the dose tests of CSAR liftoff of aluminum. The challenge here is a narrow and meandering gap between two metal electrodes. You could see the liftoff failed around the center, where the solvents really struggled to get in.*


![20191022_LiSa_mechanics_A_012.jpg](/assets/images/2024/ebeam/20191022_LiSa_mechanics_A_012.jpg)
*Here you are seeing thin-film lithium niobate (darker region in top-left) on sapphire (bright charged up region in bottom right), with aluminum electrodes evaporated on top, at large angles for it to climb the steep sidewall, and lifted off with CSAR.*


After about half a year, I got into developing/optimizing a mask and etch process for thin-film lithium niobate. There were a lot of grinding, but the relevant part here is that together with a labmate, we started developing a recipe for HSQ ([Hydrogen silsesquioxane](https://en.wikipedia.org/wiki/Hydrogen_silsesquioxane)) resist, or Flowable oxide (FOx) might sound more familiar to some people, or spin-on glass.




As for ebeam liftoff, I continued working with MMA/PMMA double layer, as well as PMMA/PMMA double layer with different concentrations and thickness. I also learnt and used single layer CSAR for liftoff. It sounds impossible or challenging because it is a single layer, but the exposure actually leaves a negative sidewall, and made the liftoff possible.


Before moving on, I'd like to put down some quick tips on stuff that is related to resist:
- positive vs. negative: if there are more areas you would like to keep, use positive resist (exposed area gets developed away), and if you have more areas you'd like to etch, use negative resist
- adhesion: use HMDS priming if you can. Use higher temperature dehydration bake if you can. Some thin metal layer like titanium could also help adhesion. O2 or ozone plasma could also help although I have not tried it personally.
- discharge layer: important if your substrate is not conductive, like most dielectrics (quartz, lithium niobate, sapphire etc.). Many people like [electra 92](https://www.allresist.com/portfolio-item/protective-coating-ar-pc-5090-02-electra-92/), but I hated it, maybe because I was using an outdated bottle. I am a fan of 5~10 nm aluminum discharge layer. Be careful about using other metal for discharge, pick ones with low melting point. I've had 5 nm titanium discharge layer cross-linked top of resist because it was too hot. If your pattern does not involve alignment and does not span across multiple writefield, you might get away with no discharge layer.
    - remove the discharge layer: I remember electra you could remove with water? Please fact check me. Be wary that water plus IPA could unintentionally develop some resist. For aluminum, it gets etched in MF319 or MF26A. You could also use acids if you are a maniac.
- selectivity: Not sure what I want to say here. If this is a problem, consider thicker resist, harder resist (like HSQ), or methods that could harden it after the development, like a hard bake, or curing it with higher dose ebeam (e.g., [Enhancing etch resistance of hydrogen silsesquioxane via postdevelop electron curing](https://doi.org/10.1116/1.2395949), it's a rare scene to see dose of 100 mC/cm$$^2$$).
- liftoff: 80 C NMP (Remover PG) is very common and effective. Sometimes long overnight soak at room temperature could also help. Sonication definitely helps until it starts breaking your structures of delaminating the metal. Making sure you have the proper resist sidewall angle (if using single layer liftoff) or enough undercut is the best and most important factor for a successful liftoff. In terms of design, anything that helps with the access of the solvents to go underneath the gaps you are trying to liftoff would help the liftoff.


### Dose and dose sweep

I was thinking about whether to skip this section. Maybe just a few comments
- When do you need a dose sweep? Including but not limited to: when you have changed your substrate, changed your resist thickness, changed the beam voltage, changed to a new bottle of resist, when you haven't been in the cleanroom for a couple of months, or when the ebeam tool just had a major maintenance, and when your pattern esp. pattern density has changed a lot (except if you are doing PEC and have faith in your PSF).
- How much should you sweep? +- 20% should be plenty. If it is a new resist for you, it is good to do a larger range to know the absolute limits.
- Put down labels next to your dose sweep patterns. Do not believe in your memory, you will not remember which pattern got which dose. Make sure you could see the labels and dose sweep patterns in both optical and scanning electron microscope (e.g. if your dose sweep pattern is tiny, you'll struggle to locate it under SEM. Put down some big labels and use a big beam to expose the labels).



## Mounting

Mounting the chip has very similar concern as for wirebonding, if you have read that post. But everything is more tight. There are pretty much three factors: no chip moving around during the exposure, rotation or tilt needs to be small, and it has to discharge properly
- No moving around: do a shake test after you've done mounting the chip. It does not need to be crazy, the EBL is not doing 10*g like commercial EUVs, but the stage will be accelerating. This is more important when you have multiple chips on the same holder or even held using the same clamp. Avoid this if you can, but sometimes you just have more chips than the holders there are.
- Tilt: make sure the top and bottom surface is clean before you put it on the holder. If a dirt is visible, it is going to be at least a few tens of microns. If you got resist on the back of the chip, try scratch the majority off, and then wipe with acetone and IPA. If you have time, redo the spin coat and use a better vacuum chuck. In general, a height variation on the order of ~10 um across ~10 mm is good.
    - The EBPG holder let's you have full control over tilt, height and rotation of your chip, so you do not need to worry as much about dirt or resist, but it does make the loading significantly more time consuming than the JEOL, and longer if you start with some poor tilt and rotation
- Rotation: the default threshold on EBPG is 0.3 deg if I remember correctly. And if you are using automatic alignment mark detection, the alignment mark should at least fit in the writefield/search window, and you should calculate how many degree is that from the window size and separation of your alignment marks.
    - When your pattern is cursed, or if you are trying to align to a previous layer that is very off (say a few degrees) from the edge of the chip, you might want to compensate it when mounting the chip. The rotation the EBPG holder is allowed to do is limited. JEOL instead you could rotate as much as you want, at the cost of no fine control of the rotation, and you really need good hand to do if right. I'd show off to people when I got the JEOL holder rotation right the first try.
- Discharge: if your substrate is insulating, you need to think a bit more about this, make sure the clamp is in contact with the discharge layer, especially when it is evaporated metal and could be missing at some edges because of the shadow of the clamps of the ebeam evaporation holder.

Also let's just look at the holders and try to understand how they hold your chip and how you adjust them.

![JEOL_holder_image1.png](/assets/images/2024/ebeam/JEOL_holder_image1.png)
![JEOL_holder_image5.png](/assets/images/2024/ebeam/JEOL_holder_image5.png)
- These are the JEOL cassette and holders. The calibration sample is not on the cassette, I'm actually not sure where that is.
- It is a front-referenced holder. The copper slots are made such that the bottom of its outer rim where it mates with the cassette, is at the same height as the bottom of its inner slot, where the top of your chip will be pushed against from below it. As a result, the surface of your chip is guaranteed to be at the same height as the top surface of the cassette.
- The chip is then secured by aluminum plates (backplates? not sure about their formal name) with copper springs that locks into grooves of the copper holder, So it pushes the chip upward against the copper slot. Be careful when you press down and rotate the copper spring, as the aluminum plate is only balanced on the back of your chips. And do it slowly to avoid rotating the aluminum plate which will rotate your chips out of the slot (and they'll drop upside down on the table, or through the hole on the floor if you are unlucky).
- The copper holders can rotate freely, so you could expose your chip at any angle you like. The copper holder is secured by two clamps. Always check all the holders have their clamps tightened. You never know.
- You can load multiple chips into the same slot, and if you do, you better check that their top and bottom surfaces are clean so that they'd be held secure at the same time. Always do a shake test before you send the cassette in.
- If you are doing aligned beamwrite on multiple chips, they'll need to be in separate holders because they'll need separate rotation correction, unless you got gold hand to load them into the slot with less than 0.3 degree rotation alignment.


Here is the EBPG cassette and holders, from [UPenn EBPG5200 SOP](https://wiki.nano.upenn.edu/wiki/images/0/0a/EBPG5200%2B_SOP.pdf):
![EBPG_holder](/assets/images/2024/ebeam/EBPG_holder_image1.png)
- The EBPG cassette looks similar to the JEOL's at a glance, but it is totally different
- The reference/calibration chip is on the holder, and mounted in a very mindful place, protruding out of the holder, so that you'll bump into and crack it, and they could sell you more.
- It is back-referenced. You will need to adjust the tilt and height of the individual holders to make the top surface of your chip aligned and parallel to the reference/calibration chip and the surface of the cassette. If the user before you had very different chip thickness, good luck you got a lot of screws to turn.
- The tilt adjustment is done similar to a kinematic mount if you are coming from optics background. It is pushed up against three set screws, the tips of which determines the plane of the holder surface. HOWEVER it is also secured or locked by the table lock release levers, by friction, so you always need to remember to release them whenever you are about to measure the height, or after you adjusted the screws. And the friction is not strong enough to hold much downward force, so you could easily push the holder down and away from the screws, and it would still be locked by the levels. When in doubt, always release the levers.
- The rotation correction is done by the adjustment screw on the left and right sides of the holder. The gear ratio is pretty high, at least 10x from eyeballing, so fine rotation adjustment is much easier than on the JEOL holder. It even got a hole on the side for you to stick a lever in to adjust it. However, if your rotation correction is more than ~5 degrees or so, it will be out of range for the adjustment lever to fit in without running into the outer rim of the cassette, brilliant mechanical design. It is still possible to manually rotate the holder by hand instead of using the adjustment screw, it's just much harder to get it right. And you are likely doing this under the alignment microscope. Make sure you check that the cassette is still in place on the alignment stage after you manually rotated the holder.



A few minor and common things and comments
- Make sure your pattern won't overlap with the clamps or slots, as well as the clamp won't shadow your pattern or alignment marks. Even when the alignment marks are not under but close to the edge of the clamp, you might see some drift when you are imaging the marker with the ebeam.
- Be careful with the holders and screws as they are expensive.

Here is how expensive they are:
![JEOL holder cost](/assets/images/2024/ebeam/JEOL_holder_cost.jfif)
*A photo I took at Stanford SNC, summer 2016*
![EBPG holder cost](/assets/images/2024/ebeam/EBPG_holder_cost.PNG)
*From [UD NanoFab EBPG5200 SoP](https://bpb-us-w2.wpmucdn.com/sites.udel.edu/dist/9/3681/files/2016/11/EBPG5200_Operating-Procedure_03.pdf)*


## Locating

Ok you have mounted your chip, now how do you find your chip and alignment mark, and how do you know where to put your pattern? It is the same as how you find your home, you need the country, state, city, and street address. What you are used to is a city map, that is your CAD, and you know the street address (local coordinates or your CAD coordinates) of your devices and alignment marks. Locating stuff in the tool is just converting the street address to latitude and longitude. You find where the (0, 0) of your city map is on latitude and longitude, and then add the relative coordinates.
- The details are going to be different for different tools, but the idea is the same. You'll either need to know where is the (0, 0) of the global/cassette coordinates, or have something safe to look at both outside and inside the tool, let's call this location A. On the JEOL, we usually use the top left corner of the chip as A, which we measure its coordinates using an optical microscope, as well as the center of the chip (by finding one or more corners of the chip), and then you know the relative address of the chip with respect to A. Once you find the coordinates of A inside the tool with the ebeam, you know where your chip is. For JEOL, this coordinate of the center of your chip would be the `offset` parameter that goes into the `SDF` file.
- For EBPG, you spoiled kids might have the alignment microscope, which directly tells you the global coordinates of wherever you are looking at, and it will be very close to the actual coordinates in the tool. So you do not need a reference location A, just go find corners of your chip and then calculate its center coordinates.
- Be careful with the orientation of the cassette and the direction of the axis. E.g., for our JEOL alignment optical microscope, you have to put the cassette upside down onto a stage with glass window, and that flips the y axis of the cassette. For EBPG alignment microscope, the cassette is rotated 90 degree (I actually no longer remember this, fact check it yourself.). For both JEOL and EBPG, the global coodrinates have positive y pointing downward, which is different from common sense but gets rid of minus signes when the top left of the cassette is chosen to be global (0, 0).
- For aligned beamwrite, now you need to tell the tool where the alignment markers are, in the global coordinates. So saome procedure, except, instead of finding the center of the chip, you find one of your global marks.
- The optical microscope and the ebeam will always have some misalignment, and the further away your chip is from the reference chip, the larger it will be. I always check for the first one or two global marks for automatic alignment, to make sure the marker is visible, and the auto-align will run properly.

Anyway, the above all sound complicated and unnecessary, but all you are doing is just measuring and adding a bunch of vectors, and at most three layer of them. Should be totally manageable when you start tracking them with a spreadsheet and build up a picture in your head about how they add up from the global (0, 0) or the reference point you choose, to the location (e.g. chip center) or feature (e.g. the first global mark) you are looking for.


## Alignment


This is the fun part. This is probably the most fun and satisfying part of the beamwrite. Actually watching the ongoing exposure showing up on the SEM window is the most satisfying part (can't believe Raith 150-2 or voyager does not show that to you). But watching the automatic marker detection on both JEOL and EBPG are fun in different ways. The JEOL one makes you feel like a radar operator, and the EBPG one feels like firing a shotgun lol.


Why do we need alignment? It's because you crazy people want to put down another layer of pattern that is within ~10 nm from one existing layer. And the existing layer could be off with some translation, rotation, and even stretched or sheared a bit. The way to tell the ebeam tool how your existing pattern is transformed, is to let the beam finds the actual location of a few markers, and compare them to the location in the cad (where they are supposed to be), and the tool will calculate how to shoot the second layer with the same transformation, that it will align with the first layer.


Ok now you know what the markers are for, how do you choose the size, shape and location of your markers? 
- Think about if you also want to use the marker for photolitho alignment, a nested marker might help with that. 
- Learn what the tool allows, e.g. JEOL prefers crosshair style, and EBPG prefers a square. I remember recently (as of Oct. 2024) seeing EBPG will support more marker types soon (or already). 
- Learn what locations the tool prefer, such as JEOL only accept PQRS style global markers at north, south, west and east of your chip, and M1, M2, M3, M4 style markers for chip marks (at four corners of a rectangle), and EBPG is four corners of a rectangle for both global marks and pattern marks. 
- Try if you could use only three or two markers. One day you will have one marker missing or not usable for various reasons, and you'd still want to align to that chip instead of starting over from the previous layer.



Now you got markers on the chip, how to let the tool finds them automatically?
- For manual alignment, it is much more straight forward, just tell the tool where the markers are (in the `jdf` or `sdf` I no longer remember which one, or in the `cjob` for EBPG, either global marks or chip/pattern marks should work). 
- For JEOL, you need someone to guide you through the magic spells like `MDRG`, `SETWFR`, `CHIPAL`, or dig into the manual, or play on the tool when you are waiting for the LL is pumping down. Going into these details are too much for here. They are really not that hard to figure out. It is a logical process
    1. First adjust the scan parameters just like how you'd optimize the beam for a nice SEM image, gain (contrast) and offset (brightness) to get good SNR of a line scan on the arm of your marker. As well as where to scan on the arm (from the center of the crosshair) and width of the scan
    2. Then you test the scan in `MDRG` as well as playing with number of scans, averages, do you want multiple scans on the same arm, how much spacing should they have etc. `CHIPAL` is the subprogram for the chip mark detection.
    3. Then the `SETWFR` is for automatic detection of the global marks, where you could have a coarse scan first to look for the mark, and then a fine scan to get a more precise coordinates of it.
- For EBPG, it is simpler or I have not dig into it as much as on JEOL. You pretty much only need the size and whether your mark is positive or negative, and then add it in your `cjob`.
    - If you want manual marker detection because somehow the automatic did not work, use `JOY` type for the markers.

A few comments before moving on
- If you are putting down markers, it's good to also give them labels. Sometimes you just can't help but doubt yourself, am I on the correct marker?
- Put down multiple sets of markers. Sometimes you'll just forget the marker would get exposed and damaged or destroyed in the following process. Sometimes some of them just did not come out properly from the previous process.
- Use larger marker for global alignment. Always easier to find larger markers, and then let the tool fine tune on the smaller chip or pattern markers
- By the way chip markers and pattern markers are the same thing, it is just JEOL calls them chip markers and EBPG calls them pattern markers



## Calibrations

I already mentioned some of the calibrations in the section on ebeam specs. Maybe I'll just continue that discussion.

There are mainly the following states that need to be good
- properties of the beam: current/dose, size/focus, and position
    - current: measured by the Faraday cup. If the tool is dumb like Raith voyager, you'd need to remember to manually ask the tool to automatically calculate the dwell time for your target dose
    - size/focus: this will be covered in the calibration section. In short, it scans the beam off a marker or a sharp edge, and optimize the sharpness of the scan signal
    - position: also more in the calibration section. The tool points the beam to existing markers, use the beam to find the marker position, and thus correcting where the beam is pointing.
- position of the stage: measured with [laser inteferometers](https://www.ligo.caltech.edu/page/what-is-interferometer).
- relative position between the stage and the beam: this is also called writefield stitching: the tool will move around the stage, and thus moving around a marker. The beam will then point around accordingly and look for the same marker, This links the position of where the stage is going and where the beam is going.

I know better how JEOL does it, so I'll explain the JEOL calibration process in a bit more detail, and what you should pay attention to and adjust if needed.

1. Beam focus: the beam will doa  line scan across a sharp edge, along both x and y direction, and stepping the focus. 
    - You will see it outputs a table with rows being different focusing depth, and in the columns the measured beam size along x and y, and the overall beam size. For a reasonable beam, the optimal should be somewhere around the middle of all the rows since it intentionally starts above and finish below the optimal focus (or the other way around). If the optimal is near the top or bottom, that means it was very off before the calibration.
    - If the beam size is larger than usual, it is usually because that sharp edge is getting scanned too much and getting dirty. You could (but usually not recommended) move the scanning position a bit (~100 nm) to a fresh spot.

2. Beam deflection: the beam gets deflected towards a few different markers on a calibration sample with known coordinates, and line scans across their arms to find the coordinates.
![jeol_alignment_scan](/assets/images/2024/ebeam/20200615_LNSOI11/image67.jpg)
    - This is how the scans look like. The first row includes raw signal of the x and y line scan. If you see flat lines with no noise, that means the signal is saturated, and the scan parameters need adjustment
    - The second row is the derivative of the first row, with some smoothing
    - No one (I do not) knows what the third row is. Likely some correlation stuff.
    - The middle inset shows where the beam is deflecting within the writefield
    - After this, the tool knows how to deflect the beam properly to hit a given coordinate

3. Writefield alignment: very similar to the beam deflection calibration, but now the stage also moves
    - You could watch the stage coordinates, as well as the middle inset. The beam will also look up, down, left, and right, and line scan to find the marker, but the stage will also move at the same time, so that the beam is looking at the same marker four times.
    - After this, the tool knows where or how much to send the stage to a given coordinate


Now the tool is calibrated, you have prepared your job (oops skipped this part, honestly not much else if you could find where to put your pattern, and where to find your alignment marks). It is time to send it, and watch some fresh errors you have never seen before!

## Common errors

I'm just going to make a list of stuff I could immediately think of
- Exceed the DAC rate: EBPG should be able to catch this when you import your `GPF` file in the `cjob`. For JEOL you would need to run the `schd` on your `jdf` and `sdf` to let it check.
- Height detection error: the tool use an LED at near-grazing angle onto the chip, and bounce it off onto a CCD to detect the height of the chip. It might miss the chip, or hit the clamp, or maybe your chip is transparent. Try shrink the size of your chip in the job file. Try paint the backside of your chip with sharpie (I've never done it myself), or disable the height check and go with the flow lol (esp. if you know that the pattern you are exposing is not critical).
- Can't measure height at the marker: the chip might be too dirty near the marker, or the marker might be too close to the clamp or edge of the chip. Try unload, shift the chip a bit, and re-align and reload (if you have time). More likely you'll just skip this bad marker
- Rotation angle is too big: if it is just a bit above the threshold the tool usually allow, AND you are sure if found the correct marker, you could adjust the threshold. There is a good chance it found the wrong marker, e.g., the one from a different set of markers. Double check with your own eyes on the SEM. If you just did a horrible job mounting the chip, take it out and redo it.
- The most sacry errors are errors that do not show up as errors on the tool, including but not limited to:
    - You messed up the extent or center of your pattern: if everything is smooth untill you developed the resist and found out everything is nicely off by a huge but same amount, it is likely the extent or center of your pattern got messed up during fracturing
    - You made a typo in the center/offset for the pattern, or which holder to expose: non-zero probability this could happen especially for no alignment. Watch where the beam is on the cassette after you start the exposure
    - You did not check the final output of the fracturing and messed up the layers, or the writefield path: you should always keep an eye on the pattern that is being exposed in the SEM window, at least for the beginning. You should know how it should look like, and notice if there is anything going wrong.

Ok you've really been through a lot at this point, it is time to sit back, watch the beam going around in the SEM window, and relax a bit. When your exposure is ~ 5 min left, get your lazy ass off the chair and start preparing for the development. Good luck!



# Acknowledgements

As I have been boasting about my ebeam litho experience this whole section, I also would like to mention where I got all these knowledge so that I still sound like a reasonable human being and thus you would still be happy to continue reading. My lab manager/advisor at Tsinghua IIIS helped me start my cleanroom experience with nearly infinite patience. And as mentioned above, I really appreciate that he insisted on making us operate every single valve, shutter, and setpoints manually, immensely helped me with understanding of the working principles of various cleanroom tools and components. During my time at Stanford, many many senior lab members and cleanroom staff guided me and answered many questions from me, as well as worked on documentations of the existing process and for the cleanroom tools.

Lastly, I would like to say that even with all these years of experience, I am no where near of being an expert on ebeam tool or ebeam lithography. Although I routinely do things that normal users would be afraid to do or never thought of doing (which I enjoy a lot), my experience and knowledge would pale in comparison to the amount the field engineers or ebeam engineers have. They have been working with these tools for their whole career, and only if they were more active in perserving their knowledge... If your facility has an ebeam engineer that is talkative and senior, talk to them! Ask them to share their knowledge!

# References

## Lab resources
1. Caltech KNI lab: [EBPG 5000+: 100 kV Electron Beam Lithography](https://lab.kni.caltech.edu/EBPG_5000%2B:_100_kV_Electron_Beam_Lithography)
2. Stanford [EBL Practical Guide](https://drive.google.com/file/d/1QefNaVA8mRoXeRkXaiWEuVK5TIaO3ECp/view) ([backup](/assets/doc/2024/EBL Practical Guide-Feb 2024.pdf))
3. BEAMER training from GenISys: [Webinar Series - BEAMER Training](https://www.genisys-gmbh.com/webinar-series-beamer-training.html)
4. Yale Institute for Nanoscience and Quantum Engineering: [Electron-Beam Lithography Training](https://nano.yale.edu/electron-beam-lithography-training).
5. The University of Manchester: [Raith: EBPG5200 100kV e-Beam Lithography System (aka Vistec)](https://research.manchester.ac.uk/en/equipments/raith-ebpg5200-100kv-e-beam-lithography-system-aka-vistec)
5. [UPenn EBPG5200 SOP](https://wiki.nano.upenn.edu/wiki/images/0/0a/EBPG5200%2B_SOP.pdf)
6. University of Delaware Nanofab [EBPG5200 SOP](https://bpb-us-w2.wpmucdn.com/sites.udel.edu/dist/9/3681/files/2016/11/EBPG5200_Operating-Procedure_03.pdf)

## Training videos
4. [JEOL JBX-9300FS EBL (1 of 2) - training video (Georgia Tech - Microelectronics Research Center)](https://www.youtube.com/watch?v=q8h5xYJX-_U)
5. [JEOL JBX-9300FS EBL (2 of 2) - training video (Georgia Tech - Microelectronics Research Center)](https://www.youtube.com/watch?v=SQhP-k8iYWM)


## Papers and books
1. Altissimo, Matteo. "E-beam lithography for micro-/nanofabrication." Biomicrofluidics 4.2 (2010). [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2917861/)
2. Chen, Yifang. "Nanofabrication by electron beam lithography and its applications: A review." Microelectronic Engineering 135 (2015): 57-72. [link](https://www.sciencedirect.com/science/article/abs/pii/S016793171500101X?via%3Dihub)
3. Gilmour Jr, Alexander S., and A. S. Gilmour. Klystrons, traveling wave tubes, magnetrons, crossed-field amplifiers, and gyrotrons. Artech House, 2011.
4. Rai-Choudhury, Prosenjit. Handbook of microlithography, micromachining, and microfabrication: microlithography. Vol. 39. SPIE press, 1997.
5. Pfeiffer, Hans C. "Direct write electron beam lithography: a historical overview." Photomask Technology 2010. Vol. 7823. SPIE, 2010.




# Appendix: my ebeam lithography journey

I will use this section to quickly go through the ebeam tool I have used in the past, and the things I like and hate the most about them. With SEMs of devices made with these tools! (so that you don't fall asleep) I will also look back at what different aspects of ebeam litho I focused on during different periods of time, as well as resists and chip/substrates I have used. These are the stuff I have the most experience on and could speak about.

## Tools

### Raith 150 Two (2015 - 2017)
- Why is the GUI completely frozen when the sample plate is loading or unloading? Why can't I check my patterns or configure the beam/column parameters?
- Why is there a joystick? Some people might like it but I absolutely do not want to accidentally bumped into it. Disabling the x and y channel on the joystick is the first thing I do when I got to the tool.
- I am struggling to come up with a good thing about it. Maybe the lower beam voltage is good for not damaging 2D materials? The holder sucks (the one that literally works like a clipboard, I always worry about my chip being tilted..), the focusing sucks (you have to apply gold nanoparticles or make a scratch on your chip), queuing up the schedule/job sucks, the GUI and toolbar are so stacked and not intuitive... I should stop here.

![graphene_quantum_dot.jpeg](/assets/images/2024/graphene_quantum_dot.jpeg)
*A graphene quantum dot with gate electrodes defined by ebeam litho with Raith 150 Two. The scalebar in (b) is 500 nm. [paper](https://pubs.acs.org/doi/full/10.1021/acs.nanolett.6b02522)*

### JEOL JBX 6300FS (2017 - 2022)
- It is perfect, please do not change.
- Hmm maybe make it easier to copy the log message from the GUI. Maybe this is partly because of the linux system, it took me a while to figure out I have to triple click to "select-all, and then drag-drop while holding the SCROLLING WHEEL to copy the log messages out.
- It has one of the best loadlock / loading arm in the whole cleanroom. The cassette/holder is also front referenced, there is no need to tune the tilt and height of your chip. God I love the JEOL.
- Writefield for low current beam is small though, 62.5 um. Why is it 62.5 um? Because it is 1000 um divided by $$2^4$$.


![LN_OMC_SEM.png](/assets/images/2024/LN_OMC_SEM.png)
*A thin-film lithium niobate (LN) optomechanical crystal, where etching of the LN is masked by ebeam litho resist mask, and the aluminum is also lifted off with ebeam resist. Minimum dimension is 10 nm! (iirc) [paper](https://opg.optica.org/optica/fulltext.cfm?uri=optica-6-7-845&id=414988)*


![LNSOI_SEM.png](/assets/images/2024/LNSOI_SEM.png)
*Another thin-film LN device, this time on silicon-on-insulator (SOI). Colored by my labmate and friend Felix, purple sausage is LN, and silicon is green. [paper](https://www.nature.com/articles/s41567-023-02129-w)*

### Raith Voyager (2022 - 2023)
- Same complains as Raith 150 Two. Very similar in terms of user experience.
- Maybe the max writefield got larger?


### EBPG 5200+ (2023 - 2024)
- Looks like a JEOL, GUI is as responsive. Easy to schedule and queue jobs.
- The exposure time estimation is great!
- Unfortunately the cassette/holder is back referenced. You need to fix the tilt and thickness of your chip. The alignment microscope is also smart and dumb at the same time. It is smart in the wrong way that disabled the user's ability to think.

\[SEM redacted\]

*Hopefully one day I'll be able to talk about devices I made with colleagues during this period of time. They look absolutely stunning and insane...*


## Ebeam sessions

I'm surprisingly organized enough to have spreadsheet to keep track of all my beamwrites (a very rare case, pbb because the tool is just too expensive to not be organized about it). The total number of sessions turns out to be ~ 420 total. This is too many... I should have moved on sooner.
- 2023 - 2024: 60?  Played with proximity effect correction a lot during this time.
- 2021 - 2022: 109. Started and perfected automatic mark detection and alignment on JEOL.
- 2019 - 2021: 92 (damn covid). Mainly grinding other fab process during this time. Explored with discharge layers when working with insulating substrate like sapphire.
- 2017 - 2018: 162. Developing a certain fab process with a labmate, was doing beamwrite almost every week, sometimes more than once a week.
- pre 2017: sporadic. This was the graphene quantum dot period of my career. I did not know much about what is going on in the fab, but got a lot of operation-from-first-principle kind of experience since my lab manager does not trust automation, and want us to operate as manually as possible. It was a blessing in disguise.

I have been talking about the spreadsheets for logging the beamwrite sessions. I should actually show you guys a screenshot of one. These are the parameters (most of them) I keep track of every single beamwrite, and hopefully you will have a much better idea what they are when you keep reading more.

![beamwrite_log_sheet.png](/assets/images/2024/beamwrite_log_sheet.png)
*Log sheet I created for keeping track of beamwrites from me and the team. This is specifically for JEOL, but most of the parameters are relevant in general, and will make more sense as you read on.*

(This post is started on 2024-08-15, and finished on 2024-10-15. Last updated on 2024-10-15.)
