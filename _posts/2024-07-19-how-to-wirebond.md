---
title: "How to wirebond (practical)"
categories:
  - Tutorial
tags:
    - Nanofab
    - Wirebond
    - Packaging
toc: true
toc_sticky: true
use_math: true
header:
  overlay_image: /assets/images/IMG_8543_meander_wirebond_20220408.JPG
  cover: /assets/images/IMG_8543_meander_wirebond_20220408.JPG
  show_overlay_excerpt: false
  overlay_filter: 0.5
---

What you are looking at is a microwave coplanar waveguide, sitting on an overpriced (?) PCB from Rogers, with the ground and signal wirebonded, under the stereoscope of a manual [West Bond 7476E wire bonder](https://snsf.stanford.edu/facilities/fab/wirebonder).

![West-Bond-7476E.jpg](/assets/images/West-Bond-7476E.jpg)

I choose wirebonding as the topic of the first blog of hopefully a series about practical nanofabrication, because it was the first tool I got trained to use in the early 2015, and it was the last tool I used before I draw an end of my hands-on nanofab journey at Stanford. It is also at a good scale, the boundary between the macro and micro world, where things are small yet not too small for you to see under optical microscope, and you got to control, touch, and feel things with your own hands (the manual wireebonder pretty much shrinks the motion of your hand, and really feels like an extension of your arm after you get good at it). Let's jump right in after I throw some reference for [basics](https://en.wikipedia.org/wiki/Wire_bonding) and [advanced](https://www.accessengineeringlibrary.com/content/book/9780071476232) (also on [Amazon](https://www.amazon.com/WIRE-BONDING-MICROELECTRONICS-George-Harman/dp/0071476237)). This book is really really good. If you are not satisfied by the emprical practice or suspecting the statements here (as you always should), read and trust this book instead.

# Preparation

When you come and sit in front of the wirebonder, the first, and the most important advice, which is also the first one I got during my training, is to make yourself comfortable. Adjust the chair, loosen your belt, collar or tie, whatever you need. You will need focus and endurance, and making yourself comfortable is as important as making your chip feel secure and comfortable. I would also give this advice in general for nanofab, you should warm up your arms, wrists and fingers before you develop in 25% TMAH or pour some acids. I'm getting derailed, let's focus back on wirebonding.

After you've prepared yourself, it's time to prepare your sample. Actually it is usually done before you come to the wirebonder, preparing, soldering and cleaning the PCB, gluing the chip to the PCB etc. Maybe these will be covered in a future blog (I'm learning from the academics as they cite themselves and say *in preparation*). What is worth mentioning here is that, you should keep the height of the wirebonder wedge/tip in mind when you design your own fixture, or the size and height of the holder and spacer aluminum blocks you have. Does your PCB fits between the clamps? Is it ok to double-sided tape your PCB to the holder/Al block? Will it crack when you try to pry it off the double-sided tape? Will the PCB bend and pop your chip out of it? Run the whole process of getting your sample under the wirebonder tip during the preparation in your head, as well as how you are going to safely remove it afterwards.

It's also worth mentioning that how well your chip and PCB are secured can affect your whole wirebonding experience because it affects **how well the ultrasonic power is applied and absorbed**. Avoid holding and securing your jig or fixture by hand. Your hand is a very good vibration attenuator even without you sensing any of the vibration at the ultrasonic frequency and its short duration. You want the power to be dissipated and absorbed at the wirebonding interface, i.e., between the wire and the metal pad, not by your finger, and not by the wacky glue or epoxy. Clamp your PCB is better than taping it. If you have to, use thinner tape, and tape it firmly. Make sure you have fully cured or baked the adhesive/epoxy you have under or around your chip, and make sure the chip and PCB is horizontal. Most wirebonders do not have the luxury of tilting the tip to match the surface of your chip. Avoid using 3D printed jig as they are too light. If you do, clamp or tape it to a more heavy and firm metal holder or block.


# Parameters

You turn on the machine, and start flipping through the settings. I do not have it in front of me, but I'm familiar with it enough to see all the settings, and so should you after using it a handful of times, at least for the most important ones. The West Bond machines have recommended values for most parameters, and you would need to be doing crazy shit (like trying to wirebond with NbTi wires) to go more than 0.3x or 3x of the recommendation (and it still did not work).

The most important ones are **power**, and **duration**, for both bond one and two. When you see the squished wire is too flat, either the power or the duration is too high. The next most important parameter is the force, controlled by a spring that can be adjusted by a knob holding it. Most staff member would tell you not to ever touch the force, but I always at least check the force. You never know what state the previous user would leave the tool in. This is how the force gauge looks like:

![9101-04A-tester-gauge-with-hook-5-50-grams.jfif](/assets/images/9101-04A-tester-gauge-with-hook-5-50-grams.jfif)

*Force gauge, from [Terra Universal](https://www.terrauniversal.com/portable-wire-bond-strength-tester.html)*


To be continued...
