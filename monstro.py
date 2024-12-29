import pygame
import random
from medidor import *
from ataque import *
from infotext import *
from eventos import *

pygame.init()

class Monstro:

    def __init__(self, nome, vida, defesa, ataque, skill, custo, magia, fraqueza): 
        self.nome = nome
        self.vidamax = vida
        self.vida = vida
        self.vivo = True
        self.custo = custo
        self.defesa = defesa
        self.ataque = ataque
        self.defesaBase = defesa
        self.ataqueBase = ataque
        self.MODdef = 1
        self.MODatk = 1
        self.CounterAtk = 0
        self.CounterDef = 0
        self.player = False
        self.ativo = False
        self.magia = magia
        self.fraqueza = fraqueza
        self.x_pos = 0
        self.y_pos = 0
        self.x_loja = 0
        self.y_loja = 0
        self.especial = 0
        self.skill = skill
        self.image = pygame.image.load(f"imagem/lutador/{self.nome}/0.png")
        self.imageLoja = pygame.image.load(f"imagem/lutador/{self.nome}/loja.png")
        self.animation_cooldown = 100
        self.update_time = pygame.time.get_ticks()
        self.animation_list = []
        self.index = 0
        self.count = 0
        self.action = 0
        self.freezeTime = 0
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f"imagem/lutador/{self.nome}/{i}.png")
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(7, 5, -1):
            img = pygame.image.load(f'imagem/lutador/{self.nome}/{i}.png')
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.rectLoja = self.imageLoja.get_rect(center=(self.x_loja, self.y_loja))
    
    def machucado(self):
        #set variables to hurt animation
        self.action = 1
        self.index = 0
        self.update_time = pygame.time.get_ticks()

    def idle(self):
        self.action = 0
        self.index = 0
        self.update_time = pygame.time.get_ticks()

    def update_animation(self):
        self.image = self.animation_list[self.action][self.index]
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            if self.action == 0 or (self.action == 1 and self.index == 0):
                self.index += 1
            self.count += 1
            if self.action == 0:
                if self.index >= 6:
                    self.index = 0
            elif self.action == 1:
                if self.freezeTime > 8:
                    self.idle()
                    self.freezeTime = 0
                self.freezeTime += 1
        return self.count
    
    def desenhaMonstro(self, janela):
        janela.blit(self.image, self.rect)
    
    def desenhaMonstroLoja(self, janela, fonte, rubis):
        janela.blit(self.imageLoja, self.rectLoja)
        if rubis < self.custo:
            custoTxt = fonte.render("Custo: ", True, "gray")
            preco = fonte.render(f"{self.custo}", True, "gray")
        else:
            custoTxt = fonte.render("Custo: ", True, "crimson")
            preco = fonte.render(f"{self.custo}", True, "crimson")
        janela.blit(preco, (self.x_loja + 60, self.y_loja))
        janela.blit(custoTxt, (self.x_loja + 60, self.y_loja - 30))
    
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
    
    def updateStatus(self):
        if self.MODdef != 1:
            self.CounterDef += 1
        if self.MODatk != 1:
            self.CounterAtk += 1

        if self.CounterAtk >= 4:
            self.MODatk = 1
            self.CounterAtk = 0
            DefineTextoStatus("         NORMAL", self, j.txt_grupo, "gray", 14)
        if self.CounterDef >= 4:
            DefineTextoStatus("         NORMAL", self, j.txt_grupo, "gray", 15)
            self.MODdef = 1
            self.CounterDef = 0
        
        self.ataque = self.ataqueBase * self.MODatk
        self.defesa = self.defesaBase * self.MODdef

        print(f"Nome: {self.nome}, Ataque: {self.ataque}, Defesa: {self.defesa}")
    
    def ativarSkill(self, alvo):
        if self.skill.nome == "Explosao":
            alvo.vida -= self.skill.dano
            alvo.machucado()
            DefineTextoDano(self.skill.dano, alvo, j.txt_grupo, "red", 5)
            DefineAnimacaoAtaque(self, alvo.skill.tipo)
        

#JOGAVEIS --- /// 
# 3 - corte, 4 - soco, 5 - fogo, 6 - agua, 7 - raio, 8 - neutro

ico = Monstro       ("Ico"     , 1000, 50, 10, explosao, 10, 5, 6)
linguico = Monstro  ("Linguico", 1000, 50, 10, explosao, 10, 4, 3)
amigo = Monstro     ("Amigo"   , 1000, 50, 10, explosao, 10, 8, 0)

