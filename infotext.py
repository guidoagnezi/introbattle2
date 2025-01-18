import pygame
import random
from eventos import *
pygame.init()
pygame.display.set_mode((1,1), pygame.NOFRAME)

fonte = pygame.font.Font("fonts/pixel.ttf", 24)
fonte1 = pygame.font.Font("fonts/pixel.ttf", 18)
fonte2 = pygame.font.Font("fonts/pixel.ttf", 24)

direcao = [1, -1]
velocidade = [-6, -8, -10]

# Classes que informam a situacao, dano e status dos personagens em batalha.
# A diferenca entre os tipos de sprites de texto estao no tamanho, na forma de atualizacao
# e no tipo de posicao que recebe como paramentro

class DamageText(pygame.sprite.Sprite):
        
        def __init__(self, x, y, damage, colour):
            pygame.sprite.Sprite.__init__(self)
            self.image = fonte.render(damage, True, colour) # texto
            self.direction = random.choice(direcao)         # direcao de lancamento do texto
            self.vinicial = random.choice(velocidade)       # velocidade vertical inicial do texto
            self.rect = self.image.get_rect()               # retangulo
            self.vel_y = self.vinicial                      # velocidade vertical
            self.vel_x = 5 * self.direction                 # velocidade horizontal
            self.rect.center = (x, y)
            self.counter = 0                                # contador de tempo de vida do texto
        
        def update(self):
            #move damage text up
            self.rect.y += self.vel_y                       # simulacao de lancamento obliquo com acao da gravidade
            self.rect.x += self.vel_x           
            self.vel_y += 0.8

            #delete the text after a few seconds
            self.counter += 1
            if self.counter > 30:                           
                self.kill()
    
txt_grupo = pygame.sprite.Group()

class MedidorText(pygame.sprite.Sprite):
        
        def __init__(self, x, y, damage, colour):
            pygame.sprite.Sprite.__init__(self)
            if colour != "black":
                self.image = fonte2.render(damage, True, colour)    # mudanca do tamanho baseado na cor
            else:
                self.image = fonte1.render(damage, True, colour)
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.colour = colour                                    # cor do texto
            self.counter = 0
        
        def update(self):
            if self.colour == "black":                              # subida com origem acima da cabeca do alvo
                self.rect.x += 1
            else:
                self.rect.y -= 1
            #delete the text after a few seconds
            self.counter += 1
            if self.counter > 50:
                self.kill()

# Icone - icone que aparecera ao lado de certos tipos de texto

