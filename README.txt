HOW TO RUN THE PROJECT
-----------------------

Run the Game.py by using python
python Game.py

the game will start by printing the statements.
And because the agents are NOT intelligent, humans has to take the decision
that means, when a agent/player want to make decision, it will just prompt in the command line
"Player 0 wanna build house?"
the we need to manually type "y" or "n".

If you type yes, then it will ask, enter the number of the box where you are building the house,
then we need to manually type ex: "10" (some relevant number where you need to build house)


Flow of the game
--------------------

The Game.py will take "each_box_data.json" file and read it and create a game chart based on the data of the
"each_box_data.json". In that file, there will be indexes like 0, 1,2...40
the data of each box at particular index will be present in that dict format.
If you wish to change the data then you can edit the file simply.

example. If you want the "card" at index 8 should have "price" as 1000 then you can edit it in json file, where key is  "8"


After reading the data, by default the game will take a "naive dice",
naive dice will always prompt for the user input which is conisdered as the dice values at each step.

For example: it will prompt...it is player 0's turn...enter the dice values
then human will enter the values as 2,1, then it will assume that the dice values are 2 and 1 and the player 0 is moved
towards 3 steps

