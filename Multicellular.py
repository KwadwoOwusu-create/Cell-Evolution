from typing import Dict, List, Tuple
import pygame, random
from Cells import Cells

class Multicellular:
    def __init__(self, num_cells: int) -> None:
        # Initialize the number of cells and cell ID counter
        self.num_cells = num_cells
        self.cell_id_counter = 0
        
        # Create a list of Cells objects, each with a unique ID
        self.cells: List[any] = [Cells(self.create_id()) for _ in range(self.num_cells)]
        
        # Create a dictionary to store cell generations (currently only first generation)
        self.cells_dict = {
            "First_Gen": self.cells
        }
        
    def create_id(self) -> str:
        '''Generates a unique ID for each cell'''
        self.cell_id_counter += 1  # Increment the ID counter
        return f'cell_id_{self.cell_id_counter}'  # Return a formatted ID string
    
    
    def cell_life(self, screen: any) -> None:
        '''Updates the state of each cell: draws, moves, checks health, and manages reproduction'''
        for cells in self.cells_dict.values():
            for cell in cells:
                cell.draw(screen)          # Draw the cell on the screen
                cell.movement()            # Update the cell's position based on movement logic
                cell.health_(cells)        # Check and update the health of the cell
                cell.reproduce()           # Handle reproduction logic for the cell
                
               
    def info(self, eventpos):
        '''Displays information about each cell if clicked'''
        for cells in self.cells_dict.values():
            for cell in cells:
                cell.information(eventpos)  # Call the information method of the cell to display details
