#!/usr/bin/env python3
##################################################################################################################################################################
### Importing Modules ###
from datetime import datetime
from os import system
import os
import pathlib
import requests
import json
import random

##################################################################################################################################################################
### User Variables for Steam Web API ###
info = {"key": "", "steamid": ""}  # Dictionary for loading and saving config
##################################################################################################################################################################
### Steam API Variables ###
include_appinfo = "true"  # Include App Info or Not
include_played_free_games = "true"  # Include Free Games or Not
appids_filter = "false"  # This filters something
Steam_Web_API_Game_URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"  # To get game information
Steam_Web_API_Player_URL = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"  # To get a player name
Steam_Web_API_ID_URL = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"  # To get a player id from their vanity url name
##################################################################################################################################################################
### Variables ###
Game_List = {}
Random_Game_List = {}
Random_Game = ""
Player_Stats = ""
key = ""  # Your Steam Web API Key
steamid = ""  # Your Steam User ID
### Directories ###
directory_path = str(pathlib.Path().resolve()) + "/Steam_Files/"  # Base path to save to
directory_path_config = directory_path + "config.json"
directory_path_games = directory_path + "purged_games.json"
directory_path_stats = directory_path + "player_stats.txt"
directory_path_purge = directory_path + "purge_list.txt"
directory_path_unplayed_games = directory_path + "purged_unplayed_games.json"
directory_path_played_games = directory_path + "purged_played_games.json"

##################################################################################################################################################################
### Getting ID from vanity name ###
def GetID(vanity_url, api_key):
    API_Request = (
        Steam_Web_API_ID_URL + "?" + "key=" + api_key + "&" + "vanityurl=" + vanity_url
    )
    ### Calling the API ###
    response_API = requests.get(API_Request)
    raw_info = response_API.json()["response"]  # Filtering the JSON
    steam_id = dict.get(raw_info, "steamid")
    return steam_id


##################################################################################################################################################################
### If config file doesn't exist, run through set up. If it does exist load it. Ask if you have the id or not. If don't use vanity to get id, if not just ask for id.
def CreateInfo_Id():  # 1b
    system("cls")
    User_Input = input("Insert your steam id:\n")
    return User_Input


def CreateInfo_Vanity(api_key):  # 1a ###api key
    system("cls")
    User_Input = input("Insert your steam vanity:\n")
    vanity = ""
    vanity = GetID(User_Input, api_key)
    return vanity


def CreateInfo_Start():  # 1
    system("cls")
    info = {"key": "", "steamid": ""}  # New dictionary
    # Getting the api key
    api_key = ""
    Key_Input = input("Insert your steam web api key:\n")
    api_key = Key_Input
    # Getting the id number
    id_number = ""
    Id_Input = input("Do You have the steam id? (1 or 2):\n")
    Input_Decision = int(Id_Input)
    if Input_Decision == 1:  # If they do have the id
        id_number = CreateInfo_Id()
    elif Input_Decision == 2:  # If they don't have the id
        id_number = CreateInfo_Vanity(api_key)
    else:
        system("cls")
        print("That was not a choice >:(")
        input("Press Enter to Continue")
        CreateInfo_Start()
    # Setting dictionary
    info["key"] = api_key
    info["steamid"] = id_number
    # Saving config file
    with open(directory_path_config, "w") as outputfile:
        json.dump(
            info, outputfile, sort_keys=False, indent=4
        )  # Format and write JSON to file
    return info


# If the config file does exist then load it
def LoadInfo():
    with open(directory_path_config) as inputfile:
        loaded_info = json.load(inputfile)  # Load JON from file
    return loaded_info  # Returning the games loaded from the file


