import pygame, random

class Ecosystem:
    
    def __init__(self, screen) -> None:
        # Initialize the Ecosystem with a given screen for rendering
        self.screen = screen
        
        # Color is initialized to None (used for grid coloring later)
        self.color = None
        
        # Define the area of the weather zone within the ecosystem
        self.weather_zone = pygame.Rect(0, 0, 800, 600)
        
        # Initialize weather condition (will be set randomly later)
        self.weather_condition = None
        
    def type(self, type):
        '''Sets the type of ecosystem based on the input type'''
        if type == 1:
            # If type is 1, create a grid with specified dimensions
            #TODO: add more types later on
            self.grid(70, 12)
        
    def grid(self, grid_size, square_size) -> None:
        '''Draws a grid on the screen with alternating colors'''
        for i in range(grid_size):
            for j in range(grid_size):
                # Determine the color based on the sum of the row and column indices
                if (i + j) % 2 == 0:
                    self.color = (80, 63, 68)  # Darker color for even indices
                else:
                    self.color = (85, 67, 72)   # Lighter color for odd indices

                # Draw the square on the screen at calculated position
                pygame.draw.rect(self.screen, self.color, [square_size * i, square_size * j, square_size, square_size])
    
    def set_weather(self, x, y, w, h):
        '''Sets the dimensions and position of the weather zone'''
        self.weather_zone = pygame.Rect(x, y, w, h)
        
    def weather(self, cell_rect, cell):
        '''Determines weather conditions and applies effects to the cell based on weather'''
        # Randomly choose a weather condition (1 for hot, 2 for cold)
        weather_type = random.randint(1, 2)
        
        # Assign the weather condition based on the random choice
        if weather_type == 1:
            self.weather_condition = "hot"  # Set condition to hot
        elif weather_type == 2:
            self.weather_condition = "cold"  # Set condition to cold
        
        # Set the position and size of the weather zone
        self.set_weather(200, 200, 300, 300)
           
        # Check if the cell's rectangle collides with the weather zone
        if self.weather_zone.colliderect(cell_rect):
            # If the weather is hot, decrease the cell's health
            if self.weather_condition == "hot":
                cell.health -= 1  # Reduce health in hot weather
            # If the weather is cold, adjust the cell's speed and health
            elif self.weather_condition == "cold":
                cell.speed -= 0.1  # Decrease speed in cold weather
                # Ensure speed does not go below 0
                if cell.speed < 0:
                    cell.speed = 0
                cell.health -= 1  # Reduce health in cold weather
