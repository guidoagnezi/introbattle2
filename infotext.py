import pygame
pygame.init()

fonte = pygame.font.Font("fonts/pixel.ttf", 24)
fonte1 = pygame.font.Font("fonts/pixel.ttf", 18)

class DamageText(pygame.sprite.Sprite):
        
        def __init__(self, x, y, damage, colour):
            pygame.sprite.Sprite.__init__(self)
            self.image = fonte.render(damage, True, colour)
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.counter = 0
        
        def update(self):
            #move damage text up
            self.rect.y -= 1

            #delete the text after a few seconds
            self.counter += 1
            if self.counter > 30:
                self.kill()
    
txt_grupo = pygame.sprite.Group()

class MedidorText(pygame.sprite.Sprite):
        
        def __init__(self, x, y, damage, colour):
            pygame.sprite.Sprite.__init__(self)
            if colour != "black":
                self.image = fonte.render(damage, True, colour)
            else:
                self.image = fonte1.render(damage, True, colour)
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.colour = colour
            self.counter = 0
        
        def update(self):
            if self.colour == "black":
                self.rect.x += 1
            else:
                self.rect.y -= 1
            #delete the text after a few seconds
            self.counter += 1
            if self.counter > 30:
                self.kill()

class Icone(pygame.sprite.Sprite):
     
    def __init__(self, x, y, tipo):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = tipo
        if self.tipo == 1:
            self.image = pygame.image.load("imagem/medidor/rubi.png")
        elif self.tipo == 2:
            self.image = pygame.image.load("imagem/medidor/energia.png")
        elif self.tipo == 3:
            self.image = pygame.image.load("imagem/medidor/coracao.png")
        elif self.tipo == 4:
            self.image = pygame.image.load("imagem/medidor/soco.png")
        elif self.tipo == 5:
            self.image = pygame.image.load("imagem/medidor/fogo.png")
        elif self.tipo == 6:
            self.image = pygame.image.load("imagem/medidor/agua.png")
        elif self.tipo == 7:
            self.image = pygame.image.load("imagem/medidor/raio.png")
        elif self.tipo == 8:
            self.image = pygame.image.load("imagem/medidor/magica.png")
        elif self.tipo == 10:
            self.image = pygame.image.load("imagem/medidor/atk_up.png")
        elif self.tipo == 11:
            self.image = pygame.image.load("imagem/medidor/def_up.png")
        elif self.tipo == 12:
            self.image = pygame.image.load("imagem/medidor/atk_down.png")
        elif self.tipo == 13:
            self.image = pygame.image.load("imagem/medidor/def_down.png")
        elif self.tipo == 14:
            self.image = pygame.image.load("imagem/medidor/atk_normal.png")
        elif self.tipo == 15:
            self.image = pygame.image.load("imagem/medidor/def_normal.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
        
    def update(self):
        #move damage text up
        self.rect.y -= 1

        #delete the text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


def DefineTextoMedidor(valor, event_rubi, event_energia, posicao, txt_grupo):
    
    if valor >= 0:
        sinal = "+"
        if event_rubi:
            cor = "crimson"
    elif valor < 0:
        sinal = "-"
        if event_rubi:
            cor = "gray27"
    
    if event_energia:
        cor = "black"
        
    valor = abs(valor)

    if event_rubi:
        texto = MedidorText(posicao[0], posicao[1], f"{sinal} {str(int(valor))}", cor)
        icone = Icone(posicao[0] - 50, posicao[1], 1)
    if event_energia:
        texto = MedidorText(posicao[0], posicao[1], f"{sinal} {str(int(valor))}", cor)

    if valor != 0:
        txt_grupo.add(texto)
    
    if not event_energia:
        txt_grupo.add(icone)


def desenhaTexto(txt_grupo, janela):
    txt_grupo.update()
    txt_grupo.draw(janela)

def DefineTextoDano(dano, posicao, txt_grupo, cor, tipo):

    offX = 90
    offY = -10
    texto = DamageText(posicao.rect.x + offX, posicao.rect.y + offY, f"{str(int(dano))}", cor)
    icone = Icone(posicao.rect.x + offX - 50, posicao.rect.y + offY, tipo)

    txt_grupo.add(texto)
    txt_grupo.add(icone)

def DefineTextoStatus(nome, posicao, txt_grupo, cor, tipo):

    offX = 90
    offY = -10
    texto = DamageText(posicao.rect.x + offX, posicao.rect.y + offY, f"{nome}", cor)
    icone = Icone(posicao.rect.x + offX - 50, posicao.rect.y + offY, tipo)

    txt_grupo.add(texto)
    txt_grupo.add(icone)
