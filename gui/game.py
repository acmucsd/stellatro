# include the main logic of the game
from enum import Enum
from jokers import *
from card import Card
from deck import Deck
from checker import Checker, HandType

JOKER_POOL_SIZE = 15
JOKER_HAND_SIZE = 2
PLAYER_CARDS = 10

HAND_SCORES = {
    HandType.HIGH_CARD: (10, 1),
    HandType.PAIR: (20, 1),
    HandType.TWO_PAIR: (30, 2),
    HandType.THREE_OF_A_KIND: (40, 2),
    HandType.STRAIGHT: (60, 3),
    HandType.FLUSH: (70, 3),
    HandType.FULL_HOUSE: (90, 4),
    HandType.FOUR_OF_A_KIND: (120, 5),
    HandType.STRAIGHT_FLUSH: (160, 6),  # optional, included
}


class Phase(Enum):
    DRAFT = 1
    PLAY = 2
    OVER = 3


class PlayerTurn(Enum):
    PLAYER1 = 1
    PLAYER2 = 2


class GameState:
    def __init__(self, phase, p1hand : List[Card], p2hand : List[Card], jokers, p1score, p2score, current_turn):
        self.phase = phase
        self.player1_hand = p1hand
        self.player2_hand = p2hand
        self.jokers = jokers
        self.player1_score = p1score
        self.player2_score = p2score
        self.current_turn = current_turn


class Game:
    def __init__(self, bg_sheet,sheet,cardBackground):
        self.player1_score = 0
        self.player2_score = 0
        self.phase = Phase.DRAFT
        self.draft_turn = 0
        self.jokers = []
        self.p1hand = []
        self.p2hand = []
        self.p1jokers = []
        self.p2jokers = []
        self.current_turn = PlayerTurn.PLAYER1
        self.bg_sheet = bg_sheet
        self.sheet = sheet
        self.cardBackground = cardBackground



    def evaluate_hand(self, hand: List[Card], jokers: List[Joker]) -> int:

        # before we find out what hand we have, apply the pre-phase jokers

        # apply each pre-phase joker
        for joker in jokers:
            hand = joker.pre_card_phase(hand)

        # then, check our hand type so we get our base chips and mult
        checker = Checker(hand)
        hand_type = checker.check()

        # debugging
        print(hand_type)
        # print_card_list(hand)
        # print_jokers(jokers)

        chips, mult = HAND_SCORES.get(hand_type, (0, 0))
        print(chips, mult)
        # apply each card-phase joker

        # for each card...
        for card in hand:
            # if the card is scored...
            if card.scored:
                # then for each time the card triggers...
                for _ in range(card.num_triggers):
                    # apply each card-phase joker
                    chips += card.rank  # Add the proper amount of chips
                    for joker in jokers:
                        chips, mult = joker.apply_card_phase(
                            chips, mult, card.rank, next(iter(card.suits))
                        )

        # apply each post-phase joker
        for joker in jokers:
            chips, mult = joker.post_card_phase(chips, mult, hand)
        print(chips, mult)
        return chips * mult

    def start_round(self):
        # start the game
        self.phase = Phase.DRAFT
        print("Game started between Player 1 and Player 2")
        # Placeholder for game logic

        # 1. generate deck for both players
        game_deck = Deck(bg_sheet=self.bg_sheet, sheet=self.sheet, cardBackground=self.cardBackground)
        self.p1hand = game_deck.draw(10)
        self.p2hand = game_deck.draw(10)

        # 2. generate jokers
        jokers = generate_jokers(JOKER_POOL_SIZE)
        self.jokers = jokers

        # 3. set turn
        self.current_turn = PlayerTurn.PLAYER1

    def get_game_state(self) -> GameState:
        # return the game state that include phase, both players' hands, jokers, scores, and current turn
        return GameState(
            self.phase,
            self.p1hand,
            self.p2hand,
            self.jokers,
            self.player1_score,
            self.player2_score,
            self.current_turn,
        )

    def step(
        self, player: int, action: int = None, hand_list: List[int] = None
    ) -> Tuple:
        # check if the player is correct in the first place
        if (player == 1 and self.current_turn != PlayerTurn.PLAYER1) or (
            player == 2 and self.current_turn != PlayerTurn.PLAYER2
        ):
            # Invalid turn
            print(f"Player {player} tried to play out of turn!")
            return (False, self.get_game_state())

        # draft phase
        if self.phase == Phase.DRAFT:
            # Error check
            if action is None:
                print(f"Player {player} did not provide an action!")
                return (False, self.get_game_state())

            if action < 0 or action >= len(self.jokers):
                # Invalid action
                print(f"Player {player} tried to pick an invalid joker!")
                return (False, self.get_game_state())

            # Handle draft phase actions
            if player == 1:
                # if it's player 1's turn, give them the joker and switch turns
                picked_joker = self.jokers.pop(action)
                self.p1jokers.append(picked_joker)
                self.current_turn = PlayerTurn.PLAYER2
            else:
                # if it's player 2's turn, give them the joker and switch turns, increase draft turn by 1
                picked_joker = self.jokers.pop(action)
                self.p2jokers.append(picked_joker)
                self.current_turn = PlayerTurn.PLAYER1
                self.draft_turn += 1

            # check if draft phase is over
            if self.draft_turn >= JOKER_HAND_SIZE:
                self.phase = Phase.PLAY
                self.current_turn = PlayerTurn.PLAYER1
            return (True, self.get_game_state())

        # play phase
        elif self.phase == Phase.PLAY:
            # conditions: no duplicates, 1 <= len(hand_list) <= 5, all cards are within range

            # check if input is valid
            if hand_list is None:
                print(f"Player {player} did not provide a hand to play!")
                return (False, self.get_game_state())

            # check if length is valid
            if len(hand_list) < 1 or len(hand_list) > 5:
                print(f"Player {player} provided an invalid number of cards!")
                return (False, self.get_game_state())

            # check if duplicates exist
            if len(hand_list) != len(set(hand_list)):
                print(f"Player {player} provided duplicate cards!")
                return (False, self.get_game_state())

            # check if all cards are within range
            for card_index in hand_list:
                if card_index < 0 or card_index >= PLAYER_CARDS:
                    print(f"Player {player} provided an out-of-range card index!")
                    return (False, self.get_game_state())

            # All checks done, allocate cards for correct player
            if player == 1:
                played_hand = [self.p1hand[i] for i in hand_list]
                round_score = self.evaluate_hand(played_hand, self.p1jokers)
                self.player1_score += round_score
                self.current_turn = PlayerTurn.PLAYER2
                return (True, self.get_game_state())
            else:
                played_hand = [self.p2hand[i] for i in hand_list]
                round_score = self.evaluate_hand(played_hand, self.p2jokers)
                self.player2_score += round_score
                self.phase = Phase.OVER  # end game after both players have played
                self.current_turn = None
                return (True, self.get_game_state())

        elif self.phase == Phase.OVER:
            return (False, self.get_game_state())
        else:
            print("Invalid game phase!")
            return (False, self.get_game_state())
