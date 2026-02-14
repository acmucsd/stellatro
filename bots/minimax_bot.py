# bots/minimax_bot.py
import math
from itertools import combinations
from dataclasses import dataclass
from typing import List, Tuple

from src.card import Card
from src.jokers import Joker
from src.game import JOKER_HAND_SIZE, evaluate_hand
from src.checker import Checker, HandType
from src.game import HAND_SCORES

def all_subsets_upto_5(hand: List[Card]):
    n = len(hand)
    for k in range(1, min(5, n) + 1):
        for idxs in combinations(range(n), k):
            yield idxs

def best_play_value(hand10: List[Card], jokers: List[Joker]) -> int:
    best = -math.inf
    for idxs in all_subsets_upto_5(hand10):
        subset = [hand10[i] for i in idxs]
        v = evaluate_hand(subset, jokers)
        if v > best:
            best = v
    return best

def best_play_indices(hand10: List[Card], jokers: List[Joker]) -> List[int]:
    best = -math.inf
    best_idxs = None
    for idxs in all_subsets_upto_5(hand10):
        subset = [hand10[i] for i in idxs]
        v = evaluate_hand(subset, jokers)
        if v > best:
            best = v
            best_idxs = idxs
    return list(best_idxs)


@dataclass(frozen=True)
class DraftState:
    remaining: Tuple[Joker, ...]
    p1_picks: Tuple[Joker, ...]
    p2_picks: Tuple[Joker, ...]
    turn: int  # 1 = P1 (max), 2 = P2 (min)


class MinimaxBot:
    """
    Perfect-information minimax.
    Assumes bot is Player 1.
    """

    def __init__(self):
        self.my_picks: List[Joker] = []
        self.opp_picks: List[Joker] = []

    def reset_round(self):
        self.my_picks = []
        self.opp_picks = []

    def pick_joker(self, game_state) -> int:
        """
        Return index into game_state.jokers.
        Requires perfect info: game_state.player1_hand and player2_hand visible.
        """
        p1_hand = list(game_state.player1_hand)
        p2_hand = list(game_state.player2_hand)
        pool = list(game_state.jokers)

        # If GameState doesn't expose drafted jokers, we track internally
        root = DraftState(
            remaining=tuple(pool),
            p1_picks=tuple(self.my_picks),
            p2_picks=tuple(self.opp_picks),
            turn=1,
        )

        best_idx = 0
        best_val = -math.inf

        for i, jk in enumerate(pool):
            new_state = DraftState(
                remaining=tuple(pool[:i] + pool[i+1:]),
                p1_picks=root.p1_picks + (jk,),
                p2_picks=root.p2_picks,
                turn=2,
            )
            v = self._minimax(p1_hand, p2_hand, new_state, -math.inf, math.inf)
            if v > best_val:
                best_val = v
                best_idx = i

        # update internal picks (assumes we are player 1)
        self.my_picks.append(pool[best_idx])
        return best_idx

    def observe_opponent_pick(self, picked_joker: Joker):
        # call this from the engine when opponent picks
        self.opp_picks.append(picked_joker)

    def pick_play_hand(self, game_state) -> List[int]:
        """
        Choose indices from player1_hand (size 1..5) that maximize our score.
        Since play is simultaneous-ish in your engine, this is optimal given our jokers.
        """
        return best_play_indices(list(game_state.player1_hand), self.my_picks)

    def _leaf_value(self, p1_hand, p2_hand, state: DraftState) -> float:
        p1_best = best_play_value(p1_hand, list(state.p1_picks))
        p2_best = best_play_value(p2_hand, list(state.p2_picks))
        return p1_best - p2_best

    def _minimax(self, p1_hand, p2_hand, state: DraftState, alpha: float, beta: float) -> float:
        if len(state.p1_picks) == JOKER_HAND_SIZE and len(state.p2_picks) == JOKER_HAND_SIZE:
            return self._leaf_value(p1_hand, p2_hand, state)

        rem = state.remaining

        if state.turn == 1:
            best = -math.inf
            for i, jk in enumerate(rem):
                nxt = DraftState(
                    remaining=rem[:i] + rem[i+1:],
                    p1_picks=state.p1_picks + (jk,),
                    p2_picks=state.p2_picks,
                    turn=2,
                )
                v = self._minimax(p1_hand, p2_hand, nxt, alpha, beta)
                best = max(best, v)
                alpha = max(alpha, best)
                if alpha >= beta:
                    break
            return best
        else:
            best = math.inf
            for i, jk in enumerate(rem):
                nxt = DraftState(
                    remaining=rem[:i] + rem[i+1:],
                    p1_picks=state.p1_picks,
                    p2_picks=state.p2_picks + (jk,),
                    turn=1,
                )
                v = self._minimax(p1_hand, p2_hand, nxt, alpha, beta)
                best = min(best, v)
                beta = min(beta, best)
                if alpha >= beta:
                    break
            return best
