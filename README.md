# Hasami Shogi Game

This project implements a two-player Hasami Shogi (Variant 1) game in Python. Players take turns moving game pieces on a game board according to the game rules. The objective is to capture opponent pieces and achieve victory.

## Game Rules

Hasami Shogi is a strategic board game where players aim to capture opponent pieces to win. The rules are as follows:

- Players take turns moving their own pieces on the board.
- A piece can be moved any number of cells horizontally or vertically.
- A piece cannot move beyond adjacent squares to friendly or enemy pieces.
- Enemy pieces are captured by surrounding them with the player's pieces on two sides.
- The game ends when a player captures all but one (or all) of the opponent's pieces.

## How to Play

1. Clone the repository to your local machine.
2. Run the Python script `hasami_shogi.py` using your Python interpreter.
3. Players will be prompted to enter moves using the format `from_square to_square`, where `from_square` is the current position of the player's piece, and `to_square` is the desired destination.
4. If the move is valid, the game will proceed, and players will be informed if a piece has been captured or if the game has ended.
5. The game continues until one player wins or the game state changes to 'RED_WON' or 'BLACK_WON'.

## Code Structure

The project includes the following main components:

- `GamePiece`: A class representing a Hasami Shogi game piece with color and location attributes.
- `HasamiShogiGame`: A class representing the game itself, managing the game board, pieces, and gameplay logic.

## Running the Code

To play the game, simply execute the `hasami_shogi.py` script using a Python interpreter.
