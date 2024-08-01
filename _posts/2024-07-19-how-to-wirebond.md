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

If you are unlucky, you will see under the stereo microscope some wire starts to bend out of being behind the tip when you "open" and "feed". In this case, the best choice is to pull the wire out, cut off the dirty and bent end, and thread it through the tip (jump to the section on threading). If you could see a bit of the wire still sticking out of the tip in the front (south), and you are confident in your tweezer skill, try "open", and then use tweezers to grab and pull the wire more from the front of the tip (it is still threaded through the hole), and then you could "feed" or "close", cut with scissors if the excess is super long (> 1 cm), make sure the wirebond is in "bond 2", and bond off the excess.


*Which bond should I pick as the first bond?* I personally almost always pick the bond on the PCB for the first bond. You'll have much more metal thickness for you to attempt to destroy during debugging, instead of the mere few hundred nanometer you have on your chip. The PCB is also in general more stable and horizontal than your chip (at least for me since I'm always in a rush gluing the chip and end up doing a bad job). One thing that could change this is height difference between the first and second bond, or objects in the way. More specifically, it is almost impossible to do the first bond near a rising edge. Two reasons: the rising edge would either blocks your view to the bond, or would run into the clamp behind the tip. As a result, always start with the high ground, and then put the second bond after the height drop.


## Drawing and forming the wire

Before you start the wirebonding, take a look from the side of the tip, and get a sense of the orientation of the wire, which is held by the hole near the end of the tip. Try moving the tip around along that direction or orientation, and that is the best initial movement for drawing the wire after the first bond. If you move vertically up or horizontally forward after the first bond, you are either bending the joint between the intact wire and the smooshed wire too much, or pulling the wire with too much friction. Pulling along the direction of the hole minimizes the friction between the wire and the tip, and puts less stress at the first bond.


*Forming the arch*: this part is tricky to describe... Maybe I'll think about it in my dream tonight. Ok I have spent two nights not thinking about it, so let's just go. Actually forming the arch begins even before the first bond. Keep in mind that for wedge bonding on the manual wirebonder, the wire is pulled from north towards south under the tip where it would get pressed and applied the ultrasound. This means that you are suppose to move from south to north, or from near the bottom of your view towards the top. As a result, **route planning** is the first step. If you are a sane person (or working with higher frequencies like microwave) and designed the PCB and the chip properly, your wirebonds should be short and easily within reach of the microscope FoV and the wirebonder arm. Chances are, you are rushing and made some design mistakes, or trying to hack or repurpose a PCB for a different chip, or you have very different thickness between your chip and your PCB: you will end up making some long wirebonds. Make sure you know or have a good sense of where the first and second bond will be, play with the microscope zoom and focus to make sure you could see both locations nice and clear, and move around the tip to make sure it could reach both locations both laterally and in height, esp. when there is a considerable height change. Once you have some practice of wirebonding, you'll realize there is a quite loose tolerance on how vertical the traval of the tip needs to be. As long as the wedge could still hold down onto the wire, you will be able to make the bond, and this will come in handy whenever you have made some other mistakes that prevent the tip from traveling along a straight line (e.g. you put a connector on the PCB too close to the first bond and it blocks the view of the first bond, or if you have made the wrong wirebond order, and the travel is blocked by another wirebond).


