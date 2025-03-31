class Board:
    def __init__(self):
        self.board = [['' for x in range(3)] for y in range(3)]
    
    def print_board(self):
        for row in self.board:
            print(row)
    
    def make_move(self, x, y, player):
        if self.board[x][y] == '':
            self.board[x][y] = player
            return True
        return False

    def is_winner(self, player):
        # Check rows
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        # Check columns
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False
    
    def is_draw(self):
        return all(cell != '' for row in self.board for cell in row) and not self.is_winner('X') and not self.is_winner('O')    
    
    def is_game_over(self):
        return self.is_winner('X') or self.is_winner('O') or self.is_draw()
    
    def get_empty_cells(self):
        return [(x, y) for x in range(3) for y in range(3) if self.board[x][y] == '']
    
    def get_winner(self):
        if self.is_winner('X'):
            return 'X'
        elif self.is_winner('O'):
            return 'O'
        return None 
        
    def get_score(self):
        if self.is_winner('X'):
            return 1
        elif self.is_winner('O'):
            return -1
        return 0
    
    def get_board(self):
        return self.board

    def clone(self):
        new_board = Board()
        new_board.board = [row[:] for row in self.board]
        return new_board
    
        
    

