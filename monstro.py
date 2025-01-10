import pygame
import random

import pygame.macosx
from medidor import *
from ataque import *
from infotext import *
from eventos import *

pygame.init()

class Monstro:

    def __init__(self, nome, vida, defesa, ataque, skill, custo, magia, fraqueza, animationtam): 
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
        self.MODatk2 = 1
        self.CounterAtk = 0
        self.CounterDef = 0
        self.condicao = 0
        self.CounterCon = 0
        self.player = False
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
        self.animationtam = animationtam
        self.animation_list = []
        self.index = 0
        self.count = 0
        self.action = 0
        self.freezeTime = 0
        temp_list = []
        for i in range(self.animationtam):
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
            if (self.action == 0 and self.condicao != 2) or (self.action == 1 and self.index == 0):
                self.index += 1
            self.count += 1
            if self.action == 0:
                if self.index >= self.animationtam:
                    self.index = 0
            elif self.action == 1:
                if self.freezeTime > 8:
                    self.idle()
                    self.freezeTime = 0
                self.freezeTime += 1
        return self.count
    
    def desenhaMonstro(self, janela):
        janela.blit(self.image, self.rect)
    
    def checkForInputBatalha(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                print(f"Button Press! Monstro: {self.nome}")
                return True

    def destacar(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom): 
                return True
            else:
                return False
    
    def ativar(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        return True
    
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
            DefineTextoStatus("         NORMAL", self, j.txt_grupo, "green", 14)
        if self.CounterDef >= 4:
            DefineTextoStatus("         NORMAL", self, j.txt_grupo, "green", 15)
            self.MODdef = 1
            self.CounterDef = 0

        self.ataque = self.ataqueBase * self.MODatk
        self.defesa = self.defesaBase * self.MODdef

        print(f"Nome: {self.nome}, Ataque: {self.ataque}, Defesa: {self.defesa}")
        
    def updateCondicao(self):

        if self.condicao != 0:
            self.CounterCon += 1

        if self.CounterCon >= 3:
            DefineTextoStatus("         NORMAL", self, j.txt_grupo, "green", 16)
            self.condicao = 0
            self.CounterCon = 0
        
        if self.condicao == 1:
            dano = self.vidamax / 6
            DefineTextoDano(dano, self, j.txt_grupo, "crimson", 8)
            DefineTextoStatus("     BLEED", self, j.txt_grupo, "crimson", 3)
            self.vida -= dano
            self.machucado()

        if self.condicao == 2:
            DefineTextoStatus("     FREEZE", self, j.txt_grupo, "blue", 6)
    
    def ativarSkill(self, alvo):
        if self.skill.nome == "Explosao":
            alvo.vida -= self.skill.dano
            alvo.machucado()
            DefineTextoDano(self.skill.dano, alvo, j.txt_grupo, "red", 5)
            DefineAnimacaoAtaque(alvo, self.skill.tipo)

        if self.skill.nome == 'Cura':
            cura = int(alvo.vidamax / 3)
            alvo.vida += cura
            if alvo.vida > alvo.vidamax:
                alvo.vida = alvo.vidamax
            DefineTextoStatus(cura, alvo, j.txt_grupo, "green", 16)
        
        if self.skill.nome == 'Treinar':
            self.MODatk2 = 2.5
            DefineTextoStatus("     UUPP!!", self, j.txt_grupo, "red", 10)
        
        if self.skill.nome == 'Surra':
            for alvo in equipeInim:
                if alvo.vivo:
                    alvo.vida -= self.skill.dano
                    DefineTextoDano(self.skill.dano, alvo, j.txt_grupo, "black", 4)
                    DefineAnimacaoAtaque(alvo, 4)
                    alvo.machucado()
        if self.skill.nome == 'Correr':
            if j.acoesEquipe != 5:
                j.acoesEquipe += 2
            else:
                DefineTextoMedidor("MAX", False, False, (self.x_pos, self.y_pos - 80), j.txt_grupo)

        
        if self.skill.nome == 'Wekapipo':
            for alvo in equipeInim:
                if alvo.vivo:
                    alvo.vida -= self.skill.dano
                    DefineTextoDano(self.skill.dano, alvo, j.txt_grupo, "black", 4)
                    DefineAnimacaoAtaque(alvo, 8)
                    alvo.machucado()
        
        if self.skill.nome == 'Cortar':
            if alvo.condicao == 0:
                alvo.condicao = 1
                alvo.CounterCon = 0
                alvo.vida -= self.skill.dano
                DefineTextoDano(self.skill.dano, alvo, j.txt_grupo, "red", 5)
                DefineAnimacaoAtaque(alvo, self.skill.tipo)
                # DefineTextoStatus("    BLEED", alvo, j.txt_grupo, "crimson", 3)
                alvo.machucado()
                alvo.updateCondicao()
            else:
                DefineTextoStatus("      FALHOU", self, j.txt_grupo, "crimson", 3)
        
        if self.skill.nome == 'Congelar':
            if alvo.condicao == 0:
                alvo.condicao = 2
                alvo.CounterCon = 0
                alvo.vida -= self.skill.dano
                DefineTextoDano(self.skill.dano, alvo, j.txt_grupo, "blue", 6)
                DefineAnimacaoAtaque(alvo, self.skill.tipo)
                # DefineTextoStatus("     FREEZE", alvo, j.txt_grupo, "blue", 6)
                alvo.machucado()
                alvo.updateCondicao()
            else:
                DefineTextoStatus("       FALHOU", self, j.txt_grupo, "blue", 6)
            
        

#JOGAVEIS --- /// 
# 3 - corte, 4 - soco, 5 - fogo, 6 - agua, 7 - raio, 8 - neutro

ico = Monstro       ("Ico"     , 20, 50, 30, explosao, 10, 5, 6, 6)
linguico = Monstro  ("Linguico", 20, 50, 30, surra, 10, 4, 3, 6)
amigo = Monstro     ("Amigo"   , 20, 50, 30, wekapipo, 10, 8, 0, 6)
filho = Monstro     ("Filho",       100, 20, 20, cura, 20, 5, 6, 6)
gelo = Monstro      ("Gelo",      1090, 20, 20, congelar, 20, 6, 4, 6)
horroroso = Monstro ("Xamilo", 100, 20, 20, cortar, 20, 3, 5, 6)
adiburai = Monstro  ("Adiburai",  100, 20, 20, treinar, 40, 4, 4, 6)
demonio = Monstro   ("Odiburoi", 1000, 50, 10, corre, 40, 5, 6, 4)

#INIMIGOS --- ///

inim1 = Monstro     ("Amigo",     100, 20, 20, explosao, 10, 8, 0, 6)
inim2 = Monstro     ("Filho",     100, 20, 20, explosao, 10, 6, 7, 6)
inim3 = Monstro     ("Linguico",  100, 20, 20, explosao, 10, 4, 3, 6)
inim4 = Monstro     ("Ico",       100, 20, 20, explosao, 10, 5, 6, 6)
inim5 = Monstro     ("Gelo",      100, 20, 20, explosao, 10, 6, 4, 6)
inim6 = Monstro     ("Xamilo", 100, 20, 20, explosao, 10, 3, 5, 6)
inim7 = Monstro     ("Adiburai",  100, 20, 20, explosao, 10, 4, 4, 6)

selecao = []

selecao.append(ico)
selecao.append(linguico)
selecao.append(amigo)
selecao.append(filho)
selecao.append(gelo)
selecao.append(horroroso)
selecao.append(adiburai)
selecao.append(demonio)

equipe = []
equipeAtivos = []


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

def cliqueMonstroBatalha(equipe, posicao):
    for monstro in equipe:
        if monstro.checkForInputBatalha(posicao) and monstro.vivo:
            return monstro
    return False

def desenharMonstros(janela, equipe): #A posicao de batalha dos monstros é definida pela main, diferente da posicao dos inimigos

    for monstro in equipe:
        if monstro.vivo:
            monstro.desenhaMonstro(janela)
            monstro.update_animation()

def contarAtivos(equipe):

    return len(equipe)

def gerarInimigos(round):
    
    equipeInim.clear()
    if round <= 9:
        if (round / 3) < 1:
            nInimigos = 1
        if (round / 3) >= 1 and (round / 3) < 2:
            nInimigos = 2
        if (round / 3) >= 2:
            nInimigos = 3

    amostra = random.sample(colecaoInimigos, nInimigos)
    equipeInim.extend(amostra)

    xProx = 1250
    yProx = 320
    espYProx = 50
    espXProx = 160

    for monstro in equipeInim:
        monstro.ativar(xProx, yProx)

        yProx += espYProx
        xProx -= espXProx

def DefinirPosicao(equipe):
    
    equipe[0].ativar(650, 330)
    if len(equipe) > 1:
        equipe[1].ativar(380, 380)
    if len(equipe) == 3:
        equipe[2].ativar(515, 430)
        

def contarVivos(grupo):
    count = 0
    for monstro in grupo:
        if monstro.vida <= 0 and monstro.vivo:
            monstro.vivo = False
            DefineAnimacaoAtaque(monstro, 9)
        elif monstro.vivo:
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

img_battlebox = pygame.image.load("imagem/background/battle_box.png")

img_battlebox.set_alpha(100)

def desenharMonsVez(janela, monstro):
    
    rect = img_battlebox.get_rect(center=(monstro.x_pos, monstro.y_pos + 40))
    janela.blit(img_battlebox, rect)
    
def inimigoEscolheAlvo(equipe):

    alvo = random.choice(equipe)

    if alvo.vivo:
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

            return True
 
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

def desenhaDescricaoLoja(janela, fonte, fonteNome, equipe, posicao):

    for monstro in equipe:
        if monstro.destacarLoja(posicao):

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
            
            janela.blit(descricao_img, (posicao[0]+ 60, posicao[1] - 80))
            janela.blit(txtNome, (posicao[0] + 70, posicao[1] - 75))
            # janela.blit(txtDescricao, (posicao[0] + 10, posicao[1] - 75))
            janela.blit(txtAtaque, (posicao[0] + 70, posicao[1] - 45))
            janela.blit(txtDefesa, (posicao[0] + 70, posicao[1] - 15))
            janela.blit(txtMagia, (posicao[0] + 70, posicao[1] + 15))
            janela.blit(txtSkill, (posicao[0] + 70, posicao[1] + 45))
            janela.blit(txtCustoSkill,(posicao[0] + 70, posicao[1] + 75))   
            janela.blit(txtCusto, (posicao[0] + 70, posicao[1] + 105))

            
            barraLar = 130
            barraAlt = 25
            ratio = monstro.vida / monstro.vidamax
            pygame.draw.rect(janela, "darkred", (posicao[0] + 180, posicao[1] - 75, barraLar, barraAlt))
            pygame.draw.rect(janela, "green3", (posicao[0] + 180, posicao[1] - 75, barraLar * ratio, barraAlt))
            janela.blit(txtVida, (posicao[0] + 180, posicao[1] - 45))

            return True

def desenhaMonstrosMenuPrincipal(janela, equipe):
    x = 130
    y = 180
    espacamentoX = 210
    espacamentoY = 290
    for monstro in equipe:
        rect = monstro.image.get_rect(center=(x , y + j.buttonPosOffset))
        janela.blit(monstro.image, rect)
        x += espacamentoX
        if x > 550:
            x = 130
            y += espacamentoY