##################################################################################################################################################################
### Getting the API Info and saving the data ###
def Get_Games(games):
    ### Making the full API Call ###
    API_Request = (
        Steam_Web_API_Game_URL
        + "?"
        + "key="
        + key
        + "&"
        + "steamid="
        + steamid
        + "&"
        + "include_appinfo="
        + include_appinfo
        + "&"
        + "include_played_free_games="
        + include_played_free_games
        + "&"
        + "appids_filter="
        + appids_filter
    )
    ### Calling the API ###
    response_API = requests.get(API_Request)
    ### Getting Data ###
    raw_games = response_API.json()["response"]["games"]  # Filtering the JSON
    ### Converting the JSON into a Dictionary ###
    played_games = {}  # Making an empty dictionary for the games
    for x in raw_games:  # Going through all games in the JSON
        game_title = x["name"]  # Getting the game title
        game_time = x["playtime_forever"]  # Getting the game time in minutes
        game_time_hours = round(
            game_time / 60, 2
        )  # Converting the game time into hours
        played_games[
            game_title
        ] = game_time_hours  # Adding the games and game times to the dictionary
    ### Sorting the Dictionary by Hours ###
    games_ordering = sorted(
        played_games.items(), key=lambda x: x[1], reverse=True
    )  # Sorting the games by their hours
    games_ordered = dict(games_ordering)  # Making a new dictionary for the sorted games
    ### Loading a list of the purged games ###
    purge_list = []  # New list for the purged names
    with open(directory_path_purge, "r") as f:
        purge_list = (
            f.read().splitlines()
        )  # Reading the text file with games to not include
    ### Purging the unwanted games ###
    purged_games = {}  # New dictionary for purging unwanted entries from the dictionary
    for x in games_ordered:  # Checking every game in the dictionary
        if x not in purge_list:  # Checking the dictionary values against the purge list
            time_value = games_ordered.get(x)  # Getting the time value for the game
            purged_games[x] = time_value  # Adding the value to the new dictionary
    ### Saving Game Results ###
    with open(directory_path_games, "w") as outputfile:
        json.dump(
            purged_games, outputfile, sort_keys=False, indent=4
        )  # Format and write JSON to file
    ### Adding the games to the Dictionary for later use ###
    return purged_games  # Returning the games that were just saved


##################################################################################################################################################################
### Loading data from a json file ###
def Load_Games(games):
    with open(directory_path_games) as purged_file:
        try:
            loaded_games = json.load(purged_file)  # Load JON from file
            pass
        except:
            system("cls")
            print("Games list was empty. Using API insttead")
            input("Press Enter to Continue")
            loaded_games = Get_Games(purged_file)
            pass
    return loaded_games  # Returning the games loaded from the file


##################################################################################################################################################################
### Getting Profile Name ###
def GetProfile(username):
    API_Request = (
        Steam_Web_API_Player_URL + "?" + "key=" + key + "&" + "steamids=" + steamid
    )
    ### Calling the API ###
    response_API = requests.get(API_Request)
    raw_info = response_API.json()["response"]["players"]  # Filtering the JSON
    for x in raw_info:
        steam_name = x["personaname"]
    return steam_name


##################################################################################################################################################################
### Getting the first choice from the User about what data to get from ###
def First_Choice(games):
    system("cls")
    get_games = {}  # Dictionary to hold the games from the users choice
    User_Choice = input(
        "Do you want to call the API or Load from a previous file? (1 or 2):\n"
    )
    User_Decision = int(User_Choice)
    if User_Decision == 1:
        get_games = Get_Games(get_games)  # Getting games from the steam web api
    elif User_Decision == 2:
        get_games = Load_Games(get_games)  # Getting the games from loading
    else:
        system("cls")
        print("That was not a choice >:(")
        input("Press Enter to Continue")
        First_Choice()
    return get_games  # Returning the games from the users choice


##################################################################################################################################################################
### Check if directory exits ###
if os.path.exists(directory_path) == False:  # Make the directory if it doesn't exist
    os.mkdir(directory_path)
### Checking if the config file exists ###
# if it exists load it
if os.path.exists(directory_path_config):  # load it if it exists
    info = LoadInfo()
else:  # create it if it doesn't exist
    info = CreateInfo_Start()
key = dict.get(info, "key")
steamid = dict.get(info, "steamid")
##################################################################################################################################################################
### Check if other files exist. If not create them ###
if os.path.exists(directory_path_games) == False:
    new_file = open(directory_path_games, "x")
    new_file.close()
