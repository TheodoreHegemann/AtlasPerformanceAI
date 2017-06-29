import os,sys,random,pygame
from pygame.locals import *

import atlas
	
"""
#################################################################
#################################################################
#################################################################

Program Overview

Define players that will be joining
Set AI value, and load file name
Either load in the AI, or create a new load file

Deal each player their hand
Do first round of betting

Do flop
Do second round of betting

Do river 1 and river 2 each with a round of betting

Calculate odds of victory at each state for the AI
Use odds to create a base pattern for how the AI learns
Have the AI learn using these patterns

Play another round. The program will end with an end command. This will make sure the AI gets saved, and can be accessed again in the future

#################################################################
#################################################################
#################################################################
"""

"""
#################################################################
#################################################################
#################################################################
Fibonacci sequence used for layer size. Functions have to be defined before they are used, so it is define at the top of the program so it can be used throughout the code without causing issues. 

Commas can be used when defining variables so that multiple can be initialized in the same line of code. The a,b,c get the respective value of the 1,1,0 below. Although variables can be defined on the same line, the math cannot. 

This function takes the input i, and gets the next highest fibonacci variable based on that input. There are more effecient ways to do this, but as its only used sporatically keeping it simple is higher on the priority.
"""
def fib(i):
	a,b,c = 1,1,0
	while i > c:
		c = a+b
		a = b
		b = c
	return b

"""
#################################################################
#################################################################
#################################################################
The deck variable uses a neat looping method that is not often covered. When a new array is defined in python there is an option to use the looping methods to make the array. In this case I get every value that a card can have, and any suite that the cards can be and combine them. It loops first through the i variable here, as it is the highest priority being second in the line of code. Here it is written out for ease of readability. 

for j in values:
	for i in suites:
		deck.append(j + " " + i)
"""
values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
suites = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
deck = [j + " " + i for j in values for i in suites]
print deck

"""
#################################################################
#################################################################
#################################################################
Shuffle the deck function. Its straight forward in how it works. It is defined so that a new deck can be ordered at will. It has the side effect of making is so that the deck variable is a global var, and will not be used unless the deck is being shuffled. That way each round has a "new" deck to work with that is random. The removal of cards in play from the array will make life much easier overall. There is no ability to count cards in this game. 
"""
def shuffle():
	return random.sample(deck, len(deck))
	
"""
#################################################################
#################################################################
#################################################################
Deal sends out a certain number of cards based on the number of players. It is passed the current game deck, and the number of players to deal to. As the order of the deck is randomized before its passed just the first cards are passed out to each player. The cards chosen are removed from the deck before it is passed back. 
"""
def deal_cards(deck, players):
	pass_back = []
	for p in range(players):
		pass_back.append([])
	for p in range(players*2):
		pass_back[p%(players)].append(deck[0])
		deck.pop(0)
		
	return pass_back, deck
	
"""
#################################################################
#################################################################
#################################################################
Card to number takes a translation of the cards string value and returns an integer than can be passed to the AI. It goes from 2 to A, with the ordering numberwise being 2-14, +13*n for the suits. 
"""
def card_to_number(card):
	value = 0
	if card[0] == "A":
		value = 14
		t = 2
	elif card[0:4] == "King":
		value = 13
		t = 5
	elif card[0:5] == "Queen":
		value = 12
		t = 6
	elif card[0:4] == "Jack":
		value = 11
		t = 5
	elif card[0:2] == "10":
		value = 10
		t = 3
	else:
		value = int(card[0])
		t = 2
	"""
	Now that values are defined modify the results by a suit factor. 
	"""
	if card[t:] == "Spades":
		value += 13*3
	elif card[t:] == "Hearts":
		value += 13*2
	elif card[t:] == "Clubs":
		value += 13
	else:
		value += 0
	
	return value
	
"""
#################################################################
#################################################################
#################################################################
River sends out the top cards from the deck. It then removes the cards from the deck. The deck should be randomized and limited before being passed, so the deck will be passed back to ensure the changes go through. 
"""
def place_river(deck, river, to_draw):
	for c in range(to_draw):
		river.append(deck[0])
		deck.pop(0)
		
	return river, deck
	
