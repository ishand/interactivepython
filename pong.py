# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]


LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0,  0]
paddle1_vel = [0,0]
paddle2_vel = [0,0]

#score variables for iteration and drawing
score1 = 0
score2 = 0
p1score=0
p2score=0
scoretitle= "SCORE"
scoreplace1=[200,100]
scoreplace2=[400,100]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    #random speed with reset
    global ball_pos, ball_vel # these are vectors stored as lists
    random_vel_tuple = random.randrange(120,240), random.randrange(60,180)
    random_vel = list(random_vel_tuple)
    horspeed = random_vel[0]
    vertspeed = random_vel[1]
    
    ball_pos[0] = WIDTH / 2
    ball_pos[1] = HEIGHT / 2

    if direction == "RIGHT":
        
        ball_vel[0] = horspeed / 60
        ball_vel[1] = -vertspeed / 60
    
    elif direction == "LEFT":
        ball_vel[0] = -horspeed / 60
        ball_vel[1] = -vertspeed / 60
   
# define event handlers
def new_game():
    #default spawn left
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global p1score, p2score  # these are ints
   
    p1score=0
    p2score=0
    spawn_ball("LEFT")

def draw(canvas):
    global p1score,p2score,score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
  
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    #display scores
    canvas.draw_text(str(p1score), scoreplace1, 36, "White")
    canvas.draw_text(str(p2score), scoreplace2, 36, "White")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]        
    # draw ball
  
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen
   
    if paddle1_pos[1] >= 360:
        paddle1_pos[1] = paddle1_pos[1] - 5
    elif paddle2_pos[1] >= 360:
        paddle2_pos[1] = paddle2_pos[1] - 5
    if paddle1_pos[1] <= 40:
        paddle1_pos[1] = paddle1_pos[1] + 5
    elif paddle2_pos[1] <= 40:
        paddle2_pos[1] = paddle2_pos[1] + 5
    else:
        paddle1_pos[1] += paddle1_vel[1]
        paddle2_pos[1] += paddle2_vel[1]
   
    #ball boundaries
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1]>= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        #Left Paddle - collison detection and adds 10% to velocity    
        if (ball_pos[1] > paddle1_pos[1] - HALF_PAD_HEIGHT - BALL_RADIUS) and (ball_pos[1] < paddle1_pos[1] + HALF_PAD_HEIGHT + BALL_RADIUS):
            ball_vel[0] = -ball_vel[0] * 1.1
            
        else:
            spawn_ball("RIGHT")
            p2score = p2score + 1
            score2 = p2score    
    if ball_pos[0] >= WIDTH - (PAD_WIDTH + BALL_RADIUS):
        #Right Paddle - collison + velocity 
        if (ball_pos[1] > paddle2_pos[1] - HALF_PAD_HEIGHT - BALL_RADIUS) and (ball_pos[1] < paddle2_pos[1] + HALF_PAD_HEIGHT + BALL_RADIUS):
            ball_vel[0] = -ball_vel[0] * 1.1
        
        else:
            spawn_ball("LEFT")
            p1score = p1score + 1
            score1 = p1score
    
    # draw paddles
   
    canvas.draw_line((HALF_PAD_WIDTH, paddle1_pos[1]+HALF_PAD_HEIGHT), (HALF_PAD_WIDTH, paddle1_pos[1]- HALF_PAD_HEIGHT), 8, "Blue")
    canvas.draw_line((WIDTH-HALF_PAD_WIDTH, paddle2_pos[1]+HALF_PAD_HEIGHT), (WIDTH-HALF_PAD_WIDTH, paddle2_pos[1]- HALF_PAD_HEIGHT), 8, "Blue")
    
   
 
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    paddles_vel = 4
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] -= paddles_vel
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] += paddles_vel
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -= paddles_vel
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += paddles_vel    
       
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddles_vel = 4
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] += paddles_vel
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] -= paddles_vel
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] += paddles_vel
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] -= paddles_vel

#reset calls new game
def Reset():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("RESET", Reset, 200)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
new_game()
frame.start()