if os.path.exists(directory_path_purge) == False:
    new_file = open(directory_path_purge, "x")
    new_file.close()
if os.path.exists(directory_path_stats) == False:
    new_file = open(directory_path_stats, "x")
    new_file.close()
if os.path.exists(directory_path_unplayed_games) == False:
    new_file = open(directory_path_unplayed_games, "x")
    new_file.close()
if os.path.exists(directory_path_played_games) == False:
    new_file = open(directory_path_played_games, "x")
    new_file.close()
##################################################################################################################################################################
### Starting user experience by calling the First Choice ###
Game_List = First_Choice(Game_List)
##################################################################################################################################################################
def Save_games(played_games, unplayed_games):
    ### Saving Unplayed Game Results ###
    with open(directory_path_unplayed_games, "w") as outputfile:
        json.dump(
            unplayed_games, outputfile, sort_keys=False, indent=4
        )  # Format and write JSON to file
    ### Saving Played Game Results ###
    with open(directory_path_played_games, "w") as outputfile:
        json.dump(
            played_games, outputfile, sort_keys=False, indent=4
        )  # Format and write JSON to file


##################################################################################################################################################################
def Remove_Played_Games():
    unplayed_games = {}  # New dictionary for unplayed games
    played_games = {}  # New dictionary for played games
    for x in Game_List:  # Checking every game in the game list
        play_time = Game_List.get(x)  # Get time value
        if play_time == 0:  # If the game hasn't been played
            unplayed_games[
                x
            ] = play_time  # Adding games with no playtime to the dictionary
        else:  # If the game has been played
            played_games[x] = play_time  # Adding games with playtime to the dictionary
    Save_games(
        played_games, unplayed_games
    )  # Saving the games separately because I feel like it
    return unplayed_games  # Returning the unplayed games


##################################################################################################################################################################
### Starting the Second Choice To Get Rid Of Unplayed Games ###
def Second_Choice():
    system("cls")
    get_games = {}  # Dictionary to hold the games from the users choice
    User_Choice = input(
        "Do you want to seperate out games with no playtime? (1 or 2):\n"
    )
    User_Decision = int(User_Choice)
    if User_Decision == 1:
        get_games = Remove_Played_Games()  # Removing played games
    elif User_Decision == 2:
        get_games = Game_List  # Passthrough all games
    else:
        system("cls")
        print("That was not a choice >:(")
        input("Press Enter to Continue")
        Second_Choice()
    return get_games  # Returning the games from the users choice


##################################################################################################################################################################
### Starting to question removing played games ###
Random_Game_List = Second_Choice()
##################################################################################################################################################################
### Do they want to select a Random Game to Play ###
def Third_Choice(game):
    system("cls")
    User_Choice = input("Do you want to select a random game? (1 or 2):\n")
    User_Decision = int(User_Choice)
    if User_Decision == 1:  # Get a random game
        game = random.choice(list(Random_Game_List))
        game_hours = Random_Game_List.get(game)
        output = (
            "Random Game:\n" + game + "\nWith " + str(game_hours) + " hours played"
        )  ###
    elif User_Decision == 2:
        output = "No random game wanted"
    else:
        system("cls")
        print("That was not a choice >:(")
        input("Press Enter to Continue")
        Second_Choice()
    return output


