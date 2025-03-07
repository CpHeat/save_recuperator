import json
from functions import transfer_savegames

with open("games.json", "r") as file:
    games = json.load(file)


def select_mode():
    direction = input("Voulez-vous importer ou exporter vos sauvegardes ? (import/export)")
    if (direction == "import") or (direction == "i") or (direction == "export") or (direction == "e"):
        transfer_savegames(direction, username, games)
    else:
        print("Mauvaise entrée, réessayez")
        select_mode()

if __name__ == '__main__':
    username = input("Quel est le nom du dossier utilisateur ?")
    select_mode()