from MyAgent import MyAgent
import math
#from TacheAllocation import TacheAllocation


#inherits MyAgent

class MyAgentChest(MyAgent) :
    def __init__(self, id, initX, initY, env):
        MyAgent.__init__(self, id, initX, initY, env)
        self.bag_contents = []
        self.priority=3


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
            print(min,">",len(c),"=>",min > len(c), c)
            if min > len(c):
                min = len(c)
                chemin = c
                treasure = tr
        print(chemin," position : ",treasure["position"])
        return chemin,treasure
        
        
    def planindividuel(self,tache):
        x,y = self.posX,self.posY
        while self.bag_contents:
            print("-----------------------------------------------------")
            objectif,treasure = self.trouver_chemin_vers_tresor_plus_proche(tache)
            self.plan.extend(objectif[1:])
            print(objectif,objectif[1:])
            self.posX,self.posY= treasure['position']
            self.bag_contents.remove(treasure)
            
            """for coor in objectif[1:]:
                s = (self.posX,self.posY,coor[0],coor[1])
                print("=>",s)
                move = self.move(self.posX,self.posY,coor[0],coor[1])
                if move == 1:
                    print(move)
                elif move == -1:
                    print(move)
                    agent = self.env.grilleAgent[coor[0]][coor[1]]
                    print(agent.getId())
                    self.send(agent.getId(),f"can you pease leave this grille i need to pass")
                    agent.readMail()
                    m = tache.neighbors(id=(coor[0],coor[1]))
                    m = m[0]
                    agent.move(agent.posX,agent.posY,m[0],m[1])
                    s = (self.posX,self.posY,coor[0],coor[1])
                    self.move(self.posX,self.posY,coor[0],coor[1])
                    print("=>",s)
            if type(self).__name__== "MyAgentStones" or type(self).__name__== "MyAgentGold":
                self.load(self.env)
            elif type(self).__name__== "MyAgentChest":
                self.env.open(self,self.posX,self.posY)
            print(len(self.bag_contents))
            self.bag_contents.remove(treasure)
            print(len(self.bag_contents))
            print("------------------------------------------------")"""
        self.plan.insert(0,(x,y))
        print(self,"========>",self.plan)
        print("longuer plan ",len(self.plan))
        self.posX,self.posY=x,y

    