##################################################################################################################################################################
### Asking about wanting a random game ###
Random_Game = Third_Choice(Random_Game)
system("cls")
print(Random_Game)
input("Press Enter to Continue")  # Wait until input until continuing
##################################################################################################################################################################
### Getting Game Stats ###
def Get_Game_Stats():
    ### Variables ####
    Total_Hours = 0
    Total_Games = 0
    Played_Games = 0
    Unplayed_Games = 0
    # Extra Variables#
    More_Than_1000 = 0
    Between_500_1000 = 0
    Between_250_500 = 0
    Between_100_250 = 0
    Between_50_100 = 0
    Between_25_50 = 0
    Between_20_25 = 0
    Between_15_20 = 0
    Between_10_15 = 0
    Between_5_10 = 0
    Between_1_5 = 0
    Less_Than_1 = 0
    ### Get Game Counts & Total Hours Played###
    for x in Game_List:  # Checking every game in the game list
        play_time = Game_List.get(x)  # Get time value
        Total_Games += 1  # Adding one to the total games
        if play_time == 0:  # If Game hasn't been played
            Unplayed_Games += 1  # Adding one to the uplayed games
        else:  # If Game has been played
            Played_Games += 1  # Adding one to the played games
            Total_Hours += play_time  # Adding hours to total playtime
            if play_time >= 1000:
                More_Than_1000 += 1
            elif play_time >= 500 and play_time < 1000:
                Between_500_1000 += 1
            elif play_time >= 250 and play_time < 500:
                Between_250_500 += 1
            elif play_time >= 100 and play_time < 250:
                Between_100_250 += 1
            elif play_time >= 50 and play_time < 100:
                Between_50_100 += 1
            elif play_time >= 25 and play_time < 50:
                Between_25_50 += 1
            elif play_time >= 20 and play_time < 25:
                Between_20_25 += 1
            elif play_time >= 15 and play_time < 20:
                Between_15_20 += 1
            elif play_time >= 10 and play_time < 15:
                Between_10_15 += 1
            elif play_time >= 5 and play_time < 10:
                Between_5_10 += 1
            elif play_time >= 1 and play_time < 5:
                Between_1_5 += 1
            elif play_time > 0 and play_time < 1:
                Less_Than_1 += 1
    Total_Hours = round(Total_Hours, 2)  # Rounding total hours
    steam_name = ""
    steam_name = GetProfile(steam_name)  # Getting steam name
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = (
        "Username: "
        + str(steam_name)
        + "\nId: "
        + str(steamid)
        + "\n------------------------"
        + "\nTime: "
        + str(current_time)
        + "\n------------------------"
        + "\nTotal Hours: "
        + str(Total_Hours)
        + "\n------------------------"
        + "\nTotal Games: "
        + str(Total_Games)
        + "\n------------------------"
        + "\nPlayed Games: "
        + str(Played_Games)
        + "\nUnplayed Games: "
        + str(Unplayed_Games)
        + "\n------------------------"
        + "\nPlayed Games Breakdown: "
        + "\nOver 1000: "
        + str(More_Than_1000)
        + "\nBetween 500 & 1000: "
        + str(Between_500_1000)
        + "\nBetween 250 & 500: "
        + str(Between_250_500)
        + "\nBetween 100 & 250: "
        + str(Between_100_250)
        + "\nBetween 50 & 100: "
        + str(Between_50_100)
        + "\nBetween 25 & 50: "
        + str(Between_25_50)
        + "\nBetween 20 & 25: "
        + str(Between_20_25)
        + "\nBetween 15 & 20: "
        + str(Between_15_20)
        + "\nBetween 10 & 15: "
        + str(Between_10_15)
        + "\nBetween 5 & 10: "
        + str(Between_5_10)
        + "\nBetween 1 & 5: "
        + str(Between_1_5)
        + "\nLess Than 1: "
        + str(Less_Than_1)
    )
    ### Saving stats to a text document ###
    with open(directory_path_stats, "w") as outputfile:
        outputfile.writelines(output)
    ### Return output ###
    return output


##################################################################################################################################################################
### Do they want a sumamry of their stats ###
def Fourth_Choice():
    system("cls")
    output = ""
    User_Choice = input("Do you want player stats? (1 or 2):\n")
    User_Decision = int(User_Choice)
    if User_Decision == 1:  # Get player stats
        print("test")
        output = Get_Game_Stats()
    elif User_Decision == 2:
        output = "No stats wanted"
    else:
        system("cls")
        print("That was not a choice >:(")
        input("Press Enter to Continue")
        Second_Choice()
    return output


##################################################################################################################################################################
### Asking about if they want Player Stats ###
Player_Stats = Fourth_Choice()
system("cls")
print(Player_Stats)
input(
    "Press Enter to Exit"
)  # Prevent the application from closing until an input is given
