
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
    
    def envoiPlan(self):
        for other_id in self.env.agentSet:
            if other_id != self.id:
                self.send(other_id, self.plan)

    def detecter_et_negocier_conflits(self,tache):
        
        
        # Detection des conflits et replanification
        conflits_detectes = True
        while conflits_detectes:
            # Envoyer son plan à tous les autres agents
            self.envoiPlan()
            conflits_detectes = False
            for mail in self.mailBox:
                idSender, planSender = mail
                print(self,mail)
                # Analyser les plans reçus pour détecter les conflits
                conflit, step = self.analyser_conflit(planSender)
                if conflit:
                    conflits_detectes = True
                    agents = self.env.agentSet[idSender]
                    # Négocier un ajustement de plan en cas de conflit
                    self.negotiate(idSender,agents.priority, step,tache)
                


    def analyser_conflit(self, planSender):
        # Retourne True et l'étape de conflit si un conflit est trouvé, False sinon
        for step, action in enumerate(self.plan):
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
            #renvoyer son plan au autre agent
            self.envoiPlan()
        if priority < self.priority:

            #si la priorité de l'autre agent est plus petit alors il l'impose d'effectuer l'action wait qui est de rester sur place
            self.send(idSender,f"Je suis prioritaire par rapport à toi alors tu dois replanifier et faire l,'action wait")
            self.env.agentSet[idSender].readMail()
            self.env.agentSet[idSender].ajuster_plan(step)
            #renvoyer son plan au autre agent
            self.env.agentSet[idSender].envoiPlan()

        if priority == self.priority:
            distance = tache.a_star_search(start=(self.posX,self.posY), goal=self.goal[0],grid=tache)
            message_content = f"replanifier Conflit à l'étape {step}, distance restante jusqu'à l'objectif: {len(distance)}"
            self.send(idSender, message_content)
            distance = tache.a_star_search(start=(self.posX,self.posY), goal=self.goal[0],grid=tache)
            self.send(idSender, f"({step},{len(distance)})")
            self.env.agentSet[idSender].readMail()
            r = self.env.agentSet[idSender].propositionDeNego(step,len(distance),tache)
            if not r :
                #replanifier et envoyer le plan
                self.ajuster_plan(step)
                #renvoie du plan au autres agents
                self.envoiPlan()

    def ajuster_plan(self, step):
        # Ajuster le plan en fonction de la négociation
        # Par exemple, insérer une action 'wait' ou trouver un chemin alternatif
        self.plan.insert(step - 1, self.plan[step-1])
    

    def propositionDeNego(self,step,distance,tache):
        #comparaison de la dstance de l'agent reçu par rapport à notre distance
        d = len(tache.a_star_search(start=(self.posX,self.posY), goal=self.goal[0],grid=tache))
        if distance > d:
            return False
        else :
            self.ajuster_plan(step)
            self.envoiPlan()
            return True
    
    def __str__(self):
        res = self.id + " ("+ str(self.posX) + " , " + str(self.posY) + ")"
        return res

