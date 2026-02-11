from bot import Bot

class HighCardBot(Bot):
    def pick_joker(self, game_state):
        # Placeholder for bot decision logic
        return game_state["jokers"][0]
    def finalize_jokers(self):
        # Placeholder for finalizing jokers
        # return the best hand and the arranged jokers
        return [], []