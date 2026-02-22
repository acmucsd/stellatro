import random
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
# Allow importing modules directly from src/ when tests run from repo root.
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from card import Card, Suit
from game import Game, JOKER_HAND_SIZE, PLAYER_CARDS, Phase, PlayerTurn
from jokers import RegularJoker


def build_hand() -> list[Card]:
    """Create a deterministic 10-card hand used by both players in tests."""
    ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 14]
    suits = [Suit.DIAMOND, Suit.HEART, Suit.CLUB, Suit.SPADE]
    return [Card(rank=r, suit=suits[i % len(suits)]) for i, r in enumerate(ranks)]


def build_game_for_draft(joker_count: int = 8) -> Game:
    """Build a game already positioned at the start of draft phase."""
    game = Game()
    game.phase = Phase.DRAFT
    game.current_turn = PlayerTurn.PLAYER1
    game.draft_turn = 0
    game.p1hand = build_hand()
    game.p2hand = build_hand()
    game.jokers = [RegularJoker() for _ in range(joker_count)]
    return game


def advance_to_play_phase(game: Game) -> None:
    """Run a full draft sequence so tests can focus on play-phase behavior."""
    for _ in range(JOKER_HAND_SIZE):
        # Each draft round is two legal picks: P1 then P2.
        ok, _ = game.step(1, action=0)
        assert ok
        ok, _ = game.step(2, action=0)
        assert ok
    assert game.phase == Phase.PLAY
    assert game.current_turn == PlayerTurn.PLAYER1


