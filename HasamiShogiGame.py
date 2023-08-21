# Description: class HasamiShogiGame allows user to play a two player game of Hasami Shogi (Variant 1).
# Players take turns moving pieces on a game board. On a turn, a player can move a piece any number of
# cells horizontally or vertically. A piece can move no further than adjacent to a friendly or enemy piece.
# Enemy pieces are captured by occupying the two cells that surround it. A player wins when they capture all
# but one (or all) of the opponents pieces.

class GamePiece:
    """Represents a Hasami Shogi game piece"""

    def __init__(self, color, location):
        """Creates a game piece with color and location"""
        self._color = color
        self._location = location

    def get_color(self):
        """Returns color of game piece"""
        return self._color

    def get_location(self):
        """Returns location of game piece"""
        return self._location

    def set_location(self, new_location):
        """Sets the location of game piece"""
        self._location = new_location

class HasamiShogiGame:
    """Represents a game of Hasami Shogi (variant 1) with methods to play the game"""

    def __init__(self):
        """Creates a game of Hasami Shogi"""
        self._game_board = [
            ['.', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
            ['a', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['b', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['c', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['d', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['e', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['f', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['g', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['h', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['i', '.', '.', '.', '.', '.', '.', '.', '.', '.']
        ]
        self._red_pieces = self._game_start('RED')
        self._black_pieces = self._game_start('BLACK')
        self._game_state = 'UNFINISHED'     # can be 'UNFINISHED', 'RED_WON', 'BLACK_WON'
        self._active_player = 'BLACK'   # player either BLACK or RED. BLACK gets first move
        self._black_captured_pieces = 0
        self._red_captured_pieces = 0

    def get_game_state(self):
        """Returns the current state of the game"""
        return self._game_state

    def get_active_player(self):
        """Returns the active player"""
        return self._active_player

    def get_num_captured_pieces(self, color):
        """Returns the number of captured pieces of a given color"""
        if color == 'BLACK':
            return self._black_captured_pieces

        if color == 'RED':
            return self._red_captured_pieces

    def _game_start(self, color):
        """Places game pieces on board in starting position"""
        if color == 'BLACK':
            black_pieces = [
                GamePiece('BLACK', 'i1'),
                GamePiece('BLACK', 'i2'),
                GamePiece('BLACK', 'i3'),
                GamePiece('BLACK', 'i4'),
                GamePiece('BLACK', 'i5'),
                GamePiece('BLACK', 'i6'),
                GamePiece('BLACK', 'i7'),
                GamePiece('BLACK', 'i8'),
                GamePiece('BLACK', 'i9')
            ]
            return black_pieces
        elif color == 'RED':
            red_pieces = [
                GamePiece('RED', 'a1'),
                GamePiece('RED', 'a2'),
                GamePiece('RED', 'a3'),
                GamePiece('RED', 'a4'),
                GamePiece('RED', 'a5'),
                GamePiece('RED', 'a6'),
                GamePiece('RED', 'a7'),
                GamePiece('RED', 'a8'),
                GamePiece('RED', 'a9'),
            ]
            return red_pieces

    def _check_winner(self):
        """Checks to see if the game has been won"""
        if self._black_captured_pieces == 8 or self._black_captured_pieces == 9:
            self._game_state = 'RED_WON'

        elif self._red_captured_pieces == 8 or self._red_captured_pieces == 9:
            self._game_state = 'BLACK_WON'

    def get_square_occupant(self, square):
        """Returns color of piece if square is occupied. Otherwise, returns None."""
        for piece in self._black_pieces:
            if piece.get_location() == square:
                return 'BLACK'

        for piece in self._red_pieces:
            if piece.get_location() == square:
                return 'RED'

        return 'NONE'

    def _check_boundaries(self, to_square):
        """Return True if move is within boundaries of game board. Otherwise, return False"""
        valid_move_check = list(to_square)
        if valid_move_check[0] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']:
            if int(valid_move_check[1]) in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                return True
        else:
            return False

    def _check_occupied(self, to_square):
        """Return True if space is occupied. Otherwise, return False"""
        if self.get_square_occupant(to_square) == 'NONE':
            return False
        else:
            return True

    def _row_check(self, num_var):
        """Returns a list of other pieces in same row as moving piece"""
        pieces_in_row = []
        for piece in self._black_pieces:
            if num_var in piece.get_location():
                pieces_in_row.append(piece)

        for piece in self._red_pieces:
            if num_var in piece.get_location():
                pieces_in_row.append(piece)

        return pieces_in_row

    def _column_check(self, letter_var):
        """Returns a list of other pieces in same column as moving piece"""
        pieces_in_column = []
        for piece in self._black_pieces:
            if letter_var in piece.get_location():
                pieces_in_column.append(piece)

        for piece in self._red_pieces:
            if letter_var in piece.get_location():
                pieces_in_column.append(piece)

        return pieces_in_column

    def _check_movement(self, moving_piece, to_square):
        """Checks movement range and returns True if move is viable. Otherwise, returns False."""
        current_location = list(moving_piece.get_location())
        x_upper = 10                        # movement boundaries
        x_lower = 0
        y_upper = '`'
        y_lower = 'j'
        pieces_in_same_row = self._row_check(current_location[0])
        pieces_in_same_column = self._column_check(current_location[1])
        pieces_in_same_row.remove(moving_piece)         #exclude current piece from lists
        pieces_in_same_column.remove(moving_piece)

        #set row boundaries
        for piece in pieces_in_same_row:
            split_val = list(piece.get_location())
            if int(split_val[1]) < int(current_location[1]):       # splits row in half at current_location
                if int(split_val[1]) > x_lower:
                    x_lower = int(split_val[1])
            else:
                if int(split_val[1]) < x_upper:
                    x_upper = int(split_val[1])

        #set column boundaries
        for piece in pieces_in_same_column:
            split_val = list(piece.get_location())
            if split_val[0] < current_location[0]:     # splits column in half at current_location
                if split_val[0] > y_upper:
                    y_upper = split_val[0]
            else:
                if split_val[0] < y_lower:
                    y_lower = split_val[0]

        #check if move (to_square) is within boundaries
        xy_list = list(to_square)
        if xy_list[0] < y_lower and xy_list[0] > y_upper:
            if int(xy_list[1]) < x_upper and int(xy_list[1]) > x_lower:
                return True
            else:
                return False
        else:
            return False    # move not viable

    def _capture_y(self, moved_piece):
        """Captures any pieces that moved piece can legally capture on y axis and increases # captured"""
        current_location = list(moved_piece.get_location())
        pieces_in_same_column = self._column_check(current_location[1])
        pieces_in_same_column.remove(moved_piece)
        y_up = str(chr(ord(current_location[0]) - 1))       # decrements a letter (ex: b to a)
        y_down = str(chr(ord(current_location[0]) + 1))     # increments a letter (ex: a to b)

        opponent_color = None
        if moved_piece.get_color() == 'BLACK':  # set opponent_color
            opponent_color = 'RED'
        else:
            opponent_color = 'BLACK'

        for piece in pieces_in_same_column:                # check column for up and down captures
            up_space = y_up + current_location[1]
            down_space = y_down + current_location[1]
            capture_found = False
            possible_captures = []

            # check for and execute up captures
            if piece.get_location() == up_space and piece.get_color() == opponent_color:
                possible_captures.append(piece)
                y_up = str(chr(ord(y_up) - 1))
                up_space = y_up + current_location[1]
                no_capture_1 = False
                while y_up != '`' and capture_found is False and no_capture_1 is False:
                    up_space = y_up + current_location[1]
                    reset_loop_1 = False
                    for token in pieces_in_same_column:
                        if reset_loop_1 == True:            # exits to while loop to allow for multi-captures
                            no_capture_1 = False
                        else:
                            if token.get_location() == up_space and token.get_color() == opponent_color:
                            # when opponent's token is present, add to possible captures and check next token
                                possible_captures.append(token)
                                y_up = str(chr(ord(y_up) - 1))
                                up_space = y_up + current_location[1]
                                reset_loop_1 = True
                                no_capture_1 = False
                            elif token.get_location() == up_space and token.get_color() == moved_piece.get_color():
                            # when turn player's token is reached, capture opponents tokens
                                capture_found = True
                                for capture in possible_captures:
                                    if capture in self._red_pieces:
                                        self._red_pieces.remove(capture)
                                        self._red_captured_pieces += 1
                                    if capture in self._black_pieces:
                                        self._black_pieces.remove(capture)
                                        self._black_captured_pieces += 1
                                possible_captures.clear()
                            else:
                                no_capture_1 = True
                else:
                    possible_captures.clear()

            # check for and execute down captures
            if piece.get_location() == down_space and piece.get_color() == opponent_color:
                possible_captures.append(piece)
                y_down = str(chr(ord(y_down) + 1))
                down_space = y_down + current_location[1]
                no_capture_2 = False
                while y_down != 'j' and capture_found is False and no_capture_2 is False:
                    down_space = y_down + current_location[1]
                    reset_loop_2 = False
                    for token in pieces_in_same_column:
                        if reset_loop_2 == True:                    # exits to while loop to allow for multi-captures
                            no_capture_2 = False
                        else:
                            if token.get_location() == down_space and token.get_color() == opponent_color:
                            # when opponent's token is present, add to possible captures and check next token
                                possible_captures.append(token)
                                y_down = str(chr(ord(y_down) + 1))
                                down_space = y_down + current_location[1]
                                reset_loop_2 = True
                                no_capture_2 = False
                            elif token.get_location() == down_space and token.get_color() == moved_piece.get_color():
                            # when turn player's token is reached, capture opponents tokens
                                capture_found = True
                                for capture in possible_captures:
                                    if capture in self._red_pieces:
                                        self._red_pieces.remove(capture)
                                        self._red_captured_pieces += 1
                                    if capture in self._black_pieces:
                                        self._black_pieces.remove(capture)
                                        self._black_captured_pieces += 1
                                possible_captures.clear()
                            else:
                                no_capture_2 = True
                                #possible_captures.clear()
                else:
                    possible_captures.clear()


    def _capture_x(self, moved_piece):
        """Captures any pieces that moved piece can legally capture on x axis and increases # captured"""
        current_location = list(moved_piece.get_location())
        pieces_in_same_row = self._row_check(current_location[0])
        pieces_in_same_row.remove(moved_piece)  # exclude current piece from lists
        x_right = str(int(current_location[1]) + 1)
        x_left = str(int(current_location[1]) - 1)

        opponent_color = None
        if moved_piece.get_color() == 'BLACK':      # set opponent_color
            opponent_color = 'RED'
        else:
            opponent_color = 'BLACK'

        for piece in pieces_in_same_row:                # check row for left and right captures
            right_space = current_location[0] + x_right
            left_space = current_location[0] + x_left
            capture_found = False
            possible_captures = []

            # check for and execute right captures
            if piece.get_location() == right_space and piece.get_color() == opponent_color:
                possible_captures.append(piece)
                x_right = str(int(x_right) + 1)
                right_space = current_location[0] + x_right
                no_capture_1 = False
                while x_right != '10' and capture_found is False and no_capture_1 is False:
                    right_space = current_location[0] + x_right
                    reset_loop_1 = False
                    for token in pieces_in_same_row:
                        if reset_loop_1 == True:      # exits to while loop to allow for multi-captures
                            no_capture_1 = False
                        else:
                            if token.get_location() == right_space and token.get_color() == opponent_color:
                            # when opponent's token is present, add to possible captures and check next token
                                possible_captures.append(token)
                                x_right = str(int(x_right) + 1)
                                right_space = current_location[0] + x_right
                                reset_loop_1 = True
                                no_capture_1 = False
                            elif token.get_location() == right_space and token.get_color() == moved_piece.get_color():
                            # when turn player's token is reached, capture opponents tokens
                                capture_found = True
                                for capture in possible_captures:
                                    if capture in self._red_pieces:
                                        self._red_pieces.remove(capture)
                                        self._red_captured_pieces += 1
                                    if capture in self._black_pieces:
                                        self._black_pieces.remove(capture)
                                        self._black_captured_pieces += 1
                                possible_captures.clear()
                            else:
                                no_capture_1 = True
                else:
                    possible_captures.clear()

            # check for and execute left captures
            if piece.get_location() == left_space and piece.get_color() == opponent_color:
                possible_captures.append(piece)
                x_left = str(int(x_left) - 1)
                left_space = current_location[0] + x_left
                no_capture_2 = False
                while x_left != '0' and capture_found is False and no_capture_2 is False:
                    left_space = current_location[0] + x_left
                    reset_loop_2 = False
                    for token in pieces_in_same_row:
                        if reset_loop_2 == True:            # exits to while loop to allow for multi-captures
                            no_capture_2 = False
                        else:
                            if token.get_location() == left_space and token.get_color() == opponent_color:
                            # when opponent's token is present, add to possible captures and check next token
                                possible_captures.append(token)
                                x_left = str(int(x_left) - 1)
                                left_space = current_location[0] + x_left
                                reset_loop_2 = True
                                no_capture_2 = False
                            elif token.get_location() == left_space and token.get_color() == moved_piece.get_color():
                            # when turn player's token is reached, capture opponents tokens
                                capture_found = True
                                for capture in possible_captures:
                                    if capture in self._red_pieces:
                                        self._red_pieces.remove(capture)
                                        self._red_captured_pieces += 1
                                    if capture in self._black_pieces:
                                        self._black_pieces.remove(capture)
                                        self._black_captured_pieces += 1
                                possible_captures.clear()
                            else:
                                no_capture_2 = True
                else:
                    possible_captures.clear()

    def _corner_capture(self, moved_piece):
        """Capture piece that is in corner capture position and increase the # of pieces captured"""
        if moved_piece.get_location() == 'a2':
            if moved_piece.get_color() == 'BLACK':
                for piece in self._red_pieces:
                    if piece.get_location() == 'a1':
                        for token in self._black_pieces:
                            if token.get_location() == 'b1':
                                self._red_pieces.remove(piece)
                                self._red_captured_pieces += 1
            else:
                for piece in self._black_pieces:
                    if piece.get_location() == 'a1':
                        for token in self._red_pieces:
                            if token.get_location() == 'b1':
                                self._black_pieces.remove(piece)
                                self._black_captured_pieces += 1

        if moved_piece.get_location() == 'b1':
            if moved_piece.get_color() == 'BLACK':
                for piece in self._red_pieces:
                    if piece.get_location() == 'a1':
                        for token in self._black_pieces:
                            if token.get_location() == 'a2':
                                self._red_pieces.remove(piece)
                                self._red_captured_pieces += 1
            else:
                for piece in self._black_pieces:
                    if piece.get_location() == 'a1':
                        for token in self._red_pieces:
                            if token.get_location() == 'a2':
                                self._black_pieces.remove(piece)
                                self._black_captured_pieces += 1

        if moved_piece.get_location() == 'a8':
            if moved_piece.get_color() == 'BLACK':
                for piece in self._red_pieces:
                    if piece.get_location() == 'a9':
                        for token in self._black_pieces:
                            if token.get_location() == 'b9':
                                self._red_pieces.remove(piece)
                                self._red_captured_pieces += 1
            else:
                for piece in self._black_pieces:
                    if piece.get_location() == 'a9':
                        for token in self._red_pieces:
                            if token.get_location() == 'b9':
                                self._black_pieces.remove(piece)
                                self._black_captured_pieces += 1

        if moved_piece.get_location() == 'b9':
            if moved_piece.get_color() == 'BLACK':
                for piece in self._red_pieces:
                    if piece.get_location() == 'a9':
                        for token in self._black_pieces:
                            if token.get_location() == 'a8':
                                self._red_pieces.remove(piece)
                                self._red_captured_pieces += 1
            else:
                for piece in self._black_pieces:
                    if piece.get_location() == 'a9':
                        for token in self._red_pieces:
                            if token.get_location() == 'a8':
                                self._black_pieces.remove(piece)
                                self._black_captured_pieces += 1

        if moved_piece.get_location() == 'h1':
            if moved_piece.get_color() == 'BLACK':
                for piece in self._red_pieces:
                    if piece.get_location() == 'i1':
                        for token in self._black_pieces:
                            if token.get_location() == 'i2':
                                self._red_pieces.remove(piece)
                                self._red_captured_pieces += 1
            else:
                for piece in self._black_pieces:
                    if piece.get_location() == 'i1':
                        for token in self._red_pieces:
                            if token.get_location() == 'i2':
                                self._black_pieces.remove(piece)
                                self._black_captured_pieces += 1

        if moved_piece.get_location() == 'i2':
            if moved_piece.get_color() == 'BLACK':
                for piece in self._red_pieces:
                    if piece.get_location() == 'i1':
                        for token in self._black_pieces:
                            if token.get_location() == 'h1':
                                self._red_pieces.remove(piece)
                                self._red_captured_pieces += 1
            else:
                for piece in self._black_pieces:
                    if piece.get_location() == 'i1':
                        for token in self._red_pieces:
                            if token.get_location() == 'h1':
                                self._black_pieces.remove(piece)
                                self._black_captured_pieces += 1

        if moved_piece.get_location() == 'i8':
            if moved_piece.get_color() == 'BLACK':
                for piece in self._red_pieces:
                    if piece.get_location() == 'i9':
                        for token in self._black_pieces:
                            if token.get_location() == 'h9':
                                self._red_pieces.remove(piece)
                                self._red_captured_pieces += 1
            else:
                for piece in self._black_pieces:
                    if piece.get_location() == 'i9':
                        for token in self._red_pieces:
                            if token.get_location() == 'h9':
                                self._black_pieces.remove(piece)
                                self._black_captured_pieces += 1

        if moved_piece.get_location() == 'h9':
            if moved_piece.get_color() == 'BLACK':
                for piece in self._red_pieces:
                    if piece.get_location() == 'i9':
                        for token in self._black_pieces:
                            if token.get_location() == 'i8':
                                self._red_pieces.remove(piece)
                                self._red_captured_pieces += 1
            else:
                for piece in self._black_pieces:
                    if piece.get_location() == 'i9':
                        for token in self._red_pieces:
                            if token.get_location() == 'i8':
                                self._black_pieces.remove(piece)
                                self._black_captured_pieces += 1

    def _check_game_state(self):
        """Allows game to continue so long as no player has won"""
        if self._game_state == 'UNFINISHED':
            return True
        else:
            return False

    def _check_turn_player(self, from_square):
        """"Returns True if turn player is moving the correct piece. Otherwise returns False."""
        for piece in self._black_pieces:
            if piece.get_location() == from_square:
                if piece.get_color() == self._active_player:
                    return True

        for piece in self._red_pieces:
            if piece.get_location() == from_square:
                if piece.get_color() == self._active_player:
                    return True

        return False

    def _switch_players(self):
        """Switch active player"""
        if self._active_player == 'BLACK':
            self._active_player = 'RED'
        else:
            self._active_player = 'BLACK'

    def _identify_piece(self, current_square):
        """Finds and returns the piece to be interacted with"""
        for piece in self._black_pieces:
            if piece.get_location() == current_square:
                return piece

        for piece in self._red_pieces:
            if piece.get_location() == current_square:
                return piece

    def make_move(self, from_square, to_square):
        """Moves player piece from given square to new given square if valid"""
        if self._check_game_state() is True:
            if self._check_turn_player(from_square) is True:
                if self._check_boundaries(to_square) is True:
                    if self._check_occupied(to_square) is False:
                        moving_piece = self._identify_piece(from_square)    # piece to be moved
                        if self._check_movement(moving_piece, to_square) is True:
                            moving_piece.set_location(to_square)
                            self._capture_x(moving_piece)
                            self._capture_y(moving_piece)
                            self._corner_capture(moving_piece)
                            self._check_winner()
                            self._switch_players()
                            return True
        return False

if __name__ == "__main__":
    game = HasamiShogiGame()

    while game.get_game_state() == 'UNFINISHED':
        print(f"Current Player: {game.get_active_player()}")
    
        from_square = input("Enter the source square: ")
        to_square = input("Enter the destination square: ")
    
        if game.make_move(from_square, to_square):
            print("Move successful!")
        else:
            print("Invalid move. Try again.")
    
    print(f"Game Over! {game.get_game_state()}")
