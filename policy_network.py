import torch
import torch.nn as nn
import torch.nn.functional as F

class PolicyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(2, 32, kernel_size=2)      # 2 input channels: Xs and Os
        self.fc1 = nn.Linear(32 * 2 * 2, 64)              # After flattening 2x2x32
        self.fc2 = nn.Linear(64, 9)                       # 9 possible move positions

    def forward(self, x):
        """
        x: tensor of shape (batch_size, 2, 3, 3)
        Returns: tensor of shape (batch_size, 9) - probabilities for each move
        """
        x = F.relu(self.conv1(x))                         # -> (batch_size, 32, 2, 2)
        x = x.view(-1, 32 * 2 * 2)                         # Flatten
        x = F.relu(self.fc1(x))                           # -> (batch_size, 64)
        x = self.fc2(x)                                   # -> (batch_size, 9)
        x = F.softmax(x, dim=1)                           # Probabilities for each move
        return x

def encode_board(board_obj):
    """
    Converts a Board object into a tensor suitable for the policy network.
    Returns: torch.Tensor of shape (1, 2, 3, 3)
    """
    board = board_obj.get_board()
    tensor = torch.zeros((2, 3, 3), dtype=torch.float32)

    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                tensor[0, i, j] = 1.0
            elif board[i][j] == 'O':
                tensor[1, i, j] = 1.0

    return tensor.unsqueeze(0)  # Add batch dimension (1, 2, 3, 3)
