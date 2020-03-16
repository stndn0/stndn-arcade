# Launch window of desired width x height, set window name
pygame.init()
screen_width = 800
screen_height = 600
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")

# Rectangle Dimension and centered position
width = 64
height = 64
x = (screen_width // 2) - width // 2        # 376
y = (screen_height // 2) - height // 2      # 276