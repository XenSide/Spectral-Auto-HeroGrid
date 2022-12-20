import os
import json
import datetime
import argparse

import requests

parser = argparse.ArgumentParser()
parser.add_argument(
    "-steam_install_path",
    "-p",
    type=str,
    help="If you don't enter the Steam install path, the script will try to get it from the Windows registry.",
)
parser.add_argument(
    "-user_id",
    "-u",
    type=str,
    help="If you don't enter the user_id, the script will try to write to every user on the system.",
)
parser.add_argument(
    "-league",
    "-l",
    default="imm_ranked_meta_last_7",
    type=str,
    help="If you don't enter a custom league, the script will use the most recent \"Immortal Last 7 days\".",
)
parser.add_argument("-verbose", "-v", action="store_true", help="Show debug info.")
parser.add_argument("-filtervar", "-fv", default="median", type=str, help="median or op (One percent), note that while using OP the specific role pages might break")
parser.add_argument("-sortby", "-s", default="rank", type=str, help="Sort by either rank or matches \(number of matches\)")
args = parser.parse_args()
parser.print_help()
print()



print("Using league = "+args.league)

if not args.steam_install_path:
    print("Attempting to get Steam install path from registry.")
    try:
        import winreg

        steam_path = winreg.QueryValueEx(
            winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam"
            ),
            "InstallPath",
        )[0]
    except:
        print(
            "Cannot get steam install path from the registry, make sure you define steam_install_path in the command line arguments."
        )
else:
    steam_path = args.steam_install_path

date_str = datetime.date.today().strftime(" %d-%m-%Y")
spec_url = f"https://stats.spectral.gg/lrg2/api/?league={args.league}&mod=heroes-positions-position_"
spec_pos = {
    "Core Safelane": "1.1",
    "Core Midlane": "1.2",
    "Core Offlane": "1.3",
    "Hard Support": "0.1",
    "Soft Support": "0.3",
}

pos_confs = []  # Create tier configs from spectral.gg
all_roles = {"config_name": "S! All Roles " + date_str, "categories": []}
for pos_num, (pos_name, pos_endpoint) in enumerate(spec_pos.items()):
    hero_data = json.loads(requests.get(spec_url + pos_endpoint).content)["result"][pos_endpoint]

    if(args.filtervar.lower() == "median"):
        #Use these to calculate a hero picks median to use as value for filtervar
        hero_matches = sorted([(data["matches_s"], hero_id) for hero_id, data in hero_data.items()], key=lambda x: -x[0],)
        median = int(hero_matches[int(len(hero_matches)/2)][0])
        filtervar =  median #edit this variable with a minimum number of games acceptable, the median variable can be used to mimic spectral.gg "remove low matches" filter
    elif(args.filtervar.lower() == "op"):
        #Use these to calculate a PERCENTAGE of all games played as a value for filtervar
        hero_matches_total = sum(d['matches_s'] for d in hero_data.values() if d)
        OPhero_matches_total = hero_matches_total * 0.01 #OnePercent    
        filtervar =  OPhero_matches_total #edit this variable with a minimum number of games acceptable, the median variable can be used to mimic spectral.gg "remove low matches" filter
    else:
        print("invalid filtervar, try again")
        quit()
    if (args.sortby.lower() == "rank"):
        hero_ranks = sorted([(data["rank"], hero_id , data["matches_s"]) for hero_id, data in hero_data.items() if data['matches_s'] > filtervar], key=lambda x: -x[0],)

        #print(hero_ranks)
        pos_conf = {
            "config_name": "S! " + pos_name + date_str,
            "categories": [
                {
                    "category_name": chr(65 + i) + " tier - rank %s+" % (100 - 5 * i - 5),
                    "x_position": i // 5 * 550 + 150,
                    "y_position": (i % 5) * 120,
                    "width": 400,
                    "height": 100,
                    "hero_ids": [id for rank, id, matches in hero_ranks if (100 - 5 * i) >= rank > (100 - 5 * i - 5)],
                }
                for i in range(10)
            ],
        }
        pos_confs.append(pos_conf)
        print("Processed", pos_name + ".")
        all_roles["categories"].append(
            {
                "category_name": pos_name,
                "x_position": 0,
                "y_position": pos_num * 120,
                "width": 1200,
                "height": 100,
                "hero_ids": [id for rank, id, matches in hero_ranks[:20]],
            }
        )
    elif(args.sortby.lower() == "matches"):
        hero_ranks = sorted([(data["matches_s"], hero_id , data["rank"]) for hero_id, data in hero_data.items() if data['matches_s'] > filtervar], key=lambda x: -x[0],)

        #print(hero_ranks)
        pos_conf = {
            "config_name": "S! " + pos_name + date_str,
            "categories": [
                {
                    "category_name": chr(65 + i) + " tier - rank %s+" % (100 - 5 * i - 5),
                    "x_position": i // 5 * 550 + 150,
                    "y_position": (i % 5) * 120,
                    "width": 400,
                    "height": 100,
                    "hero_ids": [id for matches ,id, rank in hero_ranks if (100 - 5 * i) >= rank > (100 - 5 * i - 5)],
                }
                for i in range(10)
            ],
        }
        pos_confs.append(pos_conf)
        print("Processed", pos_name + ".")
        all_roles["categories"].append(
            {
                "category_name": pos_name,
                "x_position": 0,
                "y_position": pos_num * 120,
                "width": 1200,
                "height": 100,
                "hero_ids": [id for matches ,id, rank in hero_ranks[:20]],
            }
        )

    if args.verbose:
        print(pos_conf)

for user_id in (
    os.listdir(os.path.join(steam_path, "userdata"))
    if not args.user_id
    else [args.user_id]
):
    path = os.path.join(steam_path, "userdata", user_id, "570", "remote", "cfg")
    if not os.path.isdir(path):
        continue
    conf_file = os.path.join(path, "hero_grid_config.json")
    if os.path.isfile(conf_file):  # open grid config and delete existing if desired
        with open(conf_file) as f:
            grid_conf = json.load(f)
            print("Grid config loaded.")
        grid_conf["configs"] = (
            [c for c in grid_conf["configs"] if "S!" != c["config_name"][:2]]
            + pos_confs
            + [all_roles]
        )
    else:
        grid_conf = {"version": 3, "configs": []}
        print("Creating new Grid Config file.")

    with open(conf_file, "w") as f:
        print(json.dumps(grid_conf, indent=4), file=f)
        print("Grid Config written.", conf_file)