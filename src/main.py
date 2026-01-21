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
            joker1 = self.player1.pick_joker({
                "hand": p1_deck,
                "jokers": jokers
            })
            jokers.remove(joker1)
            joker2 = self.player2.pick_joker({
                "hand": p2_deck,
                "jokers": jokers
            })
            jokers.remove(joker2)
        p1_hand, p1_jokers = self.player1.finalize_jokers()
        p2_hand, p2_jokers = self.player2.finalize_jokers()

        # 4. evaluate hands and calculate scores
        hand_type = Checker(p1_hand).check()
        chips, mults = HAND_SCORES[hand_type][0] if hand_type in HAND_SCORES else 0
        for p1_joker in p1_jokers:
            chips, mults = p1_joker.apply(chips, mults, hand_type)
        score = chips * mults
        self.player1_score = score
        print(f"Player 1 hand: {p1_hand}, Score: {score}")

        hand_type = Checker(p2_hand).check()
        chips, mults = HAND_SCORES[hand_type][0] if hand_type in HAND_SCORES else 0
        for p2_joker in p2_jokers:
            chips, mults = p2_joker.apply(chips, mults, hand_type)
        score = chips * mults
        self.player2_score = score
        print(f"Player 2 hand: {p2_hand}, Score: {score}")
        
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