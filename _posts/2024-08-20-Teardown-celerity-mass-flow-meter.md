---
title: "Celerity mass flow meter teardown"
categories:
  - Teardown
tags:
  - Solenoid
  - Magnet
  - Flexure
  - Nanofab
toc: true
toc_sticky: True
use_math: true
header:
  cover: /assets/images/2024/MFC_Teardown_20240817230453.png
  overlay_image: /assets/images/2024/MFC_Teardown_20240817230453.png
  show_overlay_excerpt: false
  overlay_filter: 0.5
---


Teardown of the Celerity mass flow meter
- add how you got it


![MFC_Teardown_20240817230453.png](/assets/images/2024/MFC_Teardown_20240817230453.png)


# Very brief intro to mass flow meter and controller

If you are working in any kind of physical fabrication or manufacturing, you have likely encountered usage of various gases and liquids. To have a repeatable process, you would want to control the flow of your gas or liquid well, and that is done with a mass flow controlel (MFC).

In my case, I have seen it on more than half of the cleanroom equipments. Any kind of etcher (RIE, Ion milling) or gas/vapor based deposition tool (PVD, CVD, ALD), as long as there is gas involved, there would be a few MFCs hidden inside the tool that set your SF6 or O2 flow to the 50 sccm you wanted. And they could occasionally fuck up and ruin your process, so learn, appreciate, and prey for their well-being!

There are quite a few kinds of MFC, but they all have at least two parts, one part that is sensing the flow, and the other part that is controlling the flow (and some electronics with how to readout and calibrate the flow, and apply the control). There are many good reads for this, and [this one](https://www.mks.com/mass-flow-technology-technote) is particularly good (I admit I only read this one and [another one](https://www.bronkhorst.com/en-us/service-support/knowledge-base/coriolis-mass-flow-measuring-principle/)). A very common and cheap type of MFC is the rotameters where you pbb have seen them on nitrogen dessicator or machines with liquid/water flows that does not require high precision. We will focus on the ones with finer measurement control, and more specifically thermal mass flow meter based controllers. Another interesting type of flow meter is using Coriolis force and are called [Coriolis flow meters](https://www.bronkhorst.com/en-us/service-support/knowledge-base/coriolis-mass-flow-measuring-principle/). They 

![thermal_mass_flow_sensor_config.jpg](/assets/images/2024/thermal_mass_flow_sensor_config.jpg)
*Different sensor configuration of a thermal mass flow meter. From [MKS](https://www.mks.com/mass-flow-technology-technote).*

The core idea of the sensing part is, think about what the flow is and could carry (mass -> momentum, temperature -> heat), and how do you induce a change of it and measure its effect because of the flow. In the case of the thermal mass flow sensing, it is the temperature distribution. In the case of the Coriolis flow meters, it is the vibration phase of the sensing tube.


![thermal_mass_flow_temperature_distribution.jpg](/assets/images/2024/thermal_mass_flow_temperature_distribution.jpg)
*Asymmetric temperature distribution on the sensing tube because of the flow. From [MKS](https://www.mks.com/mass-flow-technology-technote).*


The control and actuation part of the flow controller is relatively more straight forward. Any method to increase the impedance of the flow could slow it down. Stick a "finger" into the path, or moving a cover up and down at a hole the flow must go thru, you name it.


# Initial teardown

Opening it up is pretty straight forward.

Screws removed:
- two on the flaps of the case that connect the case to the in and out port flange
- two on the two sides of the D-type connector
- cut the seal, now could lift off the case
- one on the back of the PCB that mounts it to the side of the sensor. It also holds the insulating paper between the back of the PCB and the inner side of the case (preventing electrical short)

The board with the external connectors (a D type, two that look like ethernet, and one test leads (?) sticking out from the board itself) can be unplugged from the main board.


![MFC_Teardown_20240817230505.png](/assets/images/2024/MFC_Teardown_20240817230505.png)
![MFC_Teardown_20240817230511.png](/assets/images/2024/MFC_Teardown_20240817230511.png)

The flexible cable is actually soldered onto the main PCB... I tried to desolder it, and then find out it is also glued onto the PCB on one side. My patience ran out and I just cut it in half.

![MFC_Teardown_20240817230520.png](/assets/images/2024/MFC_Teardown_20240817230520.png)


# Valve

It took me a while to trial and realize the enclosure is screwed on. I was thinking maybe they welded it really well to prevent any leak, but the hole at the top where the cable is coming out looks suspicious. The enclosure is actually part of a voice coil / solenoid.



![MFC_Teardown_20240817230531.png](/assets/images/2024/MFC_Teardown_20240817230531.png)

Further open the lid underneath the solenoid, there is a flexure inside, and a manifold to guide the gas around.


![MFC_Teardown_20240817230541.png](/assets/images/2024/MFC_Teardown_20240817230541.png)
![MFC_Teardown_20240817230549.png](/assets/images/2024/MFC_Teardown_20240817230549.png)

The gas flow path/manifold is beautiful, it goes around and up thru the two side channels, and then pass down thru the center which is covered by the flexure.

(To be continued... (20240824) )


# Sensing tube



