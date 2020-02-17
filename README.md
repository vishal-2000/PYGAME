# PYGAME
 Game : Escape it!
 Documentation:
1.	The fonts, hit messages and success messages are stored in config.cfg file
2.	You might take few minutes to perform steps 2, 3, 4 in order to setup the suitable environment but it is decent investment for lifetime access to such open source games from any other developer like myself 
3.	You must have a python>3 (maintaining a virtual environment is optional) environment setup in order to run this program.
4.	Install pygame library onto your python environment
5.	Install configparser package into your python virtual environment( I guess even this is optional now that i had included the config parser file in the zip file)
  Command: pip install configparser/configParser (There might be other methods to do this and you are free to explore them!)
6.	To run the game just open the python file named play.py using a python ide(optional: you can even use any txt editor but it must be able to build python programs) and run it or use a python interpreter
7.	Theme: You are an alien travelling in a low flying spaceship trying to safely explore Earth. The ships and network towers are the obstacles (You’ll have to play the same level when your next turn comes)
8.	Rules and Functionality:
a.	The first turn goes to player 1 who has to start from the bottom of the window
b.	After his turn is over, the second player must start playing
c.	Time taken to complete a round will be stored separately for each player and will be used for evaluation in case of draw
d.	The game doesn’t end unless you choose to end it!
e.	In each level the speed of each ship increases by 0.5 units
f.	If a player successfully completes a level, he/she will have to play next level when his turn comes
g.	On crossing the brown partition, a player secures 5 points
h.	On crossing the blue partition, a player secures 10 points
i.	You lose 10 pts if your spaceship gets hit by a ship, 5 points if it gets hit by a network tower
j.	Last but not the least, if both players die with equal scores, then the player who dies faster wins the game!! Weird right, but this how I designed it and I hope you’ll find it reasonable 😊😊

I’ll keep updating the features and gameplay from time to time so do keep visiting my repo once in a while for updates
Hope you’ll have great time playing it!
