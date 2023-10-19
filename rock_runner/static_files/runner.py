"""Rock Runner: a game where you run from rocks and torches."""

import pygame, sys, random 
from pygame.locals import *
from pathlib import Path

# Screen constants.
WINDOWWIDTH = 1200
WINDOWHEIGHT = 900
CENTERX = WINDOWWIDTH / 2
CENTERY = WINDOWHEIGHT / 2
CENTER = (CENTERX, CENTERY)

# Game constants.
FPS = 60
MOVESPEED = 9
ROCKSIZE = [150, 150]
ROCKSTARTSPEED = 7
ROCKFRAMESTARTTHRESH = 60
TORCHSPEED = 20

# Start offsets.
CATACLYSM = 0.0
BLOODBATH = 80.1
AFTERMATH = 195.6

# Color constants.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARKGRAY = (40, 40, 40)
RED = (255, 0, 0)
DARKRED = (100, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 100, 0)
BLUE = (0, 0, 255)
DARKBLUE = (0, 0, 100)
YELLOW = (255, 255, 0)
DARKYELLOW = (100, 100, 0)
PURPLE = (255, 0, 255)
DARKPURPLE = (100, 0, 100)
BGCOLOR = WHITE
TITLECOLOR = WHITE


def main():
    """The main game code."""
    global DISPLAYSURF, main_clock, MAINFONT

    # Initialize pygame and set up a clock.
    pygame.init()
    main_clock = pygame.time.Clock()

    # Set up the game window.
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Rock Runner")

    # Load the in-game font.
    MAINFONT = create_font(40)

    # Load in the assets.
    load_sprites()

    # Run the title screen, and then the main game loop.
    song_offset = title_screen()
    while True:
        score = run_game(song_offset)
        song_offset = run_game_over(score, song_offset)


def title_screen():
    """Run the game's title screen."""

    # Define the song offsets. Cataclysm is default.
    song_offset = CATACLYSM
    color_1 = RED
    color_2 = BLACK 
    color_3 = BLACK

    # Create the title screen fonts.
    title_font = create_font(100)
    dev_font = create_font(75)
    song_font = create_font(55)

    # Create the title screen text.
    title_text = title_font.render("Rock Runner", None, BLACK)
    dev_text = dev_font.render("By: Omega_XK", None, BLACK)
    song_text = song_font.render('Song Offset (press the key)', None, BLACK)

    # Create the title screen text rects.
    song_rect = song_text.get_rect()
    song_rect.center = CENTERX, CENTERY + 250
    dev_rect = dev_text.get_rect()
    dev_rect.center = CENTERX, CENTERY - 200
    title_rect = title_text.get_rect()
    title_rect.center = CENTERX, CENTERY - 300

    # Create the start button.
    start_button = pygame.Rect(0, 0, 300, 100)
    start_button.center = CENTERX, CENTERY - 65

    # Create the text that goes on the start button.
    start_button_font = create_font(85)
    start_text = start_button_font.render("Start", None, RED)
    start_rect = start_text.get_rect()
    start_rect.center = start_button.center

    # Load the instructions text.
    path = Path('game_data/instructions.txt')
    instructions = path.read_text()
    instruc_font = create_font(30)

    # Run the title screen loop.
    while True:
        # Check for events.
        for event in pygame.event.get():
            # Check for quit.
            if event.type == QUIT:
                terminate()

            # Check for key press.
            if event.type == KEYDOWN:
                # Check for escape key.
                if event.key == K_ESCAPE:
                    terminate()

                # Check for numbers to determine start offset.
                if event.key == K_1:
                    song_offset = CATACLYSM
                    color_1 = RED 
                    color_2 = BLACK 
                    color_3 = BLACK

                if event.key == K_2:
                    song_offset = BLOODBATH
                    color_1 = BLACK 
                    color_2 = RED 
                    color_3 = BLACK

                if event.key == K_3:
                    song_offset = AFTERMATH
                    color_1 = BLACK 
                    color_2 = BLACK 
                    color_3 = RED

            # Check for mouse click.
            if event.type == MOUSEBUTTONUP:
                # Check if the mouse is touching the start button.
                if start_button.collidepoint(event.pos):
                    # Start the game.
                    return song_offset
    
        # Draw the title screen.
        DISPLAYSURF.fill(TITLECOLOR)

        # Draw the title and dev text.
        DISPLAYSURF.blit(title_text, title_rect)
        DISPLAYSURF.blit(dev_text, dev_rect)

        # Draw the start button.
        pygame.draw.rect(DISPLAYSURF, BLACK, start_button)

        # Draw the start button text.
        DISPLAYSURF.blit(start_text, start_rect)

        # Draw the instructions text.
        y = CENTERY + 50
        for line in instructions.splitlines():
            instruc_surf = instruc_font.render(line, False, BLACK)
            instruc_rect = instruc_surf.get_rect()
            instruc_rect.center = (CENTERX, y)
            DISPLAYSURF.blit(instruc_surf, instruc_rect)
            y += 30

        # Draw the start offsets text.
        DISPLAYSURF.blit(song_text, song_rect)
        draw_song_offsets(color_1, color_2, color_3)

        # Update the title screen.
        pygame.display.update()
        main_clock.tick(FPS)


