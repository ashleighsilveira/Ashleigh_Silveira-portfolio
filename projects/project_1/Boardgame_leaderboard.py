from collections import Counter
import sys
from tabulate import tabulate

class Leaderboard:

    #list where open_leaderboard function sends read lines
    #called by counter in player_stats function
    played = []

    def __init__(self, filename):
        self.filename = filename


    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        if not filename:
            sys.exit(ValueError("Missing file name"))

        elif not filename.isalnum():
            sys.exit(ValueError("Leaderboard can only contain letters and numbers"))
        self._filename = filename



    def gamelist(self, game):
        #for each dict in list of dicts
        for player in game:
            #writes dict to txt file to collect data
            with open(f"{self.filename}.txt", "a") as file:
                file.write(f"{player}\n")




def main():
    #create leaderboard
    leaderboard = Leaderboard(input("Enter leaderboard name: ").casefold())

    user_input = prompt_user(leaderboard)

    #pass list of dicts to gamelist function
    leaderboard.gamelist(user_input)




def prompt_user(leaderboard):
    ## Find or create leaderboard

    ## Name leaderboard for new
    while True:
        print("-------------------")
        print("Select one:")
        print("[1] Enter new game")
        print("[2] View stats")
        print("-------------------")
        response = input()
        if response  == "1":
            return get_game_info()

        elif response == "2":
            view_stats(leaderboard)
            sys.exit()

        else:
            print("Invalid Selection")
            continue



def get_game_info():
    #create empty list to collect players
    round = []
    #games list to error check- not done yet
    games = ["Catan", "Charterstone", "Scythe", "Viticulture", "Ticket To Ride"]
    #id game played and give instruction to end loop
    game = input("Game played: ").title()
    if game in games:
        print("-------------------------------------------------------------")
        print("Enter player's full name (e.g. John Doe)")
        print("followed by their finish as 'W' for win and 'L' for loss.")
        print("Input 'None' as player after all game info is added.")
        print("-------------------------------------------------------------")

        #loop to collect players and if they win/lose

        ## ADD regex to confirm first, last name of player
        ##add try, EOF error to exit; error if not match regex and continue
        while True:
            player = input("Player: ").title()
            if player == "None":
                break
            finish = input("W or L? ").upper()
            #add each result to players list as dict
            round.append({"player":player, "finish": finish, "game": game})

        #return list of dicts w/ players, W or L, game name
        return round

    else:
        sys.exit(("See games supported by leaderboard:\nCatan\nCharterstone\nScythe\nViticulture\nTicket To Ride"))



def view_stats(leaderboard):

    try:
        open_leaderboard(leaderboard)
    except FileNotFoundError:
        sys.exit("This leaderboard doesn't have game entries yet")

    #split for readability- not necessary
    print("-----------------------")
    print("Select one:\n[1] Overall Leaderboard\n[2] Player Stats\n[3] Game Stats")
    print("-----------------------")
    response = input().casefold()


    if response == "2":
        stats = player_stats(leaderboard)
        print()
        print(tabulate(stats, headers="keys"))


    elif response == "1":
        print()
        print(overall_leaderboard(player_stats(leaderboard)))


    elif response == "3":
        stats = game_stats(leaderboard)
        print()
        print(tabulate(stats, headers="keys"))


def player_stats(board):
    #python documentation and stackoverflow for using counter
    c = Counter()
    for game in board.played:
        c[game["player"], game["finish"]] += 1


    stats = []


    for k, v in c.items():
        player = k[0]
        finish = k[1]

        if finish == "W":
            stats.append({"Player": player, "Wins": v})
        elif finish == "L":
            stats.append({"Player": player, "Losses": v})

    #compare each dict in stats, update with subsequent win or loss entry
    #remove second entry once first is updated to make complete player dict
    for d in stats:
        x = stats.index(d)
        b = stats[(x + 1):]

        for i in b:
            if d["Player"] == i["Player"]:
                d.update(i)
                stats.remove(i)

    #for each entry in stats, update with 0 if no wins or losses listed
    for gamer in stats:
        if not "Wins" in gamer.keys():
            gamer.update({"Wins": 0})
        elif not "Losses" in gamer.keys():
            gamer.update({"Losses": 0})

    return stats


def game_stats(board):
    #python documentation and stackoverflow for using counter
    selection = input("Enter game\n").title()
    c = Counter()
    for game in board.played:
        if game["game"] == selection:
            c[game["player"], game["finish"]] += 1


    stats = []


    for k, v in c.items():
        player = k[0]
        finish = k[1]

        if finish == "W":
            stats.append({"Player": player, "Wins": v})
        elif finish == "L":
            stats.append({"Player": player, "Losses": v})

    #compare each dict in stats, update with subsequent win or loss entry
    #remove second entry once first is updated to make complete player dict
    for d in stats:
        x = stats.index(d)
        b = stats[(x + 1):]

        for i in b:
            if d["Player"] == i["Player"]:
                d.update(i)
                stats.remove(i)

    #for each entry in stats, update with 0 if no wins or losses listed
    for gamer in stats:
        if not "Wins" in gamer.keys():
            gamer.update({"Wins": 0})
        elif not "Losses" in gamer.keys():
            gamer.update({"Losses": 0})

    return stats



def overall_leaderboard(player_stats):

    overall = []
    for line in player_stats:
        total_played = line["Wins"] + line["Losses"]
        win_rate = (line["Wins"]/total_played) * 100
        overall.append({"Player": line["Player"], "Win Rate": f'{win_rate:.02f}%'})

    #sort overall board in reverse order of win rate
    sorted_leaderboard = sorted(overall, key = lambda x: x["Win Rate"], reverse=True)

    return(tabulate(sorted_leaderboard, headers = "keys"))




def open_leaderboard(x):
        #open txt file created by gamelist function
    with open(f"{x.filename}.txt") as file:
        #readlines and add to played list(global variable)
        games = file.readlines()
        for game in games:
            #eval converts back to dict when writing to list, found how to do this on stackoverflow
             x.played.append(eval(game.rstrip()))

if __name__ == "__main__":
    main()