*Height difference*: in the previous section we mentioned that you should start high and drop the second bond onto the lower level. Another thing to plan for is prepare for the wire length you need for the height change. As soon as you start dropping the height of the tip around or below the elevation of the first bond, the wire starts to form a sharper and sharper angle at the tip (because the wire comes down from the first bond, goes through the hole, and then bends up as it always is behind the tip). This makes it hard or nearly impossible to continue drawing it out. The friction or stiffness of the wire would be way too strong for the first bond to hold, and you will easily pull the wire off from the first bond when you keep lowering it. The solution: move up and forward until you have enough length of the wire, and then start lowering towards the second bond. If the height drop is so much that you cannot see the second bond at all because the edge of the chip or PCB blocks your view, there are pretty much two options: give it a try and trust your gut and hand. As long as the params are good and you are consistent, you do not need to see the bond to make it. Or, rotate the holder a bit so that it is less blocked, and make the wirebond at an angle wrt. the cliff instead of perpendicular. You could probably rotate the holder so that the edge of the cliff is about +- 15 deg or so away from the up direction, and you could try going along -+ 15 deg off from the vertical path that the tip is supposed to travel, likely still tolerable for the wire to be under the tip (damn this part really needs a drawing). As a result, you get 30 deg between the direction of the wire and the direction of the edge/cliff, and hopefully that gives enough separation for the second bond to be not blocked by the cliff.

![height_difference](/assets/images/2024/wirebond_height_change_20240731.jpg)
*How to deal with big height drop: rotate the chip and travel direction to avoid block of view to the second bond.*

*Coordinate your hand movement*: The coordination is mainly for long wirebond, where you will need to adjust the microscope focus with your left hand while moving the wirebonder arm with your right hand. In more extreme cases (> 10 cm length wirebonds), you'll also need to zoom-out to see where you are moving towards, move around the holder with your left hand for rough positioning, zoom-in again to see the tip and bond pads clear enough, and then make the second bond with your right hand. Another scenario that would need both hands, is when things either blocks your view, or physically blocks the tip, and you will need some creative ways to get around the obstacle such as make the first bond while it is visible or accessible, and then rotate the holder so that the movement of the tip is vertical to keep the pulled wire underneath it. I find around 30 to 45 deg to be the max rotation tolerable, or you will need some strong first bond to hold onto the torque from the rotation.



# Threading the wire

I have been yapping too much... I really need more drawings and less words. Anyway here are some nice SEMs to cleanse your mind from my gibberish before I yap more on how to thread the wire.

