import pygame
import random
from medidor import *
from infotext import *
from ataque import *
from eventos import j

pygame.init()

class Card():
    def __init__(self, nome, custo, descricao):
        self.image = pygame.image.load("imagem/card/cardframe.png")
        self.entalho = pygame.image.load(f"imagem/card/{nome}.png")
        self.nome = nome
        self.custo = custo
        self.descricao = descricao
        self.x_pos = 0
        self.y_pos = 0
        self.recem = True
        self.y_recem = 30
        self.recemCooldown = 20
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
    
    def desenhaCards(self, janela):
        janela.blit(self.image, self.rect)
        janela.blit(self.entalho, self.rect)

    def checkForInput(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom + 75):
                print("Button Press!")
                return True
            

    def destacar(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom + 75):
                return True
            else:
                return False
            
    def ativarEfeito(self, equipeInim, equipe):
        if self.nome == 'Avareza':
            j.event_ganhouRubi = True
            med.valor = 10

        if self.nome == 'Raio':
            for monstro in equipeInim:
                if monstro.vivo:
                    monstro.vida -= 10
                    DefineTextoDano(10, monstro, j.txt_grupo, "lightslateblue", 7)
                    DefineAnimacaoAtaque(monstro, 7)
                print(monstro.vida)

        if self.nome == 'Louco':
            while 1:
                alvo = random.choice(equipeInim)
                if alvo.vivo:
                    break
            alvo.vida = 0

        if self.nome == 'Mensagem':
            print("Eu sou MENSAGEM")

        if self.nome == 'Troca':
            temp = med.rubis
            med.rubis = med.energia
            med.energia = temp
            if med.energia >= med.energiaMax:
                med.energia = med.energiaMax
            
            med.valorE = 0
            med.valor = 0
            j.event_ganhouEnergia = True
            j.event_ganhouRubi = True
            j.event_perdeuEnergia = False
            
        if self.nome == 'Energia':
            j.event_ganhouEnergia = True
            j.event_perdeuEnergia = False
            med.valorE = 20          

        if self.nome == 'Diabo':
            for monstro in equipe:
                if monstro.vivo and monstro.ativo:
                    monstro.vida = int(monstro.vida / 2)
                    print(f"{monstro.nome}: {monstro.vida}")
                    DefineTextoDano(int(monstro.vida / 2), monstro, j.txt_grupo, "darkred", 3)
                    DefineAnimacaoAtaque(monstro, 5)

            for monstro in equipeInim:
                if monstro.vivo:
                    monstro.vida = int(monstro.vida / 2)
                    print(f"{monstro.nome}: {monstro.vida}")
                    DefineTextoDano(int(monstro.vida / 2), monstro, j.txt_grupo, "darkred", 3)
                    DefineAnimacaoAtaque(monstro, 5)
        
        if self.nome == 'Fisico':
            while 1:
                alvo = random.choice(equipe)
                if alvo.vivo:
                    break
            alvo.MODatk = 1.3
            alvo.CounterAtk = 0
            DefineTextoStatus("UP", alvo, j.txt_grupo, "red", 10)
        
        if self.nome == 'Resistencia':
            while 1:
                alvo = random.choice(equipe)
                if alvo.vivo:
                    break
            alvo.MODdef = 1.3
            alvo.CounterDef = 0
            DefineTextoStatus("UP", alvo, j.txt_grupo, "darkgreen", 11)
            
                

descricao_img = pygame.image.load("imagem/background/descricao.png")
descricao_img.set_alpha(200)

carta = Card("Avareza", 10, "+10 rubis")
carta1 = Card("Raio", 20, "10 de dano a todos os inimigos")
carta2 = Card("Louco", 30, "Mata um inimigo aleatorio")
carta3= Card("Diabo", 20, "A vida de TODOS será metade")
carta4 = Card("Energia", 0, "+20 energia")
carta5 = Card("Troca", 0, "Troca os rubis e energia")
carta6 = Card("Mensagem", 40, "Imprime uma mensagem")
carta7 = Card("Fisico", 20, "+ATQ para um aliado aleatorio")
carta8 = Card("Resistencia", 20, "+DEF para um aliado aleatorio")

deck = []

deck.append(carta)
deck.append(carta1)
deck.append(carta2)
deck.append(carta3)
deck.append(carta4)
deck.append(carta5)
deck.append(carta6)
deck.append(carta7)
deck.append(carta8)

mao = []

def adicionaCarta(deck, mao):
    nCartas = len(mao)
    if nCartas != 4:
        numero = random.randint(0, len(deck) - 1)
        mao.append(deck.pop(numero))

def cliqueCarta(mao, deck, posicao, equipeInim, equipe):
     
    for cartas in mao:
        if cartas.checkForInput(posicao):
            if cartas.custo <= med.energia:
                med.valorE = cartas.custo
                j.event_perdeuEnergia = True
                cartas.ativarEfeito(equipeInim, equipe)
                mao.remove(cartas)
                deck.append(cartas)
            

def desenhaMao(mao, largura, altura, janela, fonte):

    posicao = pygame.mouse.get_pos()
    y_axis = altura - 100
    x_axis = 110
    destacado = False
    nCartas = len(mao)
    if nCartas != 0:
        for i, cards in enumerate(mao):
            if cards.destacar(posicao):
                cards.y_pos = y_axis - 75
            else:
                cards.y_pos = y_axis
            if cards.recem:
                cards.y_pos -= cards.y_recem
                cards.y_recem -= 5
                if cards.y_recem <= 0:
                    cards.recem = False

            cards.x_pos = x_axis + 170 * i
            cards.rect = cards.image.get_rect(center=(cards.x_pos, cards.y_pos))
            cards.desenhaCards(janela)

def desenhaDescricao(janela, fonte):

    posicao = pygame.mouse.get_pos()
    for cards in mao:
        if cards.destacar(posicao):
            txtDescricao = fonte.render(cards.descricao, True, "white")
            txtNome = fonte.render(f"{cards.nome}", True, "white")
            txtCusto = fonte.render(f"Custo: {cards.custo}", True, "yellow")
            janela.blit(descricao_img, (posicao[0], posicao[1] - 100))
            janela.blit(txtNome, (posicao[0] + 10, posicao[1] - 95))
            janela.blit(txtDescricao, (posicao[0] + 10, posicao[1] - 75))
            janela.blit(txtCusto, (posicao[0] + 10, posicao[1] - 55))

rubiImagem = pygame.image.load("imagem/medidor/rubi.png")

def desenhaPrecoCompra(janela, fonte):

    janela.blit(rubiImagem, (1225, 560))
    if med.rubis >= med.custoComprar:
        txtPreco = fonte.render(f"{med.custoComprar}", True, "crimson")
    else:
        txtPreco = fonte.render(f"{med.custoComprar}", True, "gray")
    janela.blit(txtPreco, (1275, 565))