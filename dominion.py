#!/usr/bin/python
from random import shuffle
from random import randint
from itertools import cycle

# Config
DRAW_SIZE = 5

# Error codes
# TODO: Move these to a function / class?
ERROR_NUM_CARDS_TOO_FEW = 100
ERROR_CARD_NOT_IN_SUPPLY = 101

class Card:
	"""Represents a card."""
	def __init__(self, name, cost, kind, value, points, actions = None, end_game = False):
		self.name = name
		self.cost = cost
		self.kind = kind
		self.value = value
		self.points = points
		self.actions = actions
		self.end_game = end_game

	def __repr__(self):
		return self.name

	def __str__(self):
		return ("name: {0} cost: {1} kind: {2} value: {3} points: {4} actions: {5}".format(
				self.name, self.cost, self.kind, self.value, self.points, self.actions))

	def __eq__(self, other):
		return self.name == other.name

class Pile:
	"""Represents a pile in play that a player can purchase cards from or interact with."""
	def __init__(self, card, num):
		self.card = card
		self.num = num
		self.end_game = card.end_game

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "[{0}, {1}]".format(self.card.name, self.num)

	def get_quantity(self):
		"""Returns the number of cards in this pile."""
		return self.num

	def get_card(self):
		"""Returns the card associated with this pile."""
		return self.card

	def add_cards(self, amount):
		"""Adds a card to this pile."""
		self.num += amount

	def remove_cards(self, amount):
		"""Removes a card from this pile."""
		if self.num > amount:
			self.num -= amount
			return True
		else:
			return ERROR_NUM_CARDS_TOO_FEW

	def is_same(self, card_name):
		is_same = card_name == self.card.name
		return is_same

	def is_empty(self):
		"""Returns true if there are no cards left in the pile."""
 		return self.num == 0

	def can_end_game(self):
		"""Returns true if the game is over when this pile is empty."""
		return self.end_game

class Deck:
	"""Handles the state of a player's deck.

	Members:
	hand    -- cards in a player's hand
	draw    -- "facedown" cards a player may draw from when necessary
	discard -- "faceup" cards that have been played or are out of play
	           if the player needs to draw cards and the draw is empty
	           this pile will become the draw pile
	in_play -- cards that are currently in play, these typically will
	           have been played from a player's hand and get moved into
	           the discard pile once no longer in_play
	"""
	def __init__(self, starting_cards):
		self._init_deck(starting_cards, DRAW_SIZE)

	def __repr__(self):
		return str(self)

	def __str__(self):
		return ("hand: {0} \ndiscard: {1}\ndraw: {2}\nin play: {3}".format(
				str(self.hand), str(self.discard), str(self.draw), str(self.in_play)))

	def _init_deck(self, starting_cards, hand_size):
		"""Shuffles starting cards and puts hand_size into hand and the rest into draw.

		Arguments:
		num_copper  -- the number of copper to start with
		num_estates -- the number of estates to start with
		hand_size   -- the number of cards to go into hand
		"""
		print "init deck..."
		self.hand = []
		self.discard = []
		self.draw = starting_cards
		self.in_play = []
		shuffle(self.draw)
		self.draw_cards(DRAW_SIZE)

	def draw_cards(self, num_cards):
		"""Puts num_cards into hand. Shuffles and moves discard into draw as necessary."""
		in_draw = []
		in_draw = self.draw[0:num_cards]
		del self.draw[0:num_cards]
		needed_cards = num_cards - len(in_draw)
		if needed_cards > 0:
			self.shuffle_cards()
			in_draw += self.draw[0:needed_cards]
			del self.draw[0:needed_cards]
		self.hand += in_draw
		print "hand after draw {0} card: {1}".format(num_cards, str(self.hand))

	def shuffle_cards(self, check_empty = True):
		"""Moves discard into draw and shuffles the draw cards.

		Arguments:
		check_empty -- in general cards shouldn't be shuffled unless the draw is empty
					   this defaults to True and is mainly a saftey check, however, some
					   cards have effects that immediately put the discard into draw so
					   a way to disable this is necessary.
		"""
		if check_empty:
			assert len(self.draw) == 0, "Trying to shuffle cards but draw is not empty."
		self.draw = self.discard
		self.discard = []
		shuffle(self.draw)

	def gain_card(self, card, pile_name):
		"""Adds the given card to the specified pile ("draw", "discard", "hand", "in_play")."""
		if pile_name is "draw":
			# I think in general if things are gained to the draw they go on top, this 
			# is probably fine for now but may need to eventually change.
			self.draw.insert(-0, card)
		elif pile_name is "discard":
			self.discard.insert(-0, card) 
		elif pile_name is "hand":
			self.hand.append(card)
		elif pile_name is "in_play":
			# Not sure if this case is super relevant but I think there might be "play immediately"
			# cards which would require this and probably further logic, this is mainly here so
			# that I don't forget about it.
			self.in_play.append(card)

	def play_card(self, card_index):
		"""Moves the card at card_index from hand and into in_play. Returns the Card for conveinence."""
		assert len(self.hand) > card_index, "Trying to play card not in hand index: %r" % card_index
		played_card = self.hand.pop(card_index)
		self.in_play.append(played_card)
		return played_card

	def end_turn(self):
		"""Cleans up cards at the end of the turn.

		Moves cards in hand and in_play into discard and draws a new hand."""
		# TODO discard should be inserted on top for consistency with gain_card "draw" case.
		# TODO some cards have effects that happen during the clean up phase, this may need
		#      to be less specific.
		self.discard += self.in_play
		self.discard += self.hand
		self.in_play = []
		self.hand = []
		self.draw_cards(DRAW_SIZE)

	def count_card(self, card_to_count):
		"""Returns the count of the given card in a players deck."""
		count = 0
		for card in self.get_deck():
			if card == card_to_count:
				count += 1
		return count

	def get_deck(self):
		"""Returns all cards in a list."""
		return self.hand + self.draw + self.discard + self.in_play

	def get_hand(self):
		"""Returns cards in hand."""
		return self.hand

	def get_draw(self):
		"""Returns cards in draw."""
		return self.draw

	def get_discard(self):
		"""Returns cards in discard."""
		return self.discard

	def get_in_play(self):
		"""Returns cards in_play."""
		return self.in_play


