import sys, pygame, random, time

# Application setup and game information
pygame.init()
screen_width = 800
screen_height = 600
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Reaction Lab by stndn")
bg_img = pygame.image.load('bg.png')
font = pygame.font.Font('8-Bit Madness.ttf', 24)            # or use font.sysfont for default Windows fonts

# Colors (RGB)
white = (255,255,255)
black = (0,0,0)
yellow = (255,255,0)
custom = (245,245,220)

# Store game data
start_time = time.time()
running = True
eliminated = True
score = 0
time_paused = 0
react_time_start = 0
react_time = 0
feedback = ['Mediocre', 'Good', 'Great', 'Legendary']

# Setup initial rectangle target
colour = yellow
width = 116
height = 116
rand_x = (screen_width // 2) - width // 2        
rand_y = (screen_height // 2) - height // 2      


def drawText(str, position):
    """ (str, [x][y]) -> draw on screen at x,y
    
    Function that draws text to the screen via str and position parameters.
    """
    
    # Assign text contents and position
    text = font.render(str, True, white)
    text_surface = text
    text_rect = text.get_rect()
    text_rect.x = position[0]
    text_rect.y = position[1]
    
    # Draw to screen at specified position
    window.blit(text_surface, text_rect)
    
  
def drawScreen():
    """
    Function that redraws the display with updated game data pertaining to score, time,
    and the placement of objects on the screen.
    """
    
    global react_time_start, eliminated
    
    # Create a blank canvas every frame. 
    window.fill(black)
    window.blit(bg_img, (0,0))
    
    # Compute the total running time for the game
    total_time = round((running_time - start_time) - time_paused, 2)
    total_time = '{0:.2f}'.format(total_time)
    
    # Redraw score, time and reaction time
    drawText("Reaction Time: " +str(react_time) +" ms", [0, 0])
    drawText("Score: " +str(score), [365, 0])
    drawText("Time: " +str(total_time), [670, 0])

    # Redraw target on the screen
    pygame.draw.rect(window, colour, (rand_x, rand_y, width, height))
    
    # Track the amount of time the target is on the screen before being eliminated.
    if eliminated == True:                      # If target has been eliminated...
        react_time_start = time.time()          # ...restart the timer
        eliminated = False                     


def pause():
    """
    Function that pauses the game and 'stops' time for the duration of the pause.
    
    Must use global keyword to refer to the global variable time_paused, else python will create 
    a local variable for time_paused which will result in UnboundLocalError.
    """
    
    global time_paused
    paused = True
    paused_time_start = time.time() 

    while paused:
        drawText("PAUSED!", [360, 500] )
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    time_paused = time_paused + (time.time() - paused_time_start)
                    paused = False



# Establish the main game loop
while running:    
    pygame.time.delay(5)
    running_time = time.time()
           
    for event in pygame.event.get():  
        # Track if user wants to quit
        if event.type == pygame.QUIT:
            running = False
            
        # Track if user wants to pause the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause()

        # Track cursor position and mouse button (LMB)
        mouse_pos = pygame.mouse.get_pos()       
        if pygame.mouse.get_pressed() == (1,0,0):
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                # Check if the mouse cursor is hovering over the target (I forgot why this works but it works....)
                if mouse_pos[0] >= rand_x - width//10 and mouse_pos[0] <= rand_x + width and mouse_pos[1] >= rand_y - height//10 and mouse_pos[1] <= rand_y + height:   
                
                    # If so, increment score and update reaction time
                    score += 1
                    eliminated = True
                    react_time = str(round((time.time() - react_time_start), 3))
                    
                    # If the users reaction time is greater than 999ms, then set react_time to '999' because we won't display anything higher.
                    if float(react_time) <= 0.999:
                        react_time = react_time[2 : len(react_time) : 1]    # remove decimals. E.g. '0.500' is converted to '500'.
                    else:
                        react_time = 999
                    
                    # Determine feedback based on reaction time (in ms)
                    if int(react_time) >= 500:
                        print(feedback[0])
                    elif int(react_time) > 350 and int(react_time) < 500:
                        print(feedback[1])
                    elif int(react_time) > 250 and int(react_time) <= 350:
                        print(feedback[2])
                    elif int(react_time) <= 250:
                        print(feedback[3])

                    # Randomise new target position for next refresh
                    rand_x = random.randrange(250, 650, 65)
                    rand_y = random.randrange(200, 500, 50)
            
                # If user misclicked, manually reset score and time. Reset target to center position 
                else:
                    eliminated = True
                    score = 0
                    time_paused = 0
                    start_time = time.time()
                    react_time = 0
                    rand_x = (screen_width // 2) - width // 2       # Center Position
                    rand_y = (screen_height // 2) - height // 2     # Center Position
        
    # Draw and refresh game every cycle
    drawScreen()
    pygame.display.update()
    
pygame.quit()