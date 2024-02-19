
from Environment import Environment
class Planification():
    def __init__(self,env:Environment):
        self.env=env


    def detecter_conflits(self):
        conflits = {}
        for id_agent, agent in self.env.agentSet.items():
            for step, position in enumerate(agent.plan):
                for other_id, other_agent in self.env.agentSet.items():
                    if other_id != id_agent and position in other_agent.plan:
                        print(other_agent,agent,step,position)
                        other_step = other_agent.plan.index(position)
                        conflit_key = frozenset({id_agent, other_id, position})
                        if conflit_key not in conflits:
                            conflits[conflit_key] = (step, other_step)
        print(conflits)
        print(len(conflits))
        return conflits

    def resoudre_conflits(self):
        conflits = self.detecter_conflits()
        #for (agent1_id, agent2_id, position), (step1, step2) in conflits.items():
        for conflit in conflits: 
            agents_ids = [item for item in conflit if isinstance(item, str)]  # Identifiants d'agents sont des chaînes
            position_conflit = [item for item in conflit if isinstance(item, tuple)][0]
            (step1, step2) = conflits[conflit]
            print(step1,step2)
            print(agents_ids,position_conflit)
            #print(agent1_id,agent2_id,position,step1,step2)
            if len(agents_ids) == 2:
                agent1_id, agent2_id = agents_ids
                try:
                    agent1, agent2 = self.env.agentSet[agent1_id], self.env.agentSet[agent2_id]
                    if agent1.priority > agent2.priority:
                        # Assurez-vous que l'index pour l'insertion est dans les limites
                        if step2 < len(agent2.plan):
                            agent2.plan.insert(step2 + 1, agent2.plan[step2])
                        else:
                            # Gérer le cas où step2 est à la fin du plan
                            agent2.plan.append(agent2.plan[-1])
                    else: 
                        if agent2.priority > agent1.priority:
                            if step1 < len(agent1.plan):
                                agent1.plan.insert(step1 + 1, agent1.plan[step1])
                            else:
                                agent1.plan.append(agent1.plan[-1])
                        elif agent1.priority == agent2.priority:
                            ag1 =  int(agent1.getId()[-1])
                            ag2 = int(agent2.getId()[-1])
                            if ag1 > ag2:
                                #agent = agent1
                                if step1 < len(agent1.plan):
                                    agent1.plan.insert(step1 + 1, agent1.plan[step1])
                                else:
                                    # Gérer le cas où step2 est à la fin du plan
                                    agent1.plan.append(agent1.plan[-1])
                            else:
                                if step2 < len(agent2.plan):
                                    agent2.plan.insert(step2 + 1, agent2.plan[step2])
                                else:
                                    # Gérer le cas où step2 est à la fin du plan
                                    agent2.plan.append(agent2.plan[-1])
                except KeyError as e:
                    print(f"Clé non trouvée dans agentSet: {e}")
            """if agent1_id in self.env.agentSet and agent2_id in self.env.agentSet:
                agent1, agent2 = self.env.agentSet[agent1_id], self.env.agentSet[agent2_id]"""
            # Appliquer une logique de résolution de conflit, par exemple :
            # Si agent1 a une priorité plus élevée que agent2, alors agent2 attend
            """if agent1.priority > agent2.priority:
                agent2.plan.insert(step2 + 1, agent2.plan[step2])  # Fait attendre agent2
            else:
                agent1.plan.insert(step1 + 1, agent1.plan[step1])  # Fait attendre agent1
            else:
                print(f"Erreur: un des agents ({agent1_id} ou {agent2_id}) est introuvable.")"""
        for a in self.env.agentSet:
            print(a,"=====================>",self.env.agentSet[a].plan)
