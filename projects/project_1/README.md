# Board Game Leaderboard
The board game leaderboard is just what it sounds like: a way to create custom leaderboards among a group of people for board games played.
When the program is run, a user is first promted to "Enter leaderboard name". The leaderboard name entered will be assigned to the leaderboard file name. If no name is entered, the program will quit with an error message "Missing file name".

Once leaderboard name has been entered, user will be prompted to select if they want to enter a game or view stats.

Enter game should be used if user wants to input a new game that has been played.

View stats should be selected to view the current stats of the leaderboard selected when program was initially run.

Enter game:
When entering a game, user will be promted to type the game they played. Currently, the program supports only a few specific games. The reason for this is because I believe it would be unfair to compare winning a game of war, which is purely based on luck, with winning a more complicated strategy game. I have included a list of games to check against at the "game played" input line. If the user inputs a game that is not on the list, the program will quit and provide a list of games that are supported by the leaderboard (currently: Catan, Charterstone, Scythe, Viticulture, Ticket To Ride)
List of supported games in "games" list under get_game_info() function.

Once user enters a game that is supported, they will be given directions to enter game information, as follows:
Enter player full name (e.g. John Doe) followed by their finish as 'W' for win and 'L' for loss. Input 'None' as player after all game info is added.

get_game_info() function collects user input and stores it in a list called round. List houses dictionaries holding each player's name, finish (win or loss), and the game played. Once 'None' is entered, the function ends and returns the round to user_input and then back to main. Main sends the input(round) to gamelist, which is a Leaderboard class function. Gamelist writes line by line the round info into a .txt file (with the filename matching the leaderboard name initially given). New file is created or existing file is appended with round info.

These .txt files will be what "View stats" selection uses to pull data.
