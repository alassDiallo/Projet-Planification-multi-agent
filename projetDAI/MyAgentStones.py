from MyAgent import MyAgent
import math



#inherits MyAgent

class MyAgentStones(MyAgent):

    def __init__(self, id, initX, initY, env, capacity):
        MyAgent.__init__(self, id, initX, initY, env)
        self.bag_contents = []
        self.stone = 0
        self.backPack = capacity

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

    def make_bid(self, treasure,i,j,tache):
        if treasure.type == 2 and self.backPack - self.stone >= treasure.value:
            distance = self.calculate_distance_to(i,j)
            bid_amount = self.evaluate_bid(distance, self.backPack)
            tache.bid_on_treasure(self.id, treasure, bid_amount)

    def calculate_distance_to(self, i,j):
        #distances_to_treasures = abs(self.posX - i) + abs(self.posY - j)
        distances_to_treasures = math.sqrt(((i - self.posX)**2 + (j-self.posY )**2))
        return distances_to_treasures

    def evaluate_bid(self, distance, capacity):
        # Formule d'évaluation d'une offre basée sur la distance et la capacité
        bid_value = distance
        return bid_value
    
    def collecter_tresor(agent, tresor, tresors):
        if agent.position == tresor:
            agent.tresors_collectes.append(tresor)  # Ou toute autre logique de collecte
            tresors.remove(tresor)

    def collecter_tous_les_tresors(agent, tresors, grille):
        while tresors:
            chemin = trouver_chemin_vers_tresor_plus_proche(agent.position, tresors, grille)
            for pos in chemin:
                agent.deplacer_vers(pos)
                if pos in tresors:
                    collecter_tresor(agent, pos, tresors)
                    break  # Sortir de la boucle pour replanifier si nécessaire


    
    def trouver_chemin_vers_tresor_plus_proche(self, tache):
        # Trouver le trésor le plus proche
        content = self.backPack - self.stone
        print("---------content---------",content)
        treasure = [ t for t in self.bag_contents if (self.backPack - self.stone) >= t['treasure'].value]
        if treasure:
            t = treasure[0]
            chemin = tache.a_star_search(start=(self.posX,self.posY), goal=t["position"],grid=tache)
            #treasure = self.bag_contents[0]
            min = len(chemin)
            for tr in treasure[1:]:
                c = tache.a_star_search(start=(self.posX,self.posY), goal=tr["position"],grid=tache)
                print(min,">",len(c),"=>",min > len(c), c)
                if min > len(c):
                    min = len(c)
                    chemin = c
                    t = tr
            print(chemin," position : ",t["position"])
            
            return chemin,t
        else:
            chemin_vers_depot = tache.a_star_search(start=(self.posX,self.posY), goal=self.env.posUnload,grid=tache)
            return chemin_vers_depot, None

        
    def planindividuel(self,tache):
        x,y = self.posX,self.posY
        while self.bag_contents:
            print("-----------------------------------------------------")
            objectif,treasure = self.trouver_chemin_vers_tresor_plus_proche(tache)
            self.plan.extend(objectif[1:])
            print("============>>>>",objectif,"<<<<<=======================")
            print(treasure)
            if treasure:
                self.stone = self.stone + treasure["treasure"].value
                print(f" backpack ={self.backPack},stone = {self.stone} ==> {self.stone + treasure['treasure'].value}")
                self.posX,self.posY = treasure['position']
                self.bag_contents.remove(treasure)
            else:
                self.posX,self.posY = self.env.posUnload
                self.stone=0
            
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
        chemin_vers_depot = tache.a_star_search(start=(self.posX,self.posY), goal=self.env.posUnload,grid=tache)
        self.plan.extend(chemin_vers_depot[1:])
        self.plan.insert(0,(x,y))
        print(self,"========>",self.plan)
        print("longuer plan ",len(self.plan))
        self.posX,self.posY=x,y
        