def draw_song_offsets(color_1, color_2, color_3):
    """Draw text displaying the song offset options."""
    font = create_font(40)
    
    # Generate surfacce objects.
    cataclysm = font.render('1: Cataclysm', False, color_1)
    bloodbath = font.render('2: Bloodbath', False, color_2)
    aftermath = font.render('3: Aftermath', False, color_3)

    # Generate rect objects.
    cataclysm_rect = cataclysm.get_rect()
    bloodbath_rect = bloodbath.get_rect()
    aftermath_rect = aftermath.get_rect()

    # Position rect objects.
    cataclysm_rect.midleft = 70, WINDOWHEIGHT - 130
    bloodbath_rect.center = CENTERX, WINDOWHEIGHT - 130
    aftermath_rect.midright = WINDOWWIDTH - 70, WINDOWHEIGHT - 130

    # Blit the text.
    DISPLAYSURF.blit(cataclysm, cataclysm_rect)
    DISPLAYSURF.blit(bloodbath, bloodbath_rect)
    DISPLAYSURF.blit(aftermath, aftermath_rect)


def run_game(music_offset):
    """Run the game's code and return when the player loses."""
    global rock_frame, rock_frame_thresh, all_rocks, level, game_over
    global rock_speed, torch_frame, torch_frame_thresh

    # Define game variables.
    game_over = False
    score = 0
    level = 1
    right = left = False
    torch_frame = 0
    torch_frame_thresh = 500

    rock_frame_thresh = ROCKFRAMESTARTTHRESH
    rock_frame = 0
    rock_speed = ROCKSTARTSPEED
    all_rocks = []

    # Reset the player's position to the bottom of the screen.
    player_rect.center = (CENTERX, WINDOWHEIGHT - player_rect.height)

    # Start the music.
    pygame.mixer.music.load("sounds/at_the_speed_of_light.mp3")
    pygame.mixer.music.play(-1, music_offset)

    # Game running loop.
    while not game_over:
        for event in pygame.event.get(): # Handle events.
            # Check for quit.
            if event.type == QUIT:
                terminate()

            # Check if the player is pressing a key.
            if event.type == KEYDOWN:
                # Check if the player is pressing the escape key.
                if event.key == K_ESCAPE:
                    terminate()

                # Check if the player is pressing an arrow key or WASD.
                if event.key in (K_LEFT, K_a):
                    right = False
                    left = True
                elif event.key in (K_RIGHT, K_d):
                    left = False
                    right = True

            # Check if the player has released a key.
            if event.type == KEYUP:
                # Check for arrow keys or WASD.
                if event.key in (K_LEFT, K_a):
                    left = False 
                elif event.key in (K_RIGHT, K_d):
                    right = False 

        # Draw the game.
        DISPLAYSURF.fill(BGCOLOR)

        # Update score.
        score += 1

        # Draw the text.
        draw_score(score)
        draw_level(level)
        draw_pb()

        # Update the rocks.
        handle_rock_spawning(score)
        update_rocks()

        # Update the torches.
        torch_frame += 1
        spawn_torch()

        # Update the player.
        update_player(right, left)
        DISPLAYSURF.blit(player, player_rect)

        # Update the game.
        pygame.display.update()
        main_clock.tick(FPS)

    return score


