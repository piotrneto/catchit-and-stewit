import pygame
import random
import os
import sys
import csv

# Set the working directory to the same folder as this Python file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize Pygame
pygame.init()

def load_high_scores():
    global high_scores
    if os.path.exists(HIGH_SCORES_FILE):
        with open(HIGH_SCORES_FILE, "r") as file:
            reader = csv.reader(file)
            high_scores = [row for row in reader]
    high_scores = sorted(high_scores, key=lambda x: int(x[1]), reverse=True)[:MAX_HIGH_SCORES]

def save_high_scores():
    with open(HIGH_SCORES_FILE, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(high_scores)

def reset_game():
    global score, lives, ingredient_speed, ingredient_sprite, ingredient_x, ingredient_y, player_x, player_velocity, game_state
    score = 0
    lives = 5
    ingredient_speed = 3
    ingredient_sprite = random.choice([ingredient_black, ingredient_red, ingredient_green, ingredient_orange])
    ingredient_x = random.randint(0, width - ingredient_size)
    ingredient_y = 0
    player_x = width // 2 - player_width // 2
    player_velocity = 0
    game_state = PLAYING

def draw_playing_state(screen, player_sprite, player_x, player_y, ingredient_sprite, ingredient_x, ingredient_y, score, lives, font, width):
    # Draw player
    screen.blit(player_sprite, (player_x, player_y))

    # Draw ingredient
    screen.blit(ingredient_sprite, (ingredient_x, ingredient_y))

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (width - 120, 10))

    # Add this at the end of the function
    return score_text, lives_text

