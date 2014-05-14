#!/usr/bin/python
from random import shuffle
from random import randint
from itertools import cycle

# Configurations
NUM_STARTING_COPPER = 7
NUM_STARTING_ESTATES = 3

NUM_MONEY_CARDS = 30
NUM_POINT_CARDS = 10
NUM_PILE_CARDS = 10

DRAW_SIZE = 5

# Card types
CARD_COIN = "coin"
CARD_POINT = "point"
CARD_ACTION = "action"

class Card:
	' Simple card representation '
	' This will be updated with functionality for actions etc.'

	def __init__(self, name, cost, kind, value, points):
		self.name = name
		self.cost = cost
		self.kind = kind
		self.value = value
		self.points = points

	def __repr__(self):
		return self.name

	def __str__(self):
		return ("name: {0} cost: {1} kind: {2} value: {3} points: {4}".format(
				self.name, self.cost, self.kind, self.value, self.points))

class Pile:
	' Represents a pile in play '

	def __init__(self, card, num):
		self.card = card
		self.num = num

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "[{0}, {1}]".format(self.card.name, self.num)

	def buy_card(self, card_name, money):
		if card_name == self.card.name:
			if money >= self.card.cost and self.num > 0:
				self.remove_cards(1)
				return self.card
		return None

	def add_cards(self, amount):
		self.num += amount

	def remove_cards(self, amount):
		self.num -= amount

	def is_empty(self):
		return self.num == 0

class Cards:
	' Handles operations on a players cards for hand, discard, and draw'

	def __init__(self):
		self.hand = []
		self.discard = []
		self.draw = []
		self.create_starting_deck(NUM_STARTING_COPPER, NUM_STARTING_ESTATES)
		self.draw_hand(DRAW_SIZE)

	def __repr__(self):
		return str(self)

	def __str__(self):
		return ("hand: {0} \ndiscard: {1}\ndraw: {2}".format(
				str(self.hand), str(self.discard), str(self.draw)))

	def create_starting_deck(self, num_copper, num_estates):
		' Creates a standard shuffled starting deck '
		for i in range(0, num_copper):
			self.draw.append(Copper())
		for i in range(0, num_estates):
			self.draw.append(Estate())
		shuffle(self.draw)

	def draw_hand(self, draw_size = DRAW_SIZE):
		self.hand = self.draw[0:draw_size]
		del self.draw[0:draw_size]
		needed_cards = draw_size - len(self.hand)
		if needed_cards > 0:
			self.shuffle_cards()
			self.hand = self.hand + self.draw[0:needed_cards]
			del self.draw[0:needed_cards]
		if len(self.hand) > DRAW_SIZE:
			# TODO: possible throw an error here (mainly for debugging)
			print "WARNING: Cards.draw_hand returning hand of size greater than " + str(DRAW_SIZE)

	def shuffle_cards(self):
		self.draw = self.discard
		self.discard = []
		shuffle(self.draw)

	def buy_card(self, card):
		self.discard.append(card)

	def play_card(self, card_index):
		played_card = self.hand.pop(card_index)
		self.discard.append(played_card)
		return played_card

	def get_deck(self):
		return self.hand + self.draw + self.discard

	def get_hand(self):
		return self.hand

	def get_draw(self):
		return self.draw

	def get_discard(self):
		return self.discard

class Player:
	' Player representation '

	def __init__(self, name):
		self.name = name
		self.cards = Cards()
		self.turn_options = TurnOptions()

	def __repr__(self):
		return self.name

	def __str__(self):
		return self.name

	def get_turn_options(self):
		return self.turn_options

	def get_cards(self):
		return self.cards

	def get_deck(self):
		return self.cards.get_deck()

	def play_card(self, card_index):
		played_card = self.cards.play_card(card_index)
		self.turn_options.update_for_card_played(played_card)
		return played_card

	def buy_card(self, bought_card):
		self.cards.buy_card(bought_card)
		self.turn_options.update_for_card_bought(bought_card)
		return bought_card

	def end_turn(self):
		self.turn_options.reset()
		self.cards.draw_hand()

	def count_points(self):
		points = 0
		for card in self.cards.get_deck():
			points += card.points
		return points

class TurnOptions:
	' Tracks the options available to a player per turn '

	def __init__(self):
		self.reset()

	def __repr__(self):
		return str(self)

	def __str__(self):
		return ("actions: {0}, buys: {1}, money: {2}".format(
				self.actions, self.buys, self.money))

	def reset(self):
		self.actions = 1
		self.buys = 1
		self.money = 0

	def update_for_card_played(self, played_card):
		if played_card.kind is CARD_COIN:
			self.money += played_card.value
			self.actions = 0

	def update_for_card_bought(self, bought_card):
		self.buys -= 1
		self.money -= bought_card.cost

	def get_actions(self):
		return self.actions

	def get_buys(self):
		return self.buys

	def get_money(self):
		return self.money

