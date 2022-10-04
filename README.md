# Random Steam Game Picker

## What it does
- Gets a list of all your games and hours on steam
- Can remove certain games you don't wish to include
- Selects a random game from your collection to play
    - Lets you select a random game from only your unplayed games
- Gives you a summary of statistics about your games
    - Total games owned
        - Total games played
        - Total games unplayed
    - Total hours played
        - Total hours played per hour ranges

## What you will need
- You will need python
- You will need a Steam Web Api Key
    - [Can be got here](https://steamcommunity.com/dev/apikey)
- You will need your Steam Id
    - You will either need:
        - Your actual steam id
        - Your steam vanity from the end of your accounts url

## Reason for Creation

This was made for me to be able to get a list of all my games on steam. Specifically to sort out the unplayed games. Then select a random unplayed game for me to play.

## Running the Python Script
Windows
- Initial Run
    - cd /your/folder
    - python3 -m venv env
    - call env/Scripts/activate.bat
    - python3 -m pip install -r requirements.txt
    - python3 Random_Steam_Game_Picker.py
- Running After
    - cd /your/folder
    - call env/Scripts/activate.bat && python3 Random_Steam_Game_Picker.py
Linux
- Initial Run
    - cd /your/folder
    - python3 -m venv env
    - source env/bin/activate
    - python3 -m pip install -r requirements.txt
    - python3 Random_Steam_Game_Picker.py
- Running After
    - cd /your/folder
    - source env/bin/activate && python3 Random_Steam_Game_Picker.py