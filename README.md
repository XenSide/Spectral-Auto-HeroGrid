# Changes in this fork
v1.2
1. Added a filter (-fv) for low games, it has two options: op (onepercent) or median (which is default and the same functionality of "Remove low picks" in the web version of Spectral.gg)
1. Added a sort (-s) choice where you can choose to sort either for rank or for number of matches, sorting by matches offers a more neutral overview of the current meta while sorting for rank offers more niche but very powerful heroes

v1.0
1. Reduced the columns from 3 to 2 (from 25+ rank to 50+ rank only) 
1. Added a specific Hard Support and Soft Support tab, removed the mixed "Support" tab

![image](https://i.imgur.com/hRrqf2q.png)
![image](https://i.imgur.com/oPpCi7S.jpeg)

# Windows guide

1. Install [Python](https://www.microsoft.com/en-us/p/python-38/9mssztt1n39l) and download [this package](https://github.com/derac/Auto-Dota2-Hero-Grid/archive/refs/heads/master.zip).
1. `Unzip` and `open` the folder in file explorer.
1. `Shift+right click` empty space in the folder and click `Open PowerShell window here`.
1. Type `pip install requests` and press `Enter`
1. Type `python generate-grid.py` and press `Enter`

A personal suggestion of mine is using the league for your current patch instead of leaving the default one (last week Immortal meta) by typing `python generate-grid.py -l LEAGUENAME` where LEAGUENAME is taken from the [Spectral.gg league list](https://stats.spectral.gg/lrg2/?cat=ranked)

# Linux usage

1. `pip install requests`

1. `python generate-grid.py -steam_install_path /THE/PATH/TO/STEAM --user_id YOUR_STEAM_USER_ID`

The tier lists will be saved with a S! prefix. Anything with an S! prefix will get deleted when this is run to allow for quick updating.

A special thanks to [leamare](https://github.com/leamare) for [spectral.gg](https://spectral.gg/) and its API, a godsend for dota 2 stats. Check his [ingame hero builds](https://github.com/leamare/nerds-builds/blob/master/BUILDS.md) out aswell!

