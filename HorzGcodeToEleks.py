# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 00:43:29 2017
HorzGcodeToEleks.py

The Gcode from awesome horizontal Gcode tool varys a bit from Eleks laser stuff
Not sure why, but this changes it to make the output identical as that from Eleks
Save as *.nc if desired. Wouldn't be worth it, but 40+ hrs of effort into this
woodworking project so the engraving must be perfect

I have included 2 sample files for comparison, as well as a brief description in readme
Sorry it's crude, but I at least wanted to upload what I hacked together
as /u/warkilt's code was so very useful to me. 
https://github.com/warkilt/inkscape-laser

@author: IVIUPPET
"""

#### clear;
from IPython import get_ipython
get_ipython().magic('reset -sf')
get_ipython().magic('clear')
#####
# ASCII Lulz:
#http://stackoverflow.com/questions/18057962/regex-pattern-including-all-special-characters

import re
import os

import numpy as np
import matplotlib.pyplot as plt

# Import plotting functions to check data
# user defined libs
#import sys
#sys.path.append('C:\\Users\\YourName\\Dropbox\\Documents\\Programming\\Python\\ClassDev')
#import Plottr

###############################################################################
################################# User_Params #################################
###############################################################################
# Define directory and names for source and output file
pwd = 'C:\\Users\\YourName\\Dropbox\\Documents\\Hobby\\Woodworking\\Projector Stand\\'
#file_names = pwd + 'testlogoTest2.gcode'
file_names = pwd + 'Logo90.nc'

export_name = pwd + 'testlogoTest2.nc'

################################# Import_Data #################################
print('Opening Files...')
with open(file_names, 'r') as f:
    #data_raw = list(f)
    data_raw = f.readlines()
f.closed
print('Read.')

################################ Process_Data #################################
out_lines = []
# Will match for Gcode commands present in Elks laser *.nc style gcode
# Thank you regex101.com
relevant_gcode_pattern = re.compile('G1 +X[a-zA-Z0-9. ]+|M0[3|5] +[A-Za-z0-9]+')
# Look for G1 1 or more spaces, X[anyofthese]+toendofline OR M03 or M05 1 or more space, to rest of line
# Eliminates G4 (pause, not used) and feedrate G1 because starts with F not X 

useful_lines = []

#for line in data_raw:
print('Regexing...')
for match in re.finditer(relevant_gcode_pattern, str(data_raw)):
    tmp = str(data_raw)[match.start():match.end()]
    useful_lines.append(tmp)
print('Lines found.')

# From the useful lines, dive in, modify them and add any extras
dist_list = []
print('Postprocessing...')
out_lines = ['%\n']
for line in useful_lines:
    if line[0] == 'M':
        # Remove the power setting
        out_lines.append(line[0:3] + '\n')
    elif line == 'G1 X0 Y0':
        # Put extra M05 before move home just in case (Eleks does it)
        out_lines.append('M05\n' + line + '\n')
    else:
        # Leave alone, the double space shouldn't harm anything
        out_lines.append(line + '\n')
        # OPTIONAL SECTION: for showing distance between y moves (see bottom)
        
        if line[0] == 'G':
            dist_list.append(line)
# Add this as per output Elks file
out_lines.append('M05\nM30\n%')
print('Done.')

################################# Export_File #################################
print('Writing...')
with open(export_name, 'w') as f:
    f.writelines(out_lines)
f.closed
print('Saved as: ' + export_name)


###############################################################################
########################### OPTIONAL::Plot_Y_Deltas ###########################
###############################################################################
delta_list = []
for i in range(len(dist_list)-1):
    delta_list.append(np.abs(float(dist_list[i].split('Y')[1]) - float(dist_list[i+1].split('Y')[1])))
    
#Plottr.plot(delta_list)
plt.plot(delta_list)
''' This was because I noticed the y step is not consistent
    This was due to the offset created by making a path from some level
    of stroke. Make sure stroke << desired step size or just set to 0.001, or 0
    This allowed for quickly graphing deltas from gcode to isolate the 
    problem. '''