#INIMIGOS --- ///

inim1 = Monstro     ("Amigo",     100, 20, 20, explosao, 10, 8, 0)
inim2 = Monstro     ("Filho",     100, 20, 20, explosao, 10, 6, 7)
inim3 = Monstro     ("Linguico",  100, 20, 20, explosao, 10, 4, 3)
inim4 = Monstro     ("Ico",       100, 20, 20, explosao, 10, 5, 6)
inim5 = Monstro     ("Gelo",      100, 20, 20, explosao, 10, 6, 4)
inim6 = Monstro     ("Horroroso", 100, 20, 20, explosao, 10, 3, 5)
inim7 = Monstro     ("Adiburai",  100, 20, 20, explosao, 10, 4, 4)

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
            DefineAnimacaoAtaque(monstro, 9)
            grupo.remove(monstro)
        else:
            count += 1

    return count

def contarVivosInimigos(grupo):
    count = 0

    for monstro in grupo:
        if monstro.vida <= 0 and monstro.vivo:
            med.valor += monstro.custo
            DefineAnimacaoAtaque(monstro, 9)
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
descricao_img = pygame.transform.scale(descricao_img, (300, 240))
descricao_img.set_alpha(200)

def desenhaDescricaoMonstro(janela, fonte, fonteNome, equipe, posicao):

    for monstro in equipe:
        if monstro.destacar(posicao):

            if monstro.magia == 3:
                magia = "Corte"
            if monstro.magia == 4:
                magia = "Impacto"
            if monstro.magia == 5:
                magia = "Fogo"
            if monstro.magia == 6:
                magia = "Agua"
            if monstro.magia == 7:
                magia = "Raio"
            if monstro.magia == 8:
                magia = "Neutro"
            
            cor = retornaCor(monstro)
            if cor == "gray20":
                cor = "gray"
            
            txtNome = fonteNome.render(f"{monstro.nome}", True, "white")
            txtVida = fonte.render(f"Vida: {monstro.vidamax}/{int(monstro.vida)}", True, "white")
            # txtDescricao = fonte.render(monstro.descricao, True, "white")
            txtCusto = fonte.render(f"Custo de compra: {int(monstro.custo)}", True, "crimson")
            txtAtaque = fonte.render(f"Atq: {int(monstro.ataque)}", True, "white")
            txtDefesa = fonte.render(f"Def: {int(monstro.defesa)}", True, "white")
            txtMagia = fonte.render(f"Tipo de ataque: {magia}", True, cor)
            txtCustoSkill = fonte.render(f"Custo da Skill: {monstro.skill.custo}", True, "yellow")
            txtSkill = fonte.render(f"Skill: {monstro.skill.nome}", True, "white")
            janela.blit(descricao_img, (posicao[0], posicao[1] - 240))
            janela.blit(txtNome, (posicao[0] + 10, posicao[1] - 235))
            # janela.blit(txtDescricao, (posicao[0] + 10, posicao[1] - 75))
            janela.blit(txtAtaque, (posicao[0] + 10, posicao[1] - 205))
            janela.blit(txtDefesa, (posicao[0] + 10, posicao[1] - 175))
            janela.blit(txtMagia, (posicao[0] + 10, posicao[1] - 145))
            janela.blit(txtSkill, (posicao[0] + 10, posicao[1] - 115))
            janela.blit(txtCustoSkill,(posicao[0] + 10, posicao[1] - 85))   
            janela.blit(txtCusto, (posicao[0] + 10, posicao[1] - 55))

            
            barraLar = 130
            barraAlt = 25
            ratio = monstro.vida / monstro.vidamax
            pygame.draw.rect(janela, "darkred", (posicao[0] + 120, posicao[1] - 235, barraLar, barraAlt))
            pygame.draw.rect(janela, "green3", (posicao[0] + 120, posicao[1] - 235, barraLar * ratio, barraAlt))
            janela.blit(txtVida, (posicao[0] + 120, posicao[1] - 205))
 
def retornaCor(monstro):

    if monstro.magia == 3:
        cor = "gray20"
    if monstro.magia == 4:
        cor = "gray20"
    if monstro.magia == 5:
        cor = "red"
    if monstro.magia == 6:
        cor = "blue"
    if monstro.magia == 7:
        cor = "yellow"
    if monstro.magia == 8:
        cor = "purple"

    return cor
