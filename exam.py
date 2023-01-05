
# Vertical-horizontal illusion experiment
# Mateusz Psujek 2022


from psychopy import data, visual, event, gui, core
import random, os
import pandas as pd

#dialogue box
Dialoguebox = gui.Dlg(title = "Information")
Dialoguebox.addField("Name:")
Dialoguebox.addField("Gender:", choices=["Female", "Male", "Other"])
Dialoguebox.addField("Age:")
Dialoguebox.show()

#saving the data from the dialogue box
if Dialoguebox.OK:
    ID = Dialoguebox.data[0]
    gender = Dialoguebox.data[1]
    age = Dialoguebox.data[2]
elif Dialoguebox.Cancel:
    core.quit()

# creating a logfile
#making sure there is a data folder
if not os.path.exists("data"):
    os.makedirs("data")
    
# defining the results dataframe (logfile)
results = pd.DataFrame(
    columns = ["ID", "gender", "age", "trail", "stimulus", "x", "y", "trail_time"]
    )
filename = "data/experiment/logfile_{}.csv".format(ID)


# define window
win = visual.Window(
    fullscr = True,
    monitor = 'testMonitor',
    units = "deg", 
    color = (1,1,1),
    allowGUI = True)

# define stopwatch 
stopwatch = core.Clock()


#define text message function
def msg(txt):
    message = visual.TextStim(win, text = "", color = [-1,-1,-1], height = 0.7, anchorHoriz = 'center', anchorVert = 'center')
    message.text = txt
    message.draw()
    win.flip()
    event.waitKeys()


#define fixation cross
def fixation_cross():
    
    vertical = visual.Line(
        win,
        start = (-0.4,0), 
        end = (0.4,0),
        units = 'deg',
        lineColor = "#2e5a39",
        pos = (0,0),
        lineWidth = 5
        )
        
    horizontal = visual.Line(
        win,
        start = (0,-0.4),
        end = (0,0.4), 
        units = 'deg',
        lineColor = "#2e5a39",
        pos = (0,0),
        lineWidth = 5
        )
        
    vertical.draw()
    horizontal.draw()
    win.flip()


#defining the stimulus for the horizontal-vertical inverted T illusion
def horizontal_vertical(y, x):
    
    vertical = visual.Line(
        win,
        start = (0, y),
        end =(0,0),
        units = 'deg',
        lineColor = [-1,-1,-1],
        pos = (0, - y / 2)
        )
        
    horizontal = visual.Line(
        win,
        start = (-x / 2,0),
        end = (x / 2, 0),
        units = 'deg',
        lineColor = [-1,-1,-1],
        pos = (0,- y / 2)
        )
    
    vertical.draw()
    horizontal.draw()
    win.flip()

# defining the trail stmiulus

def training(x, y):
    
    line1 = visual.Line(
        win,
        start = (-y / 2,0), 
        end = (y / 2,0),
        units = 'deg',
        lineColor = [-1,-1,-1],
        pos = (0,0)
        )
    
    line2 = visual.Line(
        win,
        start = (-x / 2 ,0), 
        end = (x / 2,0),
        units = 'deg',
        lineColor = [-1,-1,-1],
        pos = (0,2)
        )
        
    line1.draw()
    line2.draw()
    win.flip()

def control(x, y):
        
    line1 = visual.Line(
        win,
        start = (-y / 2,0), 
        end = (y / 2,0),
        units = 'deg',
        lineColor = [-1,-1,-1],
        pos = (-3,0)
        )
    
    line2 = visual.Line(
        win,
        start = (-x / 2 ,0), 
        end = (x / 2,0),
        units = 'deg',
        lineColor = [-1,-1,-1],
        pos = (3, 1.5)
        )
    
    line1.draw()
    line2.draw()
    win.flip()


def method_of_adjustment(increment, n_trails, fun_stimulus, ys):
    for trail in range(n_trails):
        fixation_cross()
        core.wait(0.7)
        
        y = ys[trail]
        x = y * random.choice([0.75, 1, 1.25])
        fun_stimulus(y = y, x = x)
        
        stopwatch.reset()
        while True:
            global results
            key = event.waitKeys(maxWait = 300, keyList = ['f', 'j', 'd', 'k', 'escape', 'space'], clearEvents = True)[0]
            if key == 'escape':
                results.to_csv(filename)
                core.quit()
                
            elif key == 'j':
                # i think you have to embed another loop in here
                x += increment
            elif key == 'f':
                x += - increment
            elif key == 'k':
                x += increment / 2
            elif key == 'd':
                x += - increment / 2
            elif key == 'space':
                trail_time = stopwatch.getTime()
                results = results.append({
                    "ID": ID, 
                    "gender": gender,
                    "age": age,
                    "trail": trail + 1,
                    "stimulus": stimulus,
                    "x": x,
                    "y": y,
                    "trail_time": trail_time
                    },
                    ignore_index = True
                )
                break
                
            fun_stimulus(y = y, x = x)

# the experiment
#intro
intro = """
    Welcome to the experiment! \n
    In a moment you will see 2 different lines. Your task is to make the length of both of them equal.\n
    You can make one of the lines longer by pressing the 'j' (bigger increament) or the 'k' key (smaller increament). \n
    You can also make the line shorter by presing the f' key (bigger decrease) or the 'd' key (smaller decrease). \n
    Press "space" when the lines are equal to move on to the next trail. \n
    You can use the 'escape' key if you need to quit the experiment.\n
    \n
    <Press any key to begin the training session>
"""

msg(intro)

stimulus = "training"
method_of_adjustment(
    n_trails = 6, 
    increment =  0.2, 
    fun_stimulus = training,
    ys = random.choices([2,4,6], k = 6)
    )
    
msg(txt = "The training session is now finished. Please ask the experimenter if you have any questions about the experiment. \n \n <Press any key to continue to the experiment>")



# control condition
stimulus = "control"
method_of_adjustment(
    n_trails = 15, 
    increment = 0.2, 
    fun_stimulus = control,
    ys = random.sample([4.4] *5 + [5.2]*5 + [6]*5, k = 15)
    )


msg(txt = "Break time. Take your time to rest. \n \n <Press any key to continue to the rest of the experiment>")

# experimental condition
stimulus = "horizontal-vertical"
method_of_adjustment(
    n_trails = 15, 
    increment = 0.2, 
    fun_stimulus = horizontal_vertical,
    ys = random.sample([4.4]*5 + [5.2]*5 + [6]*5, k = 15)
    )

results.to_csv(filename)

msg("The experiment is finished. Thank you for your participation! \n \n <Press any key to exit>")