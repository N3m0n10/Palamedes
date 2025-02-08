import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Ball properties
ball_radius = 10
ball_x = width // 2
ball_y = height // 2
ball_dx = 5  # Initial x velocity
ball_dy = 3  # Initial y velocity

# Paddle properties
paddle_width = 10
paddle_height = 100
paddle_y = height // 2 - paddle_height // 2
paddle_x = 20  # Left paddle x-position
paddle_speed = 5

# enemy paddle properties
enemy_paddle_width = 10
enemy_paddle_height = 100
enemy_paddle_y = height // 2 - enemy_paddle_height // 2
enemy_paddle_x = width - 30  # Right paddle x-position

# Game variables
player_life = 3
opponent_life = 3
winner = None

# Function to predict ball's y position at paddle's x
def predict_ball_y(ball_x, ball_y, ball_dx, ball_dy, paddle_x):
    if ball_dx == 0:  # Avoid division by zero
        return ball_y  # Ball won't move horizontally

    time_to_paddle = (paddle_x - ball_x) / ball_dx

    if time_to_paddle < 0 and ball_dx > 0: #Ball is going to the right side of the screen
        return None #Ignore, we don't want to calculate it
    elif time_to_paddle < 0 and ball_dx < 0: #Ball is going to the left side of the screen
        return None #Ignore, we don't want to calculate it
    
    predicted_y = ball_y + ball_dy * time_to_paddle

    return predicted_y


# Game loop
running = True
menu = True
ending = False
game = False
while running:
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    menu = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game = True
                        menu = False
            
            screen.fill(black)
            font = pygame.font.Font(None, 36)
            text = font.render("Press SPACE to start the game", True, white)
            text_rect = text.get_rect(center=(width // 2, height // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                    running = False

            # Paddle movement (example - you'll need to control this)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and enemy_paddle_y > 0:
                enemy_paddle_y -= paddle_speed
            if keys[pygame.K_DOWN] and enemy_paddle_y < height - paddle_height:
                enemy_paddle_y += paddle_speed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and paddle_y > 0:
                paddle_y -= paddle_speed
            if keys[pygame.K_s] and paddle_y < height - paddle_height:
                paddle_y += paddle_speed

            # Ball movement
            ball_x += ball_dx
            ball_y += ball_dy

            # Ball collision with walls (top and bottom)
            if ball_y <= 0 or ball_y >= height - ball_radius * 2:
                ball_dy *= -1

            # Ball collision with paddles (simplified)
            if ball_x <= paddle_x + paddle_width and ball_y + ball_radius * 2 >= paddle_y and ball_y <= paddle_y + paddle_height:
                ball_dx *= -1  # Reverse x direction
                # Add some spin based on where the ball hits the paddle (optional)
                ball_dy += (ball_y - (paddle_y + paddle_height // 2)) // 10  # Example spin

            if ball_x >= enemy_paddle_x - paddle_width and ball_y + ball_radius * 2 >= enemy_paddle_y and ball_y <= enemy_paddle_y + enemy_paddle_height:
                ball_dx *= -1  # Reverse x direction
                # Add some spin based on where the ball hits the paddle (optional)
                ball_dy += (ball_y - (enemy_paddle_y + enemy_paddle_height // 2)) // 10  # Example spin 

            # Ball goes off-screen (game over - reset or handle as needed)
            if ball_x <= 0:
                if player_life == 0:
                    game = False
                    ending = True
                ball_x = width // 2
                ball_y = height // 2
                ball_dx *= -1 #Invert the direction of the ball
                player_life -= 1
                winner = "PLAYER 1"
                # Reset other game state if needed
            
            if ball_x >= width:
                if opponent_life == 0:
                    game = False
                    ending = True
                ball_x = width // 2
                ball_y = height // 2
                ball_dx *= -1 
                opponent_life -= 1
                winner = "PLAYER 2"
            # Prediction
            predicted_y = predict_ball_y(ball_x, ball_y, ball_dx, ball_dy, paddle_x)

            # Draw everything
            screen.fill(black)
            pygame.draw.circle(screen, white, (ball_x + ball_radius, ball_y + ball_radius), ball_radius)
            pygame.draw.rect(screen, white, (paddle_x, paddle_y, paddle_width, paddle_height))
            pygame.draw.rect(screen, white, (enemy_paddle_x,   enemy_paddle_y, paddle_width, paddle_height))

            #Draw the predicted position
            if predicted_y is not None:
                pygame.draw.circle(screen, (255,0,0), (paddle_x, int(predicted_y) + ball_radius) , ball_radius // 4)

            pygame.display.flip()

            # Control frame rate (adjust as needed)
            clock = pygame.time.Clock()
            clock.tick(60) # 60 frames per second

        while ending:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    ending = False
                elif event.type == pygame.KEYDOWN:
                    player_life = 3
                    opponent_life = 3
                    winner = None
                    if event.key == pygame.K_SPACE:
                        game = True
                        ending = False
                        ball_dy = 3
                    if event.key == pygame.K_BACKSPACE:
                        menu = True
                        ending = False
                        ball_dy = 3
            screen.fill(black)
            font = pygame.font.Font(None, 36)
            text = font.render("Press SPACE to start the game", True, white)
            text_ln_2 = font.render("Press BACKSPACE to go back to the menu", True, white)
            text_ln_3 = font.render(f"{winner} WON", True, white)
            text_rect = text.get_rect(center=(width // 2, height // 2))
            text_ln_2_rect = text.get_rect(center=(width // 2, height // 2 +20))
            screen.blit(text, text_rect)
            screen.blit(text_ln_2, text_ln_2_rect)
            pygame.display.flip()
            clock = pygame.time.Clock()
            clock.tick(20)

pygame.quit()