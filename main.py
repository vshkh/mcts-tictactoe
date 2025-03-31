from mcts import MCTS
from board import Board

board = Board()
mcts = MCTS(time_limit=1.0)
current_player = 'X'
turn = 1

while not board.is_game_over():
    board.print_board()
    print()

    if current_player == 'X':
        move = mcts.search(board, 'X', turn=turn)  # AI turn
        print(f"AI chooses: {move}")
        if not board.make_move(move[0], move[1], current_player):
            print(f"AI tried an invalid move: {move}")
            # Optionally, retry or raise an error
            raise ValueError("AI selected an invalid move!")
        turn += 1
    else:
        try:
            x, y = map(int, input("Enter your move (x y): ").split())
            if not (0 <= x <= 2 and 0 <= y <= 2):
                print("Move must be between 0 and 2!")
                continue
            if not board.make_move(x, y, current_player):
                print("Invalid move! Cell already taken.")
                continue
        except (ValueError, IndexError):
            print("Please enter two numbers (e.g., '1 2')")
            continue

    current_player = 'O' if current_player == 'X' else 'X'
board.print_board()
winner = board.get_winner()
print(f"Game Over! Winner: {winner if winner else 'Draw'}")
