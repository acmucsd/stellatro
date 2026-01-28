# include the main logic of the game
from bots import bot
from src.jokers import *
from src.card import Card, Deck
from src.checker import Checker

HAND_SCORES = {
    "High Card": (10, 1),
    "Pair": (20, 1),
    "Two Pair": (30, 2),
    "Three of a Kind": (40, 2),
    "Straight": (60, 3),
    "Flush": (70, 3),
    "Full House": (90, 4),
    "Four of a Kind": (120, 5),
    "Straight Flush": (160, 6),  # optional, included
}


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.player1_score = 0
        self.player2_score = 0

    def evaluate_hand(self, hand: List[Card], jokers: List[Joker]) -> int:

        # before we find out what hand we have, apply the pre-phase jokers

        # apply each pre-phase joker
        for joker in jokers:
            hand = joker.pre_card_phase(hand)

        # then, check our hand type so we get our base chips and mult
        checker = Checker(hand)
        hand_type = checker.check()
        chips, mult = HAND_SCORES.get(hand_type, (0, 0))

        # apply each card-phase joker

        # for each card...
        for card in hand:
            # if the cared is scored...
            if card.scored:
                # then for each time the card triggers...
                for _ in range(card.num_triggers):
                    # apply each card-phase joker
                    chips += next(iter(card.ranks))  # Add the proper amount of chips
                    for joker in jokers:
                        chips, mult = joker.apply_card_phase(
                            chips, mult, next(iter(card.ranks)), next(iter(card.suits))
                        )

        # apply each post-phase joker
        for joker in jokers:
            chips, mult = joker.post_card_phase(chips, mult, hand)

        return chips * mult

    def play(self):
        print("Game started between Player 1 and Player 2")
        # Placeholder for game logic
        # 1. generate deck for both players
        game_deck = Deck()
        p1_deck = game_deck.draw(10)
        p2_deck = game_deck.draw(10)
        # 2. generate jokers
        jokers = generate_jokers()

        # 3. players read in the game state and take joker one by one
        while jokers:
            joker1 = self.player1.pick_joker({"hand": p1_deck, "jokers": jokers})
            jokers.remove(joker1)
            joker2 = self.player2.pick_joker({"hand": p2_deck, "jokers": jokers})
            jokers.remove(joker2)
        p1_hand, p1_jokers = self.player1.finalize_jokers()
        p2_hand, p2_jokers = self.player2.finalize_jokers()

        # 4. evaluate hands and calculate scores
        self.player1_score = self.evaluate_hand(p1_hand, p1_jokers)
        self.player2_score = self.evaluate_hand(p2_hand, p2_jokers)

        # 5. declare winner
        if self.player1_score > self.player2_score:
            print("Player 1 wins!")
        elif self.player2_score > self.player1_score:
            print("Player 2 wins!")
        else:
            print("It's a tie!")
        # 6. some way to record the game results
        print("Game ended")


def main():
    # Initialize bots
    player1 = bot.Bot()
    player2 = bot.Bot()

    # Start the game
    game = Game(player1, player2)
    game.play()