class TestGameLoopEdges(unittest.TestCase):
    def test_draft_rejects_out_of_turn(self):
        # Player 2 tries to draft first, but Player 1 must start.
        game = build_game_for_draft()
        with patch("builtins.print"):
            success, state = game.step(2, action=0)
        # Nothing should change on an out-of-turn move.
        self.assertFalse(success)
        self.assertEqual(state.current_turn, PlayerTurn.PLAYER1)
        self.assertEqual(len(state.jokers), 8)
        self.assertEqual(len(state.player1_hand), PLAYER_CARDS)
        self.assertEqual(len(state.player2_hand), PLAYER_CARDS)

    def test_draft_rejects_missing_or_invalid_action(self):
        # In draft phase, action must be a valid joker index.
        game = build_game_for_draft()
        with patch("builtins.print"):
            success_none, _ = game.step(1, action=None)
            success_neg, _ = game.step(1, action=-1)
            success_big, _ = game.step(1, action=999)
        self.assertFalse(success_none)
        self.assertFalse(success_neg)
        self.assertFalse(success_big)
        self.assertEqual(game.current_turn, PlayerTurn.PLAYER1)
        self.assertEqual(len(game.jokers), 8)

    def test_draft_transitions_to_play_after_expected_picks(self):
        # Verify the turn-by-turn draft state before final transition.
        game = build_game_for_draft()
        with patch("builtins.print"):
            ok, _ = game.step(1, action=0)
            self.assertTrue(ok)
            self.assertEqual(game.current_turn, PlayerTurn.PLAYER2)
            self.assertEqual(game.draft_turn, 0)
            self.assertEqual(game.phase, Phase.DRAFT)

            ok, _ = game.step(2, action=0)
            self.assertTrue(ok)
            self.assertEqual(game.current_turn, PlayerTurn.PLAYER1)
            self.assertEqual(game.draft_turn, 1)
            self.assertEqual(game.phase, Phase.DRAFT)

            ok, _ = game.step(1, action=0)
            self.assertTrue(ok)
            self.assertEqual(game.current_turn, PlayerTurn.PLAYER2)

            ok, _ = game.step(2, action=0)
            self.assertTrue(ok)

        # After both players complete joker picks, game must enter PLAY.
        self.assertEqual(game.phase, Phase.PLAY)
        self.assertEqual(game.current_turn, PlayerTurn.PLAYER1)
        self.assertEqual(game.draft_turn, JOKER_HAND_SIZE)
        self.assertEqual(len(game.p1jokers), JOKER_HAND_SIZE)
        self.assertEqual(len(game.p2jokers), JOKER_HAND_SIZE)

    def test_play_rejects_invalid_inputs(self):
        # Move to PLAY and stub scoring so validation is the only moving part.
        game = build_game_for_draft()
        advance_to_play_phase(game)
        game.evaluate_hand = lambda hand, jokers: 11

        with patch("builtins.print"):
            missing, _ = game.step(1, hand_list=None)
            empty, _ = game.step(1, hand_list=[])
            too_many, _ = game.step(1, hand_list=[0, 1, 2, 3, 4, 5])
            duplicate, _ = game.step(1, hand_list=[0, 0, 1, 2, 3])
            out_neg, _ = game.step(1, hand_list=[-1, 1, 2, 3, 4])
            out_big, _ = game.step(1, hand_list=[0, 1, 2, 3, PLAYER_CARDS])

        # Invalid play submissions should fail without mutating score/turn.
        self.assertFalse(missing)
        self.assertFalse(empty)
        self.assertFalse(too_many)
        self.assertFalse(duplicate)
        self.assertFalse(out_neg)
        self.assertFalse(out_big)
        self.assertEqual(game.player1_score, 0)
        self.assertEqual(game.phase, Phase.PLAY)
        self.assertEqual(game.current_turn, PlayerTurn.PLAYER1)

    def test_play_rejects_out_of_turn(self):
        # In PLAY phase, Player 1 should act first; Player 2 is rejected.
        game = build_game_for_draft()
        advance_to_play_phase(game)
        game.evaluate_hand = lambda hand, jokers: 33

        with patch("builtins.print"):
            success, _ = game.step(2, hand_list=[0, 1, 2, 3, 4])
        self.assertFalse(success)
        self.assertEqual(game.player2_score, 0)
        self.assertEqual(game.current_turn, PlayerTurn.PLAYER1)

    def test_play_success_and_game_over_transition(self):
        # Use deterministic scoring to validate state transitions exactly.
        game = build_game_for_draft()
        advance_to_play_phase(game)
        game.evaluate_hand = lambda hand, jokers: 42

        with patch("builtins.print"):
            # P1 makes a legal play.
            p1_ok, p1_state = game.step(1, hand_list=[0, 1, 2, 3, 4])
            # P2 responds with a legal play.
            p2_ok, p2_state = game.step(2, hand_list=[0, 1, 2, 3, 4])
            # Any further play attempts after OVER should fail.
            over_ok, over_state = game.step(1, hand_list=[0, 1, 2, 3, 4])

        self.assertTrue(p1_ok)
        self.assertEqual(p1_state.player1_score, 42)
        self.assertEqual(p1_state.current_turn, PlayerTurn.PLAYER2)
        self.assertEqual(game.phase, Phase.OVER)

        self.assertTrue(p2_ok)
        self.assertEqual(p2_state.player2_score, 42)
        self.assertEqual(p2_state.current_turn, None)
        self.assertEqual(p2_state.phase, Phase.OVER)

        self.assertFalse(over_ok)
        self.assertEqual(over_state.phase, Phase.OVER)

    def test_play_rejects_short_hand_without_raising(self):
        # Short hands are invalid and should be rejected without exceptions.
        game = build_game_for_draft()
        advance_to_play_phase(game)
        with patch("builtins.print"):
            success, state = game.step(1, hand_list=[0, 1, 2, 3])
        self.assertFalse(success)
        self.assertEqual(state.phase, Phase.PLAY)
        self.assertEqual(state.current_turn, PlayerTurn.PLAYER1)
        self.assertEqual(state.player1_score, 0)


