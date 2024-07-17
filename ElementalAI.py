import pygame
from KMRtrainer import CFRBot

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Elemental AI")

background_image = pygame.image.load('images/battleground_bg.jpg').convert()
font = pygame.font.Font('font/Roboto-Bold.ttf', 53)
score_font = pygame.font.Font('font/Roboto-Regular.ttf', 20)
result_font = pygame.font.Font('font/Roboto-Bold.ttf', 35)
play_message = font.render("ELEMENTAL AI", True, (89, 75, 1))
play_message2 = score_font.render("Pick a troupe you want to send", True, (89, 75, 1))

tie_message = result_font.render("It's Tie", True, (255, 235, 193))
won_message = result_font.render("You Won", True, (124, 252, 0))
lost_message = result_font.render("You Lost", True, (255, 0, 0))

ai_win = result_font.render("Sorry! The AI won the game.", True, (255, 0, 0))
you_win = result_font.render("Congratulations! You won the game!", True, (124, 252, 0))

score_font = pygame.font.Font('font/Roboto-Bold.ttf', 25)
user_score_message = score_font.render("You: 0 ", True, (69, 11, 183))
comp_score_message = score_font.render("AI: 0 ", True, (69, 11, 183))

button_knight = pygame.image.load('images/knight_button.png')
button_mage = pygame.image.load('images/mage_button.png')
button_ranger = pygame.image.load('images/ranger_button.png')
button_play_again = pygame.image.load('images/play_again.png')

# Resize the images
button_width, button_height = 150, 45
play_again_button_width, play_again_button_height = 180, 65
button_knight = pygame.transform.scale(button_knight, (button_width, button_height))
button_mage = pygame.transform.scale(button_mage, (button_width, button_height))
button_ranger = pygame.transform.scale(button_ranger, (button_width, button_height))
button_play_again = pygame.transform.scale(button_play_again, (play_again_button_width, play_again_button_height))

knight_rect = button_knight.get_rect(topleft=(50, 300))
mage_rect = button_knight.get_rect(topleft=(235, 300))
ranger_rect = button_ranger.get_rect(topleft=(420, 300))
play_again_rect = button_play_again.get_rect(topleft=(225, 250))

knight = pygame.image.load('images/10.png')
mage = pygame.image.load('images/12.png')
ranger = pygame.image.load('images/11.png')

image_width, image_height = 180, 200
knight = pygame.transform.scale(knight, (image_width, image_height))
mage = pygame.transform.scale(mage, (image_width, image_height))
ranger = pygame.transform.scale(ranger, (image_width, image_height))

weapon_choice = [knight, mage, ranger]
weapon_choice_text = ['R', 'P', 'S']

is_started = False
usear_weapon = None
comp_weapon = None
battle_show_sound = None
battle_show_picture = None
is_user_weapon = False
is_show_weapon = False
user_weapon_text = None
comp_weapon_text = None
result_message = None
end_result_message = None
comp_score = 0
user_score = 0
is_battle_sound_playing = False
game_over = False

bot = CFRBot()
bot.train(1000000)

def reset_game():
    global is_started, usear_weapon, comp_weapon, is_user_weapon, is_show_weapon, user_weapon_text, comp_weapon_text, result_message, comp_score, user_score, game_over
    is_started = False
    usear_weapon = None
    comp_weapon = None
    is_user_weapon = False
    is_show_weapon = False
    user_weapon_text = None
    comp_weapon_text = None
    result_message = None
    comp_score = 0
    user_score = 0
    game_over = False

def pick_weapon(user_weapon_index):
    global is_started, usear_weapon, comp_weapon, is_user_weapon, is_show_weapon, user_weapon_text, comp_weapon_text, battle_show_picture, battle_show_sound

    is_started = True
    usear_weapon = weapon_choice[user_weapon_index]
    user_weapon_text = weapon_choice_text[user_weapon_index]

    # Use the CFRBot to pick the computer's weapon
    avg_strategy = bot.get_average_strategy()
    comp_weapon_index = bot.get_action(avg_strategy)

    comp_weapon = weapon_choice[comp_weapon_index]
    comp_weapon_text = weapon_choice_text[comp_weapon_index]

    is_user_weapon = True
    is_show_weapon = False

def check_game_over():
    global game_over, end_result_message

    if user_score >= 20:
        end_result_message = you_win
        game_over = True
    elif comp_score >= 20:
        end_result_message = ai_win
        game_over = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                if play_again_rect.collidepoint(event.pos):
                    reset_game()
            else:
                if knight_rect.collidepoint(event.pos):
                    pick_weapon(0)
                elif mage_rect.collidepoint(event.pos):
                    pick_weapon(1)
                elif ranger_rect.collidepoint(event.pos):
                    pick_weapon(2)

    screen.blit(background_image, (0, 0))
    screen.blit(user_score_message, (50, 20))
    screen.blit(comp_score_message, (430, 20))

    if not is_started:
        screen.blit(play_message, (120, 150))
        screen.blit(play_message2, (160, 250))

    if is_show_weapon:
        screen.blit(usear_weapon, (20, 70))
        screen.blit(comp_weapon, (400, 60))
        if is_show_weapon and battle_show_picture is not None:
            screen.blit(battle_show_picture, (230, 150))

        screen.blit(result_message, (220, 150))
        is_user_weapon = False

    if is_user_weapon:
        is_show_weapon = True
        if comp_weapon_text == user_weapon_text:
            result_message = tie_message
        elif user_weapon_text == "R" and comp_weapon_text == "P":
            result_message = lost_message
            comp_score += 1
        elif user_weapon_text == "R" and comp_weapon_text == "S":
            result_message = won_message
            user_score += 1
        elif user_weapon_text == "S" and comp_weapon_text == "R":
            result_message = lost_message
            comp_score += 1
        elif user_weapon_text == "S" and comp_weapon_text == "P":
            result_message = won_message
            user_score += 1
        elif user_weapon_text == "P" and comp_weapon_text == "R":
            result_message = won_message
            user_score += 1
        elif user_weapon_text == "P" and comp_weapon_text == "S":
            result_message = lost_message
            comp_score += 1

        user_score_message = score_font.render("You: " + str(user_score), True, (69, 11, 183))
        comp_score_message = score_font.render("AI: " + str(comp_score), True, (69, 11, 183))

        check_game_over()

    screen.blit(button_knight, knight_rect)
    screen.blit(button_mage, mage_rect)
    screen.blit(button_ranger, ranger_rect)

    if game_over:
        screen.blit(end_result_message, (70, 200))
        screen.blit(button_play_again, play_again_rect)

    pygame.display.update()
    clock.tick(10)
