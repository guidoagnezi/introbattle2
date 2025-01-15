import pygame
from infotext import *

pygame.init()
pygame.display.set_mode((1,1), pygame.NOFRAME)
rubyFrame = pygame.image.load("imagem/background/rubiFrame.png").convert_alpha()
rubyFrameMP = pygame.image.load("imagem/background/rubiFrameMP.png").convert_alpha()

class Medidor():
    def __init__(self, rubis, energia):
        self.rubis = rubis
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

    def desenhaMedidores(self, janela, fonte):
        barraLar = 605
        barraAlt = 25
        janela.blit(rubyFrame, (30, 12))
        janela.blit(self.rubiImagem, (55, 35))
        rubiNumero = fonte.render(f"{self.rubis}", True, "white").convert_alpha()
        janela.blit(rubiNumero, (100, 45))
        txtEnergia = fonte.render(f"Energia   {self.energiaMax}/{self.energia}", True, "black").convert_alpha()
        ratio = self.energia / self.energiaMax
        pygame.draw.rect(janela, "gray", (730, 500, barraLar, barraAlt))
        pygame.draw.rect(janela, self.corEnergia, (730, 500, barraLar * ratio, barraAlt))
        janela.blit(txtEnergia, (740, 497))
    
    def desenhaRubisMP(self, janela, fonte):

        janela.blit(rubyFrameMP, (700, 2))
        janela.blit(self.rubiImagem, (730, 15))
        rubiNumero = fonte.render(f"{self.rubis}", True, "white").convert_alpha()
        janela.blit(rubiNumero, (775, 25))

    def rendaRubi(self, renda):
        med.valor = int(med.valor * self.multiRubis)
        self.rubis += med.valor  

    def prejuizoRubi(self, prejuizo):
        self.rubis -= prejuizo

    def rendaEnergia(self, renda):
        med.valorE = int(med.valorE * self.multiEnergia)
        self.energia += med.valorE
        if self.energia >= self.energiaMax:
            self.energia = self.energiaMax

    def prejuizoEnergia(self, prejuizo):
        self.energia -= prejuizo
        if self.energia <= 0:
            self.energia = 0
            
med = Medidor(60, 50)

agua = pygame.image.load("imagem/medidor/agua.png").convert_alpha()
raio = pygame.image.load("imagem/medidor/raio.png").convert_alpha()
fogo = pygame.image.load("imagem/medidor/fogo.png").convert_alpha()
soco = pygame.image.load("imagem/medidor/soco.png").convert_alpha()
magica = pygame.image.load("imagem/medidor/magica.png").convert_alpha()
corte = pygame.image.load("imagem/medidor/coracao.png").convert_alpha()

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

atk_up = pygame.image.load("imagem/medidor/atk_up.png").convert_alpha()
def_up = pygame.image.load("imagem/medidor/def_up.png").convert_alpha()
atk_down = pygame.image.load("imagem/medidor/atk_down.png").convert_alpha()
def_down = pygame.image.load("imagem/medidor/def_down.png").convert_alpha()