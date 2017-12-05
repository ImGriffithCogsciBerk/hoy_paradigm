#target_time_variable file 
paradigm_name = 'target_time_cyclone'
paradigm_version = '1.1'
from psychopy.tools.coordinatetools import pol2cart
from psychopy import visual, event, core, gui, logging, data
#from psychopy import parallel
import numpy as np
import math, time, random
#import target_time_EEG_log
from target_time_cyclone_parameters import*

exp_datetime = time.strftime("%Y%m%d%H%M%S")


#============================================================
# EXPERIMENTAL VARIABLES
#============================================================
win = visual.Window(size=(1280,1024), fullscr=full_screen, color=(0,0,0),
                    monitor='testMonitor',# screen=screen_to_show,
                    allowGUI=False, units=screen_units)#, waitBlanking=False); # !!! check on this waitBlank parameter!
#NOTE: ECoG laptop size = 36cm wide, 20sm tall

exp_clock = core.Clock()
trial_clock = core.Clock()
if paradigm_type == 'ecog':
    block_order = np.array([0, 0, 1, 1])
else:
    block_order = np.random.permutation([b for b in [0, 1] for _ in range(n_blocks)])   #!!! consider counterbalancing future participants
def count_check(some_array):    #function that takes an array as argument and returns an array with the count of 
    result_list = np.array([])  #consecutive numbers that are same. For eg [0,0,0,1,0,1,1] would return [3,1,1,2]
    current = some_array[0]
    count = 0 
    for value in some_array:
        if value == current:
            count += 1
        else:
            result_list = np.append(result_list, count)
            current = value
            count = 1 
    result_list = np.append(result_list,count)
    return result_list

result_list = count_check(block_order)
while len(result_list[result_list >= 3]) != 0:      #checks for 3 or more consecutive same numbers. If present, will recompute permutation till less than 3 present
            block_order = np.random.permutation([b for b in [0, 1] for _ in range(n_blocks)])
            result_list = count_check(block_order)
print 'block_order = ', block_order


#============================================================
# FEEDBACK STIMULI
#============================================================
points = np.zeros(n_blocks*len(trial_types))       # point total for each block
resp_marker = visual.Line(win, start=(-resp_marker_width/2, 0),
                                end=(resp_marker_width/2, 0),
                                lineColor='blue', lineWidth=resp_marker_thickness)
outcome_win = visual.TextStim(win,text='Win!',height=2,units='cm',
                                name='feedback_win', color='green',pos=(0,0))
outcome_loss = visual.TextStim(win,text='Lose!',height=2,units='cm',
                                name='feedback_loss', color='red',pos=(0,0))#wrapWidth=550,
feedback_str = 'B{0}_T{1}: Outcome={2}; RT = {3}; trial_type = {4}; tolerance = {5}'
feedback_txt = visual.TextStim(win,text='',height=1,units='cm',
                                name='feedback_timing', color='black',pos=(0,-3),wrapWidth=14)


#===================================================
# CIRCLE & TARGET ZONE PARAMETERS
#===================================================
angle_ratio = 360/float(interval_dur)

#---------------------------------------------------
# "Light" Stimuli
circ_angles = np.linspace(-90,270,n_circ) #np.array([float(pos_ix)*(360/float(n_circ))-90 for pos_ix in range(n_circ)])
circ_radius = [loop_radius] * n_circ
circ_X, circ_Y = pol2cart(circ_angles,circ_radius)
circ_colors = [(-1,-1,-1)] * n_circ
circles = visual.ElementArrayStim(win, nElements=n_circ,sizes=circ_size,xys = zip(circ_X, circ_Y),
                           elementTex = None, elementMask = "circle",
                           colors=circ_colors)
circ_start = [circ_ix * (interval_dur/float(n_circ)) for circ_ix in range(n_circ)]  # onset time of each light
hidden_pos = {True: [(circ_start[circ_xi] > (1-covered_portion)*interval_dur) for circ_xi in range(n_circ)],
              False: [(False) for circ_xi in range(n_circ)]}

#---------------------------------------------------
# Target Zone
target_upper_bound = {'easy': angle_ratio * (tolerances['easy']*2),  # Get angle of +/- tolerance from interval_dur
                      'hard': angle_ratio * (tolerances['hard']*2)}
target_origin = {'easy': 180 - (tolerances['easy'] * angle_ratio),   # zero starts at 12 oclock for radial stim.  
                 'hard': 180 - (tolerances['hard'] * angle_ratio)}   #!!! Ian comment: Strange indexing, -0 ending sets too far to right
