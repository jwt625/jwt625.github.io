---
title: "Teardown Celerity mass flow meter"
categories:
  - Teardown
tags:
  - Solenoid
  - Magnet
  - Flexure
  - Nanofab
  - Control
toc: true
toc_sticky: True
use_math: true
header:
  cover: /assets/images/2024/MFC_Teardown_20240817230453.png
  overlay_image: /assets/images/2024/MFC_Teardown_20240817230453.png
  show_overlay_excerpt: false
  overlay_filter: 0.5
---


This blog is about the teardown of a Celerity mass flow meter, with a bit of background materials. I got this cute thing at the electronics flea market for only 40 bucks. It got a price tag of \\$375 and the guy asked \\$75. This is a pretty old unit from Celerity, which has "technology heritage of industry leaders such as Tylan, Mykrolis and UNIT Instruments", and got acquired by Brooks in 2009 ([source](https://www.brooksinstrument.com/en/about-us/history)). Here is how it looks after opening its jacket:


![MFC_Teardown_20240817230453.png](/assets/images/2024/MFC_Teardown_20240817230453.png)

Here is some background about mass flow meters. If you are here for the porns, jump to the next section.


# Very brief intro to mass flow meter and controller

If you are working in any kind of physical fabrication or manufacturing, you have likely encountered usage of various gases and liquids. To have a repeatable process, you would want to control the flow of your gas or liquid well, and that is done with a mass flow controlel (MFC).

In my case, I have seen it on more than half of the cleanroom equipments. Any kind of etcher (RIE, Ion milling) or gas/vapor based deposition tool (PVD, CVD, ALD), as long as there is gas involved, there would be a few MFCs hidden inside the tool that set your SF6 or O2 flow to the 50 sccm you wanted. And they could occasionally fuck up and ruin your process, so learn, appreciate, and prey for their well-being!

There are quite a few kinds of MFC, but they all have at least two parts, one part that is sensing the flow, and the other part that is controlling the flow (and some electronics with how to readout and calibrate the flow, and apply the control). There are many good reads for this, and [this one](https://www.mks.com/mass-flow-technology-technote) is particularly good (I admit I only read this one and [another one](https://www.bronkhorst.com/en-us/service-support/knowledge-base/coriolis-mass-flow-measuring-principle/)). A very common and cheap type of MFC is the rotameters where you pbb have seen them on nitrogen dessicator or machines with liquid/water flows that does not require high precision. We will focus on the ones with finer measurement control, and more specifically thermal mass flow meter based controllers. Another interesting type of flow meter is using Coriolis force and are called [Coriolis flow meters](https://www.bronkhorst.com/en-us/service-support/knowledge-base/coriolis-mass-flow-measuring-principle/). They actuate and sense the vibration of the sensor tube, which depends on the mass or density of the flow. When the flow is running, the two legs (in and out) of the sensor tubes would vibrate with a phase difference  because of the angular momentum from the vibration carried by the flow.

![thermal_mass_flow_sensor_config.jpg](/assets/images/2024/thermal_mass_flow_sensor_config.jpg)
*Different sensor configuration of a thermal mass flow meter. From [MKS](https://www.mks.com/mass-flow-technology-technote).*

The core idea of the sensing part is, think about what the flow is and could carry (mass -> momentum, temperature -> heat), and how do you induce a change of it and measure its effect because of the flow. In the case of the thermal mass flow sensing, it is the temperature distribution. In the case of the Coriolis flow meters, it is the vibration phase of the sensing tube.


![thermal_mass_flow_temperature_distribution.jpg](/assets/images/2024/thermal_mass_flow_temperature_distribution.jpg)
*Asymmetric temperature distribution on the sensing tube because of the flow. From [MKS](https://www.mks.com/mass-flow-technology-technote).*


The control and actuation part of the flow controller is relatively more straight forward. Any method to increase the impedance of the flow could slow it down. Stick a "finger" into the path, or moving a cover up and down at a hole the flow must go thru, you name it.


# Initial teardown

Opening it up is pretty straight forward. Screws removed:
1. two on the flaps of the case that connect the case to the in and out port flange
2. two on the two sides of the D-type connector
3. cut the "warranty void" seal, now could lift off the case
4. one on the back of the PCB that mounts it to the side of the sensor. It also holds the insulating paper between the back of the PCB and the inner side of the case (preventing electrical short)

The board with the external connectors (a D type, two that look like ethernet, and one test leads (?) sticking out from the board itself) can be unplugged from the main board.


![MFC_Teardown_20240817230505.png](/assets/images/2024/MFC_Teardown_20240817230505.png)
![MFC_Teardown_20240817230511.png](/assets/images/2024/MFC_Teardown_20240817230511.png)

The flexible cable is actually soldered onto the main PCB... I tried to desolder it, and then find out it is also glued onto the PCB on one side. My patience ran out and I just cut it in half.

![MFC_Teardown_20240817230520.png](/assets/images/2024/MFC_Teardown_20240817230520.png)


# Valve

It took me a while to trial and realize the enclosure is screwed on. I was thinking maybe they welded it really well to prevent any leak, but the hole at the top where the cable is coming out looks suspicious. The enclosure is actually part of a solenoid. The coil looks and feels dirt cheap, wrapped with teflon tape (?).



![MFC_Teardown_20240817230531.png](/assets/images/2024/MFC_Teardown_20240817230531.png)

Further open the lid underneath the solenoid, there is a flexure inside, and a manifold to guide the gas around.


![MFC_Teardown_20240817230541.png](/assets/images/2024/MFC_Teardown_20240817230541.png)
![MFC_Teardown_20240817230549.png](/assets/images/2024/MFC_Teardown_20240817230549.png)

The gas flow path/manifold is beautiful, it goes around and up thru the two side channels, and then pass down thru the center which is covered by the flexure. I have no idea how they machined and polished the surface. To be fair the surface seems to have one principle curvature (I think this is the correct jargon based on my rotting differential geometry knowledge) that is constant, so it can be polished with one rotating disk or sphere.

The next day, I dug out the digital scope I got right before my defense hoping to show people the device I made (turns out they were way too small to see), and took some nicer pictures. Here they are:

![MFC_flexure_S20240818_0007.jpg](/assets/images/2024/MFC_flexure_S20240818_0007.jpg)
*Close-up look of the flexure from the top side. It got the magnet visible on the top to be sucked up by the solenoid.*

![MFC_valve_manifold_S20240818_0008.jpg](/assets/images/2024/MFC_valve_manifold_S20240818_0008.jpg)
*Gas manifold for the valve.*

![MFC_valve_in_out_S20240818_0010.jpg](/assets/images/2024/MFC_valve_in_out_S20240818_0010.jpg)
*Inlet and outlet to the valve from the main body of the MFC.*




# Sensing tube

After removing the sensor from the main body of the MFC, the only visible thing is just a tiny inlet and outlet opening. The actual sensor tube is inside the enclosure. The inlet/outlet hole is tiny, ~ 1 mm diameter.


![MFC_sensor_inlet_S20240818_0004.jpg](/assets/images/2024/MFC_sensor_inlet_S20240818_0004.jpg)

![MFC_sensor_opened](/assets/images/2024/MFC_sensor_opened.jpeg)
*Sensor block removed from the main body of the MFC. The solenoid above the valve was removed in this photo.*

I noticed that every single mating surface, e.g., between the valve enclosure and the main body, or between the sensor module/block and the main body, there is always a spacer. It is likely similar to the copper flange on high vacuum equipments, a clean way to provide sealing without any vacuum lubricant or grease that could cause potential contamination.


The enclosure of the sensor can be easily pried off. It is glued onto the base that got screwed onto the main MFC body, and there is no easy non-destructive way to open it. The sensor tube is covered by normal looking foam. I peeled it off with tweezers. It has aged and is super fragile.

![MFC_sensor_opened_20240818214143.png](/assets/images/2024/MFC_sensor_opened_20240818214143.png)
![MFC_sensor_tube_20240818214150.png](/assets/images/2024/MFC_sensor_tube_20240818214150.png)

Zooming in onto the sensor tube, we can clearly see two wires coiled around the sensor tube. It is a two-wire sensor as shown in the illustration in the first section.

![MFC_sensor_top_view_20240818214155.png](/assets/images/2024/MFC_sensor_top_view_20240818214155.png)
![MFC_sensor_side_view_20240818214203.png](/assets/images/2024/MFC_sensor_side_view_20240818214203.png)

You can see how the traces from the flex cable are connected to the two wires exactly as you would expect from the two-wire sensor schematics.


# Final thoughts: why does the sensor tube look like this?

There are likely a few factors that play in how the dimensions of the sensor tube got determined. For thermal based sensing:
- time scale of thermalization of the gas to the tube
- typical flow rate and its corresponding time scale of the flow through the sensing tube




I'll stop here for now. I wanted to do some order-of-magnitude estimations for why the sensor tube is this length and diameters, look into the valve more (solenoids specs, flexure spring constant and resonant freq etc.), as well as the control electronics. Oh as well as MEMS based MFCs (see [this](https://pubs.aip.org/aip/rsi/article-abstract/91/10/105006/363406/A-microfluidic-flow-meter-with-micromachined)). For now I need to go sleep and prep for the new week... Hope you have enjoyed the photos!






