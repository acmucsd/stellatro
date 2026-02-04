import pygame
from spritesheet import SpriteSheet
from card import Card,CardBackground
from rank import Rank
from suit import Suit
from deck import Deck, getCardImage
from joker import Joker

# 1. Setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True

card_background_img = pygame.image.load('../assets/CardBackgrounds.png')
card_bg_spritesheet = SpriteSheet(card_background_img)
playing_cards_img = pygame.image.load('../assets/PlayingCards.png')
playing_cards_spritesheet = SpriteSheet(playing_cards_img)
joker_img =pygame.image.load('../assets/Jokers.png')
joker_spritesheet = SpriteSheet(joker_img)

jokers = pygame.sprite.Group()
joker1 = Joker(joker_spritesheet.get_image(0,0,70,94,2,(0,0,0),1,1),500,200)
jokers.add(joker1)

my_deck = Deck(playing_cards_spritesheet,card_bg_spritesheet)
my_deck.add_card(Rank.THREE, Suit.HEART, CardBackground.RED, 100, 100)
my_deck.add_card(Rank.ACE, Suit.SPADE, CardBackground.RED, 200, 100)

# 2. Main Game Loop
while running:
    
    # Check for events (clicks, keypresses)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 3. Game Logic (update positions, etc.)
    

    # 4. Rendering (Drawing things)
    screen.fill("bisque")  # Background color
    
    my_deck.cards.draw(screen)
    jokers.draw(screen)
    
    
    # Flip the display to show the new frame
    pygame.display.flip()

    # 5. Cap the frame rate to 60 FPS
    clock.tick(60)

pygame.quit()