print 'hard bound = ', target_upper_bound['hard'], 'origin' , target_origin['hard']
print 'easy bound = ', target_upper_bound['easy'], 'origin' , target_origin['easy']

target_zone = visual.RadialStim(win, tex='sqrXsqr', color='green', size=(loop_radius*2) + target_width, # size = diameter
    visibleWedge=[0, target_upper_bound['easy']], radialCycles=1, angularCycles=0, interpolate=False,   # radialCycles=1 to avoid color flip
    autoLog=False, units='cm')
target_zone_cover = visual.Circle(win, radius = loop_radius - target_width/2, edges=100,
                lineColor=None, fillColor=[0, 0, 0]) # Covers center of wedge used to draw taret zone
# target_zone.ori = target_origin['easy']  # Right edge starting point of wedge in degrees

#---------------------------------------------------
# Photodiode Trigger Rectangle
trigger_rect = visual.Rect(win, width=trigger_rect_height, height=trigger_rect_height, units='pix',  #pos based on 1920x1080 pixel screen
                            fillColor='white', pos=(trigger_rect_height/2-win.size[0]/2,trigger_rect_height/2-win.size[1]/2))

#===================================================
# INSTRUCTIONS
#===================================================
instr_strs = ['This game starts with a ball moving up the tower towards a bullseye target.\n'+\
               'Your goal is to respond at the exact moment when the ball hits the middle of the target.',
               "The time from the ball's start to the center of the target is always the same, "+\
               'so the perfect response will always be at that exact time: the Target Time!',
               'You win points if you respond when the ball is on the target.\n',#+\
#               'Responding closer to the target time gets you more points!',
               'You lose points if you respond too early or too late and the ball misses the target.',
               "Let's get started with a few examples..."]
train_str = {'easy': "Good job! From now on, the last part of the ball's movement will be hidden.\n"+\
                    "That means you need to respond at the target time without seeing the ball go all the way up.\n"+\
                    "Let's try some more examples...",
             'hard': "Great, now you're ready to try the hard level!\n"+\
                    "Don't get discouraged - hard levels are designed to make you miss most of the time.\n"+\
                    "Challenge yourself to see how many you can win!\nLet's try some examples..."}
main_str = "Ready to try the real deal and start keeping score?\n"+\
            "You'll do {0} easy and {0} hard blocks of {1} trials each.\n".format(n_blocks,n_trials)+\
            'Press Q/escape to do more practice rounds first,\n'+\
            'or press {0} to start playing Target Time!'.format(key)
block_start_str = 'Level {0}/{1}: {2}'
break_str = 'Great work! {0} blocks left. Take a break to stretch and refresh yourself for at least {1} seconds.'
block_point_str = 'Level {0} Score: {1}'
total_point_str = 'Total Score: {0}'

welcome_txt = visual.TextStim(win,text='Welcome to\nTarget Time!',height=4,units='cm',alignHoriz='center',alignVert='center',
                                name='welcome', color='black', bold=True, pos=(0,2),wrapWidth=30)
instr_txt = visual.TextStim(win,text=instr_strs[0],height=2,units='cm', alignVert='center',
                                name='instr', color='black',pos=(0,0),wrapWidth=30)
adv_screen_txt = visual.TextStim(win,text='Press {0} to advance or Q/escape to quit...'.format(key),
                                height=1.5,units='cm',name='adv_screen', color='black', pos=(0,-10),wrapWidth=40)
block_start_txt = visual.TextStim(win,text=block_start_str,height=3,units='cm',alignHoriz='center',alignVert='center',
                                name='block_start', color='black', bold=True, pos=(0,2),wrapWidth=30)
block_point_txt = visual.TextStim(win,text=block_point_str,height=1.5,units='cm', alignVert='center',
                                name='block_points', color='black',pos=(0,8),wrapWidth=20)
total_point_txt = visual.TextStim(win,text=total_point_str,height=1.5,units='cm', alignVert='center',
                                name='total_points', color='black',pos=(0,4),wrapWidth=20)
endgame_txt = visual.TextStim(win,text="Fantastic!!! You're all done. Thank you so much for participating in this experiment!",
                            height=2,units='cm',alignHoriz='center',alignVert='center',
                            name='endgame', color='black', bold=False, pos=(0,-4),wrapWidth=30)