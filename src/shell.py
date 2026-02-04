from game import Game, Phase, PlayerTurn, GameState


def render_state(state: GameState):
    """Simple text renderer for the game state."""
    print("\n" + "=" * 30)
    print(f"PHASE: {state.phase.name} | TURN: {state.current_turn}")
    print(f"P1 Score: {state.player1_score} | P2 Score: {state.player2_score}")
    print("-" * 30)

    print(f"Your current hand:")
    for i, card in enumerate(state.player1_hand):
        print(f"[{i}] Rank: {card.rank}, Suits: {', '.join(card.suits)}")
    print(f"Your opponent's hand:")
    for i, card in enumerate(state.player2_hand):
        print(f"[{i}] Rank: {card.rank}, Suits: {', '.join(card.suits)}")

    if state.phase == Phase.DRAFT:
        print("Available Jokers to pick:")
        for i, joker in enumerate(state.jokers):
            print(f"[{i}] {joker}")  # Assumes your Joker classes have a __str__

    elif state.phase == Phase.PLAY:
        print("Your Hand Indices: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]")
        # You could add logic here to show actual Card ranks/suits
    print("=" * 30)


def main():
    game = Game()
    game.start_round()  # Initialize deck and jokers

    while game.phase != Phase.OVER:
        state = game.get_game_state()
        render_state(state)

        current_p_num = 1 if state.current_turn == PlayerTurn.PLAYER1 else 2

        try:
            if state.phase == Phase.DRAFT:
                choice = input(f"Player {current_p_num}, pick a Joker index: ")
                success, _ = game.step(current_p_num, action=int(choice))

            elif state.phase == Phase.PLAY:
                cards = input(
                    f"Player {current_p_num}, enter up to 5 card indices (e.g., 0,2,4): "
                )
                indices = [int(x.strip()) for x in cards.split(",")]
                success, _ = game.step(current_p_num, hand_list=indices)

            if not success:
                print(">>> Invalid Move! Try again.")

        except ValueError:
            print(">>> Please enter valid numbers.")
        except Exception as e:
            print(f">>> Error: {e}")

    print("\nGAME OVER")
    final = game.get_game_state()
    print(f"Final Score - P1: {final.player1_score} | P2: {final.player2_score}")


if __name__ == "__main__":
    main()
