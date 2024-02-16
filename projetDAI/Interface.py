import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Paramètres de la grille
tailleX, tailleY = 8, 8  # Dimensions de la grille
taille_case = 60  # Taille d'une case de la grille en pixels

# Couleurs
couleur_fond = (255, 255, 255)  # Blanc
couleur_agent = (0, 0, 255)  # Bleu
couleur_tresor = (0, 255, 0)  # Vert

# Création de la fenêtre
taille_fenetre = (tailleX * taille_case, tailleY * taille_case)
ecran = pygame.display.set_mode(taille_fenetre)
pygame.display.set_caption("Simulation Agents")

# Positions initiales (exemple)
positions_agents = [(1, 2), (3, 4)]
positions_tresors = [(5, 5), (6, 2)]

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fond
    ecran.fill(couleur_fond)

    # Dessiner les agents
    for pos in positions_agents:
        pygame.draw.rect(ecran, couleur_agent, (pos[0]*taille_case, pos[1]*taille_case, taille_case, taille_case))

    # Dessiner les trésors
    for pos in positions_tresors:
        pygame.draw.rect(ecran, couleur_tresor, (pos[0]*taille_case, pos[1]*taille_case, taille_case, taille_case))

    pygame.display.flip()

pygame.quit()
sys.exit()