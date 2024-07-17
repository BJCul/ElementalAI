import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
FONT_SIZE = 32
BUTTON_FONT_SIZE = 24
WATER_LIMIT = 100
PLAYER_POUR_RATE = 1  # Amount of water added per tick while holding the mouse button
GLASS_WIDTH = 100
GLASS_HEIGHT = 200
GLASS_X = SCREEN_WIDTH // 2 - GLASS_WIDTH // 2
GLASS_Y = SCREEN_HEIGHT // 2 - GLASS_HEIGHT // 2

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Water Game")
font = pygame.font.Font(None, FONT_SIZE)
button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)

# Game variables
water_percentage = 0
player_pouring = False
player_pour_amount = 0
game_over = False
winner = ""

# Button properties
button_width, button_height = 200, 50
button_x, button_y = SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 50

def draw_game():
    screen.fill(WHITE)
    
    # Draw glass container
    pygame.draw.rect(screen, BLACK, (GLASS_X, GLASS_Y, GLASS_WIDTH, GLASS_HEIGHT), 2)
    
    # Draw water in the glass container
    water_height = (water_percentage / 100) * GLASS_HEIGHT
    pygame.draw.rect(screen, BLUE, (GLASS_X, GLASS_Y + GLASS_HEIGHT - water_height, GLASS_WIDTH, water_height))
    
    # Draw AI cup
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 150, 50, 100, 50), 2)
    ai_text = font.render("AI Cup", True, BLACK)
    screen.blit(ai_text, (SCREEN_WIDTH - 140, 110))
    
    # Draw Player cup
    pygame.draw.rect(screen, BLACK, (50, 50, 100, 50), 2)
    player_text = font.render("Player Cup", True, BLACK)
    screen.blit(player_text, (60, 110))
    
    # Draw water percentage
    water_text = font.render(f"Water: {water_percentage}%", True, BLACK)
    screen.blit(water_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 120))
    
    # Draw game over message and button if game is over
    if game_over:
        message = font.render(winner + " wins!", True, RED)
        screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT // 2 - message.get_height() // 2))
        
        pygame.draw.rect(screen, BLACK, (button_x, button_y, button_width, button_height), 2)
        button_text = button_font.render("Play Again", True, BLACK)
        screen.blit(button_text, (button_x + button_width // 2 - button_text.get_width() // 2, button_y + button_height // 2 - button_text.get_height() // 2))
    
    pygame.display.flip()

def fill_water(pour_amount):
    global water_percentage
    water_percentage += pour_amount
    if water_percentage >= WATER_LIMIT:
        return True  # Indicates water has spilled
    return False

def ai_turn():
    global water_percentage
    # Calculate the AI pour amount to make the player spill
    max_player_pour = PLAYER_POUR_RATE * 1  # Assuming max 30 ticks hold by player
    remaining_space = WATER_LIMIT - water_percentage
    ai_pour_amount = remaining_space - max_player_pour
    if ai_pour_amount < 1:
        ai_pour_amount = 1  # AI must pour at least 1%
    if fill_water(ai_pour_amount):
        end_game("Player")

def player_turn(pour_amount):
    if fill_water(pour_amount):
        end_game("AI")

def end_game(winner_name):
    global game_over, winner
    game_over = True
    winner = winner_name

def reset_game():
    global water_percentage, player_pouring, player_pour_amount, game_over, winner
    water_percentage = 0
    player_pouring = False
    player_pour_amount = 0
    game_over = False
    winner = ""

def main():
    global water_percentage, player_pouring, player_pour_amount, game_over
    clock = pygame.time.Clock()
    player_turn_flag = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and player_turn_flag:
                    if event.button == 1:  # Left mouse button
                        player_pouring = True
                        player_pour_amount = 0
                if event.type == pygame.MOUSEBUTTONUP and player_turn_flag:
                    if event.button == 1:  # Left mouse button
                        player_pouring = False
                        player_turn(player_pour_amount)
                        player_turn_flag = False
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                        reset_game()
                        player_turn_flag = True

        if player_pouring:
            player_pour_amount += PLAYER_POUR_RATE

        if not player_turn_flag and not game_over:
            ai_turn()
            player_turn_flag = True

        draw_game()
        clock.tick(30)

if __name__ == "__main__":
    main()
