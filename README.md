# Conniption
## Dr Wilkins will know if you take inspiration from this for your AI 2018 class 

Conniption is a modified connect-four game, in which up to four gravity flips are allowed to change the state of the game. In each player's turn the player decides to flip or not, place and again to flip or not. No consecutive flips between players are allowed.

This repository includes a command-line base version of the game which can be run by: python3 main.py

Once the program is launched you will be able to chose to play as a human, or between 5 different Artificial Intelligent agents which use separate evaluation functions and the implementation of a minimax algorithm with alpha-beta pruning implemented. There is also two available previously trained reinforcement learning agents. For more details about the architecture refer to: [AIConniptionArchitecture](results/AIConniptionArchitecture.pdf)


## Usage

Go INSIDE the [src](/src) directory and do the following

Version: Python 3.

Run: `python main.py`

## Libraries being used

- termcolor
- getch
- pickle

## Results

For a detail description of the results obtained after the experimentation of all the different evaluation functions against each other and detail analysis of the metrics obtained refer to:  [results](results/results_Conniption.pdf)
