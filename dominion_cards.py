#!/usr/bin/python
from dominion import Card, Pile

# Pile sizes
NUM_MONEY_CARDS = 30
NUM_POINT_CARDS = 10
NUM_PILE_CARDS = 10

# Card types
CARD_COIN = "coin"
CARD_POINT = "point"
CARD_ACTION = "action"

# Error codes
# TODO move this to a method in dominion.py ?
ERROR_NUM_CARDS_TOO_FEW = 100
ERROR_CARD_NOT_IN_SUPPLY = 101

# Card actions
def VillageAction(game_state_machine):
	curr_turn = game_state_machine.curr_turn_object
	curr_turn.deck.draw_cards(1)
	curr_turn.actions += 2

def SmithyAction(game_state_machine):
	curr_turn = game_state_machine.curr_turn_object
	curr_turn.deck.draw_cards(3)

# Card related functions
#    - Card(name, cost, type, value, points, actions)
#    - Actions(plus_cards, plus_buys, plus_actions, plus_money)
def Copper():
	return Card("copper", 0, CARD_COIN, 1, 0)
def Silver():
	return Card("silver", 3, CARD_COIN, 2, 0)
def Gold():
	return Card("gold", 6, CARD_COIN, 3, 0)
def Estate():
	return Card("estate", 2, CARD_POINT, 0, 1)
def Province():
	return Card("province", 8, CARD_POINT, 0, 6, None, True)
def Duchie():
	return Card("duchie", 5, CARD_POINT, 0, 3)
def Village():
	return Card("village", 3, CARD_ACTION, 0, 0, VillageAction)
def Smithy():
	return Card("smithy", 4, CARD_ACTION, 0, 0, SmithyAction)

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
