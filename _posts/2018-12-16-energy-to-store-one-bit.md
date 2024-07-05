---
title: "Energy to Store One Bit"
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
  overlay_image: /assets/images/HDD-read-head.PNG
  cover: /assets/images/HDD-read-head.PNG
  show_overlay_excerpt: false
  overlay_filter: 0.5
---


**TL;DR**: ~ 0.4 fJ for SSD and ~ 100 fJ for HDD, limited by physics of the implementation. For actual energy consumption of commercial SSD and HDD, they are both ~ 1 nJ. On the data center level, ~ 0.2 mJ.

# Introduction

With the rapid growth of internet and information technology, more and more people work online, keep their documents online and leave a lot of data while using social network service such as Facebook and Twitter. All these increasing amount of data goes to data centers of these companies. As a result, the power consumption of data centers in the U.S. has increased from 70 billion kWh in 2014 to more than 90 billion kWh in 2017. [1] These two numbers correspond to 1.7% and 2.3% of the total electric power generated in the U.S. in 2014 and 2017, respecitvely. [2] This is a considerable amount of energy. It motivates us to understand the essential energy required to store one bit of information in our current approach, which should help us identify where most of the energy is consumed.

The data storage devices, or computer memory devices, have a long history. With the advance of technology, our ability to make good computer memory has improved from few bytes in the early 1940s to more than few hundreds of Gbits within one single inch squared. [3] For massive data storage, the two categories of data storage devices are solid-state drive (SSD), and hard disk drive (HDD). Their working principles and functioning are quite different.

For research about SSD and HDD development, most efforts were aimed at higher data density, higher transfer rate and lower error rate. There were also discussions about power management but at a rather high level. Here I'll try to carry out order-of-magnitude estimation of the energy required to store one bit of information based on the underlying physics, and compare the estimates to the actual power consumption of the commercial drives and data centers.



![float-gate-transistor.png](/assets/images/float-gate-transistor.png)

*Fig. 1: Schematic drawing of a floating gate transistor, which is the basic of flash memory (Source: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Floating_gate_transistor-en.svg))*


# Working Principle and Associated Energy to Store One Bit in SSD and HDD

The building block of flash-based SSDs is floating-gate transistor. A schematic drawing of a single floating-gate transistor is shown in Fig. 1. It contains a pair of source/drain and a control gate as an ordinary transistor has, but in addition, there is a floating gate inside the control gate and the channel between source and drain. As a result of quantum mechanics, when the control gate is biased by the proper voltage, not only the source and drain is connected, but electrons can also tunnel onto the floating gate through the isolator - keeping the source and drain connected even when the voltage on the control gate is removed. Electrons that have already tunneled onto the floating gate could take years to leak out, making the floating-gate transistor a single unit of a non-volatile memory. [4]



In flash-based SSD, the storage process is essentially charging the floating-gate island. The floating-gate transistor could be modeled as various capacitances, and the physical quantities I'm interested in is charge on the floating-gate $Q = C_\text{CG}\Delta V_\text{th}$ and energy required to charge up the floating-gate $E \sim QV_\text{FG}$. [4] $C_\text{CG}$ is the capacitance between the control gate and the floating-gate, $\Delta V_\text{th}$ is the voltage difference on the control gate between idle and read/write operation, and $V_\text{FG}$ is the voltage of the floating-gate. I use the capacitance of parallel plate to estimate the value of $C_\text{CG} = \epsilon \epsilon_\text{r} A/d$. For 40 nm technical node, A ~ 0.002 μm$^2$, d ~ 10 nm, $\epsilon_\text{r} = 3.9$ for silicon dioxide isolation layer. For typical configuration from Micheloni et al., $\Delta V_\text{th} \sim 5\sim\text{V}$ and $V_\text{FG} \sim 10~\text{V}$. [4] Putting everything together, $C_\text{CG} \sim 7 \times 10^{-3}~\text{fF}$, $Q \sim 3.5 \times 10^{-17}~\text{C}$ and $E \sim 3.5 \times 10^{-16}~$J = 0.35 fJ. As a further check on this estimate, notice that, as mentioned in Micheloni et al., the typical number of electrons on the floating-gate island is around 200. This reasonably matches with the charge $Q \sim 3.5 \times 10^{-17}~$ C. [4]

For a hard drive disk, the fundamental process is magnetisation of the recording material and magnetoresistive sensing of the recorded information. As shown in Fig. 2, the read/write head of a HDD is brought to the vicinity of the disk, the magnetic stray fields from the head set the magnetisation of the local "grain" (magnetic domain) of the recording material.


