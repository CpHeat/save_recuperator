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
    for game in games["UserRelated"]:
        print(f"Processing {game}...")
        process_game(direction, username, games, game, "UserRelated", results)

    for game in games["Public"]:
        print(f"Processing {game}...")
        process_game(direction, username, games, game, "Public", results)

    print(f"Succès : {results["success"]}")
    print(f"Annulations : {results["cancel"]}")
    print(f"Introuvables : {results["not_found"]}")
    print(f"Echecs : {results["failure"]}")


def process_game(direction:str, username:str, games:json, game:str, save_type:str, results:dict):
    if direction == "export" or direction == "e":
        if save_type == "UserRelated":
            full_location = games["UserRelated"][game]["LocationFirstPart"] + username + games["UserRelated"][game]["LocationLastPart"] + games["UserRelated"][game]["FolderName"]
            full_target = EXPORT_LOCATION + game + "/" + games["UserRelated"][game]["FolderName"]
        else:
            full_location = games["Public"][game]["Location"] + "/" + games["Public"][game]["FolderName"]
            full_target = EXPORT_LOCATION + game + "/" + games["Public"][game]["FolderName"]
    else:
        if save_type == "UserRelated":
            full_location = EXPORT_LOCATION + game + "/" + games["UserRelated"][game]["FolderName"]
            full_target = games["UserRelated"][game]["LocationFirstPart"] + username + games["UserRelated"][game]["LocationLastPart"] + games["UserRelated"][game]["FolderName"]
        else:
            full_location = EXPORT_LOCATION + game + "/" + games["Public"][game]["FolderName"]
            full_target = games["Public"][game]["Location"] + games["Public"][game]["FolderName"]

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


# Fonction d'importation des sauvegardes
# def export_savegames(games: json, username: str):
#     results = {
#         "success": [],
#         "cancel": [],
#         "failure": [],
#         "not_found": []
#     }
#
#     # On traite les jeux dont la sauvegarde est dans un sous-dossier du répertoire utilisateur
#     for game in games["UserRelated"]:
#         print(f"Processing {game}...")
#
#         full_location = games["UserRelated"][game]["LocationFirstPart"] + username + games["UserRelated"][game][
#             "LocationLastPart"] + games["UserRelated"][game]["FolderName"]
#         full_target = EXPORT_LOCATION + game + "/" + games["UserRelated"][game]["FolderName"]
#
#         print(f"checking {full_location} for savegames...")
#         sourceFolderExist = os.path.exists(full_location)
#         if sourceFolderExist:
#             result = folder_copy(games, "UserRelated", game, full_location, full_target)
#             if result == "success":
#                 results["success"].append({game})
#             elif result == "cancel":
#                 results["cancel"].append({game})
#             else:
#                 results["failure"].append({game})
#         else:
#             results["not_found"].append({game})
#             print(f"{full_location} introuvable, au suivant")
#
#     # On traite les autres jeux
#     for game in games["Public"]:
#         print(f"Processing {game}...")
#
#         full_location = games["Public"][game]["Location"] + "/" + games["Public"][game]["FolderName"]
#         full_target = EXPORT_LOCATION + game + "/" + games["Public"][game]["FolderName"]
#
#         print(f"checking {full_location} for savegames...")
#         sourceFolderExist = os.path.exists(full_location)
#         if sourceFolderExist:
#             result = folder_copy(games, "Public", game, full_location, full_target)
#             if result == "success":
#                 results["success"].append({game})
#             elif result == "cancel":
#                 results["cancel"].append({game})
#             else:
#                 results["failure"].append({game})
#         else:
#             results["not_found"].append({game})
#             print(f"{full_location} introuvable, au suivant")
#
#     print(f"Succès : {results["success"]}")
#     print(f"Annulations : {results["cancel"]}")
#     print(f"Introuvables : {results["not_found"]}")
#     print(f"Echecs : {results["failure"]}")
#
#
# # Fonction d'exportation des suavegardes
# def import_savegames(games: json, username: str):
#     results = {
#         "success": [],
#         "cancel": [],
#         "failure": [],
#         "not_found": []
#     }
#
#     # On traite les jeux dont la sauvegarde est dans un sous-dossier du répertoire utilisateur
#     for game in games["UserRelated"]:
#         print(f"Processing {game}...")
#
#         full_location = EXPORT_LOCATION + game + "/" + games["UserRelated"][game]["FolderName"]
#         full_target = games["UserRelated"][game]["LocationFirstPart"] + username + games["UserRelated"][game][
#             "LocationLastPart"] + games["UserRelated"][game]["FolderName"]
#
#         print(f"checking {full_location} for savegames...")
#         sourceFolderExist = os.path.exists(full_location)
#         if sourceFolderExist:
#             result = folder_copy(games, "UserRelated", game, full_location, full_target)
#             if result == "success":
#                 results["success"].append({game})
#             elif result == "cancel":
#                 results["cancel"].append({game})
#             else:
#                 results["failure"].append({game})
#         else:
#             results["not_found"].append({game})
#             print(f"{full_location} introuvable, au suivant")
#
#     # On traite les autres jeux
#     for game in games["Public"]:
#         print(f"Processing {game}...")
#
#         full_location = EXPORT_LOCATION + game + games["Public"][game]["FolderName"]
#         full_target = games["Public"][game]["Location"] + games["Public"][game]["FolderName"]
#
#         print(f"checking {full_location} for savegames...")
#         sourceFolderExist = os.path.exists(full_location)
#         if sourceFolderExist:
#             result = folder_copy(games, "Public", game, full_location, full_target)
#             if result == "success":
#                 results["success"].append({game})
#             elif result == "cancel":
#                 results["cancel"].append({game})
#             else:
#                 results["failure"].append({game})
#         else:
#             results["not_found"].append({game})
#             print(f"{full_location} introuvable, au suivant")
#
#     print(f"Succès : {results["success"]}")
#     print(f"Annulations : {results["cancel"]}")
#     print(f"Introuvables : {results["not_found"]}")
#     print(f"Echecs : {results["failure"]}")