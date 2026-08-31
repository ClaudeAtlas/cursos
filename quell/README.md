# Quell

A Gobstones implementation of the Quell game, by Fallen Tree Games.
The author is Pablo E. -Fidel- Martínez López.

The first implementation follows the REPL style (Read-Eval-Print-Loop), where the board is only used to show the game, and to store its state between loops (current version of Gobstones does not support a persistant state in an interactive program).
It can be found on the tag REPL-Version.
It has a first operative level, but the style shown inefficient.
For that reason, another style will be tested.

The efficient implementation will only draw the model on the board, and then use the board to store the current state. 
Game operations are performed on the board, directly. 
Only basic reading of changing data is provided.