import pygame
import os
from Grid import grid


os.environ['SDL_VIDEO_WINDOWS_POS']= '%d,%d'%(400,100)
surface = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("Sudoku")

pygame.font.init()
game_font = pygame.font.SysFont('Arial', 50)
game_font2 = pygame.font.SysFont('Arial', 25)

Grid=grid(pygame, game_font)
running = True

while running: #memastikan apa yang dilakukan selama running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not Grid.win:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                Grid.get_mouse_click(pos[0],pos[1])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and Grid.win:
                Grid.restart()

    surface.fill((0,0,0))

    Grid.draw_all(pygame, surface)

    if Grid.win:
        won_surface=game_font.render("Menang Coy!",False, (9, 232, 35))
        surface.blit(won_surface, (930, 650))

        space_surface = game_font2.render("Tekan Spacebar untuk restart", False, (10, 145, 26))
        surface.blit(space_surface, (920, 750) )

    pygame.display.flip()