class Player:
	"""Player representation, tracks name and points."""
	def __init__(self, name):
		self.name = name
		self.points = 0

	def __repr__(self):
		return self.name

	def __str__(self):
		return self.name

	def __eq__(self, other):
		return self.name == other.name

	def update_points(self, points):
		"""Adds the given points to the player's score. Can be negative."""
		self.points += points

	def get_points(self):
		"""Returns the player's points."""
		return self.points

	def get_name(self):
		"""Returns the player's name."""
		return self.name

class Supply:
	"""Contols the card piles (supply) in the game."""
	def __init__(self, supply_piles, game_over_at = 3):
		self.supply_piles = supply_piles
		self.empty_piles = 0
		self.game_over_at = game_over_at

	def is_game_over(self):
		return (self.empty_piles == self.game_over_at)

	def remove_from_supply(self, card):
		"""Removes a card from the supply.

		Returns True if the game is over, False if not, and an error code otherwise.
		Any bought or gained cards must go through this function.
		"""
		for pile in self.supply_piles:
			if card == pile.get_card():
				success = pile.remove_cards(1)
				if success is True:
					if pile.is_empty():
						print "   pile is empty: " + pile.card.name
						self.empty_piles += 1
					return self.empty_piles == self.game_over_at
				else:
					return success # This will be ERROR_NUM_CARDS_TOO_FEW
		return ERROR_CARD_NOT_IN_SUPPLY

	def add_to_supply(self, card):
		"""Adds a card to the supply.

		Returns True if able to add, an error code otherwise.
		"""
		for pile in self.supply_piles:
			if card == pile.get_card():
				pile.add_cards(1)
				return True
		return ERROR_CARD_NOT_IN_SUPPLY

class GameStateMachine:
	"""Manages player turns and reactions and updates players' decks and Supply accordingly."""
	def __init__(self, players, supply_piles, starting_cards):
		self.game_state = Supply(supply_piles)
		turn_objects_list = []
		for player in players:
			turn_objects_list.append(TurnObject(player, starting_cards))
		self.turn_objects = cycle(turn_objects_list)
		self.curr_turn_object = next(self.turn_objects)

	def next_turn_object(self):
		self.curr_turn_object = next(self.turn_objects)

	def play_game(self):
		while not self.game_state.is_game_over():
			self.handle_turn()
			self.next_turn_object()

	def handle_turn(self):
		curr_turn = self.curr_turn_object
		print "---------------------------------------"
		print "TURN STARTING FOR: " + str(curr_turn.player)
		# Action / card playing phase
		while True:
			card_to_play, card = play_valid_card(curr_turn.get_deck().get_hand())
			if card_to_play == "done":
				break
			if card_to_play == "all":
				print "   Playing all money cards..."
				curr_turn.play_all_money()
			else:
				card_played = curr_turn.play_card(int(card_to_play))
				self.resolve_card(card_played)

		print "   Turn options: " + str(curr_turn)
		# Buy cards
		while curr_turn.get_buys():
			card_to_buy = buy_valid_card(self.game_state.supply_piles)
			if card_to_buy is "none":
				print "   Not buying anything..."
				break
			else:
				print "   Buying card: " + str(card_to_buy)
				self.game_state.remove_from_supply(card_to_buy)
				curr_turn.buy_card(card_to_buy)
		curr_turn.end_turn()
		print "---------------------------------------"

	def resolve_reactions(self):
		return True

	def resolve_card(self, card):
		if card:
			if card.actions:
				card.actions(self)

	def resolve_buy(self):
		return True

