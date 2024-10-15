import pygame, random

class Cells:
    def __init__(self, cell_id):
        # Initialize the cell with a unique ID
        self.cell_id: int = cell_id
        
        # Assign a random color to the cell
        self.color: Tuple = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        # Define the cell size and starting position (within window bounds)
        self.size: int = 10
        self.x: int = random.randint(0 + self.size, 800 - self.size)
        self.y: int = random.randint(0 + self.size, 600 - self.size)
        
        # Define a random movement direction and normalize it to prevent erratic movement
        self.direction: Tuple = pygame.math.Vector2(random.uniform(1, -1), random.uniform(1, -1)).normalize()
        
        # Assign a random speed between 1 and 10
        self.speed = random.uniform(1, 10)
        
        # Create a rectangular representation of the cell for drawing
        self.cell: any = pygame.Rect(self.x, self.y, self.size, self.size)
        
        # Initialize age, health, and mutation chance of the cell
        self.age = 0
        self.health = 100
        
        # Generate the DNA of the cell, defined by a string of genes
        self.dna = self.generate_dna("TtPpAaGg", 4, 4)
        
        # Convert the DNA into a vector for easier interpretation later
        self.dna_vector = self.dna_to_vector(self.dna)
        
        # Set a 10% chance for DNA mutation
        self.mutation_chance = 0.10
        
        # List to store children of this cell (upon reproduction)
        self.cell_children = []
        
        # A flag to control reproduction (0 means it can't reproduce)
        self.can_reproduce = 0
        
        # Click detection for interaction
        self.click = False
        
        
    def draw(self, screen: any) -> None:
        '''Renders the cell as a rectangle on the screen'''
        pygame.draw.rect(screen, self.color, self.cell)
        
    def simple_hash(self) -> int:
        '''Creates a hash value from a cell ID to ensure each cell's DNA is unique'''
        hash_value = 0
        for char in self.cell_id:
            # Multiply by a prime number to reduce hash collisions
            hash_value = hash_value * 31 + ord(char)
        # Return a positive integer hash value within 32-bit range
        return hash_value % (2**32)
    
    
    def generate_dna(self, gene: str, gene_length: int, genome_length: int) -> list[list]:
        '''Generates a DNA sequence based on gene string'''
        # Create a random seed based on the cell ID to ensure unique DNA
        seed = self.simple_hash()
        random.seed(seed)
        
        # Generate a list of gene_length sequences of length genome_length
        return [[random.choice(gene) for _ in range(genome_length)] for _ in range(gene_length)]
    

    def gene_meaning(self, gene: str) -> None:
        '''Interprets the meaning of DNA and applies traits (speed, size, health, mutation chance)'''
        for gene in self.dna:
            if "T" in gene:
                self.speed += 1
            if "t" in gene:
                self.speed += 0.5
            if "P" in gene:
                self.size += self.size
            if "p" in gene:
                self.size = self.size + (self.size / 2)
            if "A" in gene:
                self.health += 10
            if "a" in gene:
                self.health += 5
            if "G" in gene:
                self.mutation_chance += 0.10
            if "g" in gene:
                self.mutation_chance += 0.05
                
    
    def dna_to_vector(self, dna: list) -> list:
        '''Converts the DNA sequence into a vector (numerical form)'''
        # Define vectors for each gene
        dna_vectors = {
            "T": [0000],
            "t": [1, 1, 1, 1],
            "P": [0, 0, 0, 1],
            "p": [1, 1, 1, 0],
            "A": [0, 0, 1, 0],
            "a": [1, 1, 0, 1],
            "G": [0, 0, 1, 1],
            "g": [1, 1, 0, 0]
        }
        
        # Convert each gene in the DNA sequence into its corresponding vector
        vectors = []
        for seq in dna:
            for gene in seq:
                vectors.extend(dna_vectors[gene])
        return vectors
    
    
    
    def mutate_dna(self) -> list:
        '''Applies mutations to the DNA sequence with a certain probability'''
        # Choose a random gene to mutate
        gene_mutate = random.randint(0, len(self.dna) - 1)
        new_dna = self.dna
        
        # Check if mutation happens based on mutation chance
        if random.uniform(0, 1) <= self.mutation_chance:
            # Iterate over the DNA and mutate genes
            for i in range(len(new_dna)):
                for j in range(len(new_dna[i])):
                    if gene_mutate <= self.mutation_chance:
                        # Randomly change genes based on mutation chance
                        new_dna[i][j] = random.choice("TtPpAaGg")
                        gene_mutate = random.randint(0, len(self.dna) - 1)
        
        # Update the DNA of the cell
        self.dna = new_dna
                
        return new_dna
    
    def kill(self, all_cells) -> None:
        '''Removes the cell from the list of all cells if it dies'''
        if self in all_cells:
            all_cells.remove(self)
    
    def health_(self, all_cells) -> int:
        '''Checks cell's health; removes the cell if its health reaches 0'''
        if self.health <= 0:
            self.kill(all_cells)

        return self.health
    
    def movement(self) -> tuple[int, int]:
        '''Moves the cell across the screen and handles bouncing off screen edges'''
        # Move the cell's position based on its direction and speed
        self.x += self.direction.x
        self.y += self.direction.y
        
        self.cell.x = self.speed + self.x
        self.cell.y = self.speed + self.y
        
        # If the cell hits the window boundaries, reverse its direction
        if self.cell.x > 800 - self.size or self.cell.x < 0 + self.size:
            self.direction.x = -self.direction.x
        if self.cell.y > 600 - self.size or self.cell.y < 0 + self.size:
            self.direction.y = -self.direction.y
        
        return self.cell.x, self.cell.y
    
    def reproduce(self) -> bool:
        '''Handles cell reproduction if reproduction conditions are met'''
        if self.can_reproduce == 1:
            # Create between 0 to 3 child cells
            num_children = random.randint(0, 3)
            self.cell_children = [Cells(str(self.cell_id + "'s: " + str(i))) for i in range(num_children)]
            
            # Assign DNA to the children and apply mutations
            for i in range(len(self.cell_children)):
                self.cell_children[i].children_dna()
            self.can_reproduce = 0
            return True
        
        return False
    
    def children_dna(self) -> None:
        '''Changes up to 50% of the children's DNA to simulate random mutations'''
        num_change = 8
        bool = random.randint(0, 1)
        
        for i in range(len(self.cell_children)):
            # Inherit parent DNA for each child
            self.cell_children[i].dna = self.dna
            for j in range(len(self.cell_children[i].dna)):
                for k in range(len(self.cell_children[i].dna[j])):
                    # Apply mutation if certain conditions are met
                    if bool == 1 and num_change > 0:
                        self.cell_children[i].dna[j][k] = random.choice("TtPpAaGg")
                        num_change -= 1
                        bool = random.randint(0, 1)
                        
    
    def information(self, event_pos) -> None:
        '''Displays the information of the cell when clicked'''
        # Check if the cell was clicked
        if self.click and self.cell.collidepoint(event_pos):
            # Print the cell's information: ID, Age, DNA, Health, etc.
            print()
            print(f"ID: {self.cell_id} \n")
            print(f"Age: {self.age}\n")
            print(f"DNA: {self.dna}\n")
            print(f"DNA Vector: {self.dna_vector}\n")
            print(f"Health: {self.health}\n")
            print(f"Num of Children: {len(self.cell_children)}\n")
            print(f"Mutation Chance: {self.mutation_chance}\n")
            print(f"Speed: {self.speed}\n")
            
            # Disable the click flag
            self.click = False