"""
#################################################################
#################################################################
#################################################################
Determining hand strenth works off several factors. It goes in standard poker order, listed below. It then goes in order of suit, also listed below. Points scale up by hand incrementally. This is to allow for the different combinations of options that determine hand strength.
	High Card - 0
	Pair - 100
	Two Pair - 200 
	Three of a Kind - 300
	Flush - 400
	Straight - 500
	Full House - 600
	Four of a Kind - 700
	Straight Flush - 800
	
	Spades - 0.2
	Hearts - 0.15
	Clubs - 0.1
	Diamonds - 0.05 
"""

def get_hand_strength(hand, river):
	"""
	Move the hand to a managable list. This is so that the hand value check will use the same list variable. 
	"""
	to_check = []
	for c in hand:
		to_check.append(card_to_number(c))
	for c in river:
		to_check.append(card_to_number(c))
		
	if straight_flush(to_check):
		print('Straight Flush')
	elif four_of_a_kind(to_check):
		print('Four of a Kind')
	elif full_house(to_check):
		print('Full House')
	elif straight(to_check):
		print('Straight')
	elif flush(to_check):
		print('Flush')
	elif three_of_a_kind(to_check):
		print('Three of a Kind')
	elif two_pair(to_check):
		print('Two Pair')
	elif pair(to_check):
		print('Pair')
	else:
		print('High Card')

"""
Card checks. 
"""		
def straight_flush(to_check):
	pass
	
def four_of_a_kind(to_check):
	v = 0
	for card_list in to_check:
		for card in to_check:
			if card_list == card:
				pass
			elif card_list%13 == card:
				v += 1
			elif card%13 == card_list:
				v += 1
				
	if v == 8:
		return True
	else:
		return False
	
def full_house(to_check):
	v1 = 0
	c1 = ''
	for card_list in to_check:
		for card in to_check:
			if card_list == card:
				pass
			elif card_list%13 == card and (c1=='' or card==c1):
				v1 += 1
				c1 = card
			elif card%13 == card_list and (c1=='' or card==c1):
				v1 += 1
				c1 = card
	
	v2 = 0
	c2 = ''
	for card_list in to_check:
		for card in to_check:
			if card_list == card:
				pass
			elif card_list%13 == card and (c2=='' or card==c2):
				v2 += 1
				c2 = card
			elif card%13 == card_list and (c2=='' or card==c2):
				v2 += 1
				c2 = card
				
	if (v1 == 4 and v2 == 6) or (v1 == 6  and v2 == 4):
		return True
	else:
		return False
	
def straight(to_check):
	return False
	
def flush(to_check):
	return False
	
def three_of_a_kind(to_check):
	v = 0
	for card_list in to_check:
		for card in to_check:
			if card_list == card:
				pass
			elif card_list%13 == card:
				v += 1
			elif card%13 == card_list:
				v += 1
	
	if v == 6:
		return True
	else:
		return False
	
def two_pair(to_check):
	v = 0
	for card_list in to_check:
		for card in to_check:
			if card_list == card:
				pass
			elif card_list%13 == card:
				v += 1
			elif card%13 == card_list:
				v += 1
	print v
				
	if v == 4:
		return True
	else:
		return False
	
"""
See if two numbers in an array match
"""
def pair(to_check):
	for card_list in to_check:
		for card in to_check:
			if card_list == card:
				pass
			elif card_list%13 == card:
				return True
			elif card%13 == card_list:
				return True
				
	return False
				
	
"""
#################################################################
#################################################################
#################################################################
The get inputs function returns the inputs that are required for each player. The first two input variables will always be the hand that the player has. The next 5 will be the river, with the default being -1 if there is no card there. 
"""
def get_inputs(cards_in_hand, river, player_stats, player):
	inputs = []
	for card in cards_in_hand[player]:
		inputs.append(card_to_number(card))
	for card in range(len(river)):
		inputs.append(card_to_number(river[card]))
	for card in range(5-len(river)):
		inputs.append(-1)
	for p in range(len(player_stats)):
		if player != p:
			for info in player_stats[p]:
				inputs.append(info)
			
	return inputs

"""
#################################################################
#################################################################
#################################################################
Meta variables
"""
num_players = 4
human_players = 0

num_depth = 2

"""
#################################################################
#################################################################
#################################################################
AI Control Variables - Inputs
2 - hand
5 - river
Per Player
	Betting Values
		Bool Values
			Raised or Bet
			Called
			Fold
		Numerical Values
			How much the player raised this round
			How often this player has raised
			
Intentionally more complex than needed so that changes will effect all parts of the code as needed. This is redundancy at its finest. 
"""
player_values = 5
base_inputs = 7
num_inputs = base_inputs+((num_players-1)*player_values)

