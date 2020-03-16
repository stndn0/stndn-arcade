import sys, pygame, random, time

# https://www.pythoncentral.io/pythons-time-sleep-pause-wait-sleep-stop-your-code/

# Application setup and game information
time_paused = 0
pygame.init()
start_time = time.time()
screen_width = 800
screen_height = 600
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Reaction Lab")

# Colors (RGB)
white = (255,255,255)
black = (0,0,0)

# Store game data
running = True
score = 0
font = pygame.font.SysFont('arial', 24)


# Setup initial rectangle
width = 64
height = 64
rand_x = (screen_width // 2) - width // 2        # 376
rand_y = (screen_height // 2) - height // 2      # 276


def refreshScreen(update_time = None):
    """
    Function that redraws the display with updated game data
    """
    window.fill(black)
    
    print("BEFORE: ", running_time - start_time)
    print("PAUSED: ", time_paused)
    total_time = round( (running_time - start_time) - time_paused, 2)
    print(f"AFTER: {total_time}")

    
    # Redraw score, time and feedback
    text = font.render("Score: " + str(score), True, white) 
    text2 = font.render("Time: " + str(total_time), True, white)
    window.blit(text, [(screen_width // 2) - width // 2,0])
    window.blit(text2, [0,0])

    # Redraw objects on the screen
    pygame.draw.rect(window, white, (rand_x, rand_y, width, height))
    
    
def pause():
    global time_paused
    paused = True
    paused_time_start = time.time() 
     
    while paused:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                paused_time_end = time.time()
                time_paused = time_paused + (paused_time_end - paused_time_start)
                #print("Time Paused:", time_paused)
                paused = False

                            
# Establish the main game loop
while running:    
    pygame.time.delay(50)
    running_time = time.time()
    
    for event in pygame.event.get():  
        # Track if user wants to quit
        if event.type == pygame.QUIT:
            running = False
               
        # Track mouse position and button
        mouse_pos = pygame.mouse.get_pos()       
        if pygame.mouse.get_pressed() == (1,0,0):
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If user sucessfully targeted object
                if mouse_pos[0] >= rand_x - width//10 and mouse_pos[0] <= rand_x + width and mouse_pos[1] >= rand_y - height//10 and mouse_pos[1] <= rand_y + height: 
                    # Increment score
                    score += 1
                    
                    # Randomise object position for next refresh
                    rand_x = random.randrange(250, 650, 65)
                    rand_y = random.randrange(250, 550, 60)
                    height = random.randrange(48, 64, 12)
                    width = random.randrange(48, 64, 8)
            
                # Otherwise, manually reset score, time and obj position
                else:
                    score = 0
                    start_time = time.time()
                    rand_x = (screen_width // 2) - width // 2 
                    rand_y = (screen_height // 2) - height // 2
        
        # Pause game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            pause()
   
    # Draw and Refresh Game (display is constantly refreshed)
    refreshScreen()
    pygame.display.update()
    
# Quit
pygame.quit()