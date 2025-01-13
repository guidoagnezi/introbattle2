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
        self.event_usarSkill = False
        self.event_info = False
        self.event_vezJogador = True
        self.event_novoTurno = True
        self.event_primeiroTurno = True
        self.event_matouInimigo = False
        self.event_standby = False
        self.event_realizouAtaque = False
        self.event_realizouSkill = False
        self.event_trocouTime = False
        self.event_acertouCritico = False
        self.event_bossBattle = False
        self.event_vampirismo = False
        self.event_dropaCard = False
        self.event_oneMore = False
        self.mensagem = False
        self.flag = 0
        self.catalogoMonstro = True
        self.catalogoCarta = False
        self.botoesOff = False
        self.textoAtualizou = False
        self.selecionou = False
        self.textoGuia = ""
        self.buttonPosOffset = 0
        self.round = 1
        self.comandoPassado = -1
        self.emitir = False
        self.particula = 0
        self.cd = 0
        self.cdMax = 1000
        self.cdStandby = 0
        self.cdMaxStandby = 100
        self.acoesEquipeInimiga = 0
        self.acoesEquipe = 3
        self.alvoPar = (0, 0)
        self.txt_grupo = pygame.sprite.Group()
        self.txt_dano = pygame.sprite.Group()
        self.ataque_grupo = pygame.sprite.Group()

j = Jogo()