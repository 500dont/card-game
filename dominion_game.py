from dominion import *
from dominion_cards import *

# Config
NUM_STARTING_COPPER = 7
NUM_STARTING_ESTATES = 3

# Init things for game
players = [Player("pink"), Player("blue")]
money_cards = CreateMoneyPiles()
point_cards = CreatePointPiles()
cards = CreateCardPiles()
ending_cards = CreateEndingPiles()

all_piles = money_cards + point_cards + cards + ending_cards

# Interaction tests
def buy_test(num):
	for i in range(0, num):
		card_to_buy = buy_valid_card(all_piles)
		print card_to_buy
def play_test(num):
	test_hand = CreateTestHand()
	for i in range(0, num):
		card_to_play, card = play_valid_card(test_hand)
		print str(card_to_play) + ", " + str(card)

# Play stuff
if __name__ == "__main__":
	new_game = GameStateMachine(players, all_piles, CreateStartingCards(NUM_STARTING_COPPER, NUM_STARTING_ESTATES))
	new_game.play_game()