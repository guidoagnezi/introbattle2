import pygame
from eventos import *
import random
pygame.init()
pygame.display.set_mode((1,1), pygame.NOFRAME)
class Ataque(pygame.sprite.Sprite):

    def __init__(self, x, y, nome):
        pygame.sprite.Sprite.__init__(self)
        self.nome = nome
        self.image = pygame.image.load(f"imagem/ataque/{self.nome}/0.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x + 60 + random.randint(0, 70), y + 40 + random.randint(0, 70)))
        self.counter = 0
        self.animation_cooldown = 100
        self.update_time = pygame.time.get_ticks()
        self.animation_list = []
        self.index = 0
        self.count = 0
        self.action = 0
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f"imagem/ataque/{self.nome}/{i}.png").convert_alpha()
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.index]
        
    def update(self):
        self.image = self.animation_list[self.action][self.index]
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
            self.count += 1
            if self.index >= 5:
                self.index = 0
                self.kill()
        return self.count

class Skill():
    def __init__(self, nome, dano, custo, tipo, auto, benigno , descricao, descricao2):
        self.nome = nome
        self.dano = dano
        self.custo = custo
        self.custoBase = custo
        self.tipo = tipo
        self.auto = auto
        self.benigno = benigno
        self.descricao = descricao

explosao = Skill("Explosao", 40, 35, 10, False, False, "40 de dano a um inimigo", "")
cura = Skill("Cura", 0, 30, 10, False, True, "Cura 1/3 da vida de um aliado", "")
treinar = Skill("Treinar", 0, 20, 10, True, True, "O proximo ataque dará muito mais dano", "")
surra = Skill("Surra", 30, 35, 4, True, False, "Saraivada de porrada a todos os inimigos", "")
corre = Skill("Correr", 0, 45, 10, True, True, "Dá +1 ação no turno", "")
wekapipo = Skill("Wekapipo", 35, 35, 8, True, False, "Dano mágico a todos os inimigos", "")
cortar = Skill("Cortar", 20, 20, 3, False, False, "Causa sangramento a um inimigo", "")
congelar = Skill("Congelar", 20, 20, 6, False, False, "Causa congelamento a um inimigo", "")
mudar = Skill("Trocar", 0, 0, 0, True, True, "O ataque se torna a fraqueza de um inimigo", "")
focar = Skill("Focar", 0, 0, 0, True, True, "O proximo ataque dará MUITO mais dano ou +DEF", "")
analisar = Skill("Analisar", 0, 20, 10, False, False, "Exibe todas as informações de um inimigo", "")
devolver = Skill("Devolver", 0, 40, 10, False, False, "Devolve o dano acumulado a um inimigo", "")
comer = Skill("Comer", 35, 20, 4, False, False, "Se essa skill matar, ganha 40 energia", "")
rezar = Skill("Rezar", 0, 0, 10, True, True, "Ganha 30 energia, sofre 15 dano", "")
sabotar = Skill("Sabotar", 35, 0, 10, True, False, "Perde 30 energia e dá dano em área", "")
wekapeople = Skill("Wekapeople", 45, 55, 8, False, False, "Dano mágico superior a todos os inimigos", "")
saraivada = Skill("Saraivada", 45, 55, 4, False, False, "Saraivada de tiro a todos os inimigos", "")
eletroterapia = Skill("Eletroterapia", 0, 45, 4, False, True, "Aumenta os stats de um aliado (estc)", "")
debilitar = Skill("Debilitar", 0, 0, 10, False, False, "Chance de aflingir condicao ou baixar os status aos inimigos", "")
nevasca = Skill("Nevasca", 15, 50, 6, True, False, "Chance de congelar todos os inimigos", "")
bencao = Skill("Bencao", 0, 40, 16, True, True, "Cura 1/4 da vida de toda a equipe", "")

skills = []

skills.append(explosao)
skills.append(cura)
skills.append(treinar)
skills.append(surra)
skills.append(corre)
skills.append(wekapipo)
skills.append(cortar)
skills.append(mudar)
skills.append(focar)
skills.append(analisar)
skills.append(devolver)
skills.append(comer)
skills.append(rezar)
skills.append(sabotar)
skills.append(wekapeople)
skills.append(saraivada)
skills.append(eletroterapia)
skills.append(debilitar)

def DefineAnimacaoAtaque(posicao, tipo):

    if tipo == 3:
        nome = "corte"
    if tipo == 4:
        nome = "impacto"
    if tipo == 5:
        nome = "fogo"
    if tipo == 6:
        nome = "agua"
    if tipo == 7:
        nome = "raio"
    if tipo == 8:
        nome = "neutro"
    if tipo == 9:
        nome = "kill"
    if tipo == 10:
        nome = "explosao"
    if tipo == 11:
        nome = "cura"
    
    ataque = Ataque(posicao.rect.x, posicao.rect.y, nome)
    ataque1 = Ataque(posicao.rect.x, posicao.rect.y, nome)
    ataque2 = Ataque(posicao.rect.x, posicao.rect.y, nome)

    j.ataque_grupo.add(ataque)
    j.ataque_grupo.add(ataque1)
    j.ataque_grupo.add(ataque2)

    if nome == "neutro" or nome == "kill":

        ataque3= Ataque(posicao.rect.x, posicao.rect.y, nome)
        ataque4 = Ataque(posicao.rect.x, posicao.rect.y, nome)
        ataque5 = Ataque(posicao.rect.x, posicao.rect.y, nome)
        j.ataque_grupo.add(ataque3)
        j.ataque_grupo.add(ataque4)
        j.ataque_grupo.add(ataque5)


def desenhaAtaque(ataque_grupo, janela):
    ataque_grupo.draw(janela)
    ataque_grupo.update()
