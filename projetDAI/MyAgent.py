
import Environment

class MyAgent:


    def __init__(self, id, initX, initY, env:Environment):
        self.id = id
        self.posX = initX
        self.posY = initY
        self.env = env
        self.mailBox = []
        self.plan = []
        self.ex=0

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.getId() == self.getId()
        return False


    #make the agent moves from (x1,y1) to (x2,y2)
    def move(self,  x1,y1, x2, y2) :
        if x1 == self.posX and y1 == self.posY :
            print("departure position OK")
            if self.env.move(self, x1, y1, x2, y2) :
                self.posX = x2
                self.posY = y2
                print("deplacement OK")
                return 1

        return -1

    #return the id of the agent
    def getId(self):
        return self.id

    #return the position of the agent
    def getPos(self):
        return (self.posX, self.posY)

    # add a message to the agent's mailbox
    def receive(self, idReceiver, textContent):
        self.mailBox.append((idReceiver, textContent))

    #the agent reads a message in her mailbox (FIFO mailbox)
    #return a tuple (id of the sender, message  text content)
    def readMail (self):
        idSender, textContent = self.mailBox.pop(0)
        print("mail received from {} with content {}".format(idSender,textContent))
        return (idSender, textContent)


    #send a message to the agent whose id is idReceiver
    # the content of the message is some text
    def send(self, idReceiver, textContent):
        self.env.send(self.id, idReceiver, textContent)


    """def trouver_chemin_vers_tresor_plus_proche(self, tache):
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
        return chemin,treasure"""
        
        
    """ def planindividuel(self,tache):
        x,y = self.posX,self.posY
        while self.bag_contents:
            print("-----------------------------------------------------")
            objectif,treasure = self.trouver_chemin_vers_tresor_plus_proche(tache)
            self.plan.extend(objectif[1:])
            print(objectif,objectif[1:])
            if type(self).__name__== "MyAgentStones" or type(self).__name__== "MyAgentGold":
                chemin_vers_depot = tache.a_star_search(start=treasure["position"], goal=self.env.posUnload,grid=tache)
                self.plan.extend(chemin_vers_depot[1:])
                print("chemin vers depots : ",chemin_vers_depot)
                self.posX,self.posY = self.env.posUnload
            else:
                self.posX,self.posY= treasure["position"]
            self.bag_contents.remove(treasure)"""
            
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
    """self.plan.insert(0,(x,y))
        print(self,"========>",self.plan)
        print("longuer plan ",len(self.plan))
        self.posX,self.posY=x,y"""
        


    def executionPlanIndividuel(self,tache,i):
        x = self.ex
        
        if x+1 < len(self.plan):
            coor = self.plan[x+1]
            s= (self.posX,self.posY,coor[0],coor[1])
            print(self,s)
            move = self.move(self.posX,self.posY,coor[0],coor[1])
            #move = self.move(self.posX,self.posY,coor[0],coor[1])
            if move == 1:
                print(move)
            else:
                self.posX,self.posY=coor
                print("pppppp",self.posX,self.posY)
            self.ex = self.ex +1
            
            return move
            """elif move == -1:
                print(coor[0],coor[1])
                print(self.env.grilleAgent[coor[0]][coor[1]])
                agent = self.env.grilleAgent[coor[0]][coor[1]]
                print(agent)
                self.send(agent.getId(),f"can you pease leave this grille i need to pass")
                agent.readMail()
                m = tache.neighbors(id=(coor[0],coor[1]))
                if agent.ex+1 < len(agent.plan):
                    coordA = agent.plan[agent.ex+1]
                else:
                    coordA = agent.plan[agent.ex]
                m1 = tache.neighbors(id=coordA)
                ensemble1 = set(m)
                ensemble2 = set(m1)

                # Trouver l'intersection des ensembles
                intersection = ensemble1.intersection(ensemble2)

                # Convertir l'intersection en liste (si nécessaire)
                intersection_liste = list(intersection)

                # Afficher le résultat
                print("intersection------------------",intersection_liste)
                print(agent.posX,agent.posY,"+",coordA)

                #m = m1[0]
                print(m1)
                print(m)
                print(agent.posX,agent.posY,intersection_liste[0][0],intersection_liste[0][1])
                mv = agent.move(agent.posX,agent.posY,intersection_liste[0][0],intersection_liste[0][1])
                if mv == 1:
                    move = self.move(self.posX,self.posY,coor[0],coor[1])
                    return move
                elif mv==-1:
                    #return agent.executionPlanIndividuel(tache=tache,i=i)
                    print("move conflic ",mv)
                    s = (self.posX,self.posY,coor[0],coor[1])
                
                return move
                print("=>",s)"""
        """if i < len(self.plan)-1:
            coor = self.plan[i+1]
            s= (self.posX,self.posY,coor[0],coor[1])
            print(self,s)
            move = self.move(self.posX,self.posY,coor[0],coor[1])
            print(move)
            return move"""
        """for coor in self.plan[1:]:
            s= (self.posX,self.posY,coor[0],coor[1])
            print("ssssss ===>",s)
            move = self.move(self.posX,self.posY,coor[0],coor[1])
            if move == 1:
                print(move)
            elif move == -1:
                print(move)
                agent = self.env.grilleAgent[coor[0]][coor[1]]
                #print(agent.getId())
                #self.send(agent.getId(),f"can you pease leave this grille i need to pass")
                #agent.readMail()
                m = tache.neighbors(id=(coor[0],coor[1]))
                m = m[0]
                #agent.move(agent.posX,agent.posY,m[0],m[1])
                #s = (self.posX,self.posY,coor[0],coor[1])
                #self.move(self.posX,self.posY,coor[0],coor[1])
                #print("=>",s)
            if type(self).__name__== "MyAgentStones" or type(self).__name__== "MyAgentGold":
                self.load(self.env)
            elif type(self).__name__== "MyAgentChest":
                self.env.open(self,self.posX,self.posY)
            print(len(self.bag_contents))
            print(len(self.bag_contents)) """

    """
    def collecte_treasure(self,tache):
        x,y = self.posX,self.posY
        while self.bag_contents:
            print("-----------------------------------------------------")
            objectif,treasure = self.trouver_chemin_vers_tresor_plus_proche(tache)
            self.posX,self.posY = treasure["position"] 
            self.plan.extend(objectif[1:])
            print(objectif,objectif[1:])
            self.bag_contents.remove(treasure)
            for coor in objectif[1:]:
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
            print("------------------------------------------------")
        self.plan.insert(0,(x,y))
        print(self,"========>",self.plan)
        print("longuer plan ",len(self.plan))"""
    def detecter_conflit(self,position, autres_agents,i):
        for agent in autres_agents:
            #print(agent)
            for ind in range(len(agent.plan)-1):
                #print(position," ",agent.plan[ind]," ",agent.plan[ind+1],ind,i)
                #print("indice a1",i,"position",position, "indice ag2 ",ind," position ag2 = ",p)
                if (agent.plan[ind] == position and ind == i) or agent.plan[ind+1] == position:
                    return True, agent
        return False, None
        #return False, None
    
    def executer_plan(self, autres_agents):
        conf =[]
        print(self)
        for i,position in enumerate(self.plan):
            conflit, agent_conflit = self.detecter_conflit(position, autres_agents,i)
            if conflit:
                print(f"Conflit détecté avec l'agent {agent_conflit.id} en {position}")
                conf.append({
                    "conflit pos ":position,
                    "agent impliques":[self.id,agent_conflit.id]
                })
                    # Appliquer la stratégie de résolution de conflit ici
                continue  # Exemple simplifié, passer à la position suivante
                #self.deplacer_vers(position)
            #print("pas de confil")
        
        print(len(conf))
                
    

    def __str__(self):
        res = self.id + " ("+ str(self.posX) + " , " + str(self.posY) + ")"
        return res

