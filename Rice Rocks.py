# Implementation of Spaceship / Rice Rocks

import simplegui
import math
import random

# global values for new game
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False

#groups / sets to append
rock_group = set([])
missiles_group = set([])
explosion_group = set([])


# Game velocity / acceleration / friction parameters
# Ships rotation speed in radians
SHIP_ROTATION_VELOCITY = 0.15
# Fraction of the forward acceleration vector, so the ship does not accelerate too fast
ACCELERATION_LIMIT = 0.175
# This constant affects the braking speed of the ship, caused by friction
COEFFICIENT_OF_FRICTION = 0.01
# Constant to control the velocity of the missile, which is the sum of the ship's velocity
# and a multiple of the ship's forward vector
FORWARD_MISSILE_VEL_MULTIPLIER = 15
MAX_ROCKS = 12
# Constant to declare how many rocks would be at most on the game

class ImageInfo:
    #This class describes the images attributes
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False, tile_dim = 1):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated
        self.tile_dim = tile_dim

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    def get_tile_dim(self):
        return self.tile_dim
    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True, 24)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def group_collide(group, other_object):
    #Identify if any of the objects in the group is colliding with the other_object
    remove_set = set([])

    collision = False
    
    #collision detection
    for element in group:
        if element.collide(other_object) == True:
            collision = True
            remove_set.add(element)

    #removes rocks that collide
    group.difference_update(remove_set)
    return collision
               

def group_group_collide(group1, group2):
    #Identify if any of the objects in each group collide
    global score
    
   
    
    remove_set1 = set([])
    remove_set2 = set([])

    for element1 in group1:
        collision = False
        for element2 in group2:
            if element1.collide(element2) == True:
                #Missile hit a rock
                #Need to remove the missile
                collision = True
                remove_set2.add(element2)
            if(collision):
                #A rock was hit and need to be removed
                a_collision = Sprite(element1.get_pos(), element1.get_vel(), 0, 0, explosion_image, explosion_info) 
                explosion_group.add(a_collision)
                explosion_sound.play()
                score += 10
                remove_set1.add(element1)
                               
    #Here is to actually remove the objects from the groups
    group1.difference_update(remove_set1)
    group2.difference_update(remove_set2)



# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.sound = False
        
    def draw(self,canvas):
        # If the ship is thrusting or not draw different ship image
        if self.thrust != True:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, (self.image_center[0] + 90, self.image_center[1]), self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        # Update the angle of the ship according to the angle velocity
        self.angle += self.angle_vel
        
        # Update the position of the ship on the canvas
        # Use modular arithmetic to enable "wrapping" the canvas
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # Calculate the forward vector of the ship
        forward = angle_to_vector(self.angle)
        
        # Enable friction, by reducing the ship's velocity in each update
        self.vel[0] *= (1 - COEFFICIENT_OF_FRICTION)
        self.vel[1] *= (1 - COEFFICIENT_OF_FRICTION)
        
        # If thrusting, accelerate the ship. Limit the acceleration rate with a constant
        if self.thrust:
            self.vel[0] += forward[0] * ACCELERATION_LIMIT
            self.vel[1] += forward[1] * ACCELERATION_LIMIT
    

    def get_pos(self):
        #returns ship's position
        return self.pos

    def get_vel(self):
        #returns current ship's velocity
        return self.vel

    def get_radius(self):
        #returns the ship's radius
        return self.radius

    def rotate_left(self):
        # Rotate the ship to the left
        self.angle_vel = SHIP_ROTATION_VELOCITY * -1
    
    def rotate_right(self):
        # Rotate the ship to the right
        self.angle_vel = SHIP_ROTATION_VELOCITY
        
    def stop_rotate(self):
        # Stop the rotation of the ship
        self.angle_vel = 0
        
    def thrust_on(self, status):
        # Define the thrust status. True when thrusting, False when not thrusting.
        self.thrust = status
                
        # Play the thrust sound when the thrusters are on
        if self.thrust:
            ship_thrust_sound.set_volume(.5)
            ship_thrust_sound.play()
        # Rewind the thrust sound when not thrusting
        else:
            ship_thrust_sound.rewind()
        
    def shoot(self):
        # This method implements the firing of missiles from the ship's cannon
        global missiles_group
             
        # Calculate the forward vector of the ship
        forward = angle_to_vector(self.angle)
        
        # Cannon is the distance between the ship position and the missile starting position
        CANNON = 37
        missile_x_pos = self.pos[0] + CANNON * forward[0]
        missile_y_pos = self.pos[1] + CANNON * forward[1]

        # Calculate the velocity of the missile.
        # The missile's velocity is the sum of the ship's velocity
        # and a multiple of the ship's forward vector
        missile_x_vel = self.vel[0] + forward[0] * FORWARD_MISSILE_VEL_MULTIPLIER
        missile_y_vel = self.vel[1] + forward[1] * FORWARD_MISSILE_VEL_MULTIPLIER
        
        # Create a new missile object. It replaces the previous object.
        a_missile = Sprite([missile_x_pos, missile_y_pos], [missile_x_vel, missile_y_vel], 0, 0, missile_image, missile_info, missile_sound)
        missiles_group.add(a_missile)
        
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.time = 0
        self.age = 0
        self.tile_dim = info.get_tile_dim()
        if sound:
            sound.rewind()
            sound.play()

    def get_pos(self):
        #returns x, y where it's centered the sprite
        return self.pos

    def get_vel(self):
        #returns current sprite's velocity
        return self.vel

    def get_radius(self):
        #returns sprite's radius
        return self.radius
   
    def draw(self, canvas):
        # Draw the image of the sprite object. 
        if self.animated:
            current_index = (self.time % self.tile_dim) // 1
            current_image_center = [self.image_center[0] +  current_index * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, current_image_center, self.image_size, self.pos, self.image_size, self.angle) 
            self.time += 0.2
        else:
            #if not animated it just draw one image
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def collide(self, other_object):
        #Check if this sprite collides with other object
        
        oo_pos = list(other_object.get_pos())
        oo_radius = other_object.get_radius()
        
        distance = math.sqrt((oo_pos[0] - self.pos[0]) ** 2 + (oo_pos[1] - self.pos[1]) ** 2 )
        radiuses = float(oo_radius + self.radius)
        if distance > radiuses:
            return False
        else:
            return True
        
        
    def update(self):
        # Update the angle of the sprite according to the angle velocity
        self.angle += self.angle_vel
        # Update the position of the sprite on the canvas    
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        #calculates duration of object and whether to remove       
        self.age += 1
        if(self.age >= self.lifespan):
            return True
        else:
            return False
        
        
        

    
