import Environment
from MyAgentChest import MyAgentChest
from MyAgentGold import MyAgentGold
from MyAgentStones import MyAgentStones
import random
from queue import PriorityQueue
import math

class TacheAllocation :
    
    """
    Pour la methode d'allocation des taches, nous utilisons la methode des enchere Anglaise où chaque agent 
    encherie une offre de tresor suivant sa capacité en envoyant sa distance entre lui et le tresor et l'agent ayant la plus petite distance remporte l'enchere
    """

    def __init__(self,env:Environment):
        self.env = env
        self.auctions = [] #liste pour gerer les encheres
        self.grid = self.construire_grille_unifiee()  # 0 pour libre, 1 pour obstacle

    #cette fonction permet de recuperer les case vide de la grille ou non occupées, on met a 0 leur valeur et 1 sinon
    def construire_grille_unifiee(self):
    # Créer une grille avec 0 pour les cases libres
        grid = [[0 for _ in range(self.env.tailleX)] for _ in range(self.env.tailleY)]
    
    # Marquer les positions des agents comme obstacles dans la grille
        for x in range(self.env.tailleX):
            for y in range(self.env.tailleY):
                if self.env.grilleAgent[x][y] is not None:
                    grid[x][y] = 1  # 1 pour un obstacle
    
    # Note: Pas besoin de marquer les trésors pour le calcul du chemin, 
    # mais vous pouvez choisir de le faire si cela influence le calcul du chemin
        return grid

    #cette fonction permet de lancer ou plutot d'initialiser une enchere pour un tresor pour l'allocation des taches
    def start_auction_for_treasure(self, treasure,i,j):
        # Initialiser une enchère pour un trésor donné
        self.auctions.append({'treasure': treasure, 'bids': {},'position':(i,j)})

    #cette fonction permet de retrouver l'enchere correspondant a une offre ou chaque agent fait sont offre
    def bid_on_treasure(self, agent_id, treasure, bid_amount):
        # Trouver l'enchère correspondante et enregistrer l'offre
        for auction in self.auctions:
            if auction['treasure'] == treasure:
                auction['bids'][agent_id] = bid_amount
                break
    """ cette fonction permet de faire la resolution de l'enchere d'un tresor donnée c'est a dire attribuer le tresor l'agent
    ayant fait la meilleur proposition en terme de distance ou de proximité avec le tresor en question
    """
    def resolve_auctions(self):
        # Attribuer chaque trésor à l'offre la plus élevée et vider les enchères
        for auction in self.auctions:
            highest_bid = min(auction['bids'].items(), key=lambda x: x[1])
            agent_id, bid_amount = highest_bid
            # Ici, vous devez déplacer le trésor vers l'agent ou vice versa, selon votre logique de jeu
            agent = self.env.agentSet[agent_id]
            agent.bag_contents.append({"treasure":auction['treasure'],"position":auction['position']})
            print(f"Agent {agent_id} wins auction for treasure : {auction['treasure']} with bid {bid_amount}")
        self.auctions.clear()

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.env.tailleX and 0 <= y < self.env.tailleY and (self.env.grilleAgent[x][y] is None or self.env.grilleTres[x][y] is None) and id != self.env.posUnload

    def passable(self, id):
        (x, y) = id
        return self.grid[x][y] == 0
    
    """
    Cette methode permet de trouver la case voisine d'une case donnée poour faire un move 
    """
    def neighbors(self, id):
        (x, y) = id
        # Inclut les directions diagonales
        result = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]  
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]) and self.passable((nx, ny)):
                result.append((nx, ny))
        return result
    #dans cette fonction nous definissons le coup d'un deplace qui est de 1 pour notre cas
    def cost(self, from_node, to_node):
        return 1  # Ou une logique plus complexe si certains mouvements coûtent plus cher
        
    #dans cette fonction nous recuperrons l'enssemble des agents et nous les retournant en fonction de leur type
    def getAgent(self):
        pierre,por,somme  =  self.getTresor()
        #print(pierre)
        #print(por)
        ramasseurOR=[]
        ramasseurPierre=[]
        Deverouilleur=[]
        for i in range(self.env.tailleX):
             for j in range(self.env.tailleY):
                if self.env.grilleAgent[i][j] is not None:
                    if type(self.env.grilleAgent[i][j]) == MyAgentStones:
                        ramasseurPierre.append(self.env.grilleAgent[i][j])
                    elif type(self.env.grilleAgent[i][j]) == MyAgentChest:
                        Deverouilleur.append(self.env.grilleAgent[i][j])
                    elif type(self.env.grilleAgent[i][j]) == MyAgentGold:
                        ramasseurOR.append(self.env.grilleAgent[i][j])
        return (ramasseurPierre,ramasseurOR,Deverouilleur)
    

    def getTresor(self):
        pierre = []
        somme =0
        por = []
        for i in range(self.env.tailleX):
             for j in range(self.env.tailleY):
                if self.env.grilleTres[i][j] is not None:
                    if self.env.grilleTres[i][j].type == 1:
                        somme +=self.env.grilleTres[i][j].value
                        pierre.append([i,j])
                    elif self.env.grilleTres[i][j].type == 2:
                        somme +=self.env.grilleTres[i][j].value
                        por.append([i,j])
        
        return(pierre,por,somme)
        
    

    """cette methode nous permet de calculer la distance entre un agent et un tresor donnée.
    Nous utilisons la distance euclidienne vu que les deplacement en diagonale son autorisés 
    """
    def euclidean_distance(self,start, goal):
        """
        Calcule la distance euclidienne entre deux points 'start' et 'goal'.
        
        Args:
            start (tuple): Coordonnées (x, y) du point de départ.
            goal (tuple): Coordonnées (x, y) du point d'arrivée.
        
        Returns:
            float: La distance euclidienne entre les deux points.
        """
        (x1, y1) = start
        (x2, y2) = goal
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    #cette methode permet de reconstruoire le chemin à parcourrir par un agent pour atteindre un objectif cad aller ramasser ou ouvrir le coffre d'un tresor
    def reconstruct_path(self,came_from, start, goal):
        """
        Reconstruit le chemin trouvé par l'algorithme A* du point d'arrivée au point de départ.

        Args:
            came_from (dict): Un dictionnaire qui enregistre pour chaque nœud le nœud précédent.
            start (tuple): Coordonnées du point de départ.
            goal (tuple): Coordonnées du point d'arrivée.

        Returns:
            list: Le chemin du point de départ au point d'arrivée, incluant les deux.
        """
        current = goal
        path = []
        while current != start:  # Remonte le chemin à partir du goal jusqu'au start
            path.append(current)
            current = came_from[current]
        path.append(start)  # optional, ajoute le point de départ à la fin du chemin
        path.reverse()  # inverse le chemin pour qu'il commence par le point de départ
        return path

    """
    cette methode permet de trouver le chemin le plus court à parcourir entre un agent et sa cible(tresors ou point de collecte)
    """
    def a_star_search(self,start=(0,5), goal=(5,8), grid=None):
        # Initialisation...
        open_set = PriorityQueue()
        open_set.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        
        while not open_set.empty():
            current = open_set.get()
            
            if current == goal:
                break  # Chemin trouvé
            
            for next in grid.neighbors(current):
                new_cost = cost_so_far[current] + grid.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.euclidean_distance(start=next,goal=goal)
                    open_set.put(next, priority)
                    came_from[next] = current
        
        # Reconstruire et retourner le chemin...
        return self.reconstruct_path(came_from=came_from,start=start,goal= goal)
    


    

