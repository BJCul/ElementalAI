import pygame
from KMRtrainer import CFRBot

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Elemental AI")
base_font = 'font/PressStart2P-Regular.ttf'

background_image = pygame.image.load('images/battleground_bg.jpg').convert()
font = pygame.font.Font(base_font, 32)
score_font = pygame.font.Font(base_font, 10)
result_font = pygame.font.Font(base_font, 20)
label_font = pygame.font.Font(base_font, 15)  # Smaller font for the label

play_message = font.render("ELEMENTAL AI", True, (89, 75, 1))
play_message2 = score_font.render("Pick a troupe you want to send", True, (89, 75, 1))

tie_message = result_font.render("It's Tie", True, (186, 141, 19))
won_message = result_font.render("You Won", True, (32, 156, 12))
lost_message = result_font.render("You Lost", True, (153, 20, 15))

ai_win = score_font.render("Sorry! The AI won the game.", True, (255, 0, 0))
you_win = score_font.render("Congratulations! You won the game!", True, (124, 252, 0))

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

knight_rect = button_knight.get_rect(topleft=(50, 350))
mage_rect = button_knight.get_rect(topleft=(235, 350))
ranger_rect = button_ranger.get_rect(topleft=(420, 350))
play_again_rect = button_play_again.get_rect(topleft=(225, 250))

knight = pygame.image.load('images/10.png')
mage = pygame.image.load('images/12.png')
ranger = pygame.image.load('images/11.png')

image_width, image_height = 180, 249
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
comp_health = 100
user_health = 100
is_battle_sound_playing = False
game_over = False
user_combo_count = 0
ai_combo_count = 0
user_damage = 0
ai_damage = 0

bot = CFRBot()
bot.train(1000000)

def reset_game():
    global is_started, usear_weapon, comp_weapon, is_user_weapon, is_show_weapon, user_weapon_text, comp_weapon_text, result_message, comp_health, user_health, game_over, user_combo_count, ai_combo_count, user_damage, ai_damage
    is_started = False
    usear_weapon = None
    comp_weapon = None
    is_user_weapon = False
    is_show_weapon = False
    user_weapon_text = None
    comp_weapon_text = None
    result_message = None
    comp_health = 100
    user_health = 100
    game_over = False
    user_combo_count = 0
    ai_combo_count = 0
    user_damage = 0
    ai_damage = 0

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

    if user_health <= 0:
        end_result_message = ai_win
        game_over = True
    elif comp_health <= 0:
        end_result_message = you_win
        game_over = True

def draw_health_bar(x, y, health, label, damage, align):
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 200, 20))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, 200 * (health / 100), 20))
    health_text = score_font.render(f"{int(health)}%", True, (255, 69, 69))
    label_text = label_font.render(label, True, (247, 229, 213))
    screen.blit(health_text, (x, y + 20))  # Left-align the percentage below the health bar
    screen.blit(label_text, (x, y - 20))   # Left-align the label above the health bar

    # Display damage dealt only if damage is greater than zero
    if damage > 0:
        damage_text = score_font.render(f"{damage}hp", True, (237, 0, 0))
        if align == 'left':
            screen.blit(damage_text, (x + 260, y))  # Display damage to the right of the health bar
        else:
            screen.blit(damage_text, (x - 100, y))  # Display damage to the left of the health bar

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
    draw_health_bar(50, 30, user_health, "You", ai_damage, 'left')
    draw_health_bar(350, 30, comp_health, "AI", user_damage, 'right')

    if not is_started:
        screen.blit(play_message, (120, 150))
        screen.blit(play_message2, (160, 250))

    if is_show_weapon:
        screen.blit(usear_weapon, (20, 85))
        screen.blit(comp_weapon, (400, 85))
        if is_show_weapon and battle_show_picture is not None:
            screen.blit(battle_show_picture, (230, 150))

        screen.blit(result_message, (220, 150))
        is_user_weapon = False

    if is_user_weapon:
        is_show_weapon = True
        user_damage = 0
        ai_damage = 0

        if comp_weapon_text == user_weapon_text:
            result_message = tie_message
            user_combo_count = 0
            ai_combo_count = 0
        elif user_weapon_text == "R" and comp_weapon_text == "P":
            result_message = lost_message
            user_health -= 10
            user_damage = 10
            user_combo_count = 0
            ai_combo_count += 1
            if ai_combo_count >= 5:
                user_health -= 20  # additional 20 damage for a total of 30
                user_damage = 30
            elif ai_combo_count >= 3:
                user_health -= 10  # additional 10 damage for a total of 20
                user_damage = 20
        elif user_weapon_text == "R" and comp_weapon_text == "S":
            result_message = won_message
            comp_health -= 10
            ai_damage = 10
            ai_combo_count = 0
            user_combo_count += 1
            if user_combo_count >= 5:
                comp_health -= 20  # additional 20 damage for a total of 30
                ai_damage = 30
            elif user_combo_count >= 3:
                comp_health -= 10  # additional 10 damage for a total of 20
                ai_damage = 20
        elif user_weapon_text == "S" and comp_weapon_text == "R":
            result_message = lost_message
            user_health -= 10
            user_damage = 10
            user_combo_count = 0
            ai_combo_count += 1
            if ai_combo_count >= 5:
                user_health -= 20  # additional 20 damage for a total of 30
                user_damage = 30
            elif ai_combo_count >= 3:
                user_health -= 10  # additional 10 damage for a total of 20
                user_damage = 20
        elif user_weapon_text == "S" and comp_weapon_text == "P":
            result_message = won_message
            comp_health -= 10
            ai_damage = 10
            ai_combo_count = 0
            user_combo_count += 1
            if user_combo_count >= 5:
                comp_health -= 20  # additional 20 damage for a total of 30
                ai_damage = 30
            elif user_combo_count >= 3:
                comp_health -= 10  # additional 10 damage for a total of 20
                ai_damage = 20
        elif user_weapon_text == "P" and comp_weapon_text == "R":
            result_message = won_message
            comp_health -= 10
            ai_damage = 10
            ai_combo_count = 0
            user_combo_count += 1
            if user_combo_count >= 5:
                comp_health -= 20  # additional 20 damage for a total of 30
                ai_damage = 30
            elif user_combo_count >= 3:
                comp_health -= 10  # additional 10 damage for a total of 20
                ai_damage = 20
        elif user_weapon_text == "P" and comp_weapon_text == "S":
            result_message = lost_message
            user_health -= 10
            user_damage = 10
            user_combo_count = 0
            ai_combo_count += 1
            if ai_combo_count >= 5:
                user_health -= 20  # additional 20 damage for a total of 30
                user_damage = 30
            elif ai_combo_count >= 3:
                user_health -= 10  # additional 10 damage for a total of 20
                user_damage = 20

        check_game_over()

    screen.blit(button_knight, knight_rect)
    screen.blit(button_mage, mage_rect)
    screen.blit(button_ranger, ranger_rect)

    if game_over:
        screen.blit(end_result_message, (180, 200))
        screen.blit(button_play_again, play_again_rect)

    pygame.display.update()
    clock.tick(10)
