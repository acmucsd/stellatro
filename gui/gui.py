import pygame
from spritesheet import SpriteSheet
from card import Card,CardBackground
from rank import Rank
from suit import Suit
from deck import Deck
from jokers import JokerSprite
from utils import get_assets_path, getCardImage,instantiate_card
from game import Game, Phase, PlayerTurn
from card_hand_container import CardHandContainer
from button import Button



# 1. Setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True

# Card Background Sprite Sheets
card_background_img = pygame.image.load(get_assets_path('CardBackgrounds.png'))
card_bg_spritesheet = SpriteSheet(card_background_img)
# Front Card Sprite Sheets
playing_cards_img = pygame.image.load(get_assets_path('PlayingCards.png'))
playing_cards_spritesheet = SpriteSheet(playing_cards_img)
# Joker Sprite Sheet
joker_img = pygame.image.load(get_assets_path('Jokers.png'))
joker_spritesheet = SpriteSheet(joker_img)

play_button = Button("PLAY HAND", (34, 139, 34), (400, 500))


### GAME





selected_card_indices = []

## PLAYER's CARDS
player_hand = CardHandContainer(pygame.math.Vector2(screen.get_size()[0] / 2,screen.get_size()[1] / 2),5.0)

game = Game(card_bg_spritesheet,playing_cards_spritesheet,CardBackground.WHITE_FRONT)
game.start_round()

initial_state = game.get_game_state()
for card in initial_state.player1_hand:
    player_hand.add(card)
player_hand.draw(screen)

last_selected_card = None
selected_count = 0

# 2. Main Game Loop
while running:
    state = game.get_game_state()
    # Check for events (clicks, keypresses)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for card in player_hand:
                if card.rect.collidepoint(mouse_pos):
                    if card.selected:
                        card.selected = False
                        selected_count -= 1
                    elif selected_count < 5:
                        card.selected = True
                        selected_count += 1
                    break
            if play_button.is_clicked(event.pos):
                print(f"Button '{play_button.text}' pressed!")   
                
                
    # 3. Game Logic (update positions, etc.)
    player_hand.update()
    

    # 4. Rendering (Drawing things)
    screen.fill("bisque")  # Background color
    
    player_hand.update()
    play_button.draw(screen)
    player_hand.draw(screen)
    
    # Flip the display to show the new frame
    pygame.display.flip()

    # 5. Cap the frame rate to 60 FPS
    clock.tick(60)

pygame.quit()