class TestGameLoopFuzz(unittest.TestCase):
    def test_randomized_state_machine_does_not_break_invariants(self):
        # Fuzz the state machine with reproducible seeds and mixed valid/invalid moves.
        for seed in range(200):
            rng = random.Random(seed)
            game = build_game_for_draft(joker_count=15)
            game.evaluate_hand = lambda hand, jokers: len(hand) * 10

            # Phase should only move forward: DRAFT -> PLAY -> OVER.
            phase_order = {Phase.DRAFT: 0, Phase.PLAY: 1, Phase.OVER: 2}
            highest_phase = phase_order[game.phase]

            with patch("builtins.print"):
                for _ in range(50):
                    player = rng.choice([1, 2])

                    if game.phase == Phase.DRAFT:
                        # During draft, randomly sample legal and illegal action shapes.
                        action_mode = rng.choice(["none", "neg", "big", "valid"])
                        if action_mode == "none":
                            result = game.step(player, action=None)
                        elif action_mode == "neg":
                            result = game.step(player, action=-1)
                        elif action_mode == "big":
                            result = game.step(player, action=999)
                        else:
                            if len(game.jokers) == 0:
                                result = game.step(player, action=999)
                            else:
                                result = game.step(
                                    player, action=rng.randrange(len(game.jokers))
                                )
                    elif game.phase == Phase.PLAY:
                        # During play, sample hand payloads across boundary cases.
                        hand_mode = rng.choice(
                            [
                                "none",
                                "empty",
                                "too_many",
                                "duplicate",
                                "out_neg",
                                "out_big",
                                "valid",
                            ]
                        )
                        if hand_mode == "none":
                            result = game.step(player, hand_list=None)
                        elif hand_mode == "empty":
                            result = game.step(player, hand_list=[])
                        elif hand_mode == "too_many":
                            result = game.step(player, hand_list=[0, 1, 2, 3, 4, 5])
                        elif hand_mode == "duplicate":
                            result = game.step(player, hand_list=[0, 0, 1, 2, 3])
                        elif hand_mode == "out_neg":
                            result = game.step(player, hand_list=[-1, 1, 2, 3, 4])
                        elif hand_mode == "out_big":
                            result = game.step(
                                player, hand_list=[0, 1, 2, 3, PLAYER_CARDS]
                            )
                        else:
                            hand_size = rng.randint(1, 5)
                            result = game.step(
                                player,
                                hand_list=rng.sample(range(PLAYER_CARDS), hand_size),
                            )
                    else:
                        # Once OVER, any new step call should keep terminal invariants.
                        result = game.step(player, hand_list=[0, 1, 2, 3, 4])

                    # Always returns (success, state) regardless of path.
                    self.assertIsInstance(result, tuple)
                    self.assertEqual(len(result), 2)
                    success, state = result

                    # Core invariants that should never be violated.
                    self.assertIn(success, (True, False))
                    self.assertIn(state.phase, (Phase.DRAFT, Phase.PLAY, Phase.OVER))
                    self.assertGreaterEqual(state.player1_score, 0)
                    self.assertGreaterEqual(state.player2_score, 0)
                    self.assertEqual(len(state.player1_hand), PLAYER_CARDS)
                    self.assertEqual(len(state.player2_hand), PLAYER_CARDS)
                    self.assertLessEqual(len(game.p1jokers), JOKER_HAND_SIZE)
                    self.assertLessEqual(len(game.p2jokers), JOKER_HAND_SIZE)

                    # Phase monotonicity check.
                    self.assertGreaterEqual(phase_order[state.phase], highest_phase)
                    highest_phase = phase_order[state.phase]

                    if state.phase in (Phase.DRAFT, Phase.PLAY):
                        # Non-terminal phases must always have an active turn owner.
                        self.assertIn(
                            state.current_turn,
                            (PlayerTurn.PLAYER1, PlayerTurn.PLAYER2),
                        )
                    else:
                        # Terminal state must clear turn ownership.
                        self.assertIsNone(state.current_turn)


if __name__ == "__main__":
    unittest.main()