def draw_game_over_state(screen, score, player_name, high_scores, font, width, height):
    # Draw game over and high score screen
    game_over_text = font.render("GAME OVER", True, (0, 0, 0))
    final_score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
    name_prompt = font.render("Enter your name:", True, (0, 0, 0))
    # Create a black background surface for the name input
    name_bg = pygame.Surface((200, 30))
    name_bg.fill((0, 0, 0))
    # Render the player name in white text
    name_text = font.render(player_name, True, (255, 255, 255))
    # Blit the black background first, then the white text on top
    screen.blit(name_bg, (width // 2 - 100, height // 4 + 100))
    screen.blit(name_text, (width // 2 - 100, height // 4 + 105))
    
    # Add blinking cursor
    cursor_pos = (width // 2 - 100 + name_text.get_width() + 5, height // 4 + 105)
    if pygame.time.get_ticks() % 1000 < 500:  # Blink every 0.5 seconds
        pygame.draw.line(screen, (255, 255, 255), cursor_pos, (cursor_pos[0], cursor_pos[1] + 20), 2)
    
    exit_text = font.render("Press ESC to exit", True, (0, 0, 0))
    restart_text = font.render("Press ENTER to restart game", True, (0, 0, 0))
    
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 4 - 50))
    screen.blit(final_score_text, (width // 2 - final_score_text.get_width() // 2, height // 4))
    screen.blit(name_prompt, (width // 2 - name_prompt.get_width() // 2, height // 4 + 50))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 200))
    screen.blit(exit_text, (width // 2 - exit_text.get_width() // 2, height // 2 + 250))

    # Draw high scores (only top 5)
    high_score_text = font.render("HIGH SCORES", True, (0, 0, 0))
    screen.blit(high_score_text, (width // 2 - high_score_text.get_width() // 2, height // 2 - 30))
    for i, (name, high_score) in enumerate(high_scores[:5]):  # Only iterate through the first 5 scores
        score_text = font.render(f"{i+1}. {name}: {high_score}", True, (0, 0, 0))
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 + 20 + i * 30))
def draw_paused_state(screen, font, width, height):
    pause_text = font.render("PAUSED", True, (0, 0, 0))
    resume_text = font.render("Press P to resume", True, (0, 0, 0))
    screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 - 50))
    screen.blit(resume_text, (width // 2 - resume_text.get_width() // 2, height // 2 + 50))

# Set up the display
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Catch Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load sprites
sprite_dir = os.path.join("assets", "sprites")
player_sprite = pygame.image.load(os.path.join(sprite_dir, "player_pot_200x250.png"))
ingredient_black = pygame.image.load(os.path.join(sprite_dir, "ingredient_black_32x32.png"))
ingredient_red = pygame.image.load(os.path.join(sprite_dir, "ingredient_red_32x32.png"))
ingredient_green = pygame.image.load(os.path.join(sprite_dir, "ingredient_green_32x32.png"))
ingredient_orange = pygame.image.load(os.path.join(sprite_dir, "ingredient_orange_32x32.png"))
ingredient_evil = pygame.image.load(os.path.join(sprite_dir, "ingredient_evil_32x32.png"))

# Player
player_width = 100
player_height = 10
player_x = width // 2 - player_width // 2
player_y = height - player_height - 200
player_speed = 5
player_acceleration = 1.2
player_max_speed = 10
player_velocity = 0

# Ingredient
ingredient_size = 32
ingredient_x = random.randint(0, width - ingredient_size)
ingredient_y = 0
ingredient_speed = 3
ingredient_sprite = random.choice([ingredient_black, ingredient_red, ingredient_green, ingredient_orange, ingredient_evil])

# Score and lives
score = 0
lives = 5
font = pygame.font.Font(None, 36)

# Game states
PLAYING = 0
GAME_OVER = 1
PAUSED = 2
game_state = PLAYING

# High scores
high_scores = []
HIGH_SCORES_FILE = "high_scores.csv"
MAX_HIGH_SCORES = 5

load_high_scores()

# Game loop
running = True
clock = pygame.time.Clock()
player_name = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if game_state == PLAYING:
                    game_state = PAUSED
                elif game_state == PAUSED:
                    game_state = PLAYING
        if game_state == GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_name:
                        high_scores.append([player_name, str(score)])
                        high_scores.sort(key=lambda x: int(x[1]), reverse=True)
                        high_scores = high_scores[:MAX_HIGH_SCORES]
                        save_high_scores()
                        player_name = ""
                        reset_game()
                    else:
                        reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

    if game_state == PLAYING:
        # Move player with acceleration
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_velocity -= player_acceleration
        elif keys[pygame.K_RIGHT]:
            player_velocity += player_acceleration
        else:
            player_velocity *= 0.9  # Decelerate when no key is pressed

        # Clamp velocity to max speed
        player_velocity = max(-player_max_speed, min(player_velocity, player_max_speed))

        # Update player position
        player_x += player_velocity

        # Keep player within screen bounds
        player_x = max(0, min(player_x, width - player_width))

        # Move ingredient
        ingredient_y += ingredient_speed

        # Check for collision
        if (player_x < ingredient_x < player_x + player_width and
            player_y < ingredient_y + ingredient_size < player_y + player_height):
            if ingredient_sprite == ingredient_evil:
                game_state = GAME_OVER
            else:
                score += 1
                ingredient_x = random.randint(0, width - ingredient_size)
                ingredient_y = 0
                ingredient_speed += 0.5
                ingredient_sprite = random.choice([ingredient_black, ingredient_red, ingredient_green, ingredient_orange, ingredient_evil])

        # Check if ingredient is out of bounds
        if ingredient_y > height:
            if ingredient_sprite != ingredient_evil:
                lives -= 1
                if lives == 0:
                    game_state = GAME_OVER
            ingredient_x = random.randint(0, width - ingredient_size)
            ingredient_y = 0
            ingredient_sprite = random.choice([ingredient_black, ingredient_red, ingredient_green, ingredient_orange, ingredient_evil])

    # Clear the screen
    screen.fill(WHITE)

    # Draw game states
    if game_state == PLAYING or game_state == PAUSED:
        score_text, lives_text = draw_playing_state(screen, player_sprite, player_x, player_y, ingredient_sprite, ingredient_x, ingredient_y, score, lives, font, width)
        if game_state == PAUSED:
            # Create a semi-transparent overlay
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 128))  # White with 50% opacity
            screen.blit(overlay, (0, 0))
            draw_paused_state(screen, font, width, height)
            # Redraw score and lives on top of the overlay
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (width - 120, 10))
    elif game_state == GAME_OVER:
        draw_game_over_state(screen, score, player_name, high_scores, font, width, height)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
