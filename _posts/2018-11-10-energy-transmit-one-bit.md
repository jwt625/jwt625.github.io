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
use_math: true
header:
  overlay_image: /assets/images/submarine-cable-network-prev.png
  cover: /assets/images/submarine-cable-network-prev.png
  show_overlay_excerpt: false
  overlay_filter: 0.5
---



# Introduction

The internet has become an essential tool for people to communicate, for both work and entertainment. Since the first internet service providers in 1989, the population of internet users around the world has reached 2.5 billion in 2013. [1] Along with the growth of the internet, the amount of energy comsumed by information communication technology (ICT) is also drastically increasing. From 2007 to 2012, the worldwide electricity consumption has increased by 10.1% on annual average, from 219 TWh to 354 TWh. In the same time period, the share of energy consumption for communication networks in total electricity consumption has grown from 1.3% to 1.8%. [2]

Given the limited natural resources we have and the fact that the advance in ICT results in a positive impact on electricity consumption, it is necessary to exam and reduce the energy we spend on transmitting one bit of information. [3] I will consider two simple case, the energy required to transmit one bit using electrical cables and the energy required to transmit one bit, with optical fibers.

# Part I: Energy of Electrical Signals

To transmit an electrical signal, a voltage is built up on one end of the electrical cable, and the voltage propagates through the cable to the other end. The energy involved in this process is essentially used to charge up the capacitance of the wire, which is proportional to the length of the wire. Therefore, we will measure the capacitance by unit length and also the energy spent by unit distance the signal propagates. With estimations of the unit length capacitance, the voltage used for encoding the bit and the length involved, we can estimated the energy by $E \sim CV^2$.

However, for long range connections, only the length occupied by one single bit is charged and consumes energy. The length for each bit can be approximated by the propagation speed multiplied by the clock cycle. Take USB 3.0 as an example (see Fig. 1), the 5 Gbps transfer rate corresponds to clock cycle $\sim 200~\text{ps}$. [4] The electromagnetic wave propagates at the speed of light, which gives the corresponded length scale to be 6 cm. Longer sigal occupies longer length, and requires more energy.

For estimating the unit length capacitance, the first thing to notice is that the unit length capacitance of different electrical cables and transmission lines are roughly on the same order of magnitude. For example, the capacitance of a typical 50 Ω coaxial cable is around 1.5 pF/cm. In comparison, on-chip interconnections have size that's smaller than the coaxial cable by five orders of magnitude, but the corresponded capacitance is ~ 2 pF/cm, comparable to coaxial cables. [5]

Typical voltage involved in semiconductor devices are ~ 1V. [6] Putting the estimations of unit length capacitance, length of one bit and the operating voltage together, the energy for one bit using electrical signal is on the order of 10 pJ.

![USB3p0-connector.jpg](/assets/images/USB3p0-connector.jpg)

*Fig. 1: USB 3.0 connector (Source: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Connector_USB_3_IMGP6022_wp.jpg))*


# Part II: Energy of Optical Signals

The most important difference between optical signal and electrical signal is that, instead of charging up the cable or electromagnetic medium to a certain voltage, the signals are carried by photons. The photons are converted to voltages at the photodetector, and this photon detection is essentially a quantum process: ~ 1 electron is excited from each absorbed photon. For photons at wavelength $\lambda = 1.55$ μm which is typically used in fiber communication, the energy of one single photon hν ~ 1 eV, where eV is the electron-volt (energy of one electron at one volt). The current from 1 nW oof optical power at this wavelength is ~ 1 nA. With a 1 GΩ load resistor, the photodetector generates ~ 1 V. [5]

In reality, the photocurrent charges up the capacitance from the detector circuit, and the resulting voltage must be enough to flip a CMOS logic gate, typically U = 1 V. Assuming a total capacitance $C_\text{TOT} = 1$ fF, then the total charge required is $Q = CU$. [5] The number of electrons roughly equals the number of photons impinging on the detector, which is $N_\text{photon} = E/h\nu = N_\text{electron} = Q/e$. Thus the energy per bit is $E = h\nu\cdot CU/e = 1$ fJ. This estimate is roughly equal that based on an optical signal-to-noise ratio. The energy consumption of optically amplified transportation in the ideal case and limited by Shannon bound is estimated to be 4.4 fJ per bit. [7]

![optical-fiber.jpg](/assets/images/optical-fiber.jpg)

*Fig. 2: Optical fibers along with a 1 euro cent coin. (Source: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Optical-fiber-pbc.jpg))*


# Conclusion

From the simple estimation discussed above, we show that on an electric channel with similar capacitance, data rate and signal voltage, the energy required by one bit is on the level of 10 pJ, four orders of magnitude larger than the energy of one bit via a typical optical fiber. In addition, the short wavelength of optical signal also enables much smaller cable cross section (see Fig. 2). As a result of this energy scale difference, modern submarine cables are using optical fibers for intercontinential communication.

One more thing to notice is that, our computers are built with electronic components. At the end of optical fibers, optoelectronic components and photodetectors are necessary to transduce electrical signal to optical signal. The optical fibers also have finite loss and repeaters or amplifiers are required for long range communication. They contribute to most of the energy consumption for optical fiber communication. As a result, the figure of merit is energy per bit per distance and it's typically orders of magnitude higher than the simple estimation in part II. [7]



# References

[1] J. D. Negroponte, S. J. Palmisano, and A. Segal, Defending an Open, Global, Secure and Resilient Internet (Council on Foreign Relations Press, 2013).

[2] S. Lambert et al., "Worldwide Electricity Consumption of Communication Networks," Opt. Express 20, B513 (2012).

[3] K. Saidi, H. Toumi, and S. Zaidi, "Impact of Information Communication Technology and Economic Growth on the Electricity Consumption: Empirical Evidence from 67 Countries," J Knowl. Econ. 8, 789 (2017).

[4] B. Dudley, "[Comcast to Shuffle Channels in August](https://www.seattletimes.com/business/comcast-to-shuffle-channels-in-august/)," Seattle Times, 2 Jul 09.

[5] D. A. B. Miller, "Attojoule Optoelectronics for Low-Energy Information Processing and Communications," J. Lightwave Technol. 35, 346 (2017).

[6] C. C. Hu, Modern Semiconductor Devices for Integrated Circuits (Pearson, 2009).

[7] R. S. Tucker, "Green Optical Communications - Part I: Energy Limitations in Transport," IEEE J Sel. Top. Quant. 17, 245 (2011).

(First published at [http://large.stanford.edu/courses/2018/ph240/jiang1/](http://large.stanford.edu/courses/2018/ph240/jiang1/))