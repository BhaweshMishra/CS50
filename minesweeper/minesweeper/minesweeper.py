import itertools
import random
from turtle import width

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return None
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return None
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        self.cells.remove(cell)
        self.count -= 1
        return
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        self.cells.remove(cell)
        return
        raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for knowledge in self.knowledge:
            if cell in knowledge.cells:
                knowledge.mark_mine(cell)



    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        
        self.safes.add(cell)
        for knowledge in self.knowledge:
            if cell in knowledge.cells:
                knowledge.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # mark the cell as a move that has been made
        self.moves_made.add(cell)
        print("move made:",cell)
        # mark the cell as safe
        
        self.knowledge.append(Sentence({cell},0))
        self.mark_safe(cell)
        # add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        # taken care of in mark_mine fn

        # mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        neighbour_cells,mine_count = self.neighbours(cell,count)
        self.knowledge.append(Sentence(neighbour_cells,mine_count))
        print("neighbours:",neighbour_cells,mine_count)
        
        temp_safe_cells = []
        temp_mines = []
        print("219 knowledge:")
        for knowledge in self.knowledge:
            
            #print(knowledge.cells,":",knowledge.count)
            if knowledge.count == 0 :
                for cells in knowledge.cells:
                    temp_safe_cells.append(cells)
            if knowledge.count == len(knowledge.cells) :
                for cells in knowledge.cells:
                    temp_mines.append(cells)
        for cells in temp_safe_cells:
            self.mark_safe(cells)
        for cells in temp_mines:
            self.mark_mine(cells)

        #remove empty knowledge
        non_empty_knowledge =[]
        for knowledge in self.knowledge:
            if len(knowledge.cells) > 0:
                non_empty_knowledge.append(knowledge)
        self.knowledge = non_empty_knowledge

        # inferring knowledge
        


        print("knowledge:")
        for knowledge in self.knowledge:
            print(knowledge.cells,":",knowledge.count)
        print("safes: ",self.safes)
        print("unopened safes: ",self.safes-self.moves_made)

        print("mines: ",self.mines)
        #print("moves made:",self.moves_made)
        print("----------------------------")
        return




        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_cells = self.safes - self.moves_made
        if len(safe_cells) == 0:
            return None
        a = safe_cells.pop()

        #self.moves_made.add(a)
        return a
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_possible_moves = set()
        for i in range(self.height):
            for j in range(self.height):
                all_possible_moves.add((i,j))

        not_played = all_possible_moves - self.moves_made - self.mines
        for i in not_played:
            if random.randint(0,2) == 1:
                return i
        for i in not_played:
            return i
        return None
        raise NotImplementedError

    def neighbours(self,cell,count):
        i,j = cell
        neighbours = set()
        for x in range(-1,2):
            for y in range(-1,2):

                if x+i == i and y+j == j:
                    continue
                if i+x < 0 or y+j < 0:
                    continue
                if i+x == self.height or y+j == self.width:
                    continue
                # if (i+x,y+j) in self.moves_made:
                #     continue

                neighbours.add((x+i,y+j))

        for mine in self.mines:
            if mine in neighbours:
                count -= 1
        return neighbours - self.safes - self.mines,count






