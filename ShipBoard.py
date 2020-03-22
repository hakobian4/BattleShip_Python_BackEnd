import random
import numpy as np


class Ship_Board():
    def __init__(self):
        self.board = None

    def set_ships_board(self, row, col, direction, ship_size):
        """
            This method allows to set the given ship with the given direction.
        """

        if direction == 1:
            for i in range(row - ship_size + 1, row + 1):
                self.board[i][col] = ship_size
        
        elif direction == 2:
            for j in range(col, col + ship_size):  
                self.board[row][j] = ship_size
        
        elif direction == 3:
            for i in range(row, row + ship_size):
                self.board[i][col] = ship_size

        else:
            for j in range(col - ship_size +1, col + 1):  
                self.board[row][j] = ship_size
        

    def set_single_ships(self, row, col):
        """
            This method checks empty cells for single-valued ship and sets it.
            If single-valued ship is set, then returns 1, otherwise None.
        """

        empty = True
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if self.board[i][j] != 0:
                    empty = False
                    break
        if empty:
            self.board[row][col] = 1
            return 1


    def first_direction(self, row, col, ship_size):
        """
            This method checks wether the given ship can be set above the given position.
            The given ship can only be 2 or 3 valued ships.
        """

        empty = True
        for i in range(row - ship_size, row + 2):
            for j in range(col - 1, col + 2):
                if self.board[i][j] != 0:
                    empty = False
                    break
        if empty:
            return 1          


    def second_direction(self, row, col, ship_size):
        """
            This method checks wether the given ship can be set right the given position.
            The given ship can only be 2 or 3 valued ships.
        """

        empty = True
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + ship_size + 1):
                if self.board[i][j] != 0:
                    empty = False
                    break
        if empty:
            return 2     


    def third_direction(self, row, col, ship_size):
        """
            This method checks wether the given ship can be set bellow the given position.
            The given ship can only be 2 or 3 valued ships.
        """

        empty = True
        for i in range(row - 1, row + ship_size + 1):
            for j in range(col - 1, col + 2):
                if self.board[i][j] != 0:
                    empty = False
                    break
        if empty:
            return 3    


    def fourth_direction(self, row, col, ship_size):
        """
            This method checks wether the given ship can be set left the given position.
            The given ship can only be 2 or 3 valued ship.
        """

        empty = True
        for i in range(row - 1, row + 2):
            for j in range(col - ship_size, col + 2):
                if self.board[i][j] != 0:
                    empty = False
                    break
        if empty:
            return 4   

    def get_available_directions(self, row, col, ship_size):
        """
            This method checks all available directions for the given ship and returns the list of that directions.
            The given ship can only be 2 or 3 valued ship.
        """

        directions = []

        line1 = ship_size
        if ship_size == 3:
            line2 = 9
        else:
            line2 = 10

        if col < line1:
            if row < line1:
                directions.append(self.second_direction(row, col, ship_size))
                directions.append(self.third_direction(row, col, ship_size))
            elif row < line2:
                directions.append(self.first_direction(row, col, ship_size))
                directions.append(self.second_direction(row, col, ship_size))
                directions.append(self.third_direction(row, col, ship_size))
            else:
                directions.append(self.first_direction(row, col, ship_size))
                directions.append(self.second_direction(row, col, ship_size))
        
        elif col < line2:
            if row < line1:
                directions.append(self.second_direction(row, col, ship_size))
                directions.append(self.third_direction(row, col, ship_size))
                directions.append(self.fourth_direction(row, col, ship_size))
            elif row < line2:
                directions.append(self.first_direction(row, col, ship_size))
                directions.append(self.second_direction(row, col, ship_size))
                directions.append(self.third_direction(row, col, ship_size))
                directions.append(self.fourth_direction(row, col, ship_size))
            else:
                directions.append(self.first_direction(row, col, ship_size))
                directions.append(self.second_direction(row, col, ship_size))
                directions.append(self.fourth_direction(row, col, ship_size))
        
        else:
            if row < line1:
                directions.append(self.third_direction(row, col, ship_size))
                directions.append(self.fourth_direction(row, col, ship_size))
            elif row < line2:
                directions.append(self.first_direction(row, col, ship_size))
                directions.append(self.third_direction(row, col, ship_size))
                directions.append(self.fourth_direction(row, col, ship_size))
            else:
                directions.append(self.first_direction(row, col, ship_size))
                directions.append(self.fourth_direction(row, col, ship_size))

        return directions


    def get_fourth_available_directions(self, row, col):
        """
            This method returns the list of all available directions for the given ship.
            The given ship can only be 4 valued ship.
        """

        if col < 4:
            if row < 4:
                directions = [2, 3]
            elif row < 8:
                directions = [1, 2, 3]
            else:
                directions = [1, 2]
        
        elif col < 8:
            if row < 4:
                directions = [2, 3, 4]
            elif row < 8:
                directions = [1, 2, 3, 4]
            else:
                directions = [1, 2, 4]
        
        else:
            if row < 4:
                directions = [3, 4]
            elif row < 8:
                directions = [1, 3, 4]
            else:
                directions = [1, 4]
        
        return directions
        

    def set_ships_random(self):
        """
            This method sets all ships randomly on the BattleShip game board.
        """

        # create board
        self.board = np.zeros([12, 12])

        # generate random row and column for 4 valued ship
        row = np.random.choice(range(1, 11))
        column = np.random.choice(range(1, 11))

        ship_size = 4
        directions = self.get_fourth_available_directions(row, column)
        direction = np.random.choice(directions)

        # set 4 vlued ship on the board
        self.set_ships_board(row, column, direction, ship_size)


        ship_size = 3
        ships_count = 0
        while ships_count < 2:

            # generate random rows and columns for 3 valued ships
            row = np.random.choice(range(1, 11))
            column = np.random.choice(range(1, 11))

            directions = self.get_available_directions(row, column, ship_size)

            # remove Nones from directions list
            directions = list(filter(None, directions))

            # check len(directions) and set 3 valued ship
            if len(directions) != 0:
                direction = np.random.choice(directions)
                self.set_ships_board(row, column, direction, ship_size)
                ships_count += 1


        ship_size = 2
        ships_count = 0
        while ships_count < 3:

            # generate random rows and columns for 2 valued ships
            row = np.random.choice(range(1, 11))
            column = np.random.choice(range(1, 11))
            directions = self.get_available_directions(row, column, ship_size)

            # remove Nones from directions list
            directions = list(filter(None, directions))

            # check len(directions) and set 2 valued ship
            if len(directions) != 0:
                direction = np.random.choice(directions)
                self.set_ships_board(row, column, direction, ship_size)
                ships_count += 1

        ship_size = 1
        ships_count = 0
        while ships_count < 4:

            # generate random rows and columns for 1 valued ships
            row = np.random.choice(range(1, 11))
            column = np.random.choice(range(1, 11))

            # result is 1, when the 1 valued ship set
            result = self.set_single_ships(row, column)

            if result == 1:
                ships_count += 1

        # get board ready to play
        self.board = self.board[1 : -1, 1 : -1]
 
        return self.board


def main():
    board = Ship_Board()
    print(board.set_ships_random())
    
if __name__ == '__main__':
    main()
