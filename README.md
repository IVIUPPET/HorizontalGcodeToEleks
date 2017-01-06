# HorizontalGcodeToEleks
Convert Gcode output from Warkilt's excellent inkscape-laser to identical code output from the software 'Elek's Laser'

## INTRO:
The stupid software that came with my Banggood laser engraver had NO documentation (actually, I found the software through wayback machine to an old Banggood site, it had no download link, guide, or anything else)

In the matrix of folders, there is a Java based universal gcode sender, Benbox, and a tool called 'Eleks Easy G-code Tools.exe' I eventually deciphered some images and by trial and error figured out they use Benbox for firmware/GRBL updates, Eleks for generating the gcode itself, and then you're supposed to use universal gcode sender to send the .nc file to the Banggood engraver.

PROBLEM/Motivation for coding: Eleks laser does not support the entire size of the engraving area, and I got the small 20cm engraver. What?!? Are you f*k*ing kidding me?? What about the bigger lasers? I heard emailing any of these East exporters is a waste of time. Time to frantically google, fail, then break out Python.

You can engrave the outline of an image, or the image itself, known as raster engraving I assume since it's a raster image. None of the programs I found supported raster engraving which seemed silly since 95% of the work (interpreting the image, generating a toolpath from it) was already done, it just needed to traverse the inside back and forth with some step instead of tracing the outline.  

This led me to inkscape, a Python-backed imaging program that these nice Russians appear to have already put a lot of work into a Gcode generation plugin
http://www.cnc-club.ru/forum/viewtopic.php?f=33&t=35&start=20
Too complicated, it's really designed for milling, not a laser. Also didn't seem to do raster

This Jtechphotonics Inkscape Laser Tool Plug-in gave me some hope, but nope, another (more simple) method of doing outlines from vectors. But at least people are developing gcode for inkscape, and it's in.. PYTHON! So much easier than my days in C/C++ or even C#. I love it
https://jtechphotonics.com/?page_id=602

Then I saw a comment from @Cale linking to a program on his Git to do 'horizontal engraving'. An outline of horizontal lines would be stupid so another glimmer of hope.. raster engraving.. could it be?
Yes! Here is his video on how to use:
https://www.youtube.com/watch?v=8bl8vIKZ9y8&feature=youtu.be

And here is his program/plugin:
https://github.com/makejs/inkscape-laser

## WHAT THIS PROGRAM IS FOR:
But this did not run on my Banggood engraver, so I made this to use his method to do raster engraving on my Banggood laser engraver! It converts the output gcode files to files identical to what would have been produced from Eleks laser software if the idiots designing it  had given it a bigger (or adjustable) work area. I post in haste, I apologize, this is not my best work by any means but it's late and I just wanted to give something back that would have saved me so much time in the last few days.

## Comparison of Gcodes: (Set github viewer to 'Raw' for proper layout of this section)
# Some sample Gcode from Eleks laser:
%
G1 X29.750 Y0.000
M03
G1 X29.833 Y0.000
M05
G0 X30.000 Y0.083
M03
G1 X29.750 Y0.083
M05
G0 X29.667 Y0.167
M03
G1 X30.000 Y0.167
M05
G0 X30.167 Y0.250
M03
G1 X29.750 Y0.250
M05
G0 X29.667 Y0.333

...

M03
G1 X7.500 Y107.833
M05
M05
G0 X0.0 Y0.0
M30
%

# Sample Gcode from Horizontal Gcode Tool:
M05 S0

G90
G21
G1 F2000
G1  X13.726 Y0.035
G4 P0 
M03 S256
G4 P0
G1 F2000.000000
G1  X13.875 Y0.035
G4 P0 
M05 S0
G1 F2000
G1  X13.87 Y0.056
G4 P0 
M03 S256
G4 P0
G1 F2000.000000
G1  X13.66 Y0.056

...

G1 F2000.000000
G1  X10.407 Y18.21
G4 P0 
M05 S0
G1 F2000
G1 X0 Y0



M18


