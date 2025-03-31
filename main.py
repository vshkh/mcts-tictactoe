from mcts import MCTS
from board import Board

def benchmark(ai1, ai2, games=50):
    results = {'ai1_wins': 0, 'ai2_wins': 0, 'draws': 0}

    for i in range(games):
        board = Board()
        current_player = 'X' if i % 2 == 0 else 'O'
        players = {'X': ai1 if current_player == 'X' else ai2,
                   'O': ai2 if current_player == 'X' else ai1}

        while not board.is_game_over():
            ai = players[current_player]
            move = ai.search(board, current_player)
            board.make_move(*move, current_player)
            current_player = 'O' if current_player == 'X' else 'X'

        winner = board.get_winner()
        if winner == 'X':
            results['ai1_wins' if players['X'] == ai1 else 'ai2_wins'] += 1
        elif winner == 'O':
            results['ai1_wins' if players['O'] == ai1 else 'ai2_wins'] += 1
        else:
            results['draws'] += 1

    return results

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
