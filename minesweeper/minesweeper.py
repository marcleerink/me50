import random


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
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)



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
        self.knowledge: list[Sentence] = []

    @property
    def board_size(self):
        return self.height * self.width

    @property
    def moves_left(self):
        return self.board_size - len(self.moves_made) - len(self.mines)

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def get_neighbours(self, cell, count):
        """
        Returns a set of neighbouring cells and the count of mines
        in those cells
        """
        neighbouring_cells = set()
        row = cell[0]
        column = cell[1]

        for i in range(row - 1, row + 2):
            for j in range(column - 1, column + 2):
                if (i, j) == cell or (i, j) in self.safes:
                    continue

                if (i, j) in self.mines:
                    count -= 1
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbouring_cells.add((i, j))

        return neighbouring_cells, count

    def update_safes_mines(self):
        """
        Updates the safes and mines sets
        based on the knowledge base
        """
        safes = set()
        mines = set()
        for sentence in self.knowledge:
            safes.update(sentence.known_safes())
            mines.update(sentence.known_mines())

        if safes:
            for safe in safes:
                self.mark_safe(safe)
        if mines:
            for mine in mines:
                self.mark_mine(mine)

    def add_new_sentences(self):
        """
        Tries to infer new sentences based on the knowledge base
        """
        for sentence_1 in self.knowledge:
            for sentence_2 in self.knowledge:

                if sentence_1 == sentence_2:
                    continue

                if sentence_1.cells.issubset(sentence_2.cells):
                    new_sentence_cells = sentence_2.cells - sentence_1.cells
                    new_sentence_count = sentence_2.count - sentence_1.count

                    new_sentence = Sentence(new_sentence_cells, new_sentence_count)

                    if new_sentence not in self.knowledge:
                        self.knowledge.append(new_sentence)

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
        self.moves_made.add(cell)
        self.mark_safe(cell)

        neighbours, new_count = self.get_neighbours(cell, count)
        self.knowledge.append(Sentence(neighbours, new_count))

        self.update_safes_mines()

        self.add_new_sentences()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # Return None if no safe moves available:
        if len(self.safes) == 0:
            return None

        # Return a safe move if available:
        for move in self.safes:
            if move not in self.moves_made:
                return move

        # Return None if no safe moves available:
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        if self.moves_left == 0:
            return None

        while True:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            cell = (i, j)
            if cell not in self.moves_made and cell not in self.mines:
                return cell
