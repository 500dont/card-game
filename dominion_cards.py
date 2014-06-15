#!/usr/bin/python
from dominion import Card, Pile

# Pile sizes
NUM_MONEY_CARDS = 30
NUM_POINT_CARDS = 10
NUM_PILE_CARDS = 10

# Card types
CARD_COIN = "coin"
CARD_POINT = "point"
CARD_POITION = "potion"
CARD_ACTION = "action"

# Error codes
# TODO move this to a method in dominion.py ?
ERROR_NUM_CARDS_TOO_FEW = 100
ERROR_CARD_NOT_IN_SUPPLY = 101

# Basic cards
def CoinCard(name, cost, value):
	return Card(name, cost, CARD_COIN, value, 0)

def PointCard(name, cost, points, end_game = False):
	return Card(name, cost, CARD_POINT, 0, points, None, end_game)

def ActionCard(name, cost, action):
	return Card(name, cost, CARD_ACTION, 0, 0, action)

# Card definitions
# Standard cards
def Copper():
	return CoinCard("copper", 0, 1) # name, cost, value
def Silver():
	return CoinCard("silver", 3, 2) # name, cost, value
def Gold():
	return CoinCard("gold", 6, 3)   # name, cost, value
def Platinum():
	return CoinCard("platinum", 9, 5) # name, cost, value
def Potion():
	return Card("potion", 4, CARD_POITION, 1, 0) # name, cost, kind, value, points
def Estate():
	return PointCard("estate", 2, 1) # name, cost, points
def Province():
	return PointCard("province", 8, 6, True) # name, cost, points, will end game
def Duchie():
	return PointCard("duchie", 5, 3) # name, cost, points
def Colony():
	return PointCard("colony", 11, 10) # name, cost, points
def Curse():
	return PointCard("curse", 0, -1) # name, costs, points

# Base set
def Village():
	return ActionCard("village", 3, VillageAction) # name, cost, action
def Smithy():
	return ActionCard("smithy", 4, SmithyAction) # name, cost, action

# Card actions
def VillageAction(game_state_machine):
	curr_turn = game_state_machine.curr_turn_object
	curr_turn.deck.draw_cards(1)
	curr_turn.actions += 2

def SmithyAction(game_state_machine):
	curr_turn = game_state_machine.curr_turn_object
	curr_turn.deck.draw_cards(3)

# Simple game piles
def CreateStartingCards(numCopper, numEstates):
	cards = []
	for i in range(0, numEstates):
		cards.append(Estate())
	for i in range(0, numCopper):
		cards.append(Copper())
	return cards
def CreateMoneyPiles():
	cards = []
	cards.append(Pile(Copper(), NUM_MONEY_CARDS))
	cards.append(Pile(Silver(), NUM_MONEY_CARDS))
	cards.append(Pile(Gold(), NUM_MONEY_CARDS))
	return cards
def CreatePointPiles():
	cards = []
	cards.append(Pile(Estate(), NUM_POINT_CARDS))
	cards.append(Pile(Duchie(), NUM_POINT_CARDS))
	return cards
def CreateEndingPiles():
	cards = []
	cards.append(Pile(Province(), NUM_POINT_CARDS))
	return cards
def CreateCardPiles():
	cards = []
	cards.append(Pile(Village(), NUM_PILE_CARDS))
	cards.append(Pile(Smithy(), NUM_PILE_CARDS))
	return cards
def CreateTestHand():
	cards = []
	cards.append(Copper())
	cards.append(Silver())
	cards.append(Village())
	cards.append(Gold())
	cards.append(Estate())
	return cards