"""
#################################################################
#################################################################
#################################################################
AI Control Variables - Outputs
Boolean Values
	Raise or Bet
	Call
	Fold
Numerical Values
	How much to raise
"""
num_outputs = 4

"""
#################################################################
#################################################################
#################################################################
AI Control Variables - Neural Network Size
Hidden Layers - 3
Size per layer will follow fibonaci sequence with the first being the next size up from the inputs. 

Try Except is a catch statement. It means it tries the first section of code and if it fails due to an error it does the second part. I am using it here so that when atlas_network is empty is returns an error and puts the first item in the list. It then uses itself to determine the next layer size in the fibonacci sequence.
"""
num_layers = 3
atlas_network = []
for l in range(num_layers):
	try:
		atlas_network.append(fib(atlas_network[l-1]+1))
	except:
		atlas_network.append(fib(num_inputs))
		
"""
#################################################################
#################################################################
#################################################################
AI Control Variables - Filenames

This section is incomplete. It will be finished up as the rest of the code is tested. The save and load functionalities are implimented, however, untested until that point is reached.

I will be using a variable in the filename so that multiple AIs can be ran from the same program. In this case the ai will be name 'TexasHoldEmAI(N).atlastAI' where (N) is the placement order of the AI. So player 1 is a human, player 2 would get 'TexasHoldEmAI2.atlasAI' as the filename. 
"""
ai_filename_base = 'TexasHoldEmAI'
ai_filename_ext = '.atlasAI'

"""
#################################################################
#################################################################
#################################################################
Game Variables

These directly control the game itself. I put the deck and related variables above this section as a just in case they are needed. The order only matters if a variable is being used. It has to be defined before math can be done to it. 

The running variable is used as a catch method. If I need to have the game crash at any point I can set the running to 0 and the main loop will be broken. It can be set to use a predefined number of loops or games and altered. 

The AI is initialized in this section. 
"""
running = 10

ai_players = [] #Array to store the AI objects
river = [] #Array to store the river cards

player_stats = [] #Stores the game specific variables the AI needs
for np in range(num_players): #Adds an array per person
	player_stats.append([0,0,0,0,0]) #sets values of stats to 0 for defaults

cards_in_hand = [] #Stores the cards in use this particular game
for np in range(num_players): #Adds an array per person
	cards_in_hand.append([]) #Left empty as it fills early in the loops

for ai in range(num_players-human_players): #Generates the neural networks that power the AI
	print 'Generating AI - '+str(ai+1)
	tname = ai_filename_base+str(ai+1)+ai_filename_ext
	ai_players.append(atlas.NeuralNet(num_inputs, atlas_network, num_outputs, num_depth, file=tname))

print 'Initialization of Artificial Intelligence is complete'
"""
#################################################################
#################################################################
#################################################################
Main game loop
"""

while running:
	game_deck = shuffle()
	cards_in_hand, game_deck = deal_cards(game_deck, num_players)
	river = []
	# Add in the ability for a person to play
	"""
	First round of betting based on cards drawn. Player rotation will be computed at the end of the cycle so that the ordering matters very little. As each hand will effectivley only go to the order of the AI in thier array there is no need to do ordering except at the end of the cycle. After betting in each round the river and game deck are updated. 
	"""
	for round in range(4):
		for ai in range(len(ai_players)):
			inputs = [get_inputs(cards_in_hand, river, player_stats, ai)]
			print(cards_in_hand[ai], river)
			print(inputs)
			vars = ai_players[ai].pass_down_forward(inputs)
			#print vars
			print('')
		if round == 0:
			river, game_deck = place_river(game_deck, river, 3)
		else:
			river, game_deck = place_river(game_deck, river, 1)
		for ai in ai_players:
			ai.clear_history()
			
	# Add in people things
	strengths = []
	for hand in cards_in_hand:
		strengths.append(get_hand_strength(hand, river))
	#get_hand_strength()
	#calculate victor
	#have AI learn based on victory conditions
	running -= 1 #Reduce the number of loops to be done

	
temp_var = raw_input('Please type y to save: ')
if temp_var == 'y':
	for ai in ai_players:
		ai.save_manager()