import torch
from board import Board
from policy_network import PolicyNet, encode_board

# Create a sample board
board = Board()
board.make_move(0, 0, 'X')
board.make_move(1, 1, 'O')
board.make_move(0, 1, 'X')
board.print_board()

# Load the policy network
model = PolicyNet()
model.eval()  # Turn off dropout, etc.

# Encode the board
input_tensor = encode_board(board)

# Run a forward pass
with torch.no_grad():
    output = model(input_tensor)  # Shape: (1, 9)

# Interpret the result
probabilities = output.squeeze().tolist()  # Remove batch dimension

print("\nMove probabilities from the policy network:")
for i in range(3):
    row = []
    for j in range(3):
        idx = i * 3 + j
        prob = probabilities[idx]
        row.append(f"{prob:.2f}")
    print(" | ".join(row))
