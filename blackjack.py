#Import modules
import random
import sys
import signal
import time

#Define variables
card_suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
card_faces = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
player_chips = 100
current_bet = 10
line_length = 70
sleep_time = 1

#Define Functions
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
		handv += card_value(hand[x])
	return handv

def short_card(card):
	card = card.split(" ")
	if card[0] == "Jack" or card == "Queen" or card == "King":
		cardf = card[0][0]
	else:
		cardf = card[0]
	return cardf + "o" + card[2][0]

def short_hand(hand):
	shortHand = []
	for x in len(hand):
		shortHand.append(short_card(hand[x]))
	return shortHand

def contains_ace(hand): #Check if the current hand contains Aces
	for c in range(len(hand)):
		cardf = hand[c].split(" ")[0]
		if cardf == "Ace":
			return True
		else:
			continue
	return False

def new_game():
	global currentDeck
	global current_bet
	global player_chips
	time.sleep(1)
	print "-" * line_length
	if player_chips <= 0:
		gameOver()
	print "Current chips:", player_chips
	print "Options:"
	print "1) Deal new hand"
	try:
		input = None
		input = int(raw_input("> "))
		if input == 1:
			while True:
				try:
					current_bet = int(raw_input("Enter bet (1 - " + str(player_chips) + "): "))
					if current_bet < 1 or current_bet > player_chips:
						print "Invalid amount."
						continue
					break
				except ValueError:
					print "Invalid bet. (Please enter a number)"
					continue
			currentDeck = generateDeck() #Create a new deck of cards
			random.shuffle(currentDeck) #Randomize order of new deck
			deal_hand(currentDeck)
			return game_options()
	except ValueError:
		print "Invalid option. (%s)" % str(input)
		return new_game()
	return

def game_options():
	time.sleep(1)
	print "-" * line_length
	print "Your Hand: {" + list_to_string(currentHand) + "}\nYour Hand Value:", hand_value(currentHand)
	if hand_value(currentHand) == 21:
		return playerBlackJack()
	elif hand_value(currentHand) > 21:
		return playerBust()
	print "Dealer's Hand: {" + list_to_string(dealerHand) + "}\nDealer Hand Value:", hand_value(dealerHand)
	if hand_value(dealerHand) == 21:
		return dealerBlackJack()
	return hit_or_stay()

def dealer_turn():
	time.sleep(1)
	global currentDeck
	global currentHand
	global dealerHand
	print "Dealer's Hand: {" + list_to_string(dealerHand) + "}\nDealer Hand Value:", hand_value(dealerHand)
	if hand_value(dealerHand) > 21:
		return dealerBust()
	elif hand_value(dealerHand) > hand_value(currentHand):
		return dealerWin()
	elif hand_value(dealerHand) == hand_value(currentHand):
		return playerDraw()
	elif hand_value(dealerHand) < 17:
		print "Dealer hits."
		draw_card(currentDeck, dealerHand)
		print "Dealer drew the %s" % str(dealerHand[-1])
		return dealer_turn()
	else:
		return playerWin()

def playerBust():
	global player_chips
	global current_bet	
	player_chips -= current_bet
	print "Your hand BUST! You LOST!"
	time.sleep(sleep_time*2)
	return new_game()

def dealerBust():
	global player_chips
	global current_bet	
	player_chips += current_bet
	print "Dealer hand BUST! You WIN!"
	time.sleep(sleep_time*2)
	return new_game()

def hit_or_stay():
	time.sleep(1)
	global currentDeck
	global currentHand
	global dealerHand
	print "Options:"
	print "1) Hit me"
	print "2) Stay"
	try:
		input = int(raw_input("> "))
		if input == 1:
			draw_card(currentDeck, currentHand)
			print "You drew the %s" % str(currentHand[-1])
			return game_options()
		elif input == 2:
			return dealer_turn()
	except ValueError:
		print "Invalid option."
		return hit_or_stay()
	else:
		print "Invalid option."
		return hit_or_stay()
	return

def playerBlackJack():
	global player_chips
	global current_bet
	player_chips += current_bet * 2
	print "Player got BLACKJACK! You WIN!"
	time.sleep(sleep_time*2)
	return new_game()

def dealerBlackJack():
	global player_chips
	global current_bet
	player_chips -= current_bet
	print "Dealer got BLACKJACK! You LOST!"
	time.sleep(sleep_time*2)
	return new_game()

def dealerWin():
	global player_chips
	global current_bet
	player_chips -= current_bet
	print "Dealer WON! You LOST!"
	time.sleep(sleep_time*2)
	return new_game()

def playerWin():
	global player_chips
	global current_bet
	player_chips += current_bet
	print "Player WON! Dealer LOST!"
	time.sleep(sleep_time*2)
	return new_game()

def playerDraw():
	print "DRAW!"
	time.sleep(sleep_time*2)
	return new_game()

def gameOver():
	print "Game Over! YOU LOSE!"
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

#Start Game
print "Welcome to BlackJack!"
#playerName = raw_input("What is your name?: ") #Collect player name from input
#print "Greetings", playerName, "!"

#Boilerplate
if __name__ == '__main__':
    new_game()