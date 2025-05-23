import time
import random
from node import Node # type: ignore
from board import Board
from visualization import plot_mcts_summary

class MCTS:
    def __init__(self, time_limit=1.0):
        """Initializes the MCTS with a time limit for the search."""
        self.time_limit = time_limit  # Time to think (in seconds)

    def train(self, board, player, iterations=1000):
        """Trains the MCTS on the given board for the specified player."""
        root = Node(board.clone(), player=player)
        for _ in range(iterations):
            node = self.selection(root)
            node = self.expand(node)
            result = self.simulate_random_playout(node.board.clone(), node.get_next_player())
            self.backpropagate(node, result, player)
        self.pre_trained_root = root

    def search(self, initial_board, player, turn=0):
        """Performs a Monte Carlo Tree Search on the given board for the specified player."""
        root = self.pre_trained_root if hasattr(self, 'pre_trained_root') else Node(initial_board.clone(), player=player)
        end_time = time.time() + self.time_limit

        # Within the time limit, perform the search:
        while time.time() < end_time:
            node = root

            # SELECTION
            while not node.board.is_game_over() and node.is_fully_expanded():
                node = node.best_child()

            # EXPANSION
            if not node.board.is_game_over():
                node = node.expand()

            # SIMULATION
            result = self.simulate_random_playout(node.board.clone(), node.get_next_player())

            # BACKPROPAGATION
            self.backpropagate(node, result, player)

        # Return the move with the most visits:
        best_move = max(root.children, key=lambda child: child.visits).move
        if initial_board.board[best_move[0]][best_move[1]] != '':
            print(f"Warning: MCTS selected occupied cell {best_move}")
        
        print("\n--- MCTS Search Summary ---")
        for child in root.children:
            move = child.move
            visits = child.visits
            wins = child.wins
            win_rate = wins / visits if visits > 0 else 0
            print(f"Move {move}: Visits = {visits}, Win Rate = {win_rate:.2f}")
        print("---------------------------\n")
        plot_mcts_summary(root.children, move_number=turn)

        return best_move

    def simulate_random_playout(self, board, current_player):
        """Simulates a random playout on the given board for the specified player."""
        while not board.is_game_over():
            moves = board.get_empty_cells()
            move = random.choice(moves)
            board.make_move(move[0], move[1], current_player)
            current_player = 'O' if current_player == 'X' else 'X'

        # Return the result of the playout:
        winner = board.get_winner()
        if winner == 'X':
            return 1
        elif winner == 'O':
            return -1
        return 0  # draw

    def backpropagate(self, node, result, root_player):
        """Backpropagates the result of the playout to the parent nodes."""
        while node is not None:
            node.visits += 1
            # Assuming root_player is maximizing player
            if node.player == root_player:
                node.wins += result  # +1 if root wins, -1 if opponent wins, 0 if draw
            else:
                node.wins -= result  # -1 if root wins, +1 if opponent wins, 0 if draw
            node = node.parent