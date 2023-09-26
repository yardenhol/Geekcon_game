import pygame
import random
import math


# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


# Ball dimensions
BALL_RADIUS = 15

goal_entry_time = None  # Time when the ball entered the goal
no_goal = False  # Flag to determine if "NO GOAL :(" should be displayed

# Variables for ball movement
speed = 5  # Pixels per frame
target_position = None
no_goal_time = None
GAP = 50
dagamta = False


# Load the ball image and scale it
ball_image = pygame.image.load('/Users/holtzery/Downloads/ball.png')
ball_image = pygame.transform.scale(ball_image, (BALL_RADIUS*2, BALL_RADIUS*2))

# Load the cheering sound
cheering_sound = pygame.mixer.Sound('/Users/holtzery/Downloads/cheering.mp3')
booing_sound = pygame.mixer.Sound('/Users/holtzery/Downloads/boo.mp3')
background_image = pygame.image.load('/Users/holtzery/Downloads/soccer_court.png')
SCREEN_WIDTH, SCREEN_HEIGHT = background_image.get_size()

# Adjusting Goal dimensions and position
GOAL_WIDTH = int(0.5 * SCREEN_WIDTH)  # 50% of screen width
GOAL_HEIGHT = SCREEN_HEIGHT // 2

# Center the goal horizontally
GOAL_X = (SCREEN_WIDTH - GOAL_WIDTH) // 2

