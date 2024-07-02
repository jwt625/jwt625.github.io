---
title: "Energy to Transmit One Bit"
categories:
  - Blog
tags:
  - Telecom
  - Energy
toc: True
toc_sticky: True
pin: true
header:
  overlay_image: /assets/images/submarine-cable-network-prev.png
  teaser: /assets/images/submarine-cable-network-prev.png
  show_overlay_excerpt: false
  overlay_filter: 0.5
---



# Introduction

The internet has become an essential tool for people to communicate, for both work and entertainment. Since the first internet service providers in 1989, the population of internet users around the world has reached 2.5 billion in 2013. [1] Along with the growth of the internet, the amount of energy comsumed by information communication technology (ICT) is also drastically increasing. From 2007 to 2012, the worldwide electricity consumption has increased by 10.1% on annual average, from 219 TWh to 354 TWh. In the same time period, the share of energy consumption for communication networks in total electricity consumption has grown from 1.3% to 1.8%. [2]

Given the limited natural resources we have and the fact that the advance in ICT results in a positive impact on electricity consumption, it is necessary to exam and reduce the energy we spend on transmitting one bit of information. [3] I will consider two simple case, the energy required to transmit one bit using electrical cables and the energy required to transmit one bit, with optical fibers.

# Part I: Energy of Electrical Signals

To transmit an electrical signal, a voltage is built up on one end of the electrical cable, and the voltage propagates through the cable to the other end. The energy involved in this process is essentially used to charge up the capacitance of the wire, which is proportional to the length of the wire. Therefore, we will measure the capacitance by unit length and also the energy spent by unit distance the signal propagates. With estimations of the unit length capacitance, the voltage used for encoding the bit and the length involved, we can estimated the energy by $E ~ CV^2$.


# References

[1] J. D. Negroponte, S. J. Palmisano, and A. Segal, Defending an Open, Global, Secure and Resilient Internet (Council on Foreign Relations Press, 2013).

[2] S. Lambert et al., "Worldwide Electricity Consumption of Communication Networks," Opt. Express 20, B513 (2012).

[3] K. Saidi, H. Toumi, and S. Zaidi, "Impact of Information Communication Technology and Economic Growth on the Electricity Consumption: Empirical Evidence from 67 Countries," J Knowl. Econ. 8, 789 (2017).

[4] B. Dudley, "[Comcast to Shuffle Channels in August](https://www.seattletimes.com/business/comcast-to-shuffle-channels-in-august/)," Seattle Times, 2 Jul 09.

[5] D. A. B. Miller, "Attojoule Optoelectronics for Low-Energy Information Processing and Communications," J. Lightwave Technol. 35, 346 (2017).

[6] C. C. Hu, Modern Semiconductor Devices for Integrated Circuits (Pearson, 2009).

[7] R. S. Tucker, "Green Optical Communications - Part I: Energy Limitations in Transport," IEEE J Sel. Top. Quant. 17, 245 (2011).

(First published at [http://large.stanford.edu/courses/2018/ph240/jiang1/](http://large.stanford.edu/courses/2018/ph240/jiang1/))