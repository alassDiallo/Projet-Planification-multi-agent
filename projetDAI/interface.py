import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition des constantes pour la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 255)  # Bleu
CIRCLE_COLOR = (255, 0, 0)  # Rouge
CIRCLE_RADIUS = 50

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Exemple Pygame')

# Position initiale du cercle
circle_x = SCREEN_WIDTH // 2
circle_y = SCREEN_HEIGHT // 2
circle_speed_x = 2
circle_speed_y = 2

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   
    # Mise à jour de la position du cercle
    circle_x += circle_speed_x
    circle_y += circle_speed_y
   
    # Rebondissement sur les bords de la fenêtre
    if circle_x - CIRCLE_RADIUS <= 0 or circle_x + CIRCLE_RADIUS >= SCREEN_WIDTH:
        circle_speed_x *= -1
    if circle_y - CIRCLE_RADIUS <= 0 or circle_y + CIRCLE_RADIUS >= SCREEN_HEIGHT:
        circle_speed_y *= -1

    # Remplissage de l'arrière-plan
    screen.fill(BACKGROUND_COLOR)
   
    # Dessin du cercle
    pygame.draw.circle(screen, CIRCLE_COLOR, (circle_x, circle_y), CIRCLE_RADIUS)
   
    # Mise à jour de l'affichage
    pygame.display.flip()
   
    # Contrôle de la vitesse de la boucle
    pygame.time.Clock().tick(60)

# Quitter Pygame
pygame.quit()
sys.exit()