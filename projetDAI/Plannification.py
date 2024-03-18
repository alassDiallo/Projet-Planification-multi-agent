
from Environment import Environment
from TacheAllocation import TacheAllocation

class Planification():
    def __init__(self,env:Environment):
        self.env=env
        self.tour = 0 

    #execution de plan global obtenu
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
            #print(self.env)
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
        return a