# template for "Stopwatch: The Game"
""" This program creates a stopwatch and a game. If watch is stopped with "0" in the tenths of seconds 
    a point is awarded and the number of attempts are
    recorded"""
import math
import simplegui

# define global variables

t = 0
time = t
score = "0/0"
winning_click = 0
total_ticks = 0
first_click = True
interval = 100

#locations/titles for frame

clock = "Stop Watch"
clockplace = [25, 100]
position = [50, 200]
scoretitle = "Score"
scoreplace = [200, 100]
corner = [225, 200]

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D

def format(t):
    if t == 0:
        timer.stop()
    A = (t // 600) 
    B = (t // 100) % 6
    C = (t // 10) % 10 
    D = (t // 1) % 10 
    global time
    global unformattedtime
    unformattedtime = str(A)+ str(B)+str(C)+str(D)
    time = str(A) + ":"+ str(B)+str(C)+"."+str(D)
    return time
    
# define event handlers for buttons; "Start", "Stop", "Reset"

def Start():
    
    # button that starts stop watch
    timer.start()
    
    
    print "You have started the stopwatch"
    
def Stop():
    global total_ticks, first_click, winning_click, t
    if (first_click == True or False) and timer.is_running():
        total_ticks += 1
    if (t // 1) % 10 == 0 and timer.is_running():
        winning_click == True
        winning_click += 1
    global score
    score = str(winning_click) + "/" + str(total_ticks)
    print score
        
    # button that stops watch
    print "You have stopped the stopwatch"
    timer.stop()
    
def Reset():
    
    global t
    global winning_click
    global total_ticks
    global score
    global time
    
    #stops watch if running
    if timer.is_running()== True:
        timer.stop() 
    
    #resets ints and strings to initial values
    t = 0
    winning_click = 0
    total_ticks = 0
    score = "0/0"
    time = "0:00.0"
    print "stop watch reset"
  
# define event handler for timer with 0.1 sec interval

def increment():
    global t
    t = 1 + t
    str(t)
    print format(t) 
    

# define draw handler

def draw(canvas):
    global t
    global score
    #drawings    
    canvas.draw_text(time, position, 36, "Red")
    canvas.draw_text(score, corner, 36, "Red")
    canvas.draw_text(clock,clockplace, 26, "White")
    canvas.draw_text(scoretitle, scoreplace, 36, "White")

    
# create frame

f = simplegui.create_frame('Stop Watch', 400, 400)

# register event handlers

f.add_button("START", Start, 200)
f.add_button("STOP", Stop, 200)
f.add_button("RESET", Reset, 200)


#register draw handler

f.set_draw_handler(draw)

# timer

timer = simplegui.create_timer(interval, increment)




# start frame and timer

f.start()
timer.start()

format(0)

# Please remember to review the grading rubric