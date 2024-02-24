
from Environment import Environment
from TacheAllocation import TacheAllocation

class Planification():
    def __init__(self,env:Environment):
        self.env=env
        self.tour = 0 
    """
    cette methode permet de detecter le possible conflit qu'il va avoir entre les plans individuel des agents
    """
    def detecter_conflits(self):
        conflits = {}
        for id_agent, agent in self.env.agentSet.items():
            for step, position in enumerate(agent.plan):
                for other_id, other_agent in self.env.agentSet.items():
                    if other_id != id_agent and position in other_agent.plan:
                        other_step = other_agent.plan.index(position)
                        if step == other_step:
                            conflit_key = frozenset({id_agent, other_id, position})
                            if conflit_key not in conflits:
                                conflits[conflit_key] = (step, other_step)
        print("On a ",len(conflits)," conflits")
        return conflits
    
    """
    on utilise cette methode pour resoudre les conflits qu'il y'a entre deux agents
    - si il y'a conflit entre deux agents pour la resolution nous procédons comme suite:
    - conflit entre agent ouvreur de coffre et ramasseur pour la resolution l'agent ouveur envoi un node plan à l'agent ramsseur
    qui contient le step du conflit la position ainsi que sa priorité, la priorité permets de dire qu'il a la priorité donc il dois passer avant lui
    et dans ce cas l'agent patiente le temps que l'agent ouvreur passe et libere la case
    """

    def resoudre_conflits(self):
        conflits = self.detecter_conflits()
        for conflit in conflits: 
            agents_ids = [item for item in conflit if isinstance(item, str)]  # Identifiants d'agents sont des chaînes
            position_conflit = [item for item in conflit if isinstance(item, tuple)][0]
            (step1, step2) = conflits[conflit]
            print("step    ",step1,step2)
            print("conflit entre : ",agents_ids,"à la position ",position_conflit)
            if len(agents_ids) == 2:
                agent1_id, agent2_id = agents_ids
                try:
                    agent1, agent2 = self.env.agentSet[agent1_id], self.env.agentSet[agent2_id]
                    if agent1.priority > agent2.priority:
                        # Assurez-vous que l'index pour l'insertion est dans les limites
                        agent1.send(agent2.getId(),f"{step1,agent1.priority,position_conflit}")
                        agent2.readMail()
                        if step2 < len(agent2.plan):
                            agent2.plan.insert(step2 - 1, agent2.plan[step2-1])
                        else:
                            # Gérer le cas où step2 est à la fin du plan
                            #agent2.plan.append(agent2.plan[-1])
                            x,y = agent2.posX,agent2.posY
                            self.env.grilleAgent[x][y]=None
                            del self.env.agentSet[agent2_id]
                            print("---------",self.env.grilleAgent[x][y])
                            
                    else: 
                        agent2.send(agent1.getId(),f"{step1,agent2.priority,position_conflit}")
                        agent1.readMail()
                        if step1 < len(agent1.plan):
                            agent1.plan.insert(step1 - 1, agent1.plan[step1-1])
                        else:
                            #agent1.plan.append(agent1.plan[-1])
                            x,y = agent1.posX,agent1.posY
                            self.env.grilleAgent[x][y]=None
                            del self.env.agentSet[agent1_id]
                        
                except KeyError as e:
                    print(f"Clé non trouvée dans agentSet: {e}")

    """
    Pour l'execution du plan global on fait appel à cette methode qui defini un nombre de tour pour l'execution du plan global
    - Il faudra fixer le nombre de Tour maximal pour l'execution des tache ici nous avons donné 100
    """

    def executonPlanGlobal(self):
        while not self.tous_les_plans_termines():
            print(f"Tour {self.tour}:")
            # Créer une copie des clés du dictionnaire
            agent_ids = list(self.env.agentSet.keys())
            for agent_id in agent_ids:
                agent = self.env.agentSet[agent_id]
                if not agent.plan_termine() or not self.tous_tresors_ramasses():
                    agent.executionPlanIndividuel()
            self.tour += 1
            print(self.env)
            if self.tour > 100:  # Prévenir une boucle infinie
                print("Limite de tours atteinte.")
                break
        print("fin de l'execution du plan global")

    """
    Cette methode permet de voir à chaque tour s'il reste encore des agents qui n'ont pas terminés leur plan 
    """
    def tous_les_plans_termines(self):
        # Vérifie si tous les agents ont terminé leurs plans
        return all(self.env.agentSet[agent].plan_termine() for agent in self.env.agentSet)

    """
    Cette methode return l'ensemble des tresors qui ont été ramasser aprés l'execution du plan global
    """
    def tous_tresors_ramasses(self):
        a = all(tresor is None for row in self.env.grilleTres for tresor in row)
        print(a)
        return a