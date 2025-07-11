import random
import sys
import os
import pygame
from pygame.locals import *

# Print the current working directory (for asset loading help)
print("Current working directory:", os.getcwd())

# Game window dimensions
window_width = 600
window_height = 500

# Set height/width of window
window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
framepersecond = 30

# Image filenames
pipeimage = 'pipe.png'
background_image = 'background.jpg'
birdplayer_image = 'bird.png'
sealevel_image = 'base.jfif'

def flappygame():
    your_score = 0
    horizontal = int(window_width / 5)
    vertical = int(window_width / 2)
    ground = 0
    mytempheight = 100

    # Create two pipes
    first_pipe = createPipe()
    second_pipe = createPipe()

    down_pipes = [
        {'x': window_width + 300 - mytempheight, 'y': first_pipe[1]['y']},
        {'x': window_width + 300 - mytempheight + (window_width / 2), 'y': second_pipe[1]['y']},
    ]

    up_pipes = [
        {'x': window_width + 300 - mytempheight, 'y': first_pipe[0]['y']},
        {'x': window_width + 300 - mytempheight + (window_width / 2), 'y': second_pipe[0]['y']},
    ]

    pipeVelX = -4
    bird_velocity_y = -8
    bird_Max_Vel_Y = 10
    birdAccY = 1
    bird_flap_velocity = -6
    bird_flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True

        # Check for collision
        game_over = isGameOver(horizontal, vertical, up_pipes, down_pipes)
        if game_over:
            print("Game Over! Your score:", your_score)
            return

        # Score checking
        playerMidPos = horizontal + game_images['flappybird'].get_width() / 2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                your_score += 1
                print(f"Your score is {your_score}")

        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY
        if bird_flapped:
            bird_flapped = False

        playerHeight = game_images['flappybird'].get_height()
        vertical = vertical + min(bird_velocity_y, elevation - vertical - playerHeight)

        # Move pipes
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add new pipe
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])

        # Remove offscreen pipe
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)

        # Draw game
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0], (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1], (lowerPipe['x'], lowerPipe['y']))

        window.blit(game_images['sea_level'], (ground, elevation))
        window.blit(game_images['flappybird'], (horizontal, vertical))

        # Draw score
        numbers = [int(x) for x in list(str(your_score))]
        width = sum(game_images['scoreimages'][num].get_width() for num in numbers)
        Xoffset = (window_width - width) / 1.1
        for num in numbers:
            window.blit(game_images['scoreimages'][num], (Xoffset, window_width * 0.02))
            Xoffset += game_images['scoreimages'][num].get_width()

        pygame.display.update()
        framepersecond_clock.tick(framepersecond)

def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevation - 25 or vertical < 0:
        return True
    for pipe in up_pipes:
        pipeHeight = game_images['pipeimage'][0].get_height()
        if vertical < pipeHeight + pipe['y'] and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True
    for pipe in down_pipes:
        if vertical + game_images['flappybird'].get_height() > pipe['y'] and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True
    return False

def createPipe():
    offset = window_height / 3
    pipeHeight = game_images['pipeimage'][0].get_height()
    y2 = offset + random.randrange(0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [{'x': pipeX, 'y': -y1}, {'x': pipeX, 'y': y2}]
    return pipe

# Game start
if __name__ == "__main__":
    pygame.init()
    framepersecond_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Game')

    # Load images
    try:
        game_images['scoreimages'] = tuple(pygame.image.load(f"{i}.png").convert_alpha() for i in range(10))
        game_images['flappybird'] = pygame.image.load(birdplayer_image).convert_alpha()
        game_images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha()
        game_images['background'] = pygame.image.load(background_image).convert_alpha()
        pipe_img = pygame.image.load(pipeimage).convert_alpha()
        game_images['pipeimage'] = (pygame.transform.rotate(pipe_img, 180), pipe_img)
    except Exception as e:
        print("Error loading images:", e)
        sys.exit()

    print("WELCOME BACK TO FLAPPY BIRD")
    print("Press SPACE or UP to start the game")

    while True:
        horizontal = int(window_width / 5)
        vertical = int((window_height - game_images['flappybird'].get_height()) / 2)
        ground = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    flappygame()

            window.blit(game_images['background'], (0, 0))
            window.blit(game_images['flappybird'], (horizontal, vertical))
            window.blit(game_images['sea_level'], (ground, elevation))
            pygame.display.update()
            framepersecond_clock.tick(framepersecond)
