import pygame
import pygame.freetype

# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre et les options
flags = pygame.FULLSCREEN
screen = pygame.display.set_mode((0, 0), flags)
clock = pygame.time.Clock()
running = True

# Définir les propriétés des boutons
button_color = (0, 0, 0)  # Noir
button_hover_color = (255, 255, 255)  # Blanc lumineux
button_size = (200, 50)
font_size = 36
button_margin = 20

# Charger une police médiévale
font_path = 'police/googleFont/MedievalSharp-Regular.ttf'
font = pygame.freetype.Font(font_path, font_size)
button_texts = ['Start', 'Options', 'Quitter']

# Calculer la position des boutons centrés
def calculate_button_positions(button_count):
    screen_width, screen_height = screen.get_size()
    total_height = button_count * (button_size[1] + button_margin) - button_margin
    y_start = (screen_height - total_height) // 2
    positions = []
    for i in range(button_count):
        x = (screen_width - button_size[0]) // 2
        y = y_start + i * (button_size[1] + button_margin)
        positions.append(pygame.Rect(x, y, button_size[0], button_size[1]))
    return positions

button_rects = calculate_button_positions(len(button_texts))

def draw_button(rect, text, is_hovered):
    """Dessine un bouton avec un effet de surbrillance et de flou lumineux autour du texte."""
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, button_hover_color, rect)  # Fond blanc lorsque survolé
        text_surface, _ = font.render(text, (0, 0, 0))  # Texte noir
        # Créer un effet lumineux autour du texte
        shadow_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        shadow_surface.fill((255, 255, 255, 128))  # Blanc avec opacité pour le flou lumineux
        screen.blit(shadow_surface, rect.topleft)  # Dessiner l'effet lumineux sur le bouton
    else:
        pygame.draw.rect(screen, button_color, rect)  # Fond noir lorsque non survolé
        text_surface, _ = font.render(text, (255, 255, 255))  # Texte blanc
    screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2,
                               rect.y + (rect.height - text_surface.get_height()) // 2))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(button_rects):
                if rect.collidepoint(event.pos):
                    if button_texts[i] == 'Quitter':
                        running = False
                    # Ajoute la logique pour les autres boutons ici
                    print(f'{button_texts[i]} clicked')

    # Remplir l'écran avec une couleur de fond
    screen.fill((0, 0, 0))  # Noir

    # Dessiner les boutons
    for i, rect in enumerate(button_rects):
        draw_button(rect, button_texts[i], rect.collidepoint(pygame.mouse.get_pos()))

    # Actualiser l'affichage
    pygame.display.flip()

    # Limiter le FPS à 60
    clock.tick(60)

pygame.quit()