import pygame
import random

import pygame.macosx
from medidor import *
from ataque import *
from infotext import *
from eventos import *

pygame.init()
pygame.display.set_mode((1,1), pygame.NOFRAME)

# Monstro - status, paramentros e imagens de um lutador, rege todas as situacoes e informacoes de um lutador

class Monstro:

    def __init__(self, nome, vida, defesa, ataque, sorte, skill, custo, magia, fraqueza, animationtam): 
        self.nome = nome
        self.vidamax = vida
        self.vida = vida
        self.vidaBase = vida
        self.vivo = True
        self.custo = custo
        self.custoBase = custo
        self.defesa = defesa
        self.ataque = ataque
        self.sorte = sorte
        self.ataqueNormal = ataque
        self.defesaNormal = defesa
        self.sorteBase = sorte
        self.defesaBase = defesa
        self.ataqueBase = ataque
        self.MODdef = 1
        self.MODatk = 1
        self.MODatk2 = 1
        self.CounterAtk = 0
        self.CounterDef = 0
        self.condicao = 0
        self.CounterCon = 0
        self.gauge = 0
        self.safe = False
        self.danoAcumulado = 0
        self.player = False
        self.magia = magia
        self.fraqueza = fraqueza
        self.fraquezaBase = fraqueza
        self.x_pos = 0
        self.y_pos = 0
        self.especial = 0
        self.revelouMagia = False
        self.revelouFraqueza = False
        self.revelouVida = False
        self.skill = skill #skill do monstro
        self.image = pygame.image.load(f"imagem/lutador/{self.nome}/0.png").convert_alpha()
        self.animation_cooldown = 100
        self.update_time = pygame.time.get_ticks()
        self.animationtam = animationtam
        self.animation_list = []
        self.index = 0
        self.count = 0
        self.action = 0
        self.freezeTime = 0
        temp_list = []
        for i in range(self.animationtam): # armazena o sprite sheet do monstro numa lista # sprite sheet de idle
            img = pygame.image.load(f"imagem/lutador/{self.nome}/{i}.png").convert_alpha()
            
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(7, 5, -1): # sprite sheet de machucado
            img = pygame.image.load(f'imagem/lutador/{self.nome}/{i}.png').convert_alpha()
            
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
    
    # machucado - altera a acao da lista de animacao para triggar a animacao de estar machucado do monstro

    def machucado(self):
        #set variables to hurt animation
        self.action = 1
        self.index = 0
        self.update_time = pygame.time.get_ticks()

    # idle - altera a acao da lista de animacao para triggar a animacao de idle do monstro
    def idle(self):
        self.action = 0
        self.index = 0
        self.update_time = pygame.time.get_ticks()

    # update_animation - atualiza o index (ou acao) da lista de animacao para atualizar a imagem a ser exibida

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
    
    # desenhaMonstro - desenha o monstro individualmente na tela

    def desenhaMonstro(self, janela):
        janela.blit(self.image, self.rect)

    # checkForInputBatalha - verifica se houve um clique dentro do retangulo do monstro

    def checkForInputBatalha(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                return True

    # destacar - verifica se o mouse esta sobre o retangulo do monstro

    def destacar(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom): 
                return True
            else:
                return False
    
    # ativar - define as coordenadas do monstro na tela de batalha

    def ativar(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        return True
    
    # getCusto - retorna o custo do monstro

    def getCusto(self):
        return self.custo
    
    # atualiza os status de ataque e defesa do monstro

    def updateStatus(self):
        if self.MODdef != 1: #incrementa os contadores para indicar quantos turnos o monstro esta com o status alterados
            self.CounterDef += 1
        if self.MODatk != 1:
            self.CounterAtk += 1

        if self.CounterAtk >= 4: # reinicia os modificadores dos status caso o numero de turnos necessarios forem cumpridos
            self.MODatk = 1
            self.CounterAtk = 0
            DefineTextoStatus("           NORMAL", self, j.txt_grupo, "green", 14) # lanca um texto de status para indicar que os status foram normalizados
        if self.CounterDef >= 4:
            DefineTextoStatus("           NORMAL", self, j.txt_grupo, "green", 15)
            self.MODdef = 1
            self.CounterDef = 0
        
        if self.MODatk > 2:
            self.MODatk = 2
        if self.MODdef > 2:
            self.MODdef = 2
        
        self.ataque = self.ataqueNormal * self.MODatk
        self.defesa = self.defesaNormal * self.MODdef
    
    def updateInstant(self):

        if self.MODatk > 2:
            self.MODatk = 2
        if self.MODdef > 2:
            self.MODdef = 2

        self.ataque = self.ataqueNormal * self.MODatk
        self.defesa = self.defesaNormal * self.MODdef

    # updateCondicao - atualiza a condicao do monstro

    def updateCondicao(self):

        if self.condicao != 0: #incrementa os contadores para indicar quantos turnos o monstro esta com a condicao alterada
            self.CounterCon += 1

        if self.CounterCon >= 3: # reinicia os modificadores de condicao caso o numero de turnos necessarios forem cumpridos
            DefineTextoStatus("           NORMAL", self, j.txt_grupo, "green", 16) # lanca um texto de status para indicar que as condicoes foram normalizadas
            self.condicao = 0 
            self.CounterCon = 0
        
        if self.condicao == 1: # condicao '1' - sangramento, da dano ao monstro quando esse metodo for chamado
            dano = self.vidamax / 10
            DefineTextoDano(dano, self, j.txt_grupo, "crimson", 8)
            DefineTextoStatus("       BLEED", self, j.txt_grupo, "crimson", 3)
            self.vida -= dano
            self.machucado()
            j.dano += dano

        if self.condicao == 2:# condicao '2' - congelamento, pula o turno do monstro quando for a vez dele
            DefineTextoStatus("       FREEZE", self, j.txt_grupo, "blue", 6)
        
    def updateInstantCondicao(self):

        if self.condicao == 1: # condicao '1' - sangramento, da dano ao monstro quando esse metodo for chamado
            DefineTextoStatus("       BLEED", self, j.txt_grupo, "crimson", 3)

        if self.condicao == 2:# condicao '2' - congelamento, pula o turno do monstro quando for a vez dele
            DefineTextoStatus("       FREEZE", self, j.txt_grupo, "blue", 6)
    
    # ativarSkill - ativa os efeitos da skills armazenadas pelo monstro
    def ativarSkill(self, alvo, grupo1, grupo2):
        if self.skill.nome == "Explosao":
            dano = self.skill.dano * self.MODatk
            alvo.vida -= dano
            self.danoAcumulado += dano
            alvo.machucado()
            DefineTextoDano(dano, alvo, j.txt_grupo, "red", 5)
            DefineAnimacaoAtaque(alvo, self.skill.tipo)
            if alvo.skill.nome == "Devolver":
                    alvo.gauge += int(dano * 0.8)
            j.dano += dano

        if self.skill.nome == 'Cura':
            cura = int(alvo.vidamax / 3)
            alvo.vida += cura
            if alvo.vida > alvo.vidamax:
                alvo.vida = alvo.vidamax
            DefineTextoStatus(cura, alvo, j.txt_grupo, "green", 16)
            DefineAnimacaoAtaque(alvo, 11)
            j.cura += cura
        
        if self.skill.nome == 'Treinar':
            self.MODatk2 = 2.5
            DefineTextoStatus("      UUPP!!", self, j.txt_grupo, "red", 10)
        
        if self.skill.nome == 'Surra':
            dano = self.skill.dano * self.MODatk
            for alvo in grupo1:
                if alvo.vivo:
                    alvo.vida -= dano
                    DefineTextoDano(dano, alvo, j.txt_grupo, "black", 4)
                    DefineAnimacaoAtaque(alvo, 4)
                    alvo.machucado()
                    self.danoAcumulado += dano
                    if alvo.skill.nome == "Devolver":
                        alvo.gauge += int(dano * 0.8)
                    j.dano += dano

        if self.skill.nome == 'Correr':
            if j.acoesEquipe < 4.5:
                j.acoesEquipe += 2
            else:
                DefineTextoMedidor("MAX", False, False, (self.x_pos, self.y_pos - 80), j.txt_grupo)

        
        if self.skill.nome == 'Wekapipo':
            dano = self.skill.dano * self.MODatk
            for alvo in grupo1:
                if alvo.vivo:
                    alvo.vida -= dano
                    DefineTextoDano(dano, alvo, j.txt_grupo, "black", 4)
                    DefineAnimacaoAtaque(alvo, 8)
                    alvo.machucado()
                    self.danoAcumulado += dano
                    if alvo.skill.nome == "Devolver":
                        alvo.gauge += int(dano * 0.8)
                    j.dano += dano
        
        if self.skill.nome == 'Cortar':
            dano = self.skill.dano * self.MODatk
            if alvo.condicao == 0:
                alvo.condicao = 1
                alvo.CounterCon = 0
                alvo.vida -= dano
                DefineTextoDano(dano, alvo, j.txt_grupo, "red", 5)
                DefineAnimacaoAtaque(alvo, self.skill.tipo)
                # DefineTextoStatus("    BLEED", alvo, j.txt_grupo, "crimson", 3)
                alvo.machucado()
                alvo.updateInstantCondicao()
                self.danoAcumulado += dano
                if alvo.skill.nome == "Devolver":
                    alvo.gauge += int(dano * 0.8)
                j.dano += dano
            else:
                DefineTextoStatus("       FALHOU", self, j.txt_grupo, "crimson", 3)
        
        if self.skill.nome == 'Congelar':
            dano = self.skill.dano * self.MODatk
            if alvo.condicao == 0:
                alvo.condicao = 2
                alvo.CounterCon = 0
                alvo.vida -= dano
                DefineTextoDano(dano, alvo, j.txt_grupo, "blue", 6)
                DefineAnimacaoAtaque(alvo, self.skill.tipo)
                # DefineTextoStatus("     FREEZE", alvo, j.txt_grupo, "blue", 6)
                alvo.machucado()
                alvo.updateInstantCondicao()
                self.danoAcumulado += dano
                if alvo.skill.nome == "Devolver":
                    alvo.gauge += int(dano * 0.8)
                j.dano += dano
            else:
                DefineTextoStatus("        FALHOU", self, j.txt_grupo, "blue", 6)
        
        if self.skill.nome == "Trocar":

            while 1:
                alvo = random.choice(equipe)
                if alvo.vivo:
                    break
            
            self.magia = alvo.fraqueza
            if alvo.fraqueza == 0:
                self.magia = 8
            DefineTextoStatus("         MUDOU", self, j.txt_grupo, "black", 10)
        
        if self.skill.nome == "Focar":
            num = random.randint(1, 2)
            if num == 1:
                self.MODatk2 = 3.5
                DefineTextoStatus("          FOCADO!!", self, j.txt_grupo, "red", 10)
            else:
                self.MODdef = 2
                self.CounterDef = 0
                DefineTextoStatus("          FOCADO!!", self, j.txt_grupo, "olive", 11)
        
        if self.skill.nome == "Analisar":
            alvo.revelouMagia = True
            alvo.revelouFraqueza = True
            alvo.revelouVida = True

            DefineTextoStatus("        INFO", alvo, j.txt_grupo, "black", 11)
        
        if self.skill.nome == "Devolver":
            dano = self.gauge * 1.2 * self.MODatk
            alvo.vida -= dano
            self.danoAcumulado += dano
            alvo.machucado()
            DefineTextoDano(dano, alvo, j.txt_dano, "black", 3)
            DefineAnimacaoAtaque(alvo, 10)
            self.gauge = 0
            DefineTextoStatus("       RESET", self, j.txt_grupo, "black", 15)
            j.dano += dano

        if self.skill.nome == "Comer":
            dano = self.skill.dano * self.MODatk
            alvo.vida -= dano
            alvo.machucado()
            DefineTextoDano(dano, alvo, j.txt_grupo, "black", 3)
            if alvo.vida <= 0:
                j.event_perdeuEnergia = False
                j.event_ganhouEnergia = True
                med.valorE = 20
            j.dano += dano

        if self.skill.nome == "Rezar":
            j.event_perdeuEnergia = False
            j.event_ganhouEnergia = True
            self.vida -= 15
            self.machucado()
            DefineTextoDano(15, self, j.txt_dano, "black", 3)
            DefineAnimacaoAtaque(self, 8)
            med.valorE = 30
            j.dano += 15
        
        if self.skill.nome == "Sabotar":
            num = random.randint(1, 2)
            if num == 1:
                j.event_perdeuEnergia = True
                med.valorE = 30
            else:
                for alvo in grupo1:
                    if alvo.vivo:
                        dano = self.skill.dano * self.MODatk
                        alvo.vida -= dano
                        DefineTextoDano(dano, alvo, j.txt_grupo, "black", 4)
                        DefineAnimacaoAtaque(alvo, 4)
                        alvo.machucado()
                        self.danoAcumulado += dano
                        if alvo.skill.nome == "Devolver":
                            alvo.gauge += int(dano * 0.8)
                        j.dano += dano
        
        if self.skill.nome == 'Saraivada':
            for alvo in grupo1:
                if alvo.vivo:
                    dano = self.skill.dano * self.MODatk
                    alvo.vida -= dano
                    DefineTextoDano(dano, alvo, j.txt_grupo, "black", 4)
                    DefineAnimacaoAtaque(alvo, 6)
                    alvo.machucado()
                    self.danoAcumulado += dano
                    if alvo.skill.nome == "Devolver":
                        alvo.gauge += int(dano * 0.8)
                    j.dano += dano

        if self.skill.nome == 'Wekapeople':
            for alvo in grupo1:
                if alvo.vivo:
                    dano = self.skill.dano * self.MODatk
                    alvo.vida -= dano
                    DefineTextoDano(dano, alvo, j.txt_grupo, "black", 4)
                    DefineAnimacaoAtaque(alvo, 8)
                    alvo.machucado()
                    self.danoAcumulado += dano
                    if alvo.skill.nome == "Devolver":
                        alvo.gauge += int(dano * 0.8)
                    j.dano += dano
        
        if self.skill.nome == 'Eletroterapia':
            alvo.MODatk *= 1.3
            alvo.MODdef *= 1.2
            alvo.CounterAtk = 0
            alvo.CounterDef = 0
            alvo.updateInstant()
            DefineTextoStatus("UP", alvo, j.txt_grupo, "black", 10)
            DefineTextoStatus("UP", alvo, j.txt_grupo, "black", 11)
        
        if self.skill.nome == 'Debilitar':

            for alvo in grupo1:
                if random.randint(1, 2) == 1:
                    alvo.condicao = random.randint(1, 2)
                    alvo.CounterCon = 0
                    alvo.updateInstantCondicao()
                else:
                    alvo.MODdef = 0.8
                    alvo.MODatk = 0.8
                    alvo.updateInstant()
                    DefineTextoStatus("     DOWN", alvo, j.txt_grupo, "black", 12)
                    DefineTextoStatus("     DOWN", alvo, j.txt_grupo, "black", 13)

        if self.skill.nome == 'Nevasca':
            dano = self.skill.dano * self.MODatk
            for alvo in grupo1:
                if random.randint(1, 4) == 5:
                    alvo.condicao = 2
                    alvo.CounterCon = 0
                    alvo.updateInstantCondicao()
                alvo.vida -= dano
                alvo.machucado()
                DefineTextoDano(dano, alvo, j.txt_dano, "black", 6)
                DefineAnimacaoAtaque(alvo, 6)
                j.dano += dano
        
        if self.skill.nome == 'Bencao':
            for alvo in grupo2:
                cura = int(alvo.vidamax / 4)
                alvo.vida += cura
                if alvo.vida > alvo.vidamax:
                    alvo.vida = alvo.vidamax
                DefineTextoStatus(cura, alvo, j.txt_grupo, "green", 16)
                DefineAnimacaoAtaque(alvo, 11)
                j.cura += cura
#JOGAVEIS --- /// 
# 3 - corte, 4 - soco, 5 - fogo, 6 - agua, 7 - raio, 8 - neutro

                    #nome        vda def atq srt  skl     cst mga fqz animationtam                                
ico = Monstro       ("Ico"     , 100,  35, 25, 6,  explosao, 10, 5, 6, 6)
linguico = Monstro  ("Linguico", 100,  25, 25, 6,  surra,    10, 4, 3, 6)
amigo = Monstro     ("Amigo"   , 100,  20, 30, 8,  wekapipo, 15, 8, 0, 6)
filho = Monstro     ("Filho",    120,  25, 40, 12, cura,     20, 7, 4, 6)
gelo = Monstro      ("Gelo",     130,  30, 40, 8,  congelar, 20, 6, 5, 6)
horroroso = Monstro ("Xamilo",   145,  25, 45, 6,  cortar,   25, 3, 4, 6)
bombinha = Monstro  ("Bombinha", 140,  30, 45, 8,  devolver, 30, 5, 7, 6)
camboja = Monstro   ("Camboja",  150,  35, 40, 6,  eletroterapia, 30, 7, 5, 3)
monge = Monstro     ("Monge",    160,  25, 40, 10, rezar,   30, 4, 8, 1)
camboja.animation_cooldown = 200
bireco = Monstro    ("Birecos",  190,  30, 30, 15, bencao,  35, 8, 0, 1)
adiburai = Monstro  ("Adiburai", 180,  35, 50, 12, treinar, 40, 4, 4, 6)
kamirider = Monstro ("Kamirider",175,  30, 55, 15, comer,   40, 3, 3, 4)
demonio = Monstro   ("Demonio",  200,  50, 20, 6,  analisar,40, 8, 0, 6)
odiburoi = Monstro  ("Odiburoi", 180,  30, 45, 6,  corre,   40, 7, 6, 4)
 
parceiro = Monstro  ("Parceiro", 190,  35, 55, 12, wekapeople, 0, 8, 0, 6)
azuliu = Monstro    ("Azuliu",   210,  30, 60, 8,  saraivada,  0, 6, 0, 6)
ediburei = Monstro  ("Ediburei", 200,  40, 55, 12, focar,      0, 4, 0, 6)

#INIMIGOS --- /// # 3 - corte, 4 - soco, 5 - fogo, 6 - agua, 7 - raio, 8 - neutro

inim1 = Monstro     ("Amigo",    120, 20, 35, 12, wekapipo,  15, 8, 0, 6)
inim2 = Monstro     ("Filho",    120, 25, 25, 12, cura,      15, 5, 7, 6)
inim3 = Monstro     ("Linguico", 120, 20, 25, 12, surra,     20, 4, 3, 6)
inim4 = Monstro     ("Ico",      140, 20, 30, 12, explosao,  25, 5, 6, 6)
inim5 = Monstro     ("Gelo",     130, 20, 25, 12, congelar,  25, 6, 4, 6)
inim6 = Monstro     ("Xamilo",   130, 25, 30, 12, cortar,    25, 3, 5, 6)
inim7 = Monstro     ("Adiburai", 130, 20, 35, 12, treinar,   25, 4, 4, 6)

inim8 = Monstro     ("Demonio",  190, 50, 40, 12, wekapipo,  30, 8, 0, 6)
inim9 = Monstro     ("Bombinha", 155, 30, 50, 12, devolver,  30, 5, 3, 6)
inim10 = Monstro    ("Linguico", 150, 30, 55, 18, surra,     35, 4, 7, 6)
inim11 = Monstro    ("Ico",      170, 30, 50, 12, explosao,  40, 5, 7, 6)
inim12 = Monstro    ("Gelo",     150, 35, 45, 12, nevasca,   40, 6, 5, 6)
inim13 = Monstro    ("Xamilo",   160, 35, 60, 18, cortar,    40, 3, 0, 6)
inim14 = Monstro    ("Adiburai", 160, 30, 60, 18, treinar,   40, 4, 6, 6)

inim15 = Monstro    ("Demonio",  250, 55, 45, 18,nevasca,   45, 8, 0, 6)
inim16 = Monstro    ("Bombinha", 220, 40, 60, 12, devolver,  45, 6, 6, 6)
inim17 = Monstro    ("Kamirider",190, 30, 75, 16,surra,     45, 3, 3, 4)
inim18 = Monstro    ("Odiburoi", 210, 30, 70, 14, corre,     55, 7, 6, 4)
inim19 = Monstro    ("Monge",    200, 35, 60, 21,saraivada, 55, 6, 4, 1)
inim20 = Monstro    ("Camboja",  230, 45, 65, 16,eletroterapia,55, 3, 5, 3)
inim21 = Monstro    ("Adiburai", 230, 40, 70, 16,treinar,   55, 4, 7, 6)

#BOSS --- ///

pepeteco = Monstro  ("Pepeteco", 1000, 55, 45, 18, sabotar, 90, 3, 0, 6)
pepeteco.bg = pygame.image.load("imagem/background/bg2.png").convert()
mestre = Monstro    ("Mestre", 800, 40, 65, 20, focar, 90, 4, 0, 6)
mestre.bg = pygame.image.load("imagem/background/bg3.png").convert()
mago = Monstro      ("Mago", 900, 40, 50, 16, mudar, 90, 8, 0, 6)
mago.bg = pygame.image.load("imagem/background/bg0.png").convert()
bobonauta = Monstro ("Bobonaut", 800, 35, 45, 18, debilitar, 90, 6, 0, 6)
bobonauta.bg = pygame.image.load("imagem/background/bg4.png").convert()
bobonauta.animation_cooldown = 200

# lista que armazena os personagens jogaveis
selecao = []

selecao.append(ico)
selecao.append(linguico)
selecao.append(amigo)
selecao.append(filho)
selecao.append(gelo)
selecao.append(horroroso)
selecao.append(adiburai)
selecao.append(demonio)
selecao.append(odiburoi)
selecao.append(kamirider)
selecao.append(bombinha)
selecao.append(ediburei)
selecao.append(azuliu)
selecao.append(parceiro)
selecao.append(camboja)
selecao.append(monge)
selecao.append(bireco)

# equipe que foi selecionada e que sera usada para a batalha

equipe = []

# inativo
equipeAtivos = []

# colecao dos inimigos que aparecerao nos primeiros 3 turnos

colecaoInimigos = []

colecaoInimigos.append(inim1)
colecaoInimigos.append(inim2)
colecaoInimigos.append(inim3)
colecaoInimigos.append(inim4)
colecaoInimigos.append(inim5)
colecaoInimigos.append(inim6)
colecaoInimigos.append(inim7)

# colecao dos inimigos que aparecerao dos turnos 5 a 7

colecaoInimigos2 = []

colecaoInimigos2.append(inim8)
colecaoInimigos2.append(inim9)
colecaoInimigos2.append(inim10)
colecaoInimigos2.append(inim11)
colecaoInimigos2.append(inim12)
colecaoInimigos2.append(inim13)
colecaoInimigos2.append(inim14)

# colecao dos inimigos que aparecerao dos turnos 9 a 11

colecaoInimigos3 = []

colecaoInimigos3.append(inim15)
colecaoInimigos3.append(inim16)
colecaoInimigos3.append(inim17)
colecaoInimigos3.append(inim18)
colecaoInimigos3.append(inim19)
colecaoInimigos3.append(inim20)
colecaoInimigos3.append(inim21)

equipeInim  = []

colecaoBoss = []

colecaoBoss.append(pepeteco)
colecaoBoss.append(mestre)
colecaoBoss.append(mago)
colecaoBoss.append(bobonauta)


#FUNCOES --- ///

# cliquecliqueMonstroBatalha - detecta se um monstro em batalha teve um input de clique na batalha
# retorna o monstro em que o input é verdadeiro

def cliqueMonstroBatalha(equipe, posicao):
    for monstro in equipe:
        if monstro.checkForInputBatalha(posicao) and monstro.vivo:
            return monstro
    return False

# desenharMonstros - desenha os monstros numa equipe
def desenharMonstros(janela, equipe): #A posicao de batalha dos monstros é definida pela main, diferente da posicao dos inimigos

    for monstro in equipe:
        if monstro.vivo:
            monstro.desenhaMonstro(janela)
            monstro.update_animation()

# gerarInimigos - gera os inimigos com base no round atual
# sao selecionados em samples, nunca se repetem

def gerarInimigos(round):
    
    equipeInim.clear()
    if round == 1:
        nInimigos = 1
    if round == 2:
        nInimigos = 2
    if round >= 3:
        nInimigos = 3
    
    if round <= 4:
        amostra = random.sample(colecaoInimigos, nInimigos)
    if round >= 5 and round <= 8:
        amostra = random.sample(colecaoInimigos2, nInimigos)
    if round >= 9:
        amostra = random.sample(colecaoInimigos3, nInimigos)
    equipeInim.extend(amostra)

    xProx = 1250
    yProx = 320
    espYProx = 50
    espXProx = 160

    for monstro in equipeInim:
        monstro.ativar(xProx, yProx)

        yProx += espYProx
        xProx -= espXProx

# gerarBoss - se for os rounds 4, 8 ou 12, adiciona um boss a equipe inimiga
# nunca é selecionado o mesmo boss mais de uma vez numa run

def gerarBoss(round):

    equipeInim.clear()

    xProx = 1250 - 210
    yProx = 320 + 50

    boss = random.choice(colecaoBoss)
    equipeInim.append(boss)
    colecaoBoss.remove(boss)

    boss.ativar(xProx, yProx)

    return boss.bg
    
# definirPosicao - ativa todos os monstros da equipe com base na ordem

def DefinirPosicao(equipe):
    
    equipe[0].ativar(650, 330)
    if len(equipe) > 1:
        equipe[1].ativar(380, 380)
    if len(equipe) == 3:
        equipe[2].ativar(515, 430)
        
# contarVivos - conta quando monstros da equipe aliada estao vivos (vida > 0)
# mata os que a vida < 0
# ativa o efeito de safe do monstro

def contarVivos(grupo):
    count = 0
    for monstro in grupo:
        if monstro.vida <= 0 and monstro.vivo:
            if monstro.safe == False:
                monstro.vivo = False
                DefineAnimacaoAtaque(monstro, 9)
                monstro.vida = 0
            elif monstro.safe:
                DefineTextoStatus("       SAFE", monstro, j.txt_grupo, "black", 16)
                monstro.vida = int(monstro.vidamax / 10)
                count += 1
        elif monstro.vivo:
            count += 1

    return count

# contarVivosInimigos - conta quando monstros da equipe inimiga estao vivos (vida > 0)
# ativa certos eventos que sao acionados a partir da morte de monstros inimigos

def contarVivosInimigos(grupo):
    count = 0

    for monstro in grupo:
        if monstro.vida <= 0 and monstro.vivo:
            med.valor += monstro.custo
            DefineAnimacaoAtaque(monstro, 9)
            monstro.revelouVida = True
            j.event_ganhouRubi = True
            monstro.vivo = False
            monstro.vida = 0
            if j.event_dropaCard:
                from carta import mao, deck, adicionaCarta
                num = random.randint(1, 4)
                if num == 4 and len(mao) < 4:
                    adicionaCarta(deck, mao)
                    DefineTextoStatus("     CARD", monstro, j.txt_grupo, "black", 17)
            j.event_ganhouEnergia = True
            med.valorE += 30
                    
        elif monstro.vivo:
            count += 1

    return count

img_battlebox = pygame.image.load("imagem/background/battle_box.png").convert_alpha()

img_battlebox.set_alpha(100)

# desenharMonsVez - desenha um disco abaixo do monstro da vez

def desenharMonsVez(janela, monstro):
    
    rect = img_battlebox.get_rect(center=(monstro.x_pos, monstro.y_pos + 40))
    janela.blit(img_battlebox, rect)

# inimigoEscolheAlvo - retorna um monstro aliado aleatorio para servir de alvo para os inimigos
# so retorna monstros vivos

def inimigoEscolheAlvo(equipeAlvo):

    alvo = random.choice(equipeAlvo)

    if alvo.vivo:
        return alvo
    else:
        return -1

descricao_img = pygame.image.load("imagem/background/descricao.png").convert()

descricao_img = pygame.transform.scale(descricao_img, (380, 240)).convert()
descricao_img.set_alpha(200)

# desenhaDescricaoMonstro - exibe os specs do monstro num retangulo flutuante a partir da posicao do mouse

def desenhaDescricaoMonstro(janela, fonte, fonteNome, equipe, posicao):

    for monstro in equipe:
        if monstro.destacar(posicao):

            cor = retornaCor(monstro.magia)
            txtNome = fonteNome.render(f"{monstro.nome}", True, "white")
            txtVida = fonte.render(f"Vida: {monstro.vidamax}/{int(monstro.vida)}", True, "white")
            txtCusto = fonte.render(f"Custo de compra: {int(monstro.custo)}", True, "crimson")           
            txtAtaque = fonte.render(f"Atq: {int(monstro.ataque)}", True, "white")            
            txtDefesa = fonte.render(f"Def: {int(monstro.defesa)}", True, "white")            
            txtMagia = fonte.render(f"Ataque:", True, cor)
            txtFraqueza = fonte.render(f"Fraqueza:", True, retornaCor(monstro.fraqueza))         
            txtCustoSkill = fonte.render(f"Custo da Skill: {monstro.skill.custo}", True, "yellow")            
            txtSkill = fonte.render(f"Skill: {monstro.skill.nome}", True, "white")
            txtSorte = fonte.render(f"Srt: {int(monstro.sorte)}", True, "white")
          
            janela.blit(descricao_img, (posicao[0], posicao[1] - 240))
            janela.blit(txtNome, (posicao[0] + 10, posicao[1] - 235))
            janela.blit(txtAtaque, (posicao[0] + 10, posicao[1] - 205))
            janela.blit(txtDefesa, (posicao[0] + 10, posicao[1] - 175))
            janela.blit(txtSorte, (posicao[0] + 10, posicao[1] - 145))

            janela.blit(txtMagia, (posicao[0] + 280, posicao[1] - 235))
            janela.blit(retornaImagem(monstro.magia), (posicao[0] + 300, posicao[1] - 195))
            if monstro.fraqueza != 0:
                janela.blit(txtFraqueza, (posicao[0] + 270, posicao[1] - 140))
                janela.blit(retornaImagem(monstro.fraqueza), (posicao[0] + 300, posicao[1] - 100))

            janela.blit(txtSkill, (posicao[0] + 10, posicao[1] - 115))
            janela.blit(txtCustoSkill,(posicao[0] + 10, posicao[1] - 85))   
            janela.blit(txtCusto, (posicao[0] + 10, posicao[1] - 55))
            if monstro.MODdef > 1:
                janela.blit(def_up, (posicao[0] + 280, posicao[1] - 55))
            if monstro.MODatk > 1 or monstro.MODatk2 > 1:
                janela.blit(atk_up, (posicao[0] + 310, posicao[1] - 55))
            if monstro.MODdef < 1:
                janela.blit(def_down, (posicao[0] + 280, posicao[1] - 55))
            if monstro.MODatk < 1 and monstro.MODatk2 == 1:
                janela.blit(atk_down, (posicao[0] + 310, posicao[1] - 55))
            if monstro.condicao == 2:
                janela.blit(congelamento, (posicao[0] + 240, posicao[1] - 55))
            elif monstro.condicao == 1:
                janela.blit(sangramento, (posicao[0] + 240, posicao[1] - 55))
            barraLar = 130
            barraAlt = 25
            ratio = monstro.vida / monstro.vidamax
            pygame.draw.rect(janela, "darkred", (posicao[0] + 120, posicao[1] - 235, barraLar, barraAlt))
            pygame.draw.rect(janela, "green3", (posicao[0] + 120, posicao[1] - 235, barraLar * ratio, barraAlt))
            janela.blit(txtVida, (posicao[0] + 120, posicao[1] - 205))

            return True

descricaoInim_img = pygame.image.load("imagem/background/descricao.png").convert()

descricaoInim_img = pygame.transform.scale(descricao_img, (300, 240)).convert()
descricaoInim_img.set_alpha(200)

# desenhaDescricaoMonstro - exibe os specs do monstro inimigo num retangulo flutuante a partir da posicao do mouse
# so exibe informacoes ja descobertas pelo jogador

def desenhaDescricaoMonstroInim(janela, fonte, fonteNome, equipeInim, posicao):

    for monstro in equipeInim:
        if monstro.destacar(posicao) and monstro.vivo:

            cor = retornaCor(monstro.magia)
            txtNome = fonteNome.render(f"{monstro.nome}", True, "white")
            if monstro.revelouVida:
                txtVida = fonte.render(f"Vida: {monstro.vidamax}/{int(monstro.vida)}", True, "white")
                txtCusto = fonte.render(f"Recompensa: {int(monstro.custo)}", True, "crimson") 
            else:
                txtVida = fonte.render(f"Vida: ???/???", True, "white")
                txtCusto = fonte.render(f"Recompensa: ???", True, "crimson")
            if monstro.revelouMagia:
                txtMagia = fonte.render(f"Ataque:", True, cor)
            else:
                txtMagia = fonte.render(f"Ataque:", True, "white")
            if monstro.revelouFraqueza or monstro.fraqueza == 0:
                txtFraqueza = fonte.render(f"Fraqueza:", True, retornaCor(monstro.fraqueza))
            else:
                txtFraqueza = fonte.render(f"Fraqueza:", True, "white")                
            janela.blit(descricaoInim_img, (posicao[0] - 300, posicao[1] - 240))
            janela.blit(txtNome, (posicao[0] - 290, posicao[1] - 235))
            janela.blit(txtMagia, (posicao[0] - 290, posicao[1] - 205))
            janela.blit(txtFraqueza, (posicao[0] - 290, posicao[1] - 130))
            if monstro.revelouMagia:
                janela.blit(retornaImagem(monstro.magia), (posicao[0] - 275, posicao[1] - 175))
            if monstro.revelouFraqueza:
                janela.blit(retornaImagem(monstro.fraqueza), (posicao[0]  - 275, posicao[1] - 100))
            janela.blit(txtCusto, (posicao[0] - 290, posicao[1] - 55))
            if monstro.MODdef > 1:
                janela.blit(def_up, (posicao[0] - 90, posicao[1] - 55))
            if monstro.MODatk > 1 or monstro.MODatk2 > 1:
                janela.blit(atk_up, (posicao[0] - 60, posicao[1] - 55))
            if monstro.MODdef < 1:
                janela.blit(def_down, (posicao[0] - 90, posicao[1] - 55))
            if monstro.MODatk < 1:
                janela.blit(atk_down, (posicao[0] - 60, posicao[1] - 55))
            if monstro.condicao == 2:
                janela.blit(congelamento, (posicao[0] - 130, posicao[1] - 55))
            elif monstro.condicao == 1:
                janela.blit(sangramento, (posicao[0] - 130, posicao[1] - 55))

            barraLar = 130
            barraAlt = 25
            if monstro.revelouVida:
                ratio = monstro.vida / monstro.vidamax
                pygame.draw.rect(janela, "darkred", (posicao[0] - 180, posicao[1] - 235, barraLar, barraAlt))
                pygame.draw.rect(janela, "green3", (posicao[0] - 180, posicao[1] - 235, barraLar * ratio, barraAlt))
            else:
                pygame.draw.rect(janela, "gray", (posicao[0] - 180, posicao[1] - 235, barraLar, barraAlt))

            janela.blit(txtVida, (posicao[0] - 180, posicao[1] - 205))

            return True

# retornaCor - retorna uma cor nomeada pelo pygame a partir de um tipo fixo

def retornaCor(tipo):

    if tipo == 3:
        cor = "gray"
    if tipo == 4:
        cor = "gray"
    if tipo == 5:
        cor = "red"
    if tipo == 6:
        cor = "blue"
    if tipo == 7:
        cor = "yellow"
    if tipo == 8:
        cor = "purple"
    if tipo == 0:
        cor = "white"

    return cor

# retornaNome - retorna um nome do tipo de ataque a partir de um numero arbitario

def retornaNome(tipo):

    if tipo == 3:
        cor = "Corte"
    if tipo == 4:
        cor = "Impacto"
    if tipo == 5:
        cor = "Fogo"
    if tipo == 6:
        cor = "Agua"
    if tipo == 7:
        cor = "Eletrico"
    if tipo == 8:
        cor = "Neutro"
    return cor