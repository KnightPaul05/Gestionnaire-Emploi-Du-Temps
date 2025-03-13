import pickle
import os

TASKS_FILE = "tasks.pkl"
UNDO_FILE = "undo.pkl"

def load_tasks():
    """Charge les tâches depuis un fichier si disponible."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "rb") as f:
            return pickle.load(f)
    return []

def save_tasks(tasks):
    """Sauvegarde les tâches dans un fichier."""
    with open(TASKS_FILE, "wb") as f:
        pickle.dump(tasks, f)

def save_undo(tasks):
    """Sauvegarde l'état précédent pour annulation."""
    with open(UNDO_FILE, "wb") as f:
        pickle.dump(tasks, f)

def undo():
    """Annule la dernière modification en restaurant la sauvegarde précédente."""
    if os.path.exists(UNDO_FILE):
        with open(UNDO_FILE, "rb") as f:
            previous_state = pickle.load(f)
        save_tasks(previous_state)
        print("Dernière modification annulée.\n")
        return previous_state
    print("Aucune modification à annuler.\n")
    return load_tasks()

def display_progress_bar(progress, total, length=20):
    """Affiche une barre de progression en ASCII."""
    percent = int((progress / total) * 100) if total > 0 else 100
    filled_length = min(int((progress / total) * length), length) if total > 0 else length
    bar = "█" * filled_length + "-" * (length - filled_length)
    return f"{bar} ({percent}%)"

def list_tasks(tasks):
    """Affiche toutes les tâches enregistrées avec une barre de progression."""
    if not tasks:
        print("Aucune tâche enregistrée.")
    else:
        print("\nListe des tâches :")
        for task in tasks:
            bar = display_progress_bar(task["progress"], task["duration"])
            print(f"- {task['name']:10} : {bar}  {task['progress']}/{task['duration']} min")
    print()

def add_task(tasks, name, duration):
    """Ajoute une nouvelle tâche."""
    try:
        duration = int(duration)
        save_undo(tasks)  # Sauvegarde pour annulation
        tasks.append({"name": name, "duration": duration, "progress": 0})
        save_tasks(tasks)
        print(f"Tâche '{name}' ajoutée avec une durée de {duration} minutes.\n")
    except ValueError:
        print("Erreur : La durée doit être un nombre entier.\n")

def update_task(tasks, name, additional_time):
    """Ajoute du temps à la progression d'une tâche."""
    for task in tasks:
        if task["name"] == name:
            try:
                additional_time = int(additional_time)
                if additional_time < 0:
                    print("Erreur : Le temps ajouté doit être positif.\n")
                    return
                
                save_undo(tasks)  # Sauvegarde pour annulation
                task["progress"] += additional_time
                save_tasks(tasks)
                print(f"Progression mise à jour pour '{name}': {task['progress']}/{task['duration']} minutes.\n")
                return
            except ValueError:
                print("Erreur : La progression doit être un nombre entier.\n")
                return
    print(f"Erreur : Aucune tâche trouvée avec le nom '{name}'.\n")

def clear_task(tasks, name):
    """Supprime une seule tâche."""
    for i, task in enumerate(tasks):
        if task["name"] == name:
            save_undo(tasks)  # Sauvegarde pour annulation
            del tasks[i]
            save_tasks(tasks)
            print(f"Tâche '{name}' supprimée.\n")
            return
    print(f"Erreur : Aucune tâche trouvée avec le nom '{name}'.\n")

def clear_all_tasks():
    """Supprime toutes les tâches enregistrées."""
    save_undo(load_tasks())  # Sauvegarde pour annulation
    save_tasks([])
    print("Toutes les tâches ont été supprimées.\n")

def main():
    """Boucle principale du programme."""
    tasks = load_tasks()
    
    print("=== Gestionnaire de tâches en mode terminal ===")
    print("Commandes disponibles :")
    print("  - add <nom> <durée>   (Ajoute une matière)")
    print("  - update <nom> <temps ajouté>   (Ajoute du temps à la progression)")
    print("  - list   (Affiche toutes les matières avec une barre de progression)")
    print("  - clear <nom>   (Supprime une seule matière)")
    print("  - clear_all  (Supprime toutes les matières)")
    print("  - undo   (Annule la dernière modification)")
    print("  - exit   (Quitte le programme)\n")

    while True:
        command = input("> ").strip().split()

        if not command:
            continue
        
        action = command[0].lower()

        if action == "add" and len(command) == 3:
            add_task(tasks, command[1], command[2])
        elif action == "update" and len(command) == 3:
            update_task(tasks, command[1], command[2])
        elif action == "list":
            list_tasks(tasks)
        elif action == "clear" and len(command) == 2:
            clear_task(tasks, command[1])
        elif action == "clear_all":
            clear_all_tasks()
            tasks = []
        elif action == "undo":
            tasks = undo()
        elif action == "exit":
            print("Fermeture du programme...")
            break
        else:
            print("Commande non reconnue. Tapez 'list' pour voir les tâches ou 'exit' pour quitter.\n")

if __name__ == "__main__":
    main()
