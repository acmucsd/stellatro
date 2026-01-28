# Stellatro

temporary repo structure:

src/

- main.py: include the main logic of the game
- jokers.py: include all jokers as functions that take in the current card selection.
- card.py: include class Card and class Deck.
- checker.py: should contain a class called Checker that can check what is the largest hand.

bots/

- bot.py: an example bot

## TODO Refactoring:

- Jokers should consider the entire hand of the player [DONE]
- Jokers should have three separate phases --> pre card scoring, card scoring, post card scoring [DONE]
- Game logic should be firmly separated from bot logic, i.e. there should be an interface for game playing and game playing only
