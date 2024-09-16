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
  overlay_image: /assets/images/2024/tracer-bild2-2.png
  cover: /assets/images/2024/tracer-bild2-2.png
  show_overlay_excerpt: false
  overlay_filter: 0.5
---



# What is EBeam litho, and why?

Ebeam lithography, as the name suggests, is using electron beams for lithography. [Lithograph](https://en.wikipedia.org/wiki/Lithography) has a pretty old history, and involves a mask or print plate, materials to be printed (started with oil), and a physical or chemical process to shape the print using the mask. It is a powerful technique at the time to mass produce drawings and maps, and later photos (photography). When people start to think about how to reduce the size of electronic circuits in the 1950s, they adopted photographic technique (using optics to shrink and project the pattern, expose and develop the [photoresist](https://en.wikipedia.org/wiki/Photoresist) just like in photography) and thus coined the term [photolithography](https://en.wikipedia.org/wiki/Photolithography). Circuit designers would draw the circuit layout on a big canvas, that would later [tapeout](https://en.wikipedia.org/wiki/Tape-out) (it is still called tapeout to this date even physical tape is no longer involved) and be shrinked into a [photomask](https://en.wikipedia.org/wiki/Photomask), and shrinked again by the photolitho system onto the wafer. The quest for shrinking the size of electronic circuits and transistors has been on a non-stop march, and shorter wavelengths are needed because of refractive limit of the resolution. But you know what has a much shorter wavelengths? Electrons!

Let's quickly estimate typical "wavelengths" of electrons in an electron beam. Assuming 10 kV of acceleration, that makes its speed roughly $$0.2 c$$, where $$c$$ is the speed of light. This is without relativistic correction, which will be $$10\%$$ or $$ 20\%$$ so let's ignore it. The corresponding momentum is $$ 5\times 10^{-23}~\text{kg}\cdot\text{m/s} $$ (hmm this is suspiciously close to Boltzmann constant... whatever), and these electrons's [de Broglie wavelength](https://en.wikipedia.org/wiki/Matter_wave) would be $$ 1.2\times 10^{-11}~\text{m} $$ or 12 pm. If we were to get light with wavelength this small, they would be called [gamma rays](https://en.wikipedia.org/wiki/Gamma_ray).


Electrons are used for many things even before [its discovery](https://www.britannica.com/science/atom/Discovery-of-electrons) in 1897, before which electron beams would only be called [cathode rays](https://en.wikipedia.org/wiki/Cathode_ray). Electrons are nice in many ways, it is "free" (heat up a metal enough and electrons would run out of it, see thermionic emission), it is charged, which means it's easy to manipulate with electric and magnetic field, and it interacts with stuff like generating fluorescence light.

(To be continued)



# Ebeam basics
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

## Training videos
4. [JEOL JBX-9300FS EBL (1 of 2) - training video (Georgia Tech - Microelectronics Research Center)](https://www.youtube.com/watch?v=q8h5xYJX-_U)
5. [JEOL JBX-9300FS EBL (2 of 2) - training video (Georgia Tech - Microelectronics Research Center)](https://www.youtube.com/watch?v=SQhP-k8iYWM)


## Papers
1. Altissimo, Matteo. "E-beam lithography for micro-/nanofabrication." Biomicrofluidics 4.2 (2010). [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2917861/)
2. Chen, Yifang. "Nanofabrication by electron beam lithography and its applications: A review." Microelectronic Engineering 135 (2015): 57-72. [link](https://www.sciencedirect.com/science/article/abs/pii/S016793171500101X?via%3Dihub)
3. Gilmour Jr, Alexander S., and A. S. Gilmour. Klystrons, traveling wave tubes, magnetrons, crossed-field amplifiers, and gyrotrons. Artech House, 2011.


