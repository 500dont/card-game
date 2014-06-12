from dominion import *
from dominion_cards import *

NUM_STARTING_COPPER = 7
NUM_STARTING_ESTATES = 3

# Pile
# TODO test all piles as per Derek's suggestion
estate_card = Estate()
estate_pile = Pile(estate_card, NUM_POINT_CARDS)
# Get quantitiy
assert (estate_pile.get_quantity() == NUM_POINT_CARDS), "get quantity failed"
# Get card
assert (estate_pile.get_card() == estate_card), "get card failed"
# Is same as card name
assert (estate_pile.is_same(estate_card.name)), "is same failed"
assert (not estate_pile.is_same(Copper().name)), "estate the same as copper?!"
# Is empty
assert not estate_pile.is_empty(), "estate pile is empty?!"
# Can end game
assert not estate_pile.can_end_game(), "estate pile can end game?!"
province_card = Province()
province_pile = Pile(province_card, NUM_POINT_CARDS)
assert province_pile.can_end_game(), "provinces can't end game?!"
# Add cards
estate_pile.add_cards(0)
assert (estate_pile.get_quantity() == NUM_POINT_CARDS), "adding 0 failed"
estate_pile.add_cards(1)
assert (estate_pile.get_quantity() == NUM_POINT_CARDS + 1), "adding 1 failed"
estate_pile.add_cards(6)
assert (estate_pile.get_quantity() == NUM_POINT_CARDS + 7), "adding 6 failed"
# Remove cards
copper_card = Copper()
copper_pile = Pile(copper_card, 0)
assert (copper_pile.remove_cards(1) == ERROR_NUM_CARDS_TOO_FEW), "remove cards from empty pile failed"
estate_pile.remove_cards(7)
assert (estate_pile.get_quantity() == NUM_POINT_CARDS), "remove 7 cards failed"
print "PILE TESTS PASSED"

# Deck tests
test_deck = Deck(CreateStartingCards(NUM_STARTING_COPPER, NUM_STARTING_ESTATES))
compare_deck = [estate_card, estate_card, estate_card,
				copper_card, copper_card, copper_card,
				copper_card, copper_card, copper_card,
				copper_card]
# Initial deck tests
# Size and get_deck
assert (len(test_deck.get_deck()) == NUM_STARTING_COPPER + NUM_STARTING_ESTATES), "deck is not of size 10, instead size: " + str(len(test_deck.get_deck()))
# Count card: number of estates and coppers
assert (test_deck.count_card(estate_card) == NUM_STARTING_ESTATES), "deck doesn't have 3 estates"
assert (test_deck.count_card(copper_card) == NUM_STARTING_COPPER), "deck doesn't have 7 coppers"
# Count card: not in deck
assert (test_deck.count_card(province_card) == 0), "deck doesn't have 0 provinces"
# Make sure that hand was drawn
assert (len(test_deck.get_hand()) == DRAW_SIZE), "hand was not drawn"
# Play cards
test_hand = test_deck.get_hand()
compare_played = []
# Test that the correct card returned when played.
print "play test"
for i in range(0, len(test_hand)):
	compare_card = test_hand[0]
	compare_played.append(compare_card)
	played_card = test_deck.play_card(0)
	print "played: {0} compare: {1}".format(played_card.name, compare_card.name)
	assert (played_card == compare_card), "played card not correct"
# Test that played cards are correctly added to the "in_play" list of cards.
print "in play test"
test_played = test_deck.get_in_play()
for i in range(0, len(test_played)):
	played_card = test_played[i]
	compare_card = compare_played[i]
	print "played: {0} compare: {1}".format(played_card.name, compare_card.name)
	assert (played_card == compare_card)
# Test nothing is in draw at this point.
assert (test_deck.get_discard() == [])
# End turn
compare_discard = test_deck.get_hand() + test_deck.get_in_play()
compare_num = -1 * len(compare_discard)
test_deck.end_turn()
assert (test_deck.get_in_play() == []), "cards in play after turn is over"  #TODO Orange cards
assert (len(test_deck.get_hand()) == DRAW_SIZE), "new hand is not equal to draw size"
in_discard = test_deck.get_discard()[compare_num:]
for i in range(0, len(in_discard)):
	assert (in_discard[i] == compare_discard[i]), "cards in discard are incorrect"
assert (len(in_discard) == len(compare_discard)), "incorrect number of cards in discard"
# Gain card





print "DECK TESTS PASSED"