![wirebond_tip_1.png](/assets/images/2024/wirebond_tip_1.png)
![wirebond_tip_2.png](/assets/images/2024/wirebond_tip_2.png)
*SEM images of the tip and the hole on it in which the wire threads through. From [Stanford SNSF](https://drive.google.com/file/d/13c3TfuGcX3p-ovXERelZnxbrHZo0tBIx/view).*

During the part about debuging the first bond, we talked about how to feed the wire when it breaks after yoru first bond, and how if you are unlucky, you'll see the wire curling up behind the tip, and you likely have to pull it out and thread it. Relax, take a few deep breath, you will be attempting to thread for a while if this is your first time.

## Preparation

First, you need a good pair of tweezers. The wire we are working with is typically 25 um, that is 10x thinner than your hair. You can easily pinch a kink or even break the wire by just clamping onto it with a crappy pair of tweezers, or more likely you won't be able to hold it tight because of dirts, bumps, or bends on the tweezer tips. You want a pair of clean, straight, and sharp tip tweezers. The best ones I find are the ones with narrow width but thicker along the opening and closing direction of the tweezers, or where the tweezer tip has a relatively fast tapering instead of a thin and slow tapering. This type of design lets you grab a well defined spot on the wire, while still have relatively better stiffness of the tweezer tip. Some sharp tweezers are too skinny and are easily bent. If they are easily bent and they are not yours, you will find the tips bent.vIf you can, have yourself a dedicated sharp tip tweezers for your wirebonding sessions.

Second, prepare the wire. There are a few aspects about preparing the wire. Let's start from the spool. When you cut off old wire and pull more fresh one, do it slowly so that the spool is not turning because of inertia after you stopped pulling. Dealing with a mess of loose wire is the worst nightmare on the wirebonder. Next, check the wire is not stuck or caught anywhere. You could easily pull it off from where it got caught, and would have more stuff to thread through if it broke before some of the guide tubes. Before you grab the wire for threading, make sure the end of the wire is locally straight, no small loops, no kinks, nothing that would get caught at the hole when you have threaded the very end of the wire. Lastly, check the clamp is actually open, and the wire is between the two halves of the clamp when it came out of the tube (needs a picture here). This is not necessary at this point, but better make sure it is the case so that later the wire would be in between the clamp all the way from the tube to the tip.

To illustrate how weak the wire is, let's do some order of magnitude estimations. The wire diameter is 25 um, that is a cross section of ~ 500 um$^2$. The Young's modulus of aluminum is 69 GPa. Assuming the wire would break at 0.5% deformation, and we get as little as **0.17 N** could break the wire. How much is 0.17 N? Let's say your tweezer is 15 g, then its weight is about 0.15 N. Hmm this actually turns out to be really close to how much the wire could hold... Someone should do this experiment. In practice, the wire is 1% silicon to help strengthening it, but you get the point.


## Grab the wire

Now, **how you grab the wire** determines more than 80% how easy the threading will be. There are two aspects about grabbing the wire for threading. 
1. The first aspect is the length of the wire between its end and where you grab it. This piece of wire is going to provide the stiffness to overcome the friction between the wire and the hole, so the shorter it is, the easier or more robust the wire is for you to poke it around the end of the tip to find the hole. On the other hand, this length would be the maximum you have to thread through the hole, and you want enough length so that you could be able to grab the threaded part of it on the other side of the hole to pull more out. I'd say after some practice, you should be able to grab wires as short as 1 mm or less, so I typically leave 5 mm or so when I grab the wire for threading. 
2. The second aspect is how the wire curves. The wire has a natural curvature from the diameter of the spool, which is around 15 mm ish. Grabbing the wire such that the curvature makes it bends left or right does not make sense for threading, so the remaining choice is whether to grab it such that it bends clockwise, or counterclockwise. To be more accurate, you are likely holding the wire, as well as looking at the wire and the tip from the right hand side of the tool I find it more comfortable to hold the wire near horizontal and pointing the tangential direction downward a bit at the location of the tweezer (I really need to make a drawing here). This way I could rest my hand or wrist against the table or the wirebonder platform. I would pick the curvature of the wire to be bending counterclockwise (going from where the tweezer is holding to the end of the wire). The wire would be bending more downward from the curvature, and matching better with the direction of the hole on the tip.

![wire_curve](/assets/images/2024/wirebond_wire_bend_drawing_20240731.jpg)
*Illustration of different curvature of the wire for threading.*


The actual threading is relatively straight forward once you grabbed the wire nicely. Take a look at the SEM image of the tip and the hole on the tip above. It is not that scary. As soon as you get a good sense of where the hole is, you will be able to get it in two or three tries. If you get the wire through the hole in one go, time to brag it to your colleagues. However, if this is the first few times you are threading, be prepared to keep trying for 10 min to one hour, and do some push-up to release your anger along the way (or just let it go and take a walk). I do have a few advice for the threading process:
1. Think about your hand and the tweezers as flexible fixtures. You want to support your hand and the tweezer nicely, and the motion needed for threading to be comfortable for your hand and arm.
2. watch the state of the end of the wire closely, and start with smaller motion: when you see the wire starts to deform a bit, that means the end of the wire is not hitting the hole, and you should slightly adjust the location you are poking and try again. Once you pushed too hard and the wire end is bent, you'll need to cut it off and restart from the grabbing part (adjusting the wire length, bending direction etc). So start small and slow and try more times for your own learning. If you keep hitting and not getting the wire through, while you are getting more confident you are poking around the right spot, **then** start poking with larger motion and more force. Maybe the hole is a bit dirty and the friction is higher. Or try again with a shorter wire length sticking out of the tweezer tip so that it is more stiff.


Once you got a little bit of wire through the tip, do not celebrate too early, finish the whole process and celebrate after you have bonded off the excess wire. Check the wire is not tangled or looped onto anything. Check the wire is not forming a loop because of twist. When you pull more wire through the tip at the front side, the loop could stay there and simply get shrunk and stuck into the hole, or pinch and break the wire. When everything looks good, start pulling the wire using your tweezers, and watch to make sure the wire falls in between the clamps. Pull steady and slow so that the spool will not overshoot when you stop pulling. Close the clamp, try feed, and watch if the wire is actually feeding. The tool should be in "bond 2", if not, "open" and then "feed". Bond off the excess wire, and finally, congratulations! you have done the threading!



## Replacing the tip

This is part of threading the wire because it is bound to happen every 10 threadings or so. You will start suspecting if the tip hole is clogged when you consistently feel you have poked half way into the hole, but the wire is just not coming through. You could feel even when you clean up the bent end of the wire, start again with a shorter and thus stiffer wire, you still feel it slides into the hole, refuse to go through, and the wire bent again and again as you increase the force trying to thread it through. Congratulations, the tip is likely clogged.

One way to check if the tip is clogged if your chip is nicely reflective, is to look at reflection of the tip. You need to play with the tilt of your chip, the height of the tip, as well as the focus and zoom of the scope to put the image of the tip into your view. 

The tip replacement should be in the standard training, so I won't describe the location of the screw, how the tip is stored and how to slide it on and off etc. The thing that is worth noting is the height of the tip. If the tip is mounted too high, the clamp behind it would end up being the lowest point, and make contact with the chip or bond pad before the tip and the wire. If the clamp is too low, the wire would be also too low and out of the clamp. The range or tolerance for the relative height between the clamp and the tip is likely 1 mm or 2. If you are not sure, check sideway to see if it is too low, and try feed and check if the wire is being fed by the clamp properly.


# How many wirebonds do I need?

As many as you could fit onto your bond pad.

Sorry I'm just kidding. I'd do at least two regardless of what frequency you are working with just in case one of them is broken. For RF/microwve chips, I almost always have three for the signal, and as many on the ground and as closely spaced as possible. However, when parasitics matter, like when the wirebond is part of and resonance, then you want just a single wirebond, and make it as short as possible. There are two good reference on intuition and rule of thumb for the effect of wirebonds: [Microwave Package Design for Superconducting Quantum Processors](https://journals.aps.org/prxquantum/abstract/10.1103/PRXQuantum.2.020306) is a relatively recent one, and an older one that I could not find it any more (it is also from the superconducting circuit community and I remember it is on Applied Physics Letter). One of my recent paper also had one section in the [SI](/assets/doc/41567_2023_2129_MOESM1_ESM.pdf) on modeling of cross-chip wirebond. We built the model together and my labmate Sultan wrote up the section and made the beautiful drawings and figure.

![cross_chip_wirebond_model](/assets/images/2024/cross_chip_wirebond_model.png)

In short, at least two if you are not confident on the reliability of the wirebond. The shorter and the fewer the better if you are working at higher frequencies. One wirebond by itself is roughly 1 nH/mm, and you will start getting resonances around 6 GHz when the length is around 6 mm.


# Looking back

This is my first real blog in a while, and somehow I yapped it into a 30 min read... Now I look at it near the end, I feel like the quality is pretty bad. There are many sketches I planned to do but ended up not doing any of them. Fuck it I'm going to add the sketches now. Ok 20 min later, I made two drawings. I'm still trying to figure out how I would like to pursue the style of this series of blogs on nanofab. I would like them to be more unique, to provide value and information you usually only get with hands-on training or shadowing, and also offer some entertainment at the same time. If you have any advice or feedback, please let me know!

At the very end, I should acknowledge all the trainings and help I have received during these years of fun and suffering at both the Tsinghua cleanroom and the Stanford cleanroom. There are many staff that are way more knowledgeable and way more willing to help. It is just they are always busy. And to avoid any potential trouble, part of this work was performed at the Stanford Nano Shared Facilities (SNSF), supported by the National Science Foundation under award ECCS-2026822 (see also [SNSF Acknowledgements](https://snsf.stanford.edu/labmembers/policies/acknowledgements)).

I hope you had some fun reading this, and also learnt some random stuff. See you again (hopefully soon)!


