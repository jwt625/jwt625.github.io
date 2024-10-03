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


# What is EBeam litho, and why

Ebeam lithography, as the name suggests, is using electron beams for lithography. [Lithograph](https://en.wikipedia.org/wiki/Lithography) has a pretty old history, and involves a mask or print plate, materials to be printed (started with oil), and a physical or chemical process to shape the print using the mask. It is a powerful technique at the time to mass produce drawings and maps, and later photos (photography).

When people start to think about how to reduce the size of electronic circuits in the 1950s, they adopted photographic technique (using optics to shrink and project the pattern, expose and develop the [photoresist](https://en.wikipedia.org/wiki/Photoresist) just like in photography) and thus coined the term [photolithography](https://en.wikipedia.org/wiki/Photolithography). Circuit designers would draw the circuit layout on a big canvas, that would later [tapeout](https://en.wikipedia.org/wiki/Tape-out) (it is still called tapeout to this date even physical tape is no longer involved) and be shrinked into a [photomask](https://en.wikipedia.org/wiki/Photomask), and shrinked again by the photolitho system onto the wafer. The quest for shrinking the size of electronic circuits and transistors has been on a non-stop march, and shorter wavelengths are needed because of refractive limit of the resolution. But you know what has a much shorter wavelengths? Electrons!

Let's quickly estimate typical "wavelengths" of electrons in an electron beam. Assuming 10 kV of acceleration, that makes its speed roughly $$0.2 c$$, where $$c$$ is the speed of light. This is without relativistic correction, which will be $$10\%$$ or $$ 20\%$$ so let's ignore it. The corresponding momentum is $$ 5\times 10^{-23}~\text{kg}\cdot\text{m/s} $$ (hmm this is suspiciously close to Boltzmann constant... whatever), and these electrons's [de Broglie wavelength](https://en.wikipedia.org/wiki/Matter_wave) would be $$ 1.2\times 10^{-11}~\text{m} $$ or 12 pm. If we were to get light with wavelength this small, they would be called [gamma rays](https://en.wikipedia.org/wiki/Gamma_ray). 

Another way to think about the wavelength or resolution ability of these tens of kV electrons is, 1 eV photons are around 1 um wavelength, so 10 keV photons would be 0.1 nm wavelength, pretty close to the calculation above. The reason why no one uses gamma rays for photolitho is probably they are hard to generate, and photons do not interact with each other except indirectly via atoms or nonlinear dielectrics, or high enough energy to have quantum electrodynamics shit going. People are already using mirrors for 13.5 nm photon EUV photolitho instead of lenses because of transmission loss, and those mirrors have crazy specs (the YouTube channel Asianometry has a series of videos (e.g.: [ASML's High-NA EUV Lithography: A 2024 Update](https://www.youtube.com/watch?v=UdcFpjgCnP8)) about EUV and they are very informative). Gamma rays would mostly just pass through things, and happily ionizing stuff along the way.

Ok back to ebeam. Electrons are used for many things even before [its discovery](https://www.britannica.com/science/atom/Discovery-of-electrons) in 1897, before which electron beams would only be called [cathode rays](https://en.wikipedia.org/wiki/Cathode_ray). They are nice in many ways, it is "free" (heat up a metal enough and electrons would run out of it, see thermionic emission), it is charged, which means it's easy to manipulate with electric and magnetic field, and it interacts with stuff like generating fluorescence light. Thus the cathode ray tube for display, and scanning electron microscopy for seeing small stuff. As I learnt recently, some ebeam litho equipments actually work more like a display, and it's called shaped beam.


![ebeam_evolution](/assets/images/2024/ebeam/ebeam_litho_evolution.png)
*From [Pfeiffer2010](/assets/doc/2024/EBL_paper/pfeiffer2010.pdf)*


The first use of ebeam for direct write lithography is more than 60 years old, and it has evolved into many different kinds for different purposes. Here we will focus on just some common aspects of ebeam litho, and tools that I have used which are all single pixel Gaussian beam, from Raith 150 Two, to JEOL JBX 6300FS (my favorite!), Raith Voyager, and most recently Raith EBPG 5200+.


![ebpg_histpry](/assets/images/2024/ebeam/EBPG_history.png)
*History of EBPG. From [Yale: Electron-Beam Lithography Training » History](https://nano.yale.edu/history)*




# Ebeam basic specs and why

I think many people, me included, do not appreciate the performance or requirements of ebeam lithography (EBL) enough. Before we get into the details, let's get a taste of the way I would love more people to be doing and looking at things: order of magnitude estimations. Let's take the example of how to deflect the electron beam.


## How do we deflect the electron beam

The answer is simple: there are four fundamental force, and we really only have one option: electric field and/or magnetic field.


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

These are the specs, from the Unviersity of Manchester [link](https://research.manchester.ac.uk/en/equipments/raith-ebpg5200-100kv-e-beam-lithography-system-aka-vistec):
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

Overwhelming? They are all fun to understand and some of these numbers are crazy. Let's go thru them one by one.


### Electron source and emission


I don't know much about this part. Need to read more and add more later.

One fun thing I learnt recently is that, for high current stuff, the emission could be explosive arounf sharp features, and corrode the emitter. The advantage is that the emission current density can be much higher and in the range of $$10^6\sim10^8$$ A/cm^2.

![emission_types](/assets/images/2024/ebeam/emission_types.png)
![explosive_emission](/assets/images/2024/ebeam/explosive_emission.png)
(From thesis [Relativistic magnetron with diffraction output and split cathode](https://digitalrepository.unm.edu/ece_etds/528/))


### Why higher voltage?

The beam is better. Here are two examples I ran by tweaking the comsol charged particle tracing example a bit. It solves for how the ebeam will diverge from interacting with its own E and B field.

![ebeam_physics](/assets/images/2024/ebeam/ebeam_divergence_physics.PNG)

The first solution shows the ebeam trajectories with 1e8 m/s beam or 30 kV, and the second solution shows a 2e8 m/s beam, or 175 kV (notice how nonlinear this velocity vs voltage is because of relativity. Try it yourself at [this calculator](https://www.ou.edu/research/electron/bmz5364/calc-kv.html).). I did not bother to change the current or size of the beam, but the point of having higher acceleration voltage is very clear.

![ebeam_trajectory_1e8](/assets/images/2024/ebeam/trajectory_3A_v=1e8.PNG)
*Divergence of ebeam trajectory with 30 kV acceleration voltage.*

![ebeam_trajectory_2e8](/assets/images/2024/ebeam/trajectory_3A_v=2e8.PNG)
*175 kV acceleration, much smaller divergence*

Ok now let's see if we could do this with pen and paper instead of a fancy simulation.






(To be continued)





- How stable do things need to be
- Why is the column this big
- Where are the electrons going
    - focusing (how is it done)
    - current measurement
    - beam calibration
- Where is the stage going
    - interferometer
    - writefield (WF) size, calibration, stitching
    - subfield (maybe?)
- beam parameters
    - Voltage, current
    - shot pitch
    - dose (DAC rate limit, dose sweep)

# Practical
- What resist to use
    - positive vs. negative
    - adhesion
    - discharge layer
    - selectivity
    - liftoff
- Fracturing (BEAMER)
    - Oh god maybe this should be a different yap-post
    - I should still start to write down things that matters
    - Field control: fixed, manual, different ways to meander, fully manual with layers...
    - multipass
    - PEC

![tracer-bild2-2.png](/assets/images/2024/tracer-bild2-2.png)
*Simulation of the scattering path of electrons.*

- Mounting your chip
    - front vs. back referenced
    - height measurement (under uscope, in the tool with the LED)
    - multiple chips
- Locating your chip
    - optical microscope / camera assistance
    - using the SEM
- Alignment
    - desired marks (materials, thickness, locations, reusability)
    - how to find the marks (manual & auto, mark params, scan params)
- develop
    - remove discharge layer
    - be wary water + IPA could develop some resist unintentionally
- feedback & optimization
    - dose sweep
- optimize your own workflow
    - better estimation of the exposure time
    - What is the bottleneck? What can be automated?
- TBA...





# Appendix: A quick rundown of my ebeam lithography journey

I will use this section to quickly go through the ebeam tool I have used in the past, and the things I like and hate the most about them. With SEMs of devices made with these tools! (so that you don't fall asleep) I will also look back at what different aspects of ebeam litho I focused on during different periods of time, as well as resists and chip/substrates I have used. These are the stuff I have the most experience on and could speak about.

## Tools

### Raith 150 Two (2015 - 2017)
- Why is the GUI completely frozen when the sample plate is loading or unloading? Why can't I check my patterns or configure the beam/column parameters?
- Why is there a joystick? Some people might like it but I absolutely do not want to accidentally bumped into it. Disabling the x and y channel on the joystick is the first thing I do when I got to the tool.
- I am struggling to come up with a good thing about it. Maybe the lower beam voltage is good for not damaging 2D materials? The holder sucks (the one that literally works like a clipboard, I always worry about my chip being tilted..), the focusing step sucks, queuing up the schedule/job sucks, the GUI and toolbar are so stacked and not intuitive... I should stop here.

![graphene_quantum_dot.jpeg](/assets/images/2024/graphene_quantum_dot.jpeg)
*A graphene quantum dot with gate electrodes defined by ebeam litho with Raith 150 Two. The scalebar in (b) is 500 nm. [paper](https://pubs.acs.org/doi/full/10.1021/acs.nanolett.6b02522)*

### JEOL JBX 6300FS (2017 - 2022)
- It is perfect, please do not change.
- Hmm maybe make it easier to copy the log message from the GUI. Maybe this is partly because of the linux system, it took me a while to figure out I have to triple click to "select-all, and then drag-drop while holding the SCROLLING WHEEL to copy the log messages out.
- It has one of the best loadlock / loading arm in the whole cleanroom. The cassette/holder is also front referenced, there is no need to tune the tilt and height of your chip. God I love the JEOL.



![LN_OMC_SEM.png](/assets/images/2024/LN_OMC_SEM.png)
*A thin-film lithium niobate (LN) optomechanical crystal, where etching of the LN is masked by ebeam litho resist mask, and the aluminum is also lifted off with ebeam resist. Minimum dimension is 10 nm! (iirc) [paper](https://opg.optica.org/optica/fulltext.cfm?uri=optica-6-7-845&id=414988)*


![LNSOI_SEM.png](/assets/images/2024/LNSOI_SEM.png)
*Another thin-film LN device, this time on silicon-on-insulator (SOI). Colored by my labmate and friend Felix, purple sausage is LN, and silicon is green. [paper](https://www.nature.com/articles/s41567-023-02129-w)*

### Raith Voyager (2022 - 2023)
- Same complains as Raith 150 Two. Very similar in terms of user experience.


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
- 2017 - 2018: 73 + 89. Developing a certain fab process with a labmate, was doing beamwrite almost every week, sometimes more than once a week.
- pre 2017: sporadic. This was the graphene quantum dot period of my career. I did not know much about what is going on in the fab, but got a lot of operation-from-first-principle kind of experience since my lab manager does not trust automation, and want us to operate as manually as possible. It was a blessing in disguise.

I have been talking about the spreadsheets for logging the beamwrite sessions. I should actually show you guys a screenshot of one. These are the parameters (most of them) I keep track of every single beamwrite, and hopefully you will have a much better idea what they are when you keep reading more.

![beamwrite_log_sheet.png](/assets/images/2024/beamwrite_log_sheet.png)
*Log sheet I created for keeping track of beamwrites from me and the team. This is specifically for JEOL, but most of the parameters are relevant in general, and will make more sense as you read on.*

## Ebeam resist

My first exposure of ebeam resist is with [MMA](https://en.wikipedia.org/wiki/Methyl_methacrylate)/[PMMA](https://en.wikipedia.org/wiki/Poly(methyl_methacrylate)) double layer for Josephson junctions ([Dolan bridge](https://en.wikipedia.org/wiki/Niemeyer%E2%80%93Dolan_technique)). It was such a long time ago and I did not have much "cleanroom consciousness" on what was important and what needed improvement.

When I got started at Stanford cleanroom, the first process I shadowed and learnt was using [CSAR](https://www.allresist.com/portfolio-item/e-beam-resist-ar-p-6200-series-csar-62/) to mask silicon etch on silicon-on-insulator (SOI) substrate. It was a great choice for starters, as the dose is low ($\sim 300~\text{uC/cm}^2$, exposure would be fast) and pretty robust, the development is also short (sub one minute) and pretty robust. The only annoyance is the cleaning after the plasma etch. After about half a year, I got into developing/optimizing a mask and etch process for thin-film lithium niobate. There were a lot of grinding, but the relevant part here is that together with a labmate, we started developing a recipe for HSQ ([Hydrogen silsesquioxane](https://en.wikipedia.org/wiki/Hydrogen_silsesquioxane)) resist, or Flowable oxide (FOx) might sound more familiar to some people, or spin-on glass.

As for ebeam liftoff, I continued working with MMA/PMMA double layer, as well as PMMA/PMMA double layer with different concentrations and thickness. I also learnt and used single layer CSAR for liftoff. It sounds impossible or challenging because it is a single layer, but the exposure actually leaves a negative sidewall, and made the liftoff possible.


## Acknowledgements

As I have been boasting about my ebeam litho experience this whole section, I also would like to mention where I got all these knowledge so that I still sound like a reasonable human being and thus you would still be happy to continue reading. My lab manager/advisor at Tsinghua IIIS helped me start my cleanroom experience with nearly infinite patience. And as mentioned above, I really appreciate that he insisted on making us operate every single valve, shutter, and setpoints manually, immensely helped me with understanding of the working principles of various cleanroom tools and components. During my time at Stanford, many many senior lab members and cleanroom staff guided me and answered many questions from me, as well as worked on documentations of the existing process and for the cleanroom tools.

Lastly, I would like to say that even with all these years of experience, I am no where near of being an expert on ebeam tool or ebeam lithography. Although I routinely do things that normal users would be afraid to do or never thought of doing (which I enjoy a lot), my experience and knowledge would pale in comparison to the amount the field engineers or ebeam engineers have. They have been working with these tools for their whole career, and only if they were more active in perserving their knowledge... If your facility has an ebeam engineer that is talkative and senior, talk to them! Ask them to share their knowledge!

# References

## Lab resources
1. Caltech KNI lab: [EBPG 5000+: 100 kV Electron Beam Lithography](https://lab.kni.caltech.edu/EBPG_5000%2B:_100_kV_Electron_Beam_Lithography)
2. Stanford [EBL Practical Guide](https://drive.google.com/file/d/1QefNaVA8mRoXeRkXaiWEuVK5TIaO3ECp/view) ([backup](/assets/doc/2024/EBL Practical Guide-Feb 2024.pdf))
3. BEAMER training from GenISys: [Webinar Series - BEAMER Training](https://www.genisys-gmbh.com/webinar-series-beamer-training.html)
4. Yale Institute for Nanoscience and Quantum Engineering: [Electron-Beam Lithography Training](https://nano.yale.edu/electron-beam-lithography-training).
5. The University of Manchester: [Raith: EBPG5200 100kV e-Beam Lithography System (aka Vistec)](https://research.manchester.ac.uk/en/equipments/raith-ebpg5200-100kv-e-beam-lithography-system-aka-vistec)


## Training videos
4. [JEOL JBX-9300FS EBL (1 of 2) - training video (Georgia Tech - Microelectronics Research Center)](https://www.youtube.com/watch?v=q8h5xYJX-_U)
5. [JEOL JBX-9300FS EBL (2 of 2) - training video (Georgia Tech - Microelectronics Research Center)](https://www.youtube.com/watch?v=SQhP-k8iYWM)


## Papers and books
1. Altissimo, Matteo. "E-beam lithography for micro-/nanofabrication." Biomicrofluidics 4.2 (2010). [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2917861/)
2. Chen, Yifang. "Nanofabrication by electron beam lithography and its applications: A review." Microelectronic Engineering 135 (2015): 57-72. [link](https://www.sciencedirect.com/science/article/abs/pii/S016793171500101X?via%3Dihub)
3. Gilmour Jr, Alexander S., and A. S. Gilmour. Klystrons, traveling wave tubes, magnetrons, crossed-field amplifiers, and gyrotrons. Artech House, 2011.
4. Rai-Choudhury, Prosenjit. Handbook of microlithography, micromachining, and microfabrication: microlithography. Vol. 39. SPIE press, 1997.
5. Pfeiffer, Hans C. "Direct write electron beam lithography: a historical overview." Photomask Technology 2010. Vol. 7823. SPIE, 2010.


(This post is started on 2024-08-15, and finished on TBA. Last updated on TBA.)
