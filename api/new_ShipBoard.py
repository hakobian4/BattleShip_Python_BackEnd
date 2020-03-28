import random
import numpy as np


class Ship_Board():
    def __init__(self):
        self.board = None
        self.ships_count = None
        self.ships_cord = None

    def set_ships_board(self, row, col, direction, ship_size):
        """
            This method allows to set the given ship with the given direction.
        """

        cord_list = []
        if direction == 1:
            for i in range(row, row + ship_size):
                self.board[i][col] = ship_size
                cord = []
                cord.append(i)
                cord.append(col)
                cord_list.append(cord)  
        else:
            for j in range(col, col + ship_size):  
                self.board[row][j] = ship_size
                cord = []
                cord.append(row)
                cord.append(j)
                cord_list.append(cord)

        self.ships_count[ship_size - 1] -= 1    
        self.ships_cord[ship_size - 1].append(cord_list)
        

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
            cord = []
            self.board[row][col] = 1
            cord.append(row)
            cord.append(col)
            self.ships_cord[0].append(cord)
            self.ships_count[0] -= 1
            return True

    def check_vertical_direction(self, row, col, ship_size):
        """
            This method checks wether the given ship can be set vertically from the given position.
        """

        empty = True
        for i in range(row - 1, row + ship_size + 1):
            for j in range(col - 1, col + 2):
                if self.board[i][j] != 0:
                    empty = False
                    break
        if empty:
            return 1    


    def check_horizontal_direction(self, row, col, ship_size):
            """
                This method checks wether the given ship can be set horizontally from the given position.
            """

            empty = True
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + ship_size + 1):
                    if self.board[i][j] != 0:
                        empty = False
                        break
            if empty:
                return 2     


    def get_available_directions(self, row, col, ship_size):
        """
            This method checks all available directions for the given ship and returns the list of that directions.
            The given ship can only be 2, 3 or 4 valued ship.
        """

        directions = []

        if ship_size == 4:
            line = 8
        elif ship_size == 3:
            line = 9
        else:
            line = 10

        if col < line:
            if row < line:
                directions.append(self.check_horizontal_direction(row, col, ship_size))
                directions.append(self.check_vertical_direction(row, col, ship_size))
            else:
                directions.append(self.check_horizontal_direction(row, col, ship_size))
        else:
            if row < line:
                directions.append(self.check_vertical_direction(row, col, ship_size))
            else:
                pass

        return directions


    def set_ships_random(self):
        """
            This method sets all ships randomly on the BattleShip game board.
        """
        for ship_size in reversed(range(1, 5)):
            while self.ships_count[ship_size - 1] > 0:

                # generate random row and column for given ship
                row = np.random.choice(range(1, 11))
                col = np.random.choice(range(1, 11))

                if ship_size > 1:
                    directions = self.get_available_directions(row, col, ship_size)
                    # remove Nones from directions list
                    directions = list(filter(None, directions))

                    # check len(directions) and set the given ship
                    if len(directions) != 0:
                        direction = np.random.choice(directions)
                        # set the given ship on the board
                        self.set_ships_board(row, col, direction, ship_size)

                else:
                    # set 1 valued ship on the board
                    self.set_single_ships(row, col)

        # return board as list
        return self.board[1 : -1, 1 : -1].tolist()


    def clean_board(self):
        """
            This method cleans the board.
        """

        self.board = np.zeros([12, 12])
        self.ships_count = [4, 3, 2, 1]
        self.ships_cord = [[], [], [], []]
        return "Player board is cleaned"


    def set_ship_with_hand(self, row, col, direction, ship_size):
        """
            This metod sets ships on board menually.
        """ 
        if self.ships_count[ship_size - 1] > 0:
            if ship_size == 1:
                if self.set_single_ships(row, col):
                    return "The ship is set on the board."
                else:
                    return "The ship can not be set on the board on the given position."
            else:
                directions = self.get_available_directions(row, col, ship_size)
                if direction in directions:
                    self.set_ships_board(row, col, direction, ship_size)
                    return "The ship is set from the given position on the board."
                else:
                    return "The ship can not be set by the given direction on the board on the given position."
        else:
            return "This ship with the given size is already set."            
    

    def checking_ships_fight(self, row, col):
        """
            This method globally globally provides information about board current status.
        """
        bang = True
        if self.board[row][col] in [1, 2, 3, 4]:
            ship_size_number = self.board[row][col]
            self.board[row][col] = -ship_size_number
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if self.board[i][j] == ship_size_number:
                        bang = False
                        return "You shoot it."
            if bang:
                self.remove_cord(row, col, ship_size_number)
                if self.check_win_or_lose() == 1:
                    return "Tadaaam!!! You are Winner..."
                else:
                    return "!!!Bang!!!"
        elif self.board[row][col] == 0:
            self.board[row][col] = 8
            return "You miss the ship."
        else: 
            return "You have already shoot the ship."
                

    def remove_cord(self, row, col, ship_size_number):
        """
            This method removes shot ship from all ships(self.ships_cord).
        """

        if ship_size_number == 1:
            for i in range(row - 1, row +2):
                for j in range(col - 1, col + 2):
                    if self.board[i][j] != -1:
                        self.board[i][j] = 8
            self.ships_cord[0].remove([row, col])
        else:
            cords = None
            for ship in self.ships_cord[int(ship_size_number) - 1]:
                for i in range(len(ship)):
                    if (ship[i][0] == row) and (ship[i][1] == col):
                        cords = ship
                        break

                if cords != None:
                    break
            for i in range(cords[0][0] - 1, cords[len(cords) - 1][0] + 2):
                for j in range(cords[0][1] - 1, cords[len(cords) - 1][1] + 2):
                    if self.board[i][j] != -ship_size_number:
                        self.board[i][j] = 8
            self.ships_cord[int(ship_size_number) - 1].remove(cords)
    
    def check_win_or_lose(self):
        """
            This method identifies the winner.
        """

        win = True
        for ships in self.ships_cord:
            if len(ships) != 0:
                win = False
                break
        if win:
            return 1
        else:
            return 0
                


def main():
    board = Ship_Board()
    board.clean_board()
    print(board.set_ships_random())

if __name__ == '__main__':
    main()