class TurnObject:
	"""Executes a turn"""

	def __init__(self, player, starting_cards):
		self.player = player
		self.deck = Deck(starting_cards)
		self.reset() # Resets actions, buys, and money counts.

	def __repr__(self):
		return str(self)

	def __str__(self):
		return ("actions: {0}, buys: {1}, money: {2}".format(
				self.actions, self.buys, self.money))

	def reset(self):
		self.actions = 1
		self.buys = 1
		self.money = 0

	def get_buys(self):
		return self.buys

	def update_for_card_played(self, play_card):
		if play_card.kind is CARD_COIN:
			self.money += play_card.value
			self.actions = 0
		if play_card.kind is CARD_ACTION:
			if self.actions > 0:
				self.actions -= 1
			else:
				print "   no more actions, can't play card {0}".format(play_card.name)
				return None

	def update_for_card_bought(self, bought_card):
		self.buys -= 1
		self.money -= bought_card.cost

	def play_card(self, card_index):
		card = self.deck.get_hand()[card_index]
		print "   playing card: " + card.name
		if card.kind is CARD_ACTION:
			if self.actions > 0:
				card_played = self.deck.play_card(card_index)
				self.update_for_card_played(card_played)
				return card_played
			else:
				print "   Not enough actions, can't play"
				return None
		elif card.kind is CARD_COIN:
			card_played = self.deck.play_card(card_index)
			self.update_for_card_played(card_played)
			self.actions = 0
		else:
			card_played = self.deck.play_card(card_index)
			self.update_for_card_played(card_played)
			return card_played

	def play_all_money(self):
		"""Plays all of the money cards in the current players hand."""
		hand = self.deck.get_hand()
		index = 0
		for i in range(0, len(hand)):
			card = hand[index]
			if card.kind is CARD_COIN:
				self.play_card(index)
			else:
				index += 1 # Skip non coin cards

	def buy_card(self, bought_card):
		self.deck.gain_card(bought_card, "discard")
		self.update_for_card_bought(bought_card)
		return bought_card

	def get_deck(self):
		return self.deck

	def end_turn(self):
		self.reset()
		self.deck.end_turn()

	def count_points(self):
		points = 0
		for card in self.deck.get_deck():
			points += card.points
		return points

# Input functions
def play_valid_card(cards):
	"""Returns (index, card) of a card in the given hand, or \'all\'' or \'done\'."""
	index = -1
	print "   Hand: " + str(cards) + "\n"
	print "   Type \'done\' when finished playing cards."
	msg = "   Index to play or \'all\' to play money cards: "
	while index < 0 or index > len(cards) or index != "all":
		index = raw_input(msg)
		if index == "all":
			return "all", -1 # Lets take_turn know to play all cards
		if index == "done":
			return "done", -1
		if is_number(index):
			if int(index) < len(cards):
				return int(index), cards[int(index)]
			if int(index) >= len(cards):
				msg = ("   Invalid index, choose from {0}-{1}\nType \'done\' or \'all\' to play money: "
					.format(0, len(cards)-1))


def buy_valid_card(piles):
	"""Returns a card to buy in the given supply piles or \"none\" if the user chooses to buy nothing."""
	card = None
	msg = "   Card to buy or \'none\': "
	print piles
	while not card:
		buy_card = raw_input(msg)
		if buy_card == "none":
			card = "none"
			return card
		for pile in piles:
			if pile.is_same(buy_card):
				if not pile.is_empty():
					return pile.get_card()
				else:
					print piles
					msg = "   That pile is empty, choose a different card or \'none\': "
					break
			msg = "   Card to buy or \'none\': "

# Random utility functions
def is_number(string):
	"""Returns True if the given string is a number, false otherwise."""
	try:
		int(string)
		return True
	except ValueError:
		return False



