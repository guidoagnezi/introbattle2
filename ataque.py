import pygame
from eventos import *
import random
pygame.init()

class Ataque(pygame.sprite.Sprite):

    def __init__(self, x, y, nome):
        pygame.sprite.Sprite.__init__(self)
        self.nome = nome
        self.image = pygame.image.load(f"imagem/ataque/{self.nome}/0.png")
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
            img = pygame.image.load(f"imagem/ataque/{self.nome}/{i}.png")
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
    def __init__(self, nome, dano, custo, tipo, status):
        self.nome = nome
        self.dano = dano
        self.custo = custo
        self.tipo = tipo
        self.status = status

explosao = Skill("Explosao", 50, 15, 10, False)

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