class Icone(pygame.sprite.Sprite):
     
    def __init__(self, x, y, tipo):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = tipo
        if self.tipo == 1:                 # carrega a imagem dos icones dos textos
            self.image = pygame.image.load("imagem/medidor/rubi.png").convert_alpha()
        elif self.tipo == 2:
            self.image = pygame.image.load("imagem/medidor/energia.png").convert_alpha()
        elif self.tipo == 3:
            self.image = pygame.image.load("imagem/medidor/coracao.png").convert_alpha()
        elif self.tipo == 4:
            self.image = pygame.image.load("imagem/medidor/soco.png").convert_alpha()
        elif self.tipo == 5:
            self.image = pygame.image.load("imagem/medidor/fogo.png").convert_alpha()
        elif self.tipo == 6:
            self.image = pygame.image.load("imagem/medidor/agua.png").convert_alpha()
        elif self.tipo == 7:
            self.image = pygame.image.load("imagem/medidor/raio.png").convert_alpha()
        elif self.tipo == 8:
            self.image = pygame.image.load("imagem/medidor/magica.png").convert_alpha()
        elif self.tipo == 10:
            self.image = pygame.image.load("imagem/medidor/atk_up.png").convert_alpha()
        elif self.tipo == 11:
            self.image = pygame.image.load("imagem/medidor/def_up.png").convert_alpha()
        elif self.tipo == 12:
            self.image = pygame.image.load("imagem/medidor/atk_down.png").convert_alpha()
        elif self.tipo == 13:
            self.image = pygame.image.load("imagem/medidor/def_down.png").convert_alpha()
        elif self.tipo == 14:
            self.image = pygame.image.load("imagem/medidor/atk_normal.png").convert_alpha()
        elif self.tipo == 15:
            self.image = pygame.image.load("imagem/medidor/def_normal.png").convert_alpha()
        elif self.tipo == 16:
            self.image = pygame.image.load("imagem/medidor/cura.png").convert_alpha()
        if self.tipo == 17:
            self.image = pygame.image.load("imagem/medidor/card.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.vel_y = -5
        self.vel_x = 2
        self.rect.center = (x, y)
        self.counter = 0
        
    def update(self):
        #move damage text up
        self.rect.y -= 1

        #delete the text after a few seconds
        self.counter += 1
        if self.counter > 50:
            self.kill()

# DefineTextoMedidor - inicializa um texto para indicar a situacao dos medidores do jogo (dinheiro e energia).
# armazena o texto num grupo Sprite.
# recebe posicao em uma tupla de coordenadas.

def DefineTextoMedidor(valor, event_rubi, event_energia, posicao, txt_grupo):
    
    if event_energia or event_rubi:
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
    
    else:
        cor = "crimson"

    if event_rubi:
        texto = MedidorText(posicao[0], posicao[1], f"{sinal} {str(int(valor))}", cor) #inicializacao
        icone = Icone(posicao[0] - 50, posicao[1], 1) #inicializacao
        txt_grupo.add(icone)
    elif event_energia: #muda os parametros caso seja um sprite sobre energia 
        texto = MedidorText(posicao[0], posicao[1], f"{sinal} {str(int(valor))}", cor) #inicializacao
    else:
        texto = MedidorText(posicao[0], posicao[1], f"{valor}", cor) #inicializacao

    if valor != 0:
        txt_grupo.add(texto) #adiciona o texto no grupo de sprites

# DefineTextoDano - Inicializa um texto de dano, armazena num grupo de sprites dedicados para
# textos de dano.
# recebe posicao como um objeto com .rect (retangulo).
# organiza os sprites para que nao se sobreponham

def DefineTextoDano(dano, posicao, txt_grupo, cor, tipo):

    offX = 90
    offY = -10
    offset = -40
    if j.i == 5:
        cor = "white"
    
    texto = DamageText(posicao.rect.x + offX, posicao.rect.y + offY, f"{str(int(dano))}", cor)  #inicializacao

    while 1:    #organiza os sprtes para que nao se sobreponham
        ok = True
        for sprite in j.txt_dano:
            if texto.rect.colliderect(sprite.rect):
                offY += offset
                texto = DamageText(posicao.rect.x + offX, posicao.rect.y + offY, f"{str(int(dano))}", cor)
                ok = False
        if ok:
            break

    j.txt_dano.add(texto) #adiciona o texto no grupo de sprites

# DefineTextoDano - Inicializa um texto de status, armazena num grupo de sprites dedicados para
# textos de status.
# recebe posicao como um objeto com .rect (retangulo).
# organiza os sprites para que nao se sobreponham.
# diferente do texto de dano, esse nao simula um lancamento obliquo mas um movimento retilineo vertical.
# define um icone para indicar o status em questao

def DefineTextoStatus(nome, posicao, txt_grupo, cor, tipo):

    offX = 90
    offY = -10
    offset = -40
    cor = "gray20"
    if j.i == 5:
        cor = "white"

    texto = MedidorText(posicao.rect.x + offX, posicao.rect.y + offY, f"{nome}", cor)
    icone = Icone(posicao.rect.x + offX - 50, posicao.rect.y + offY, tipo)

    while 1:
        ok = True
        for sprite in txt_grupo:
            if texto.rect.colliderect(sprite.rect):
                offY += offset
                texto = MedidorText(posicao.rect.x + offX, posicao.rect.y + offY, f"{nome}", cor)
                icone = Icone(posicao.rect.x + offX - 50, posicao.rect.y + offY, tipo)
                ok = False
        if ok:
            break

    txt_grupo.add(texto)
    txt_grupo.add(icone)

# desenhaTexto - Recebe um grupo de sprites, desenha e atualiza todos os sprites contidos.

def desenhaTexto(txt_grupo, janela):
    txt_grupo.update()
    txt_grupo.draw(janela)