import math
import random

class Node:
    def __init__(self, board, parent=None, move=None, player='X'):
        """Initializes a new node with the given board, parent, move, and player."""
        self.board = board              # A Board instance (game state)
        self.parent = parent            # Parent node
        self.children = []              # List of child nodes
        self.move = move                # The move that led to this node (x, y)
        self.player = player            # The player who made the move
        self.wins = 0                   # Number of wins from this node's simulations
        self.visits = 0                 # Number of times this node has been visited
        self.untried_moves = board.get_empty_cells()  # Moves not yet tried from this state

    def expand(self):
        """Expands one untried move and returns the new child node."""
        move = self.untried_moves.pop()
        new_board = self.board.clone()
        new_board.make_move(move[0], move[1], self.get_next_player())
        child_node = Node(new_board, parent=self, move=move, player=self.get_next_player())
        self.children.append(child_node)
        return child_node

    def get_next_player(self):
        """Returns the next player to move."""
        return 'O' if self.player == 'X' else 'X'

    def is_fully_expanded(self):
        """Checks if all untried moves have been tried."""
        return len(self.untried_moves) == 0

    def best_child(self, c_param=1.41):
        """Uses UCB to select the best child node (highest win rate, most balanced exploration and exploitation)"""
        return max(
            self.children,
            key=lambda child: (child.wins / child.visits if child.visits > 0 else float('inf')) +
            c_param * math.sqrt(math.log(self.visits) / child.visits if child.visits > 0 else float('inf'))
        )

    def update(self, result):
        """Updates this node with the result of a simulation."""
        self.visits += 1
        self.wins += result  # Result is 1 for win, 0 for loss, 0.5 for draw