import pygame

pygame.init()

rubyFrame = pygame.image.load("imagem/background/rubiFrame.png")
rubyFrameMP = pygame.image.load("imagem/background/rubiFrameMP.png")

class Medidor():
    def __init__(self, rubis, energia):
        self.rubis = rubis
        self.rubiImagem = pygame.image.load("imagem/medidor/rubi.png")
        self.energia = energia
        self.energiaMax = 100
        self.custoComprar = 5
        self.ganhoEnergia = 8
        self.corEnergia = "yellow"
        self.valor = 0
        self.valorE = 0

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
    
    def desenhaRubisMP(self, janela, fonte):

        janela.blit(rubyFrameMP, (700, 2))
        janela.blit(self.rubiImagem, (730, 15))
        rubiNumero = fonte.render(f"{self.rubis}", True, "white")
        janela.blit(rubiNumero, (775, 25))

    def rendaRubi(self, renda):
        self.rubis += renda

    def prejuizoRubi(self, prejuizo):
        self.rubis -= prejuizo

    def rendaEnergia(self, renda):
        self.energia += renda
        if self.energia >= self.energiaMax:
            self.energia = self.energiaMax

    def prejuizoEnergia(self, prejuizo):
        self.energia -= prejuizo
        if self.energia <= 0:
            self.energia = 0
            
med = Medidor(60, 50)

agua = pygame.image.load("imagem/medidor/agua.png")
raio = pygame.image.load("imagem/medidor/raio.png")
fogo = pygame.image.load("imagem/medidor/fogo.png")
soco = pygame.image.load("imagem/medidor/soco.png")
magica = pygame.image.load("imagem/medidor/magica.png")
corte = pygame.image.load("imagem/medidor/coracao.png")

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