def draw_pb():
    """Draw text displaying the player's current pb."""

    # Load in the current pb.
    path = Path('game_data/personal_best.txt')
    pb = path.read_text()

    # Draw the text.
    pb_surf = MAINFONT.render(f"Best Score: {pb}", False, BLACK)
    pb_rect = pb_surf.get_rect()
    pb_rect.midtop = (CENTERX, 5)
    DISPLAYSURF.blit(pb_surf, pb_rect)


def spawn_torch():
    "Spawn torches every 5 seconds."
    global torch_frame, all_rocks
    
    if torch_frame >= torch_frame_thresh:
        torch_frame = 0

        # Spawn the torch and put it in the rocks list so the rock loop
        #  spawns the torch. Torch is true.
        new_torch_rect = torch.get_rect()
        new_torch_rect.midtop = (player_rect.x, 0)
        new_torch = {'img': torch, 'rect': new_torch_rect, 'torch': True}
        all_rocks.append(new_torch)


def draw_score(score):
    textobj = MAINFONT.render(f'Score: {score}', None, BLACK)
    textrect = textobj.get_rect()
    textrect.topleft = (0, 5)
    DISPLAYSURF.blit(textobj, textrect)


def draw_level(level):
    textobj = MAINFONT.render(f'Level: {level}', None, BLACK)
    textrect = textobj.get_rect()
    textrect.topright = (WINDOWWIDTH - 20, 5)
    DISPLAYSURF.blit(textobj, textrect)


def handle_rock_spawning(current_score):
    """If a rock can spawn, then spawn a rock."""
    global rock_frame, rock_frame_thresh, rock_speed, level, torch_frame_thresh

    # Check if the speed of the rocks need to change.
    if current_score >= 500:
        rock_frame_thresh = 45
        rock_speed = 10
        level = 2

    if current_score >= 1500:
        rock_frame_thresh = 38
        rock_speed = 12
        level = 3
        torch_frame_thresh = 300

    if current_score >= 3000:
        rock_frame_thresh = 30
        rock_speed = 14
        level = 4

    if current_score >= 5000:
        rock_frame_thresh = 20
        rock_speed = 18
        level = 5

    # Check if it's time to spawn a new rock.
    if rock_frame >= rock_frame_thresh:
        rock_frame = 0
        spawn_rock()
    else:
        rock_frame += 1


def spawn_rock():
    """Create a new rock."""
    global all_rocks

    # Define all of the new rock's attributes.
    new_rock_img = pygame.transform.scale(rock, (ROCKSIZE[0], ROCKSIZE[1]))
    new_rock_x = random.randint(0, WINDOWWIDTH - new_rock_img.get_width())
    new_rock_rect = new_rock_img.get_rect()
    new_rock_rect.topleft = (new_rock_x, 0)

    # Add the new rock to all_rocks. Torch is false because this rock.
    new_rock = {'img': new_rock_img, 'rect': new_rock_rect, 'torch': False}
    all_rocks.append(new_rock)


def update_rocks():
    """Update all of the rocks and display them."""
    global all_rocks, game_over

    # Loop through every rock.
    for rock in all_rocks[:]:
        # Move the rock down.
        if rock['torch']:
            # This is a torch, so move it very fast.
            rock['rect'].y += TORCHSPEED
        else:
            # This is a rock, so move it at rock_speed.
            rock['rect'].y += rock_speed

        # Check if the rock hit the ground.
        if rock['rect'].y >= WINDOWHEIGHT - rock['rect'].height:
            all_rocks.remove(rock)
            
        # Check if the rock hits the player.
        if rock['rect'].colliderect(player_rect):
            game_over = True 
            return
        
        # Display the rock.
        DISPLAYSURF.blit(rock['img'], rock['rect'])


def update_player(right, left):
    """Update the player's position."""
    if right and player_rect.x < WINDOWWIDTH - player_rect.width:
        player_rect.x += MOVESPEED
    elif left and player_rect.x > 0:
        player_rect.x -= MOVESPEED


