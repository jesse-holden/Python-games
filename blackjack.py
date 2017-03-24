#Import modules
from __future__ import print_function
import random, sys, signal, time, os
#Define variables
card_suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
card_faces = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
player_chips = 100
current_bet = 10
line_length = 70
sleep_time = 0.5

#Define Functions
def print_delay(*args):
	time.sleep(sleep_time)
	if len(args) > 1:
		for arg in args:
			print (arg, " ", end='')
		print ("\n")
	else:
		print (args[0])

def generateDeck(): #Create a new shuffled deck
	deck = []
	for i in range(len(card_suits)):
		for x in range(len(card_faces)):
			deck.append(card_faces[x]+ " of "+ card_suits[i])
	return deck

def generateHand(deck, length): #Produce a new hand of the given length from a deck
	hand = []
	for x in range(length):
		draw_card(deck, hand)
	return hand

def card_value(card): #Determine the individual value of a given card
	cardf = card.split(" ")[0]
	if cardf == "Jack" or cardf == "Queen" or cardf == "King":
		cardv = 10
	elif cardf == "Ace":
		cardv = 11
	else:
		cardv = int(cardf)
	return cardv

def hand_value(hand): #Determine the value of a given hand of cards
	handv = 0
	for x in range(len(hand)):
		if card_is_ace(hand[x]) and handv + card_value(hand[x]) > 21:
			handv += 1
		else:
			handv += card_value(hand[x])
	return handv

def card_is_ace(card): #Check if the current hand contains Aces
	cardf = card.split(" ")[0]
	return cardf == "Ace"

def new_game():
	global currentDeck
	global current_bet
	global player_chips
	print_delay ("-" * line_length)
	if player_chips <= 0:
		return gameOver()
	print_delay ("Current chips:", player_chips)
	print_delay ("Options:")
	print_delay ("1) Deal new hand")
	try:
		input = None
		input = int(get_input("> "))
		if input == 1:
			while True:
				try:
					current_bet = int(get_input("Enter bet (1 - " + str(player_chips) + "): "))
					if current_bet < 1 or current_bet > player_chips:
						print_delay ("Invalid amount.")
						continue
					break
				except ValueError:
					print_delay ("Invalid bet. (Please enter a number)")
					continue
			currentDeck = generateDeck() #Create a new deck of cards
			random.shuffle(currentDeck) #Randomize order of new deck
			deal_hand(currentDeck)
			return game_options()
	except ValueError:
		print_delay ("Invalid option. (%s)" % str(input))
		return new_game()
	return

def game_options():
	print_delay ("-" * line_length)
	print_delay ("Your Hand: {" + list_to_string(currentHand) + "}\nYour Hand Value:", hand_value(currentHand))
	if hand_value(currentHand) == 21:
		return playerBlackJack()
	elif hand_value(currentHand) > 21:
		return playerBust()
	print_delay ("Dealer's Hand: {" + list_to_string(dealerHand) + "}\nDealer Hand Value:", hand_value(dealerHand))
	if hand_value(dealerHand) == 21:
		return dealerBlackJack()
	return hit_or_stay()

def dealer_turn():
	global currentDeck
	global currentHand
	global dealerHand
	print_delay ("Dealer's Hand: {" + list_to_string(dealerHand) + "}\nDealer Hand Value:", hand_value(dealerHand))
	if hand_value(dealerHand) > 21:
		return dealerBust()
	elif hand_value(dealerHand) > hand_value(currentHand):
		return dealerWin()
	elif hand_value(dealerHand) == hand_value(currentHand):
		return playerDraw()
	elif hand_value(dealerHand) < 17:
		print_delay ("Dealer hits.")
		draw_card(currentDeck, dealerHand)
		print_delay ("Dealer drew the %s" % str(dealerHand[-1]))
		return dealer_turn()
	else:
		return playerWin()

def playerBust():
	global player_chips
	global current_bet	
	player_chips -= current_bet
	print_delay ("Your hand BUST! You LOST!")
	return new_game()

def dealerBust():
	global player_chips
	global current_bet	
	player_chips += current_bet
	print_delay ("Dealer hand BUST! You WIN!")
	return new_game()

def hit_or_stay():
	global currentDeck
	global currentHand
	global dealerHand
	print_delay ("Options:\n1) Hit me\n2) Stay")
	try:
		input = int(get_input("> "))
		if input == 1:
			draw_card(currentDeck, currentHand)
			print_delay ("You drew the %s" % str(currentHand[-1]))
			return game_options()
		elif input == 2:
			return dealer_turn()
	except ValueError:
		print_delay ("Invalid option.")
		return hit_or_stay()
	else:
		print_delay ("Invalid option.")
		return hit_or_stay()
	return

def playerBlackJack():
	global player_chips
	global current_bet
	player_chips += current_bet * 2
	print_delay ("Player got BLACKJACK! You WIN!")
	return new_game()

def dealerBlackJack():
	global player_chips
	global current_bet
	player_chips -= current_bet
	print_delay ("Dealer got BLACKJACK! You LOST!")
	return new_game()

def dealerWin():
	global player_chips
	global current_bet
	player_chips -= current_bet
	print_delay ("Dealer WON! You LOST!")
	return new_game()

def playerWin():
	global player_chips
	global current_bet
	player_chips += current_bet
	print_delay ("Player WON! Dealer LOST!")
	return new_game()

def playerDraw():
	print_delay ("DRAW!")
	return new_game()

def gameOver():
	print_delay ("Game Over! YOU LOSE!")
	answer = get_input("Do you want to restart this program? (y/n): ")
	if answer.lower().strip() in "y yes".split():
		restart_program()
	else:
		return

def list_to_string(list):
	rstring = list[0]
	for i in range(1, len(list)):
		rstring = rstring + ", " + list[i]
	return rstring

def deal_hand(currentDeck):
	global currentHand
	global dealerHand
	currentHand = generateHand(currentDeck, 2) #Create a new player hand from the deck
	dealerHand = generateHand(currentDeck, 2) #Create a new dealer hand from the deck

def draw_card(deck, hand):
	randCard = random.choice(deck)
	deck.remove(randCard)
	hand.append(randCard)

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

#Boilerplate
if __name__ == '__main__':
	get_input = input
	if sys.version_info[:2] <= (2, 7):
		get_input = raw_input
	print_delay ("Welcome to BlackJack!")
	playerName = get_input("What is your name?: ") #Collect player name from input
	print_delay ("Greetings " + playerName + "!")
	new_game()