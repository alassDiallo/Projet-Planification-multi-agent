from MyAgent import MyAgent
import math
#from TacheAllocation import TacheAllocation


#inherits MyAgent

class MyAgentChest(MyAgent) :
    def __init__(self, id, initX, initY, env):
        MyAgent.__init__(self, id, initX, initY, env)
        self.bag_contents = []
        self.priority=3
        self.goal = []


    # open a chest
    def open(self):
        self.env.open(self, self.posX, self.posY)

    # the agent do not hold some treasure
    def getTreasure(self):
        return 0

    def __str__(self):

        res = "agent Chest "+ self.id + " (" + str(self.posX) + " , " + str(self.posY) + ")"
        return res
    

    def make_bid(self, treasure,i,j,tache):
        distance = self.calculate_distance_to(i,j)
        bid_amount = self.evaluate_bid(distance)
        tache.bid_on_treasure(self.id, treasure, bid_amount)

    def calculate_distance_to(self, i,j):
        #distances_to_treasures = abs(self.posX - i) + abs(self.posY - j)
        #distances_to_treasures = ((self.posX - i)**2 + (self.posY - j)**2) ** 0.5
        distances_to_treasures = math.sqrt(((i - self.posX)**2 + (j-self.posY )**2))
        return distances_to_treasures

    def evaluate_bid(self, distance):
        # Formule d'évaluation d'une offre basée sur la distance et la capacité
        bid_value = distance
        return bid_value
    
    def trouver_chemin_vers_tresor_plus_proche(self, tache):
        # Trouver le trésor le plus proche
        chemin = tache.a_star_search(start=(self.posX,self.posY), goal=self.bag_contents[0]["position"],grid=tache)
        treasure = self.bag_contents[0]
        min = len(chemin)
        for tr in self.bag_contents[1:]:
            c = tache.a_star_search(start=(self.posX,self.posY), goal=tr["position"],grid=tache)
            if min > len(c):
                min = len(c)
                chemin = c
                treasure = tr
        return chemin,treasure
    
    def plan_termine(self):
        # Retourne True si toutes les actions du plan ont été effectuées
        return self.index_plan >= len(self.plan)
        
    def planindividuel(self,tache):
        x,y = self.posX,self.posY
        while self.bag_contents:
            objectif,treasure = self.trouver_chemin_vers_tresor_plus_proche(tache)
            self.plan.extend(objectif[1:])
            self.posX,self.posY= treasure['position']
            self.goal.append(treasure['position'])
            self.bag_contents.remove(treasure)
        self.plan.insert(0,(x,y))
        self.posX,self.posY=x,y
    
    """def executionPlanIndividuel(self):
        x = self.index_plan
        if not self.plan_termine():
            if (self.posX,self.posY) in self.goal:
                self.open()
                self.goal.remove((self.posX,self.posY))
            else:
                if x+1 < len(self.plan):
                    print("position ",self.plan[x],self.plan[x+1])
                    coor = self.plan[x+1]
                    x,y=self.plan[x]
                    s= (x,y,coor[0],coor[1])
                    print(self,s)
                    move = self.move(x,y,coor[0],coor[1])
                    #move = self.move(self.posX,self.posY,coor[0],coor[1])
                    if move == 1:
                        pass
                    else:
                        self.posX,self.posY=coor
                    self.index_plan = self.index_plan + 1
                else:
                    x,y=self.posX,self.posY
                    print(self.env.agentSet)
                    self.env.agentSet = { a_id:agent for a_id,agent in self.env.agentSet.items() if a_id != self.getId()}
                    print(self.env.agentSet)
                    print("fin plan avant supp----------------------------- ",self.env.grilleAgent[x][y])
                    self.env.grilleAgent[x][y]=None
                    print("fin plan apres supp----------------------------- ",self.env.grilleAgent[x][y])
                    #return True
            self.index_plan = self.index_plan + 1
                #return move
        else:
            x,y=self.posX,self.posY
            print("fin plan avant supp ",self.env.grilleAgent[x][y])
            del self.env.agentSet[self.getId()]
            self.env.grilleAgent[x][y]=None
            print("fin plan apres supp ",self.env.grilleAgent[x][y])"""
    def executionPlanIndividuel(self):
        x = self.index_plan
        if not self.plan_termine():
            if (self.posX, self.posY) in self.goal:
                self.open()
                self.goal.remove((self.posX, self.posY))
            else:
                self.index_plan += 1
                if x < len(self.plan):
                    coor = self.plan[x]
                    move = self.move(self.posX, self.posY, coor[0], coor[1])
                    if move != 1:
                        self.posX, self.posY = coor
        else:
            x, y = self.posX, self.posY
            del self.env.agentSet[self.getId()]
            self.env.grilleAgent[x][y] = None

            

    