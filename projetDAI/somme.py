from Environment import Environment
def somme(env:Environment):
    som=0
    for i in range(env.tailleX):
             for j in range(env.tailleY):
                if env.grilleTres[i][j] is not None:
                    
                        somme +=env.grilleTres[i][j].value
    return som