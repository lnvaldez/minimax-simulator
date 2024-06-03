import pygame

def handle_events(game, mute_button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if game.mouse_caught or game.last_round:
                    game.restart()
                    game.mouse_caught = False
                    game.last_round = False
                    return
        if mute_button.is_clicked(event):
            game.toggle_music()