def draw(canvas):
    global time, lives
    global rock_group, started
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # Draw ship
    my_ship.draw(canvas)

    if started:
        # Verifies collisions between ship and rocks
        if group_collide(rock_group, my_ship):
            lives -= 1
            # Create a new explosion object.
            a_collision = Sprite(my_ship.get_pos(), my_ship.get_vel(), 0, 0, explosion_image, explosion_info) 
            explosion_group.add(a_collision)
            explosion_sound.play()
            
            #if run out of lives the game stops with all its sounds
            if lives <= 0:
                started = False
                timer.stop()
                soundtrack.pause()
                missile_sound.pause()
                ship_thrust_sound.pause()
                explosion_sound.pause()
                
        # Verifies collisions between rocks and missiles
        group_group_collide(rock_group, missiles_group)
        
        #Draws and updates rocks, missiles and explosions    
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missiles_group, canvas)
        process_sprite_group(explosion_group, canvas)
        
        # Update ship
        my_ship.update()
    
    else:
        #splash screen drawn and music rewound if game not started
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        soundtrack.rewind()

    # Draw the "Lives" and "Score" text and values on the canvas.
    canvas.draw_text("Lives: "  + str(lives), (50, 50), 25, "White", "sans-serif")
    canvas.draw_text("Score: "  + str(score), (650, 50), 25, "White", "sans-serif")



    
def process_sprite_group(group, canvas):
    #it updates and draws every object in the group
    remove_set = set([])
    
    for element in group:
        element.draw(canvas)
        #if the element reach its life span it is removed
        if element.update():
            remove_set.add(element)
    
    group.difference_update(remove_set)
       
    
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group

    # Create new rocks object. 
    # only if they are less than maximum number of rocks
    if len(rock_group) < MAX_ROCKS:
        # Generate random velocity of the new rock
        x_vel = random.random() * .6 - .3
        y_vel = random.random() * .6 - .3
    
        # Generate random position of the new rock
        x_pos = random.randint(0, WIDTH)
        y_pos = random.randint(0, HEIGHT)
    
        # Generate random angular velocity of the rock
        ang_vel = random.random() * .2 - .1
        
        a_rock = Sprite([x_pos, y_pos], [x_vel, y_vel], 0, ang_vel, asteroid_image, asteroid_info) 
        #check if the new rock collides with the ship before it appears
        if not a_rock.collide(my_ship):
            rock_group.add(a_rock)
    

# key handlers for the ship movement
def keydown(key):
    #Only if the game is started
    if started:
        # Evaluate the key_down inputs
        # If "left" is pressed, rotate the ship to the left
        if key==simplegui.KEY_MAP["left"]:
            my_ship.rotate_left()
        # If "right" is pressed, rotate the ship to the right
        elif key==simplegui.KEY_MAP["right"]:
            my_ship.rotate_right()
        # If "up" is pressed, activate the ship's thrusters
        elif key==simplegui.KEY_MAP["up"]:
            my_ship.thrust_on(True)
        # If "space" is pressed, the ship fires a missile
        elif key==simplegui.KEY_MAP["space"]:
            my_ship.shoot() 
       
def keyup(key):
    #Only if the game is started
    if started:
        # Evaluate the key_up inputs
        # If "left" is released, stop the ship's rotation
        if key==simplegui.KEY_MAP["left"]:
            my_ship.stop_rotate()
        # If "right" is released, stop the ship's rotation
        elif key==simplegui.KEY_MAP["right"]:
            my_ship.stop_rotate()
        # If "up" is released, deactivate the ship's thrusters
        elif key==simplegui.KEY_MAP["up"]:
            my_ship.thrust_on(False)

# mouse handler 
def click(pos):
    global started, lives, score
    global my_ship
    
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    #draws splash screen and resets global values if it's a new game
   
    if (not started) and inwidth and inheight:
        #start a new game
        started = True
        soundtrack.play()
        rock_group.difference_update(rock_group)
        missiles_group.difference_update(missiles_group)
        explosion_group.difference_update(explosion_group)
        lives = 3
        my_ship = Ship(center, [0, 0], 0, ship_image, ship_info)
        score = 0
        timer.start()
     
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(1000.0, rock_spawner)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

# get things rolling
#timer.start()
frame.start()