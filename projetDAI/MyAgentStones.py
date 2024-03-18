from MyAgent import MyAgent
import math


#inherits MyAgent

class MyAgentStones(MyAgent):

    def __init__(self, id, initX, initY, env, capacity):
        MyAgent.__init__(self, id, initX, initY, env)
        self.bag_contents = []
        self.stone = 0
        self.backPack = capacity
        self.priority=1
        self.goal = []

    # return quantity of precious stones collected and not unloaded yet
    def getTreasure(self):
        return self.stone

    # unload precious stones in the pack back at the current position
    def unload(self):
        self.env.unload(self)
        self.stone = 0

    #return the agent's type
    def getType(self):
        return 2

    # load the treasure at the current position
    def load(self,env):
        env.load(self)

    # add some precious stones to the backpack of the agent (quantity t)
    # if the quantity exceeds the back pack capacity, the remaining is lost
    def addTreasure(self, t):
        if(self.stone + t <= self.backPack) :
            self.stone = self.stone + t
        else :
            self.stone = self.backPack


    def __str__(self):
        res ="agent Stone "+ self.id + " ("+ str(self.posX) + " , " + str(self.posY) + ")"
        return res

    """
    -Cette methode permet à un agent de soumettre une offre pour une enchere d'un tresors
    - l'agent evalue sa distance et sa capacité de sac par rapport à la valeur du tresor
    """
    def make_bid(self, treasure,i,j,tache):
        if treasure.type == 2 and self.backPack - self.stone >= treasure.value:
            distance = self.calculate_distance_to(i,j)
            bid_amount = self.evaluate_bid(distance, self.backPack)
            tache.bid_on_treasure(self.id, treasure, bid_amount)


    def calculate_distance_to(self, i,j):
        #calcul de la distance entre l'agent et le tresor mit en echere
        #utilisation de la distance euclidienne pour prendre en compte les deplacements en diagonal 
        distances_to_treasures = math.sqrt(((i - self.posX)**2 + (j-self.posY )**2))
        return distances_to_treasures

    def evaluate_bid(self, distance, capacity):
        # Formule d'évaluation d'une offre basée sur la distance et la capacité
        bid_value = distance
        return bid_value
    
    #cette methode permet de trouver le chemin vers le tresor le plus proche
    def trouver_chemin_vers_tresor_plus_proche(self, tache):
        # Trouver le trésor le plus proche
        content = self.backPack - self.stone
        treasure = [ t for t in self.bag_contents if (self.backPack - self.stone) >= t['treasure'].value]
         #on test s'il y'a des tresors qui peuvent etre ramasser par l'agent
        # si tel est le cas on selectionne le tresor le plus proche de la l'agent à partir de sa position et on retourne le chemin vers ce tresor
        # sinon on dit tout simplement à l'agent d'aller vider son sac et de revenir chercher le tresor en retournant le chemin vers le point de collecte
        if treasure:
            t = treasure[0]
            chemin = tache.a_star_search(start=(self.posX,self.posY), goal=t["position"],grid=tache)
            min = len(chemin)
            for tr in treasure[1:]:
                c = tache.a_star_search(start=(self.posX,self.posY), goal=tr["position"],grid=tache)
                if min > len(c):
                    min = len(c)
                    chemin = c
                    t = tr
            return chemin,t
        else:
            chemin_vers_depot = tache.a_star_search(start=(self.posX,self.posY), goal=self.env.posUnload,grid=tache)
            return chemin_vers_depot, None
        

    """
    l'agent construit son plan individuel à partir de cette methode.
    L'agent construis son chemin vers le tresors le plus proche ensuite à partir de là aller vers le tresor le plus proche de sa position si 
    sa capacité de sac restant le lui permet sinon il se dirige vers le point de collecte pour decharger son sac et ensuite aller vers le trésor le plus proche pour le ramasser
    """
        
    def planindividuel(self,tache):
        x,y = self.posX,self.posY
        while self.bag_contents:
            objectif,treasure = self.trouver_chemin_vers_tresor_plus_proche(tache)
            self.plan.extend(objectif[1:])
            if treasure:
                self.stone = self.stone + treasure["treasure"].value
                self.posX,self.posY = treasure['position']
                self.goal.append(treasure['position'])
                self.bag_contents.remove(treasure)
            else:
                self.posX,self.posY = self.env.posUnload
                self.goal.append(self.env.posUnload)
                self.stone=0
        chemin_vers_depot = tache.a_star_search(start=(self.posX,self.posY), goal=self.env.posUnload,grid=tache)
        self.plan.extend(chemin_vers_depot[1:])
        self.plan.insert(0,(x,y))
        self.goal.append(self.env.posUnload)
        self.posX,self.posY=x,y

    def plan_termine(self):
        # Retourne True si toutes les actions du plan ont été effectuées
        return self.index_plan >= len(self.plan)
        
    #Execution du plan d'un agent avec l'ensemble des actions qu'il dois faire
    def executionPlanIndividuel(self):
        x = self.index_plan
        if not self.plan_termine():
            if (self.posX, self.posY) in self.goal:
                if not self.env.isAt(self, self.env.posUnload[0], self.env.posUnload[1]):
                    #si l'agent arrve à une position d'un tresor c'est dire il est à un de ses but qui different du point de collecte alors il fait un load
                    self.env.load(self)
                    self.goal.remove((self.posX, self.posY))
                #sinon il est au point de collect donc il doit faire un unload
                else:
                    #Pour faire un unload il faut qu'il est quelque chose dans son sac 
                    if self.stone > 0:
                        self.unload()
                    #sinon il fait un move
                    else:
                        self.index_plan += 1
                        if x < len(self.plan):
                            coor = self.plan[x]
                            print(self.posX, self.posY, coor[0], coor[1])
                            move = self.move(self.posX, self.posY, coor[0], coor[1])
                            if move != 1:
                                self.posX, self.posY = coor
            #s'il n'est pas dans une des positions de ses buts alors il se deplace
            else:
                self.index_plan += 1
                if x < len(self.plan):
                    coor = self.plan[x]
                    print(self.posX, self.posY, coor[0], coor[1])
                    move = self.move(self.posX, self.posY, coor[0], coor[1])
                    
                    if move != 1:
                        self.posX, self.posY = coor
         #si son plan est fini alors s'il a quelque chose dans son sac il le depose et on le supprime de l'environnement
        else:
            if self.stone > 0 and self.env.isAt(self, self.env.posUnload[0], self.env.posUnload[1]):
                self.unload()
            x, y = self.posX, self.posY
            del self.env.agentSet[self.getId()]
            self.env.grilleAgent[x][y] = None



