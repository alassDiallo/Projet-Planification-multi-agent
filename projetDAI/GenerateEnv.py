import random
import os

class Treasure:
    def __init__(self, type, posX, posY, value):
        self.type = type
        self.posX = posX
        self.posY = posY
        self.value = value

    def to_string(self):
        return f"tres:{self.type}:{self.posX}:{self.posY}:{self.value}"

class Agent:
    def __init__(self, type, posX, posY, capacity=None):
        self.type = type
        self.posX = posX
        self.posY = posY
        self.capacity = capacity

    def to_string(self):
        if self.capacity is not None:
            return f"AG:{self.type}:{self.posX}:{self.posY}:{self.capacity}"
        else:
            return f"AG:{self.type}:{self.posX}:{self.posY}"

class Environment:
    def __init__(self, sizeX, sizeY, num_treasures, num_agents):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.num_treasures = num_treasures
        self.num_agents = num_agents
        self.treasures = []
        self.agents = []

    def generate_treasures(self):
        for _ in range(self.num_treasures):
            type = random.choice(["or", "pierres"])
            posX = random.randint(0, self.sizeX - 1)
            posY = random.randint(0, self.sizeY - 1)
            value = random.randint(1, 10)
            treasure = Treasure(type, posX, posY, value)
            self.treasures.append(treasure)

    def generate_agents(self):
        for _ in range(self.num_agents):
            type = random.choice(["or", "pierres", "ouvr"])
            posX = random.randint(0, self.sizeX - 1)
            posY = random.randint(0, self.sizeY - 1)
            if type == "chest":
                agent = Agent(type, posX, posY)
            else:
                capacity = random.randint(1, 20)  # Capacité du sac aléatoire
                agent = Agent(type, posX, posY, capacity)
            self.agents.append(agent)

    def to_string(self):
        lines = []
        lines.append("#taille env")
        lines.append(f"{self.sizeX} {self.sizeY}")
        depotX = random.randint(0, self.sizeX - 1)
        depotY = random.randint(0, self.sizeY - 1)
        lines.append("# position depot")
        lines.append(f"{depotX} {depotY}")
        lines.append("# tresors tres:type:posX:posY:value")
        for treasure in self.treasures:
            lines.append(treasure.to_string())
        lines.append("#agents AG:type:posX:posY:backpack")
        for agent in self.agents:
            lines.append(agent.to_string())
        return "\n".join(lines)

# Créer un environnement aléatoire
env = Environment(30, 30, 15, 10)
env.generate_treasures()
env.generate_agents()

# Chemin du répertoire contenant les fichiers env
current_directory = os.getcwd()

# Trouver le dernier numéro de fichier
last_number = 0
for filename in os.listdir(current_directory):
    if filename.startswith("env") and filename.endswith(".txt"):
        file_number = int(filename.split("env")[1].split(".")[0])
        last_number = max(last_number, file_number)

# Incrémenter le dernier numéro de fichier de 1
new_number = last_number + 1

# Créer le nom du nouveau fichier
new_filename = f"env{new_number}.txt"

# Utiliser le nouveau nom de fichier pour écrire les informations de l'environnement
with open(new_filename, "w") as file:
    file.write(env.to_string())

print(f"Le fichier {new_filename} a été créé avec succès dans le répertoire actuel.")