# Position the goal in the middle of the top half of the screen
GOAL_Y = (SCREEN_HEIGHT // 2 - GOAL_HEIGHT) // 2

# Load the goal image and scale it
goal_image = pygame.image.load('/Users/holtzery/Downloads/gate.png')
goal_image = pygame.transform.scale(goal_image, (GOAL_WIDTH, GOAL_HEIGHT))


# Goalkeeper properties
GOALKEEPER_WIDTH = 50
GOALKEEPER_HEIGHT = 100
GOALKEEPER_SPEED = 3
goalkeeper_position = [GOAL_X + (GOAL_WIDTH - GOALKEEPER_WIDTH) // 2, GOAL_Y + GOAL_HEIGHT - GOALKEEPER_HEIGHT]  # Start at the bottom-middle of the goal
goalkeeper_direction = 1  # 1 for right, -1 for left

# Load the goalkeeper image and scale it
goalkeeper_image = pygame.image.load('/Users/holtzery/Downloads/goalkeeper.png')
goalkeeper_image = pygame.transform.scale(goalkeeper_image, (GOALKEEPER_WIDTH, GOALKEEPER_HEIGHT))



def calculate_direction_vector(start, end):
    """Calculate the normalized direction vector from start to end."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = math.sqrt(dx**2 + dy**2)
    if distance == 0:
        return (0, 0)
    return (dx/distance, dy/distance)

def move_towards_target(current, target, speed):
    if current < target:
        return min(current + speed, target)
    elif current > target:
        return max(current - speed, target)
    return current

def ball_hits_goalkeeper(ball_position):
    ball_rect = pygame.Rect(ball_position[0] - BALL_RADIUS, ball_position[1] - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
    goalkeeper_rect = pygame.Rect(goalkeeper_position[0], goalkeeper_position[1], GOALKEEPER_WIDTH, GOALKEEPER_HEIGHT)
    return ball_rect.colliderect(goalkeeper_rect)

def data_to_key(angleX):
    if angleX < (-GAP):
        return 1
    elif angleX > GAP:
        return 3
    else: 
        return 2

# Set up the screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Soccer Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def draw_goal():
    screen.blit(goal_image, (GOAL_X, GOAL_Y))

def throw_ball(number):
    third_width = SCREEN_WIDTH // 3
    y_position = GOAL_Y + GOAL_HEIGHT // 2  # Middle of the goal vertically

    if number == 1:
        return (random.randint(0, third_width), y_position)
    elif number == 2:
        return (random.randint(third_width, 2 * third_width), y_position)
    elif number == 3:
        return (random.randint(2 * third_width, SCREEN_WIDTH), y_position)


def check_goal(ball_position):
    if GOAL_X <= ball_position[0] <= GOAL_X + GOAL_WIDTH and GOAL_Y <= ball_position[1] <= GOAL_Y + GOAL_HEIGHT:
        if ball_hits_goalkeeper(ball_position):  # Check if ball hits the goalkeeper
            return False  # No goal if ball hits the goalkeeper
        return True
    return False

running = True
initial_ball_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - BALL_RADIUS - 10)
ball_position = initial_ball_position
goal_scored = False

while running:
    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Update goalkeeper's position
    goalkeeper_position[0] += GOALKEEPER_SPEED * goalkeeper_direction

    # Change direction if the goalkeeper reaches the edges of the goal
    if goalkeeper_position[0] <= GOAL_X:
        goalkeeper_direction = 1
    elif goalkeeper_position[0] + GOALKEEPER_WIDTH >= GOAL_X + GOAL_WIDTH:
        goalkeeper_direction = -1

    # Draw the goal first
    draw_goal()

    # Draw the goalkeeper on top of the goal
    screen.blit(goalkeeper_image, (goalkeeper_position[0], goalkeeper_position[1]))

    # Move ball towards target in a straight line
    if target_position and ball_position != target_position:
        direction = calculate_direction_vector(ball_position, target_position)
        ball_position = (
            ball_position[0] + direction[0] * speed,
            ball_position[1] + direction[1] * speed
        )

        # Check if the ball hits the goalkeeper
        if ball_hits_goalkeeper(ball_position):
            booing_sound.play(maxtime=2000)  # Play the booing sound
            no_goal = True
            ball_position = initial_ball_position
            target_position = None  # Reset the target_position
            pygame.time.delay(2000)  # Delay for 2 seconds
            no_goal = False

        elif abs(ball_position[0] - target_position[0]) < speed and abs(ball_position[1] - target_position[1]) < speed:
            ball_position = target_position
            target_position = None  # Reset the target_position
            goal_scored = check_goal(ball_position)
            if goal_scored:
                cheering_sound.play(maxtime=2000)  # Play the cheering sound
                goal_entry_time = pygame.time.get_ticks()
            else:
                booing_sound.play(maxtime=2000)  # Play the booing sound
                no_goal = True
                screen.blit(ball_image, (ball_position[0] - BALL_RADIUS, ball_position[1] - BALL_RADIUS))  # Redraw the ball
                text = font.render("NO GOAL :(", True, RED)
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
                pygame.display.flip()
                pygame.time.delay(2000)  # Delay for 2 seconds
                ball_position = initial_ball_position
                no_goal = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.unicode == '0':  # Reset ball to starting position
                ball_position = initial_ball_position
                goal_scored = False
                goal_entry_time = None  # Reset the goal entry time
                no_goal = False  # Reset the no goal flag
                target_position = None
            elif event.unicode.isdigit() and 1 <= int(event.unicode) <= 3:
                target_position = throw_ball(int(event.unicode))

    # Check if 5 seconds have passed since the ball entered the goal
    if goal_entry_time and pygame.time.get_ticks() - goal_entry_time > 2000:  # 2000 milliseconds = 2 seconds
        ball_position = initial_ball_position
        goal_scored = False
        goal_entry_time = None
    
    # Check if 2 seconds have passed since the "NO GOAL" event
    if no_goal and no_goal_time and pygame.time.get_ticks() - no_goal_time > 2000:  # 2000 milliseconds = 2 seconds
        no_goal = False

    # Draw the ball image
    screen.blit(ball_image, (ball_position[0] - BALL_RADIUS, ball_position[1] - BALL_RADIUS))
    
    if goal_scored:
        text = font.render("GOAL!", True, RED)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    elif no_goal:
        text = font.render("NO GOAL :(", True, RED)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


