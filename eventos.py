import pygame
pygame.init()

class Jogo():
    def __init__(self):
        self.event_comprouCarta = False
        self.event_ganhouRubi = False
        self.event_perdeuRubi = False
        self.event_ganhouEnergia = False
        self.event_perdeuEnergia = False
        self.event_atacar = False
        self.event_info = False
        self.event_vezJogador = True
        self.event_novoTurno = True
        self.event_primeiroTurno = True
        self.event_matouInimigo = False
        self.txt_grupo = pygame.sprite.Group()
        self.ataque_grupo = pygame.sprite.Group()

j = Jogo()