class GameState:

	def __init__(self, players, money_cards, point_cards, cards, ending_cards):
		# Not sure if separate piles for money / point / ending / cards are
		# entirely necessary, note that ending_cards represents cards that
		# cause the game to end if their piles run out.
		self.player_state = PlayerState(players)
		self.money_cards = money_cards
		self.point_cards = point_cards
		self.cards = cards
		self.ending_cards = ending_cards 

	def __repr__(self):
		return "GameState, currentPlayer {0}".format(self.player_state.get_curr_player())

	def __str__(self):
		return ("GAMESTATE\nplayers: {0}\nending: {1}\npoint: {2}\nmoney: {3}\ncards: {4}"
					.format(str(self.player_state.get_curr_player()),
						str(self.ending_cards), str(self.point_cards), str(self.money_cards),
						str(self.cards)))

	def get_piles(self):
		return self.money_cards + self.point_cards + self.cards + self.ending_cards

	def game_over(self):
		empty_piles = 0
		for pile in self.ending_cards:
			if pile.num is 0:
				return True
		for pile in self.get_piles():
			if pile.num is 0:
				empty_piles += 1
				if empty_piles is 3:
					return True
		return False

	def determine_winner(self):
		point_list = self.player_state.count_points()
		for player, points in point_list:
			print "{0} has {1} points".format(player.name, points)
			print "    {0} deck:\n    {1}".format(player.name, str(player.get_deck()))

	def start_game(self):
		print "STARTING GAME - player {0} starts".format(self.player_state.get_curr_player())
		while not self.game_over():
			self.take_turn()
			# todo that thing that makes sense here
			self.player_state.get_curr_player().end_turn()
			self.player_state.get_next_player()
		print "GAME OVER"
		print "----------------------------------------------"
		self.determine_winner()

	def take_turn(self):
		player = self.player_state.get_curr_player()
		player_options = player.get_turn_options()
		player_cards = player.get_cards()

		print "----------------------------------------------"
		print "TAKING TURN - player {0}".format(player)
		print "   OPTIONS - {0}".format(player_options)
		print "   HAND - {0}".format(player_cards.get_hand())
		print "   DRAW - {0}".format(player_cards.get_draw())
		print "   DISC - {0}".format(player_cards.get_discard())

		# Play cards
		player_hand = player_cards.get_hand()
		while player_hand:
			play = play_valid_card(player.get_turn_options(), player_hand)
			if play == "all":
				print "   Playing all cards..." + str(player_hand)
				for i in range(0, len(player_hand)):
					player.play_card(0)
				break
			else:
				card_played = player.play_card(int(play))
				print "   Playing card {0}".format(card_played.name)
		# Buy cards
		while player.get_turn_options().get_buys():
			print player.get_turn_options()
			buy_card = buy_valid_card(player.get_turn_options(), self.get_piles())
			player.buy_card(buy_card)
			print "   Bought card {0}".format(buy_card)

		print "STATE AFTER TAKE TURN:"
		print "   money piles : " + str(self.money_cards)
		print "   point piles : " + str(self.point_cards)
		print "   card piles  : " + str(self.cards)
		print "   ending piles: " + str(self.ending_cards)
		print "----------------------------------------------"


class PlayerState:
	# TODO: move player related stuff in GameState into PlayerState?
	def __init__(self, players):
		self.player_list = players
		self.player = cycle(self.player_list)
		self.curr_player = next(self.player)

	def get_next_player(self):
		self.curr_player = next(self.player)
		return self.curr_player

	def get_curr_player(self):
		return self.curr_player

	def count_points(self):
		scores = []
		for player in self.player_list:
			points = player.count_points()
			scores.append([player, points])
		return scores

# Input functions
# TODO: Remove these and put logic in player and game state. 
#      (buy_valid_card)
#      would like to change this so that first game state checks if specified card
#      exists in game and then player attempts to purchase. If either fail they
#      should return string error message that is used to request more input
#      if succeeds return the card
#
#      (play_valid_card)
#      player attempts to play card, if card is invalid to play return string error
#      message
def play_valid_card(turn_options, cards):
	' Gets a valid index of a card to play '
	# TODO use turn_options to verify they have actions etc.
	index = -1
	while index < 0 or index > len(cards) or index != "all":
		index = raw_input('Index to play or \'all\': ')
		if index == "all":
			return "all" # Lets take_turn know to play all cards
		if int(index) < len(cards):
			return int(index)

def buy_valid_card(turn_options, piles):
	' Gets a valid card to buy '
	card = None
	while not card:
		buy_card = raw_input('Card to buy or \'none\': ')
		if buy_card == "none":
			card = "none"
			return card
		for pile in piles:
			bought_card = pile.buy_card(buy_card, turn_options.get_money())
			if bought_card:
				return bought_card

# Card related functions
def Copper():
	return Card("copper", 0, CARD_COIN, 1, 0)
def Silver():
	return Card("silver", 3, CARD_COIN, 2, 0)
def Gold():
	return Card("gold", 6, CARD_COIN, 3, 0)
def Estate():
	return Card("estate", 2, CARD_POINT, 0, 1)
def Province():
	return Card("province", 8, CARD_POINT, 0, 6)
def Duchie():
	return Card("duchie", 5, CARD_POINT, 0, 3)

# Simple game piles
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
	return cards

# Init things for game
players = [Player("pink"), Player("blue")]
money_cards = CreateMoneyPiles()
point_cards = CreatePointPiles()
cards = CreateCardPiles()
ending_cards = CreateEndingPiles()

# Start game
gs = GameState(players, money_cards, point_cards, cards, ending_cards)
gs.start_game()