According to Plumer, for magnetic recording with areal density ~ 10 Gb/in$^2$, one bit contains roughly a 20 by 40 array of 13 × 13 × 20 nm$^3$ grains. [3] Assuming the thickness of the bit is comparable to the other two dimensions (longitudinal recording), the resulting volumn of one bit is on the order of V ~ 0.05 μm$^3$ = 5 × 10$^{-20}$ m$^3$. The saturation magnetisation of the material is on the order of M = 1000 emu/cc = 10$^6$ A/m, and the field in the medium is typically H = 5000 Oe = 0.4 × 10$^6$ A/m. The magnetic energy stored in this bit is estimated by E ~ M·B·V = μ$_0$ M(H+M)V = 8.8 × 10$^{-14}$ J ~ 100 fJ. A quick comparison shows that the energy stored in one bit in HDD is roughly two orders of magnitude higher than in SSD.

Another important comparison is with Kish et al, who used thermal leakage considerations at room temperature to obtained a minimum energy of E ~ 3 × 10$^{-19}$ J = 0.0003 fJ for a ten-year-lifetime storage of one bit. [5] This energy is a few orders of magnitude smaller than the estimate for recent SSD and HDD.


![HDD-big.jpg](/assets/images/HDD-big.jpg)

*Fig. 2: A close look of the read/write head of a HDD. Its mirror image is visible because of the reflection of the disk. (Source: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Hard_disk_head.jpg))*


# Actual Energy Consumption of Commercial SSD/HDD and Data Centers

The above energy estimate should be the lower bound of the full drive. since only processes at a single memory unit are considered, and all the wiring and controls of the device are ignored. To estimate the effective read/write energy of one bit for a commercial drive, I take the division of the average operating power by the average data transfer rate. For a typical SSD, the average read/write speed is on the order of 0.7 GB/s, and the average active power is on the order of 7 W. [1] The resulting energy per bit is ~ 10$^{-8}$ J/Byte ~ 10$^{-9}$ J/bit = 1 nJ/bit. Using the same method for HDD, the average read/write speed is on the order of 200 MB/s and average operating power 10 W. [1] The corresponding energy per bit is ~ 1.3 × 10$^{-8}$ J/Byte ~ 1.5 × 10$^{-9}$ J/bit = 1.5 nJ/bit. The energy consumption on the drive level is comparable between SSD and HDD and is roughly seven and four orders of magnitude higher than the energy stored in one single bit respectively. A possible explanation is that most of the energy is dissipated by rotation of the disk and movement of the read/write arm in HDD, by charging the wiring to every bit in SSD, and the I/O electronics in both case. [6]


On the data center level, the effective average energy consumption per bit is calculated from total electricity use and the total data center storage in the same manner as for the single-drive-level. In 2014, the annual electricity use for all data center in the U.S. is E ~ 70 billion kWh = 2.5 × 10$^{17}$ J. The storage capacity in the same year is ~ 150 million TB = 1.2 × 10$^{21}$ bits. [1] The ratio gives 0.0002 J/bit = 0.2 mJ/bit. However, this estimate uses the total capacity of the data centers, not the actual number of read/write operations. It's reasonable to assume that the read/write operations could be approximated by the capacity to within one or two orders of magnitude. Regardless of this inaccuracy, the amount of energy by one bit on average is much higher than the single-drive value. The actual power consumed by storage is less than 20% of the total power consumption for data centers. Most energy consumption is from infrastructure and servers. (See, for example, Fig. 21 in Shehabi et al). [1]


# Conclusion

In conclusion, I estimate the energy consuption for storing one bit in SSD (~ 0.35 fJ) and HDD (~ 100 fJ) based on the related physical processes and typical device parameters. The estimated energy scale is compared to the average energy consumption in commercial drives and data centers. In commercial SSD and HDD, the energy consumption for one bit is ~ 1 nJ on average. On the data center level, the effective average energy consumption per bit is ~ 0.2 mJ. When moving to higher level, the dominated energy consumption is no longer from the storage itself, but from infrastructure and I/O.


# References

[1] A. Shehabi et al., "United States Data Center Energy Usage Report," Lawrence Berkeley National Laboratory, [LBNL-1005775](http://large.stanford.edu/courses/2018/ph240/jiang2/docs/lbnl-1005775.pdf), June 2016.

[2] "Monthly Energy Review November 2018," U.S Energy Information Administration, [DOE/EIA-0035(2018/11)](http://large.stanford.edu/courses/2018/ph240/jiang2/docs/doe-eia-0035-2018-11.pdf), November 2018."

[3] M. Plumer, Ed., The Physics of Ultra-High-Density Magnetic Recording (Springer, 2001).

[4] R. Micheloni, A. Marelli, K. Eshghi, Inside Solid State Drives (SSDs) (Springer, 2012).

[5] L. Kish and C. Granqvist, "Does Information Have Mass?" Proc. IEEE 101, 1895 (2013).

[6] T Bostoen, S. Mullender, and Y. Berbers, "Power-Reduction Techniques for Data-Center Storage Systems," ACM Comput. Surv. 45, 33 (2013).