def run_game_over(score, default):
    """Run the game's game over screen."""

    # Stop the music.
    pygame.mixer.music.stop()

    # Define the song offsets. Default is what the player had before.
    song_offset = default

    # Make sure the text is the right color.
    if default == CATACLYSM:
        color_1 = RED
        color_2 = BLACK 
        color_3 = BLACK
    elif default == BLOODBATH:
        color_1 = BLACK 
        color_2 = RED 
        color_3 = BLACK
    elif default == AFTERMATH:
        color_1 = BLACK 
        color_2 = BLACK 
        color_3 = RED

    # Create the game over fonts.
    big_font = create_font(150)
    small_font = create_font(70)
    song_font = create_font(55)

    # Create the game over text.
    game_surf = big_font.render("Game Over", False, BLACK)
    game_rect = game_surf.get_rect()
    game_rect.center = CENTERX, CENTERY - 200

    score_surf = small_font.render(f"Your score was {score}!", False, BLACK)
    score_rect = score_surf.get_rect()
    score_rect.center = CENTERX, CENTERY - 50

    song_surf = song_font.render(f"Song Offset (press the key)", False, BLACK)
    song_rect = song_surf.get_rect()
    song_rect.center = CENTERX, CENTERY + 250

    # Create the restart button.
    restart_button = pygame.Rect(0, 0, 300, 100)
    restart_button.center = CENTERX, CENTERY + 100

    # Create the restart text.
    restart_surf = small_font.render('Restart', False, RED)
    restart_rect = restart_surf.get_rect()
    restart_rect.center = restart_button.center

    # See if the player has gotten a new best score.
    check_new_pb(score)

    # Run the game over loop.
    while True:
        # Check for events.
        for event in pygame.event.get():
            # Check for quit.
            if event.type == QUIT:
                terminate()

            # Check for key press.
            if event.type == KEYDOWN:
                # Check for escape.
                if event.key == K_ESCAPE:
                    terminate()

                # Check for number keys for start offset
                if event.key == K_1:
                    song_offset = CATACLYSM
                    color_1 = RED 
                    color_2 = BLACK 
                    color_3 = BLACK

                if event.key == K_2:
                    song_offset = BLOODBATH
                    color_1 = BLACK 
                    color_2 = RED 
                    color_3 = BLACK

                if event.key == K_3:
                    song_offset = AFTERMATH
                    color_1 = BLACK 
                    color_2 = BLACK 
                    color_3 = RED

            # Check for mouse press.
            if event.type == MOUSEBUTTONUP:
                # Check if mouse is touching the restart button.
                if restart_button.collidepoint(event.pos):
                    # Restart the game.
                    return song_offset

        # Draw the background.
        DISPLAYSURF.fill(WHITE)

        # Draw the restart button.
        pygame.draw.rect(DISPLAYSURF, BLACK, restart_button)

        # Draw the text.
        DISPLAYSURF.blit(game_surf, game_rect)
        DISPLAYSURF.blit(restart_surf, restart_rect)
        DISPLAYSURF.blit(score_surf, score_rect)
        DISPLAYSURF.blit(song_surf, song_rect)
        draw_song_offsets(color_1, color_2, color_3)

        # Update the game over screen.
        pygame.display.update()
        main_clock.tick(FPS)


def check_new_pb(new_score):
    """Figure out if the player got a new pb and manage the file."""

    # Load the old pb as an integer.
    path = Path('game_data/personal_best.txt')
    old_pb = int(path.read_text())

    # Compare the new score and pb.
    if new_score > old_pb:
        path.write_text(str(new_score))


def load_sprites():
    """Load in the game's sprites."""
    global player, player_rect, rock, torch
    
    # Load player, and get its rect.
    player = pygame.image.load("images/player.png")
    player_rect = player.get_rect()

    # Load in the rock image.
    rock = pygame.image.load("images/rock.png")

    # Load in the torch image.
    torch = pygame.image.load("images/torch.jpeg")


def create_font(size):
    """Return a default pygame font object with the correct size."""
    return pygame.font.Font('freesansbold.ttf', size)


def terminate():
    """Quit out of the game."""
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()