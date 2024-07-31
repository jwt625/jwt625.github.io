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


![IMG_8543_meander_wirebond_20220408.JPG](/assets/images/IMG_8543_meander_wirebond_20220408.JPG)

What you are looking at is a microwave coplanar waveguide, sitting on an overpriced (?) PCB from Rogers, with the ground and signal wirebonded, under the stereoscope of a manual [West Bond 7476E wire bonder](https://snsf.stanford.edu/facilities/fab/wirebonder).

![West-Bond-7476E.jpg](/assets/images/West-Bond-7476E.jpg)

I choose wirebonding as the topic of the first blog of hopefully a series about practical nanofabrication, because it was the first tool I got trained to use in the early 2015, and it was the last tool I used before I draw an end of my hands-on nanofab journey at Stanford. It is also at a good scale, the boundary between the macro and micro world, where things are small yet not too small for you to see under optical microscope, and you got to control, touch, and feel things with your own hands (the manual wirebonder pretty much shrinks the motion of your hand, and really feels like an extension of your arm after you get good at it). Let's jump right in after I throw some reference for [basics](https://en.wikipedia.org/wiki/Wire_bonding) and [advanced](https://www.accessengineeringlibrary.com/content/book/9780071476232) (also on [Amazon](https://www.amazon.com/WIRE-BONDING-MICROELECTRONICS-George-Harman/dp/0071476237)). This book is really really good. If you are not satisfied by the emprical practice or suspecting the statements here (as you always should), read and trust this book instead.

# Preparation

When you come and sit in front of the wirebonder, the first, and the most important advice, which is also the first one I got during my training, is to make yourself comfortable. Adjust the chair, loosen your belt, collar or tie, whatever you need. You will need focus and endurance, and making yourself comfortable is as important as making your chip feel secure and comfortable. I would also give this advice in general for nanofab, you should warm up your arms, wrists and fingers before you develop in 25% TMAH or pour some acids. I'm getting derailed, let's focus back on wirebonding.

After you've prepared yourself, it's time to prepare your sample. Actually it is usually done before you come to the wirebonder, preparing, soldering and cleaning the PCB, gluing the chip to the PCB etc. Maybe these will be covered in a future blog (I'm learning from the academics as they cite themselves and say *in preparation*). What is worth mentioning here is that, you should keep the height of the wirebonder wedge/tip in mind when you design your own fixture, or the size and height of the holder and spacer aluminum blocks you have. Does your PCB fits between the clamps? Is it ok to double-sided tape your PCB to the holder/Al block? Will it crack when you try to pry it off the double-sided tape? Will the PCB bend and pop your chip out of it? Run the whole process of getting your sample under the wirebonder tip during the preparation in your head, as well as how you are going to safely remove it afterwards.

It's also worth mentioning that how well your chip and PCB are secured can affect your whole wirebonding experience because it affects **how well the ultrasonic power is applied and absorbed**. Avoid holding and securing your jig or fixture by hand. Your hand is a very good vibration attenuator even without you sensing any of the vibration at the ultrasonic frequency and its short duration. You want the power to be dissipated and absorbed at the wirebonding interface, i.e., between the wire and the metal pad, not by your finger, and not by the wacky glue or epoxy. Clamp your PCB is better than taping it. If you have to, use thinner tape, and tape it firmly. Make sure you have fully cured or baked the adhesive/epoxy you have under or around your chip, and make sure the chip and PCB is horizontal. Most wirebonders do not have the luxury of tilting the tip to match the surface of your chip. Avoid using 3D printed jig as they are too light. If you do, clamp or tape it to a more heavy and firm metal holder or block.

The macro-scale preparation is important, so is the micro-scale, by which I mean the surface condition of the PCB and the chip. How flat is the metal contact of your PCB? What material is the contact, does it have native oxide, if so can you remove it? Get something that is known to bond well like gold plating. Did you left flux or glue residual on the PCB and are they covering the contact? Does your chip still have protection resist? Make sure your contacts are flat and clean for both bonds. If the pads on your PCB are bumpy by eye (e.g. visibly not flat at glancing angle against a light source), you are going to suffer.

I have been assuming you are doing two bonds per wire for making electrical contact, but many tools are also capable of making a single bond, which might be useful for laying down studs if you are doing crazy stuff like flip-chip bonding with those studs.


# Parameters

You turn on the machine, and start flipping through the settings. I do not have it in front of me, but I'm familiar with it enough to see all the settings, and so should you after using it a handful of times, at least for the most important ones. The West Bond machines have recommended values for most parameters, and you would need to be doing crazy shit (like trying to wirebond with NbTi wires) to go more than 0.3x or 3x of the recommendation (and it still did not work).

## Ultrasonic power and duration

The most important ones are **power**, and **duration**, for both bond one and two. When you see the squished wire is too flat, either the power or the duration is too high, and the wire could easily break off from the first bond. When the wire still looks pretty rounded, they are both too small, and the bond might not stick. West bond has a [guide for wedge bond](http://westbondmachining.com/wedge_bond_guide.htm) with SEM images of good and bad bonds. Stanford SNSF also has a great [presentation](https://drive.google.com/file/d/13c3TfuGcX3p-ovXERelZnxbrHZo0tBIx/view) on the effects of power and duration:


![wirebond_SEM_stanford.png](/assets/images/wirebond_SEM_stanford.png)



## Bond force

The next most important parameter is the force, controlled by a spring that can be adjusted by a knob holding it. Most staff member would tell you not to ever touch the force, but I always at least **check the force**. You never know what state the previous user would leave the tool in. Just like when you are using any electronics test equipments like a VNA or oscilloscope, the best practice is to reset all the settings to default and then adjust your own settings. However, many fab equipments especially the old and manual ones do not have such basic functionality, and thus it is even more important to check the settings that you care about. Having a good sense of what and how much each and every steps and parameters matter to your process is in general a type of intuition and experience you should aim to accumulate and practice, and optimize your time, energy, and attention accordingly. Focus more on the ones that matter more, and cut and simplify the ones that do not matter. I'm getting derailed again lol.

This is how the force gauge looks like:

![9101-04A-tester-gauge-with-hook-5-50-grams.jfif](/assets/images/9101-04A-tester-gauge-with-hook-5-50-grams.jfif)

*Force gauge, from [Terra Universal](https://www.terrauniversal.com/portable-wire-bond-strength-tester.html)*

The knob on the top is for turning that little red needle/pointer back, so that it will be pushed by the actual pointer and indicate the max amount of force applied to the gauge. You hold it horizontally with the tip of the lever or arm against the end of the wirebonder arm that is holding the wirebonder tip, and start pushing it up until you hear the beeping sound. I feel like this part needs a good photo, but also as long as you could push the wirebonder arm up reliably and near the location of where the tip is, you would be measuring the force that the tip would apply to the wire. The exact location does not matter unless you care about the force better than ~10%.

## Drop before clamp

You keep going through the parameters, you see loop height and tail length. These are either not effective or not critical. The length of the tail is how much the clamp behind the tip would send the wire out after you finish up the second bond, and it could matter if you have really tight spacing of adjacent wires. The next parameter after these two is worth mentioning: **drop before clamp**. This is controlling when the clamp closes to hold the wire in place when you are moving from the first bond to the second bond: you move the tip from the first bond to the second bond following an arc shaped movement, during which the wire gets pulled more out of the tip by the first bond. When you passed the apex and start lowering the tip, this is the amount of drop after which the clamp closes. I find that I only either use the default value, or set it to zero (do not clamp) when I am free roaming. Clamping the wire is almost necessary for making short wirebonds, since the wire is stiff enough when it is short, and would refuse to bend without held by the clamp. Friction between the wire and the hole in the tip that the wire passes through is not strong enough to deform a short wire. Without bending it properly, you would end up with a very low profile wirebond, and risk of shorting it to circuits on the chip. 

The reason to not enable the clamp for me is mainly when the layout was not properly designed for wirebonding, or the dicing of the chip was off, and the bond pads end up far from the edge of the chip. In both these cases, I need to form a long wirebond (sometimes up to ~ 5 mm which would start having low Q resonances around 5 to 10 GHz). It is hard to estimate how much length I need for such wirebonds, and I would turn off the clamping so that I could freely move around as needed.


# Movement

Now the parameters are all set (usually not the case for the first session with a new sets of PCBs and chips, or when you have not used it for a while, and you'll need a lot of playing and tuning), it is time to start your performance. It is not just your performance, it is your performance with the wirebonder, with the wire, with your PCB, and with your chip.

![wirebond_process_fig1p2_george_harman.png](/assets/images/wirebond_process_fig1p2_george_harman.png)

*Process of wedge bond, from Fig. 1-2 of [Harman](https://www.accessengineeringlibrary.com/content/book/9780071476232)*

What I mean by that, is you should think about how the wirebonder, the wire, the PCB, and your chip would feel about your movement. For example, the force is usually on the order of tens of mg, so there is no need at all to try pushing down on the lever you are holding with your right hand. And the ultrasonic power duration is typically tens of ms, you do not need to dwell for seconds. Even the gravity of the lever or the wirebonder arm would be able to initiate the bond, and you will hear the pneumatic actuation of the clamp, the "tss" (hearing the ultrasound is wishful thinking). This is the music, the chorus with the "beep", the sound track of your performance. 

## Movement of the clamp

You should hear the following "tss" sound of the pneumatic actuation of the clamp:
1. after you touch down and make the first bond, the clamp let go the wire
2. (optional if *drop before clamp* is 0) when you start moving downward towards the second bond, the clamp closes after you have moved down the amount of **drop before clamp**
3. after you touch down on the second bond, it lets go again so that the second bond could pull a bit of the wire out when you start moving up (if the drop before clamp is off, it will close first when you are making the second bond, and then open. These two happens in quick succession and might be hard to distinguish)
4. after you moved up by the length of the tail, the clamp closes, and pulls the wire off the second bond, and leaving a tail of the wire that you could see protruding out of the tip.

You should also hear a "beep" as soon as you touch down on either bond (also in the settings and usually on by default). If any of these sound is missing, that means either the tool is glitched (e.g., did not sense your touch down), or confused (maybe you moved too fast, or maybe you dwelled on a bond for too long), or if you bumped into something (e.g. the arm running into your fixture, or the wirebond tip running onto connectors on your PCB) and triggered the force or accelerometer used to sense the touch down, you'll hear an extra "tss" and a "beep" that is not suppose to sound. If the clamp is supposed to be closed but it is open, feed once and it will close. If it is supposed to be open but it is closed, push the switch that toggle between "feed" and "open" to "open".


## Touch down

Actually before the touch down, you want to check that the wire tail is properly below the tip. It should point downward out of the south side of the tip under the stereoscope, not the other sides. If not, try "open" and "feed", and you'll get a longer tail to push around and bond it off. After you get the wire properly under the tip, lower the tip and the wire vertically to make the first bond. Relax so that you hand is not shaky and moves the tip around horizontally during the touch down. Shake too much and you would break the wire from the smooshed part of the wire (the first bond).


## Debug the first bond

The first bond is the most likely step where you'll break the wire or clog the tip, or tuning the recipe until the wire starts to stick. If the power or time or force is too weak, you'll see the wire does not stick to the pad, and just came off when you lift up the tip, or it might stay for a while and then break off when you are half way towards the second bond. You could move somewhere irrelevant but has exposed metal or bond pad on your PCB to bond off the excess wire, or "open" and "feed" (wirebonder will still be in "bond 2"), and then bond it off. If the excess wire is very short, you can just "feed", and the wirebonder will be in "bond 1" and ready for another try.

If the wire broke immediately after the first bond, you will see just the bonded wire on the pad with no wire attached to it or getting pulled out of the tip when you start moving the tip up from the first bond. There are a few cases that could cause the wire to break:
1. The bond power, time and/or force is off, and the heel of the wire on the first bond cracked or too weak.
2. There is a knot on the wire that formed during threading, and the knot is wider than the hole on the tip.
3. The wire got stuck somewhere upstream, e.g., winded on one of the screw or under a washer near the wire spool
4. The wire got damaged during threading or manipulation, and is too weak to pull and turn the spool

If this is the first time the wire broke, check the later cases, and make sure the wire is clean and in the right place. If it is already the 2nd or 3rd or 20th time, you are likely already in the debug and recipe tuning process (case 1), and the reflect you should have is to just "feed" the wire, and try feeding it a few times if you do not see the wires immediately. Sometimes the wire does not break in a clean way, and the clamp would struggle to feed it, and you will just see the tip of the wire shaking around when "feed". If you could see a little bit of the end of the wire, congratulations, the wire is still threaded through the hole, and try "open" and "feed". This will feed a much longer segment of the wire out of the tip, and set the wirebonder to "bond 2" for you to bond off the excess wire. 

If you are unlucky, you will see under the stereo microscope some wire starts to bend out of being behind the tip when you "open" and "feed". In this case, the best choice is to pull the wire out, cut off the dirty and bent end, and thread it through the tip. If you could see a bit of the wire still sticking out of the tip in the front (south), and you are confident in your tweezer skill, try "open", and then use tweezers to grab and pull the wire more from the front of the tip (it is still threaded through the hole), and then you could "feed" or "close", cut with scissors if the excess is super long (> 1 cm), make sure the wirebond is in "bond 2", and bond off the excess.



## Drawing and forming the wire

Before you start the wirebonding, take a look from the side of the tip, and get a sense of the orientation of the wire, which is held by the hole near the end of the tip. Try moving the tip around along that direction or orientation, and that is the best initial movement for drawing the wire after the first bond. If you move vertically up or horizontally forward after the first bond, you are either bending the joint between the intact wire and the smooshed wire too much, or pulling the wire with too much friction. Pulling along the direction of the hole minimizes the friction between the wire and the tip, and puts less stress at the first bond.


*Forming the arch*: this part is tricky to describe... Maybe I'll think about it in my dream tonight.



# Threading the wire

![wirebond_tip_1.png](/assets/images/2024/wirebond_tip_1.png)
![wirebond_tip_2.png](/assets/images/2024/wirebond_tip_2.png)
*SEM images of the tip and the hole on it in which the wire threads through. From [Stanford SNSF](https://drive.google.com/file/d/13c3TfuGcX3p-ovXERelZnxbrHZo0tBIx/view).*

To be continued...


## Replacing the tip






# How many wirebonds do I need?



# Looking back

