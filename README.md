# Conniption

Conniption is a modified connect-four game, in which up to four gravity flips are allowed to change the state of the game. In each player's turn the player decides to flip or not, place and again to flip or not. No consecutive flips between players are allowed.

This repository includes a command-line base version of the game which can be run by: python3 main.py

Once the program is launched you will be able to chose to play as a human, or between 5 different Artificial Intelligent agents which use separeta evaluation functions and the implementation of a minimax algorithm with aplha-beta pruning implemented. For more details about the architecture refer to: [AIConniptionArchitecture](AIConniptionArchitecture.pdf)

For a detail description of the results obtained after the experimentation of all the different evaluation functions against each other and detail analysis of the metrics obtained refer to: results_Conniption.docx

## Usage

Go to the [src](/src) directory.

Version: `Python 2.7`
Run: `python main.py`

## Libraries being used

- termcolor
- getch
- pickle

## Results

Please refer to [results](results_Conniption.docx)
