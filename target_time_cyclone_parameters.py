#target_time parameter file 
paradigm_name = 'target_time_cyclone'
paradigm_version = '1.1'

from psychopy import visual, event, core, gui, logging, data
#from psychopy import parallel
import numpy as np
import math, time, random

exp_datetime = time.strftime("%Y%m%d%H%M%S")
#!!! implement resonses from dialogue box here
paradigm_type = 'debug'                        # Choose either 'debug' 'eeg' or 'ecog' depending on desired 
                                               # duration parameters for trials.  

#============================================================
# EXPERIMENT STRUCTURE PARAMETERS
#============================================================
def experiment_parameters(type):                        #function that selects correct parameter from corresponding dicts 
    if type == 'debug':
        return n_fullvis[type], n_training[type], n_blocks[type], n_trials[type], break_min_dur[type]
    return n_fullvis[type], n_training[type], n_blocks[type], n_trials[type], break_min_dur[type]

# probably need debug y/n and eeg/ecog input from the log file, which will then determine the values below
#   eeg/ecog is needed even for debug mode, because of parallel port for EEG and trigger rectangle for ECoG
n_fullvis     = {'debug':1, 'eeg':5,  'ecog':5}                   # number of EASY examples to start (large tolerance, full window)
n_training    = {'debug':2, 'eeg':15, 'ecog':15}                  # number of training trials PER CONDITION
n_blocks      = {'debug':1, 'eeg':4,  'ecog':2}                   # number of blocks of trials PER CONDITION
n_trials      = {'debug':2, 'eeg':75, 'ecog':75}                  # number of trials PER BLOCK
break_min_dur = {'debug':1, 'eeg':30, 'ecog':30}                  # minimum length (in s) for the break between blocks
n_fullvis, n_training, n_blocks, n_trials, break_min_dur = experiment_parameters(paradigm_type)
#!!! check if n_trials/N-blocks==integer

key = 'space'                       # Response key (eventually will be assigned in dialogue box)


#======================================
#  TOLERANCE AND INTERVAL PARAMETERS  
#======================================
interval_dur = 1                    # duration (in sec) of target time interval
feedback_delay = 2                  # duration (in s) of delay between end of interval and feedback onset
feedback_dur = 2                    # duration (in s) of feedback presentation
ITIs = [0.2, 0.4, 0.7, 1.0]         # length of inter-trial intervals (in s)
post_instr_delay = 1                # duration of delay (in s) after instructions/break to make sure they're ready
block_start_dur = 2                 # duration (in s) to display block start text (e.g., "Level _: type")
tolerances = {'easy':0.125,           # Tolerance (in s) on either side of the target interval 
             'hard':0.05}            # e.g., interval-tolerance < correct_RT < interval+ tolerance
tolerance_step = {'easy': [-0.003,0.012],
                    'hard': [-0.012,0.003]} # adjustment (in s) for [correct,incorrect] responses
tolerance_lim = [0.2, 0.015]

#======================
# STIMULUS PARAMETERS  
#======================
full_screen = True                 # Make the window full screen? (True/False)
#screen_to_show = 1                 # Select which screen to display the window on
screen_units = 'cm'                 # Set visual object sizes in cm (constant across all screens)

n_circ = 30
circ_size = .5
loop_radius = 10
target_width = 1.5  # in cm 

covered_portion = 0.6               # % of interval time obscured when covered=True
#xhr_thickness = 5                  # Thickness of the crosshair on top of the bullseye
resp_marker_width = 2.5   # Width of the response marker (marks where they pressed the button)
resp_marker_thickness = 4           # Thickness of the response marker
trial_types = ['easy', 'hard']      # labels of the trial conditions
trigger_rect_height = 150           # height of the photodiode trigger rectangle IN PIXELS (based on 1920x1080 screen)
trigger_dur = 0.3
point_fn = [100, -100]              # reward function determining points awarded for [correct, incorrect]

