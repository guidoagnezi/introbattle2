import pygame
from infotext import *

pygame.init()
pygame.display.set_mode((1,1), pygame.NOFRAME)
rubyFrame = pygame.image.load("imagem/background/rubiFrame.png").convert_alpha()
rubyFrameMP = pygame.image.load("imagem/background/rubiFrameMP.png").convert_alpha()

# Medidor - classe que define as economias do jogo: dinheiro (rubis) e energia

class Medidor():
    def __init__(self, rubis, energia):
        self.rubis = rubis
        self.rubisMax = 900
        self.rubiImagem = pygame.image.load("imagem/medidor/rubi.png").convert_alpha()
        self.energia = energia
        self.energiaMax = 100
        self.custoComprar = 5
        self.ganhoEnergia = 8
        self.corEnergia = "yellow"
        self.valor = 0
        self.valorE = 0
        self.multiRubis = 1
        self.multiEnergia = 1
        self.indice = 12
    
    # desenhaMedidores - desenha o icone e numero de rubi e a barra de energia na batalha

    def desenhaMedidores(self, janela, fonte):
        barraLar = 605
        barraAlt = 25
        janela.blit(rubyFrame, (30, 12))
        janela.blit(self.rubiImagem, (55, 35))
        rubiNumero = fonte.render(f"{self.rubis}", True, "white")
        janela.blit(rubiNumero, (100, 45))
        txtEnergia = fonte.render(f"Energia   {self.energiaMax}/{self.energia}", True, "black")
        ratio = self.energia / self.energiaMax
        pygame.draw.rect(janela, "gray", (730, 500, barraLar, barraAlt))
        pygame.draw.rect(janela, self.corEnergia, (730, 500, barraLar * ratio, barraAlt))
        janela.blit(txtEnergia, (740, 497))
    
    # desenhaRubiMP - desenha o icone e numero de rubis no Menu Principal
    
    def desenhaRubisMP(self, janela, fonte):

        janela.blit(rubyFrameMP, (700, 2))
        janela.blit(self.rubiImagem, (730, 15))
        rubiNumero = fonte.render(f"{self.rubis}", True, "white")
        janela.blit(rubiNumero, (775, 25))

    # rendaRubi - metodo que adiciona uma renda ao numero de rubis

    def rendaRubi(self, renda):
        med.valor = int(med.valor * self.multiRubis)
        self.rubis += med.valor
        if self.rubis > self.rubisMax:
            self.rubis = self.rubisMax

    # prejuizpRubi - metodo que adiciona um prejuizo ao numero de rubis

    def prejuizoRubi(self, prejuizo):
        self.rubis -= prejuizo

    # rendaEnergia - adciona uma renda ao numero de energia
    # prejuizoEnergia - adiciona um prejuizo ao numero de energia

    def rendaEnergia(self, renda):
        med.valorE = int(med.valorE * self.multiEnergia)
        self.energia += med.valorE
        if self.energia >= self.energiaMax:
            self.energia = self.energiaMax

    def prejuizoEnergia(self, prejuizo):
        self.energia -= prejuizo
        if self.energia <= 0:
            self.energia = 0
    
    # atualizaCusto - muda o custo de compra das cartas de acordo com a quantidade de rubis acumulado

    def atualizaCusto(self):
        self.custoComprar = int(self.rubis / self.indice)
        if self.custoComprar == 0:
            self.custoComprar = 1
            
med = Medidor(30, 50)

# icones que representam os tipos de ataque dos personagens

agua = pygame.image.load("imagem/medidor/agua.png").convert_alpha()
raio = pygame.image.load("imagem/medidor/raio.png").convert_alpha()
fogo = pygame.image.load("imagem/medidor/fogo.png").convert_alpha()
soco = pygame.image.load("imagem/medidor/soco.png").convert_alpha()
magica = pygame.image.load("imagem/medidor/magica.png").convert_alpha()
corte = pygame.image.load("imagem/medidor/coracao.png").convert_alpha()
congelamento = pygame.image.load("imagem/medidor/gelo.png").convert_alpha()
sangramento = pygame.image.load("imagem/medidor/sangramento.png").convert_alpha()
atk_up = pygame.image.load("imagem/medidor/atk_up.png").convert_alpha()
def_up = pygame.image.load("imagem/medidor/def_up.png").convert_alpha()
atk_down = pygame.image.load("imagem/medidor/atk_down.png").convert_alpha()
def_down = pygame.image.load("imagem/medidor/def_down.png").convert_alpha()

# retornaImagem - recebe um numero que representa um tipo de ataque, retorna o icone correspondente
# 3 - corte, 4 - soco, 5 - fogo, 6 - agua, 7 - raio, 8 - neutro
def retornaImagem(tipo):

    if tipo == 3:
        img = corte
    if tipo == 4:
        img = soco
    if tipo == 5:
        img = fogo
    if tipo == 6:
        img = agua
    if tipo == 7:
        img = raio
    if tipo == 8:
        img = magica
    if tipo == 0:
        img = magica

    return img