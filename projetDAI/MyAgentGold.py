from MyAgent import MyAgent
import math
#from TacheAllocation import TacheAllocation


#inherits MyAgent

class MyAgentGold(MyAgent):

    def __init__(self, id, initX, initY, env, capacity):
        MyAgent.__init__(self, id, initX, initY, env)
        self.bag_contents = []
        self.gold = 0 # the quantity of gold collected and not unloaded yet
        self.backPack = capacity #capacity of the agent's back pack
        self.priority=1
        self.goal = []


    #return quantity of gold collected and not unloaded yet
    def getTreasure(self):
        return self.gold

    #unload gold in the pack back at the current position
    def unload(self):
        self.env.unload(self)
        self.gold = 0

    #return the agent's type
    def getType(self):
        return 1

    # add some gold to the backpack of the agent (quantity t)
    # if the quantity exceeds the back pack capacity, the remaining is lost
    def addTreasure (self, t):
        if (self.gold+t <= self.backPack) :
            self.gold = self.gold + t
        else :
            self.gold = self.backPack


    #load the treasure at the current position
    def load(self,env):
        env.load(self)

    def make_bid(self, treasure,i,j,tache):
        
        if treasure.type == 1 and self.backPack - self.gold >= treasure.value:
            print(self.backPack,treasure.value)
            distance = self.calculate_distance_to(i,j)
            bid_amount = self.evaluate_bid(distance, self.backPack)
            tache.bid_on_treasure(self.id, treasure, bid_amount)

    def calculate_distance_to(self, i,j):
        #utilisation de la distance Manhattan
        #distances_to_treasures = abs(self.posX - i) + abs(self.posY - j)
        #utilisation de la distance euclidienne vu que les deplacements en diagonals sont permis
        #distances_to_treasures = ((self.posX - i)**2 + (self.posY - j)**2) ** 0.5
        distances_to_treasures = math.sqrt(((i - self.posX)**2 + (j-self.posY )**2))
        return distances_to_treasures

    def evaluate_bid(self, distance, capacity):
        # Formule d'évaluation d'une offre basée sur la distance et la capacité
        bid_value = distance
        return bid_value
    

    """
    Cette methode est utilisé pour retourner le tresors le plus proche 
    En effet on fait une simulation en fonction de la valeur de tresors,le capacité de sac de l'agent et le contenant de sont sac
    A chaque etape on verifie si l'agent a de l'espace dans son sac pour ramasser le tresor si tel n'est pas le cas l'agent va se diriger vers le 
    poit de collecte et vider son sac et retourner pour ramasser le tresor(s) qui lui reste à ramasser
    """
    def trouver_chemin_vers_tresor_plus_proche(self, tache):
        # Trouver le trésor le plus proche
        #on recuperer tous les tresors qui peuvent etre ramasser par l'agent selon l'espace disponible dans son sac et la valeur du tresor
        treasure = [ t for t in self.bag_contents if (self.backPack - self.gold) >= t['treasure'].value ]
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
            #print(chemin," position : ",t["position"])
            #self.gold += t['treasure'].value
            return chemin,t
        else:
            chemin_vers_depot = tache.a_star_search(start=(self.posX,self.posY), goal=self.env.posUnload,grid=tache)
            return chemin_vers_depot, None

    """
    Dans cette methode l'agent construit son plan individuel à partir des taches qui lui sont attribuées cad
    Il fait son plan en prenant en compte le tresor qui se situe le plus proche de sa position
    """  
    def planindividuel(self,tache):
        #on recuper les position initiales de l'agent pour ne pas les perdre 
        x,y = self.posX,self.posY
        #tant que l'agent a des tresors à aller chercher on calcule le chemin le plus court vers le tresors le plus proche
        while self.bag_contents:
            #on fait appel à la methode trouver_chemin_vers_tresor_plus_proche pour retrouver le tresors ainsi que le le chemin vers le tresors le plus proche
            objectif,treasure = self.trouver_chemin_vers_tresor_plus_proche(tache)
            self.plan.extend(objectif[1:])
            #si on a un tresors alors on ajoute son chemin dans notre plan et on le supprime des taches que l'agent doit accomplir
            if treasure:
                self.gold = self.gold + treasure["treasure"].value
                self.posX,self.posY = treasure['position']
                self.goal.append(treasure['position'])
                self.bag_contents.remove(treasure)
            # si on a pas de tresor c'est a dire l'agent a des tresors qui lui reste à ramasser et qu'il n'a pas assez de place dans son sac alors, il doit se rendre vers le point de collecte pour decherger
            # ainsi on ajoute le chemin vers le point de collecte dans son plan
            else:
                self.posX,self.posY = self.env.posUnload
                self.goal.append(self.env.posUnload)
                self.gold=0
        """
        Aprés avoir calculer le plan individuel de l'agent on doit remettre sa position à sa position initiale
        et ajouter le chemin vers le point de collecte pour decharger les tresors qu'il à ramasser
        """
        chemin_vers_depot = tache.a_star_search(start=(self.posX,self.posY), goal=self.env.posUnload,grid=tache)
        self.plan.extend(chemin_vers_depot[1:])
        self.plan.insert(0,(x,y))
        self.goal.append(self.env.posUnload)
        self.posX,self.posY=x,y

    def plan_termine(self):
        # Retourne True si toutes les actions du plan ont été effectuées
        return self.index_plan >= len(self.plan)

    def executionPlanIndividuel(self):
        x = self.index_plan
        if not self.plan_termine():
            if (self.posX, self.posY) in self.goal:
                if not self.env.isAt(self, self.env.posUnload[0], self.env.posUnload[1]):
                    self.env.load(self)
                    self.goal.remove((self.posX, self.posY))
                else:
                    if self.gold > 0:
                        self.unload()
                    else:
                        self.index_plan += 1
                        if x < len(self.plan):
                            coor = self.plan[x]
                            move = self.move(self.posX, self.posY, coor[0], coor[1])
                            if move != 1:
                                self.posX, self.posY = coor
            else:
                self.index_plan += 1
                if x < len(self.plan):
                    coor = self.plan[x]
                    move = self.move(self.posX, self.posY, coor[0], coor[1])
                    if move != 1:
                        self.posX, self.posY = coor
        else:
            if self.gold > 0 and self.env.isAt(self, self.env.posUnload[0], self.env.posUnload[1]):
                self.unload()
            x, y = self.posX, self.posY
            del self.env.agentSet[self.getId()]
            self.env.grilleAgent[x][y] = None


    def __str__(self):
        res = "agent Gold "+  self.id + " ("+ str(self.posX) + " , " + str(self.posY) + ")"
        return res
    
    