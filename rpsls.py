# Rock-paper-scissors-lizard-Spock template
import random
import math

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def name_to_number(name):
    if name == "rock":
        return 0
    if name == "Spock":
        return 1
    if name == "paper":
        return 2
    if name == "lizard":
        return 3
    if name == "scissors":
        return 4

def number_to_name(number):
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        return "please enter a integer between 0 and 4"


def rpsls(player_choice): 
    
    print
    # print a blank line to separate consecutive games
    
    print "The player chose " + player_choice
    # print out the message for the player's choice
    
    player_number = name_to_number(player_choice)
    # convert the player's choice to player_number using the function name_to_number()
    
    comp_number = random.randrange(0,5)
    # compute random guess for comp_number using random.randrange()
    
    comp_choice = number_to_name(comp_number)
    # convert comp_number to comp_choice using the function number_to_name()
    
    print "The computer chose " + comp_choice
    # print out the message for computer's choice
    
    
    score = (player_number - comp_number)% 5
    # compute difference of comp_number and player_number modulo five
    
    # use if/elif/else to determine winner, print winner message
    if player_number == comp_number:
        print "Player and computer tie!"
    elif score <= 2:
        print "Player Wins!"
    else:
        print "Computer Wins!"
    
    
    return player_number
    
    
    

    
 
    
   

    

   

    
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric