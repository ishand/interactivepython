# implementation of card game - Memory 

import simplegui
import random

card_value = [0,0]
card_index = [0,0]
# helper function to initialize globals
def new_game():
 
    global state, memory, position, exposed, turns
    state = 0
    #concat memory list
    a = range(8)
    b = range(8)
    memory = a + b
    random.shuffle(memory)
    position = range(18)
    #setting exposed as false
    exposed = range(18)
    for i in position:
        exposed[i] = False
    turns = 0
   
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, turns
    turns = 0
    card_placement = list(pos) 
    place = card_placement[0] / 50

    
    
    if state == 0:
        if exposed[place] is False:
            exposed[place] = True
            card_value[0] = memory[place]
            card_index[0] = place
            print "cardvalue[0] = ", card_value[0]
        state = 1
         
    elif state == 1:
        if exposed[place] is False:
            exposed[place] = True
            card_value[1] = memory[place]
            card_index[1] = place
            print "cardvalue[0] = ", card_value[0], "cardvalue[1] = ", card_value[1]
        state = 2
        
    else:
        if (exposed[card_index[0]] and exposed[card_index[1]]is True): 
           if (card_value[0] is not card_value[1]):
            print "this needs to reset"
            exposed[card_index[0]] = False
            exposed[card_index[1]] = False
        state = 1
        if exposed[place] is False:
            exposed[place] = True
        card_value[0] = memory[place]
        card_index[0] = place
        print "card value 0 = ", card_value[0], "card value 1 = ", card_value[1]
        #if card_value[0] != card_value[1]:
            #exposed[card_index[0]] = False
            #exposed[card_index[1]] = False
            
        #if card_value[0] is card_value[1]:
            #print "----MATCH----"
            #exposed[card_index[0]] == True
            #exposed[card_index[1]] == True
        
        #exposed[place] = True
        #card_value[0] = memory[place]   
    
    print "index position ", place

    
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
        for i in position:
            if exposed[i] == False:
                canvas.draw_polygon([(50*i, 0), (50*i + 50, 0), (50*i + 50, 100), (50*i, 100)], 5, 'Red', 'Green')    
            elif exposed[i]== True:    
                canvas.draw_text(str(memory[i]), ((i * 50)+20 , 50),30, 'Red')  


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

