import pygame

pygame.init()

class Medidor():
    def __init__(self, rubis, energia):
        self.rubis = rubis
        self.rubiImagem = pygame.image.load("imagem/medidor/rubi.png")
        self.energia = energia
        self.energiaMax = 100
        self.custoComprar = 5
        self.ganhoEnergia = 8
        self.valor = 0
        self.valorE = 0

    def desenhaMedidores(self, janela, fonte):
        
        barraLar = 605
        barraAlt = 25
        rubyFrame = pygame.image.load("imagem/background/rubiFrame.png")
        janela.blit(rubyFrame, (30, 12))
        janela.blit(self.rubiImagem, (55, 35))
        rubiNumero = fonte.render(f"{self.rubis}", True, "white")
        janela.blit(rubiNumero, (100, 45))
        txtEnergia = fonte.render(f"Energia   {self.energiaMax}/{self.energia}", True, "black")
        ratio = self.energia / self.energiaMax
        pygame.draw.rect(janela, "gray", (730, 500, barraLar, barraAlt))
        pygame.draw.rect(janela, "yellow", (730, 500, barraLar * ratio, barraAlt))
        janela.blit(txtEnergia, (740, 497))
    
    def desenhaRubisMP(self, janela, fonte):

        rubyFrame = pygame.image.load("imagem/background/rubiFrameMP.png")
        janela.blit(rubyFrame, (700, 2))
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