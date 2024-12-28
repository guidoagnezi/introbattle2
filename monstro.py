import pygame
import random
from medidor import *
from eventos import *

pygame.init()

class Monstro:

    def __init__(self, nome, vida, defesa, ataque, custo, magia, fraqueza): 
        self.nome = nome
        self.vidamax = vida
        self.vida = vida
        self.vivo = True
        self.custo = custo
        self.defesa = defesa
        self.ataque = ataque
        self.player = False
        self.ativo = False
        self.magia = magia
        self.fraqueza = fraqueza
        self.x_pos = 0
        self.y_pos = 0
        self.x_loja = 0
        self.y_loja = 0
        self.especial = 0
        self.image = pygame.image.load(f"imagem/lutador/{self.nome}/0.png")
        self.imageLoja = pygame.image.load(f"imagem/lutador/{self.nome}/loja.png")
        self.animation_cooldown = 100
        self.update_time = pygame.time.get_ticks()
        self.animation_list = []
        self.index = 0
        self.count = 0
        self.action = 0
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f"imagem/lutador/{self.nome}/{i}.png")
            if self.nome == "filho2":
                img = pygame.transform.scale_by(img, 2)
            if self.player == True:
                img = pygame.transform.flip(img, True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.rectLoja = self.imageLoja.get_rect(center=(self.x_loja, self.y_loja))
        
    
    def desenhaMonstro(self, janela):
        janela.blit(self.image, self.rect)
    
    def desenhaMonstroLoja(self, janela, fonte, rubis):
        janela.blit(self.imageLoja, self.rectLoja)
        if rubis < self.custo:
            preco = fonte.render(f"{self.custo}", True, "gray")
        else:
            preco = fonte.render(f"{self.custo}", True, "green")
        janela.blit(preco, (self.x_loja + 80, self.y_loja))

    def update_animation(self):
        self.image = self.animation_list[self.action][self.index]
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
            self.count += 1
            if self.index >= 6:
                self.index = 0
        return self.count
    
    def checkForInputLoja(self, position):
            if position[0] in range(self.rectLoja.left, self.rectLoja.right) and position[1] in range(self.rectLoja.top, self.rectLoja.bottom):
                print(f"Button Press! Monstro: {self.nome}")
                return True
    
    def checkForInputBatalha(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                print(f"Button Press! Monstro: {self.nome}")
                return True

    def destacar(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom): 
                return True
            else:
                return False
    def destacarLoja(self, position):
            if position[0] in range(self.rectLoja.left, self.rectLoja.right) and position[1] in range(self.rectLoja.top, self.rectLoja.bottom): 
                return True
            else:
                return False
    
    def ativar(self, x, y, rubis):
        if rubis >= self.custo and self.ativo == False:
            self.ativo = True
            self.x_pos = x
            self.y_pos = y
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
            rubis -= self.custo
            return True
        return False
    
    def getCusto(self):
        return self.custo

#JOGAVEIS --- /// 
# 3 - corte, 4 - soco, 5 - fogo, 6 - agua, 7 - raio, 8 - neutro

ico = Monstro       ("ico"     , 100, 50, 90, 10, 5, 6)
linguico = Monstro  ("linguico", 100, 50, 90, 10, 4, 3)
amigo = Monstro     ("amigo"   , 100, 50, 90, 10, 8, 0)

#INIMIGOS --- ///

inim1 = Monstro     ("amigo",     100, 20, 20, 10, 8, 0)
inim2 = Monstro     ("filho",     100, 20, 20, 10, 6, 7)
inim3 = Monstro     ("linguico",  100, 20, 20, 10, 4, 3)
inim4 = Monstro     ("ico",       100, 20, 20, 10, 5, 6)
inim5 = Monstro     ("gelo",      100, 20, 20, 10, 6, 4)
inim6 = Monstro     ("horroroso", 100, 20, 20, 10, 4, 5)
inim7 = Monstro     ("adiburai",  100, 20, 20, 10, 3, 4)

equipe = []
equipeAtivos = []
equipe.append(ico)
equipe.append(linguico)
equipe.append(amigo)

colecaoInimigos = []

colecaoInimigos.append(inim1)
colecaoInimigos.append(inim2)
colecaoInimigos.append(inim3)
colecaoInimigos.append(inim4)
colecaoInimigos.append(inim5)
colecaoInimigos.append(inim6)
colecaoInimigos.append(inim7)

equipeInim  = []

loja0_img = pygame.image.load("imagem/background/loja0.png")

#FUNCOES --- ///

def cliqueMonstroLoja(equipe, posicao):

    for monstro in equipe:
        if monstro.checkForInputLoja(posicao):
            return monstro
    return False

def cliqueMonstroBatalha(equipe, posicao):
    for monstro in equipe:
        if monstro.checkForInputBatalha(posicao) and monstro.vivo:
            return monstro
    return False

def desenharMonstros(janela, equipe): #A posicao de batalha dos monstros é definida pela main, diferente da posicao dos inimigos

    for monstro in equipe:
        if monstro.ativo and monstro.vivo:
            monstro.desenhaMonstro(janela)
            monstro.update_animation()

def desenharLoja(janela, equipe, fonte, rubis):
    x = 95
    y = 70
    espacamento = 150

    janela.blit(loja0_img, (20, 10))

    for monstro in equipe:
        monstro.x_loja = x
        monstro.y_loja = y
        monstro.rectLoja = monstro.imageLoja.get_rect(center=(monstro.x_loja, monstro.y_loja))
        monstro.desenhaMonstroLoja(janela, fonte, rubis)
        y += espacamento

def contarAtivos(equipe):

    return len(equipe)

def gerarInimigos(round):
    
    equipeInim.clear()

    if round <= 9:
        nInimigos = int(round / 3)
    else:
        nInimigos = 3

    amostra = random.sample(colecaoInimigos, nInimigos)
    equipeInim.extend(amostra)

    xProx = 1250
    yProx = 320
    espYProx = 50
    espXProx = 160

    for monstro in equipeInim:
        monstro.ativar(xProx, yProx, 999)

        yProx += espYProx
        xProx -= espXProx

def contarVivos(grupo):
    count = 0
    for monstro in grupo:
        if monstro.vida <= 0:
            monstro.vivo = False
            grupo.remove(monstro)
        else:
            count += 1

    return count

def contarVivosInimigos(grupo):
    count = 0

    for monstro in grupo:
        if monstro.vida <= 0 and monstro.vivo:
            med.valor += monstro.custo
            print(f"Valor: {med.valor}")
            j.event_ganhouRubi = True
            monstro.vivo = False

        elif monstro.vivo:
            count += 1

    return count

def desenharMonsVez(janela, monstro):

    janela.blit(monstro.image, (700, 40))

def inimigoEscolheAlvo(equipe):

    alvo = random.choice(equipe)

    if alvo.vivo and alvo.ativo:
        return alvo
    else:
        return -1

descricao_img = pygame.image.load("imagem/background/descricao.png")
descricao_img = pygame.transform.scale(descricao_img, (300, 200))
descricao_img.set_alpha(200)
def desenhaDescricaoMonstro(janela, fonte, fonteNome, equipe, posicao):

    for monstro in equipe:
        if monstro.destacar(posicao):

            if monstro.magia == 3:
                magia = "Corte"
                cor = "crimson"
            if monstro.magia == 4:
                magia = "Impacto"
                cor = "gray"
            if monstro.magia == 5:
                magia = "Fogo"
                cor = "red"
            if monstro.magia == 6:
                magia = "Agua"
                cor = "blue"
            if monstro.magia == 7:
                magia = "Raio"
                cor = "yellow"
            if monstro.magia == 8:
                magia = "Neutro"
                cor = "purple"
            
            txtNome = fonteNome.render(f"{monstro.nome}", True, "white")
            txtVida = fonte.render(f"Vida: {monstro.vidamax}/{monstro.vida}", True, "white")
            # txtDescricao = fonte.render(monstro.descricao, True, "white")
            txtCusto = fonte.render(f"Custo: {monstro.custo}", True, "crimson")
            txtAtaque = fonte.render(f"Atq: {monstro.ataque}", True, "white")
            txtDefesa = fonte.render(f"Def: {monstro.defesa}", True, "white")
            txtMagia = fonte.render(f"Tipo de ataque: {magia}", True, cor)
            janela.blit(descricao_img, (posicao[0], posicao[1] - 200))
            janela.blit(txtNome, (posicao[0] + 10, posicao[1] - 195))
            # janela.blit(txtDescricao, (posicao[0] + 10, posicao[1] - 75))
            janela.blit(txtAtaque, (posicao[0] + 10, posicao[1] - 165))
            janela.blit(txtDefesa, (posicao[0] + 10, posicao[1] - 135))
            janela.blit(txtCusto, (posicao[0] + 10, posicao[1] - 105))
            janela.blit(txtMagia, (posicao[0] + 10, posicao[1] - 75))
            barraLar = 130
            barraAlt = 25
            ratio = monstro.vida / monstro.vidamax
            pygame.draw.rect(janela, "darkred", (posicao[0] + 120, posicao[1] - 195, barraLar, barraAlt))
            pygame.draw.rect(janela, "green3", (posicao[0] + 120, posicao[1] - 195, barraLar * ratio, barraAlt))
            janela.blit(txtVida, (posicao[0] + 120, posicao[1] - 165))
 
def retornaCor(monstro):

    if monstro.magia == 3:
        cor = "crimson"
    if monstro.magia == 4:
        cor = "gray"
    if monstro.magia == 5:
        cor = "red"
    if monstro.magia == 6:
        cor = "blue"
    if monstro.magia == 7:
        cor = "yellow"
    if monstro.magia == 8:
        cor = "purple"

    return cor