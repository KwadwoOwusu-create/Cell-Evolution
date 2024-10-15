import pygame, sys, random
from Multicellular import Multicellular
from Ecosystem import Ecosystem

# Initialize Pygame
pygame.init()

# Set the title of the game window
title = "evolution"
pygame.display.set_caption(title)

class Main:
    def __init__(self) -> None:
        # Initialize the display dimensions
        self.display_width: int = 800
        self.display_height: int = 600
        
        # Create the display surface
        self.screen = pygame.display.set_mode((self.display_width, self.display_height))
        
        # Set up the clock for managing frame rate
        self.clock: int = pygame.time.Clock()
        
        # Load font for displaying FPS
        self.font: str = pygame.font.Font("04B_30__.ttf", 10)
        
        # Render initial FPS text
        self.fps = self.font.render(str(int(self.clock.get_fps())), True, (255, 255, 255))
        
        # Initialize the multicellular system with 100 cells
        self.cells = Multicellular(100)
        
        # Create an ecosystem with the display screen
        self.ecosystem = Ecosystem(self.screen)
        
        # Variable to store the position of the mouse click
        self.x = None
    
    def run_weather(self):
        '''Checks weather conditions for each cell and applies effects'''
        for cell in self.cells.cells_dict.values():
            for cell in cell:
                # Update the weather effects on each cell
                self.ecosystem.weather(cell.cell, cell)
                
    def main(self) -> None:
        '''Main game loop'''
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quit the game if the window is closed
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # When the mouse is clicked, mark the cell as clicked
                    for cells in self.cells.cells_dict.values():
                        for cell in cells:
                            cell.click = True
                    
                    # Store the position of the mouse click
                    self.x = event.pos

            # Fill the screen with the ecosystem grid
            self.ecosystem.type(1)
            self.run_weather()  # Check and apply weather conditions

            # Render the current FPS at the top left corner
            self.screen.blit(self.fps, (10, 10))
            
            # Handle the cell behavior and rendering
            self.cells.cell_life(self.screen)
            self.cells.info(self.x)  # Display cell information based on mouse click
            
            # Update the display
            pygame.display.update()
            
            # Control the frame rate to run at 60 FPS
            self.clock.tick(60)
            # Update the FPS text for rendering
            self.fps = self.font.render(str(int(self.clock.get_fps())), True, (255, 255, 255))
            

# Entry point of the program
if __name__ == "__main__":
    main = Main()  # Create an instance of the Main class
    main.main()    # Start the main game loop
