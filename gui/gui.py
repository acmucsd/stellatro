import pygame
from pygame.math import Vector2
from spritesheet import SpriteSheet
from card import Card,CardBackground
from rank import Rank, RANKS
from suit import Suit
from deck import Deck
from jokers import JokerSprite
from utils import get_assets_path, getCardImage,instantiate_card, getHandTypeStr
from game import Game, Phase, PlayerTurn, HAND_SCORES
from card_hand_container import CardHandContainer
from button import Button
from text import Text
from checker import Checker



# 1. Setup
pygame.init()
screen = pygame.display.set_mode((1000, 700))
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

font = pygame.font.SysFont('Arial', 48)


play_button = Button(
    text="PLAY HAND", 
    pos=(400, 550), 
    color=(46, 204, 113), 
    hover_color=(39, 174, 96), 
    size=(150, 40), 
    font_size=12
)

## player 1
p1_chips_text = Text((50, 450), '0', 48, (255, 255, 255), font)
p1_mult_text = Text((150, 450), '1', 48, (255, 255, 255), font)
p1_cross_text = Text((100, 450), "\u00d7", 48, (0, 0, 0), font)
p1_hand_type_text = Text((200, 450), "Select 5 Cards", 48, (255, 255, 255), font)
p1_score_text = Text((100,100),"total score here",48,(255,255,255),font)

p1_is_playing_anim = False
p1_anim_timer = 0.0
p1_anim_card_idx = 0
p1_anim_step = 'initial-wait' # or select, or deselect
p1_hand_type = None
p1_chips = 0
p1_mult = 0
p1_total_score = 0
p1_cards_to_play = []

### GAME
joker_pool = CardHandContainer(Vector2(screen.get_size()[0] / 2,screen.get_size()[1] / 2 -150),5.0)

selected_card_indices = []

## PLAYER's CARDS
player_hand = CardHandContainer(Vector2(screen.get_size()[0] / 2,screen.get_size()[1] / 2 + 50),5.0)
player_playing_hand = CardHandContainer(Vector2(screen.get_size()[0] / 2,screen.get_size()[1] / 2 - 50),5.0)

game = Game(card_bg_spritesheet,playing_cards_spritesheet,CardBackground.WHITE_FRONT)
game.start_round()

for j in game.jokers:
    joker_pool.add(j)

initial_state = game.get_game_state()
for card in initial_state.player1_hand:
    player_hand.add(card)
player_hand.draw(screen)

last_selected_card = None
selected_count = 0
selected_cards = []


def onP1Select():
    checker = Checker(selected_cards)
    hand_type = checker.checkGUI()
    
    
    chips = HAND_SCORES[hand_type][0]
    mult = HAND_SCORES[hand_type][1]
    
    p1_chips_text.updateText(str(chips))
    p1_mult_text.updateText(str(mult))
    p1_hand_type_text.updateText(getHandTypeStr(hand_type))
    global p1_chips, p1_mult
    p1_chips = chips
    p1_mult = mult
    

def onP1Play():
    global p1_anim_timer, p1_anim_card_idx, p1_anim_step, p1_cards_to_play, p1_is_playing_anim
    if len(selected_cards) != 5:
        print("Must have 5 cards to play!")
        return
    for card in selected_cards:
        player_hand.remove(card)
        player_playing_hand.add(card)
        card.selected = False
    
    # we check to figure out what cards actually scored
    checker = Checker(selected_cards) 
    checker.check()
    
    
    if not p1_is_playing_anim:
        p1_anim_timer = 0.0
        p1_anim_card_idx = 0
        p1_anim_step = 'initial-wait'
        p1_cards_to_play = list(checker.hand)
        p1_is_playing_anim = True
        while p1_anim_card_idx < len(p1_cards_to_play) and not p1_cards_to_play[p1_anim_card_idx].scored:
                p1_anim_card_idx += 1
    selected_cards.clear()
    global selected_count
    selected_count = 0
   
   
    
    
    

# 2. Main Game Loop
while running:
    delta = clock.tick(120) / 1000.0
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
                        card.toggle_selection()
                        selected_cards.remove(card)
                        onP1Select()
                        selected_count -= 1
                    elif selected_count < 5:
                        card.toggle_selection()
                        selected_cards.append(card)
                        onP1Select()
                        selected_count += 1
                    break
            if play_button.is_clicked(event.pos):
                print(f"Button '{play_button.text}' pressed!")   
                onP1Play()
    # animation update
    if p1_is_playing_anim:
        p1_anim_timer += delta
        
        if p1_anim_card_idx >= len(p1_cards_to_play):
            #deselect last card
            print("finished anim")
            # finish playing hand here
            p1_anim_timer = 0.0
            p1_anim_card_idx = 0
            p1_anim_step = 'remove'
        elif p1_anim_timer >= 0.5 and p1_anim_step == 'remove':
            score, chips, mult = game.evaluate_hand(p1_cards_to_play,game.p1jokers)
            p1_total_score += score
            p1_score_text.updateText("Total Score: " + str(p1_total_score))
            player_playing_hand.empty()
            p1_is_playing_anim = False
            
        elif p1_anim_timer >= 1.0 and p1_anim_step == 'initial-wait':
            p1_anim_timer = 0
            p1_anim_step = 'select'
            print("initial wait")
        elif p1_anim_timer >= 0.3 and p1_anim_step == 'select':
            print("select card",p1_cards_to_play[p1_anim_card_idx], "scored:",p1_cards_to_play[p1_anim_card_idx].scored)
            p1_chips += RANKS[p1_cards_to_play[p1_anim_card_idx].rank]
            p1_chips_text.updateText(str(p1_chips))
            p1_cards_to_play[p1_anim_card_idx].selected = True
            p1_anim_timer = 0.0
            p1_anim_step = 'deselect'
        elif p1_anim_timer >= 0.3 and p1_anim_step == 'deselect':
            print("deselected card",p1_cards_to_play[p1_anim_card_idx-1])
            p1_cards_to_play[p1_anim_card_idx].selected = False
            p1_anim_timer = 0.0
            p1_anim_step = 'select'
            p1_anim_card_idx += 1
            while p1_anim_card_idx < len(p1_cards_to_play) and not p1_cards_to_play[p1_anim_card_idx].scored:
                p1_anim_card_idx += 1

                
    # 3. Game Logic (update positions, etc.)
    player_hand.update(delta)
    player_playing_hand.update(delta)
    play_button.update(pygame.mouse.get_pos())
    

   

    # 4. Rendering (Drawing things)
    screen.fill("bisque")  # Background color
    
    
    p1_chips_text.draw(screen)
    p1_cross_text.draw(screen)
    p1_mult_text.draw(screen)
    p1_hand_type_text.draw(screen)
    p1_score_text.draw(screen)

    
    player_hand.draw(screen)
    player_playing_hand.draw(screen)
    
    joker_pool.draw(screen)
    screen.blit(play_button.image,play_button.rect)
    
    # Flip the display to show the new frame
    pygame.display.flip()



pygame.quit()