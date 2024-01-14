class Cell:
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.domain = [i for i in range(1,10)]
        self.box = (self.row // 3) * 3 + (self.col // 3)
    
    def print_cell(self):
        return f'({self.row} , {self.col})'
    
    