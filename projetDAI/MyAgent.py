
import Environment

class MyAgent:


    def __init__(self, id, initX, initY, env:Environment):
        self.id = id
        self.posX = initX
        self.posY = initY
        self.env = env
        self.mailBox = []
        self.plan = []
        self.index_plan = 1
        self.personalScore=0

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

    
    def detecter_et_negocier_conflits(self,tache):
        # Envoyer son plan à tous les autres agents
        for other_id in self.env.agentSet:
            if other_id != self.id:
                self.send(other_id, self.plan)
        # Analyser les plans reçus pour détecter les conflits
        for mail in self.mailBox:
            idSender, planSender = mail
            conflit, step = self.analyser_conflit(planSender)
            print(step)
            if conflit:
                agents = self.env.agentSet[idSender]
                # Négocier un ajustement de plan en cas de conflit
                self.negotiate(idSender,agents.priority, step,tache)

    def analyser_conflit(self, planSender):
        # Retourne True et l'étape de conflit si un conflit est trouvé, False sinon
        for step, action in enumerate(self.plan):
            #print("ssssssssss",planSender)
            if action in planSender:
                step2 = planSender.index(action)
                if step2 == step:
                    return True, step
            
        return False, None

    def negotiate(self, idSender,priority, step,tache):
        # Envoyer une proposition pour résoudre le conflit
        # Cela pourrait être d'attendre, de changer de route, etc.
        print(self.getId(),'-',idSender,step,self.plan[step])
        if priority > self.priority:
            self.ajuster_plan(step)
        if priority < self.priority:
            #si la priorité de l'autre agent est plus petit alors il l'impose d'effectuer l'action wait qui est de rester sur place
            self.send(idSender,f"Je suis prioritaire par rapport à toi alors tu dois replanifier et faire l,'action wait")
            self.env.agentSet[idSender].readMail()
            self.env.agentSet[idSender].ajuster_plan(step)
        if priority == self.priority:
            
            distance = tache.a_star_search(start=(self.posX,self.posY), goal=self.goal[0],grid=tache)
            self.send(idSender, f"({step},{len(distance)})")
            self.env.agentSet[idSender].readMail()
            r = self.env.agentSet[idSender].propositionDeNego(step,len(distance),tache)
            if not r :
                self.ajuster_plan(step)




    def ajuster_plan(self, step):
        # Ajuster le plan en fonction de la négociation
        # Par exemple, insérer une action 'wait' ou trouver un chemin alternatif
        self.plan.insert(step - 1, self.plan[step-1])

    def propositionDeNego(self,step,distance,tache):
        d = len(tache.a_star_search(start=(self.posX,self.posY), goal=self.goal[0],grid=tache))
        if distance > d:
            return False
        else :
            self.ajuster_plan(step)
            return True
    
    def __str__(self):
        res = self.id + " ("+ str(self.posX) + " , " + str(self.posY) + ")"
        return res