# Differences:
Eleks starts with %,
no feedrate specified (must use grbl builtin) before G1's
only one space before coordinates
M03 and M05 (on/off) don't specify a power parameter after
G0 used (move fast) when laser is off instead of all feedrate moves (G1)
G4 (pause) not specified, and not used since value is P0, removed just in case
Ends with two M05 (redundancy for shitty engravers LOL)
terminates with M30 instead of M18, and also a '%'

## WARNING: I Lol'd about the redundant M5, but after using this engraver regularly for 6 months, today, mere hours after writing and I almost left to pick something up from a friend, it had a fault, stopped moving, and sat there burning a hole in my project. May have caused a fire. Buyer beware. Watch these things like a hawk (using your cool green goggles).

This should get you going doing raster engraving on a generic/Chinese/Banggood laser engraver. Good luck.



## BONUS CONTENT: ( read if above steps/links did not get you raster engraving on a Banggood/Chinese laser engraver )
As a bonus, here is my completely uncensored summary for myself in my log folder, most information comes from his video (watch it and try it yourself first or this summary will confuse you), but I learned a few things in the process and have added them. This is the most disorganized section, proceed at your own risk. It may, however, save you time. It would have for me.

Useful info:
http://www.cnc-club.ru/forum/viewtopic.php?f=33&t=35&start=20

SUMMARY:
After installing horzgcodetools,
Drag and drop image into inkscape, trace it
	Path > Trace bitmap
Discard the original, it's not needed
Set stroke = 0 or 0.001 mm (less offset between layers)
#Look to right, set fill = none, stroke flat color, and stroke style << than desired step size, 
#If not there, Shift+Ctrl+F brings up the fill and stroke panel
#but hopefully still easy to see
#This must be equally as small as the cloned box stroke (explained next) since intersect takes largest stroke
(Edit: I actually found it is easier to remove stroke, but leave fill. Only at the very end
just before gcode generation, but after intersection, must the stroke be the only thing left)

Draw a box wider than the object to make gcode for
Set it's height to 0.1-0.3 mm, fill if you want to be visible, stroke << desired y step size
	Edit > Clone > Create Tiled Clone...

# Note: something weird happens with DPI of images in inkscape leading to scaling issues
# i.e., 100 mm in inkscape did not lead to 100 mm in gcode, shown by the universal gcode sender
# and measured with calipers

# Note 2: warkilt recommends 0.1 mm box size, and maybe this is necessary for PCB
# but if you use 0.3 mm, and 0 (or very small) stroke, it will give you the same step
# as Eleks laser gcode generator does. I only did this because I know the results
# are satisfactory, feel free to experiment and learn!

Set Shift Y to 100%, and enough rows to cover the object (columns should be 1)
DELETE the first two boxes on top of each other because they cause problems (at least 1 of them, but the creator says both)
Copy paste and run function again if more coverage needed, since the limit is 500 clones

Sometimes it clones each one the number of copies or something when combining path of both(exponential problem?)
You'll see a black box with multiple large selectable items in it but are bigger than your original box
This appears to be the first set of clones, with path joined (boolean union basically for non inkscapers)
with as many copies on top of each other as there are clones (so 500 joined copies of lines)
Just take one of the copies off then delete the rest, then try combining path of both again,
i.e., if you have two sets of 500 clones, and have deleted the 500 duplicates it produces when joining path (bug in inkscape)
take the two joined clone objects, and then join those
TL;DR If this is confusing, ignore it until  you run into problems intersecting your clones with the object you're engraving

Highlight all items,
	Path > Combine (if not already one object)
Drag over object, highlight both
	Path > Intersection
If you still have fill on, turn it off, and you should be left with outline contour looking things with which the 
horizontal lines will be used
	Extensions > Generate G-code > Horzgcode
Hit apply, default parameters are ok for this application and specifics
will be removed by the Python, but do make sure 'laser horizontal only' or whatever is checked

Take output *.gcode and run through HorzGcodeToEleks.py, which will output *.nc that is identical
to what would have come out of Eleks laser software if the damn build area was big enough 
I'd be pissed AF if I bought a big laser and couldn't use the whole platform, then again it doesn't come with software anymore. SMH
