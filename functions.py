import json
import os
import shutil
from dotenv import load_dotenv

load_dotenv()
EXPORT_LOCATION = os.getenv('EXPORT_LOCATION')

def transfer_savegames(direction:str, username:str, games:json):
    results = {
        "success": [],
        "cancel": [],
        "failure": [],
        "not_found": []
    }

    # On traite les jeux dont la sauvegarde est dans un sous-dossier du répertoire utilisateur
    for game in games["user_related"]:
        print(f"Processing {game}...")
        process_game(direction, username, games, game, "user_related", results)

    for game in games["Public"]:
        print(f"Processing {game}...")
        process_game(direction, username, games, game, "Public", results)

    print(f"Succès : {results["success"]}")
    print(f"Annulations : {results["cancel"]}")
    print(f"Introuvables : {results["not_found"]}")
    print(f"Echecs : {results["failure"]}")


def process_game(direction:str, username:str, games:json, game:str, save_type:str, results:dict):
    if direction == "export" or direction == "e":
        if save_type == "user_related":
            full_location = games["user_related"][game]["location_start"] + username + games["user_related"][game]["location_end"] + games["user_related"][game]["folder"]
            full_target = EXPORT_LOCATION + game + "/" + games["user_related"][game]["folder"]
        else:
            full_location = games["Public"][game]["location"] + "/" + games["Public"][game]["folder"]
            full_target = EXPORT_LOCATION + game + "/" + games["Public"][game]["folder"]
    else:
        if save_type == "user_related":
            full_location = EXPORT_LOCATION + game + "/" + games["user_related"][game]["folder"]
            full_target = games["user_related"][game]["location_start"] + username + games["user_related"][game]["location_end"] + games["user_related"][game]["folder"]
        else:
            full_location = EXPORT_LOCATION + game + "/" + games["Public"][game]["folder"]
            full_target = games["Public"][game]["location"] + games["Public"][game]["folder"]

    if os.path.exists(full_location):
        result = folder_copy(game, full_location, full_target)
        if result == "success":
            results["success"].append({game})
        elif result == "cancel":
            results["cancel"].append({game})
        else:
            results["failure"].append({game})
    else:
        results["not_found"].append({game})
        print(f"{full_location} introuvable, au suivant")


# Fonction de copie
def folder_copy(game: str, location: str, target: str):
    print(f"{location} exists. Copie des fichiers..")
    if os.path.exists(target):
        replace = input(f"Un dossier existe déjà pour {game}, le remplacer ? (y/n)")
        if replace == "y":
            shutil.rmtree(target)
            shutil.copytree(location, target)
            print("Copie terminée, au suivant")
            return "success"
        else:
            print("Copie annulée, au suivant")
            return "cancel"
    else:
        shutil.copytree(location, target)
        print("Copie terminée, au suivant")
        return "success"