import pygame
import random
from medidor import *
from monstro import *
from infotext import *
from ataque import *
from eventos import j

pygame.init()
pygame.display.set_mode((1,1), pygame.NOFRAME)

# Metodos que alteram a situacao das cartas do jogo
# Card - objeto que recebe uma serie de parametros que regem o custo e balanceamento das cartas.
# define os efeitos das cartas em batalha

frame = pygame.image.load("imagem/card/cardframe.png").convert_alpha()

class Card():
    def __init__(self, nome, custo, preco, descricao):
        self.image =  frame                             # imagem de quadro da carta
        self.entalho = pygame.image.load(f"imagem/card/{nome}.png").convert_alpha() # desenho da carda
        self.nome = nome
        self.custo = custo  # custo para ativar o efeito
        self.preco = preco  # preco de compra na loha
        self.descricao = descricao
        self.selecionado = False
        self.x_pos = 0
        self.y_pos = 0
        self.recem = True # se a carta foi recem comprada, ativa uma animacao de descida ate a posicao x y
        self.y_recem = 30
        self.recemCooldown = 20
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
    
    def desenhaCards(self, janela): # desenha uma carta individual
        janela.blit(self.image, self.rect)
        janela.blit(self.entalho, self.rect)

    # checkForInput - recebe uma posicao em tupla (coordenadas) para checar se um clique aconteceu dentro do retangulo
    # da carta

    def checkForInput(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom + 75):
                return True
            
    # destacar - recebe uma posicao em tupla (coordenadas) para checar se a posicao do mouse se encontra dentro do retangulo
    # da carta
    def destacar(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom + 75):
                return True
            else:
                return False
    
    # ativarEfeito - localiza e ativa o efeito da carta a partir do nome

    def ativarEfeito(self, equipeInim, equipe, equipeAtivos, monsVez):
        if self.nome == 'Avareza':
            j.event_ganhouRubi = True
            med.valor = 10

        if self.nome == 'Raio':
            for monstro in equipeInim:
                if monstro.vivo:
                    monstro.vida -= 25
                    DefineTextoDano(25, monstro, j.txt_grupo, "gray20", 7)
                    DefineAnimacaoAtaque(monstro, 7)
                    j.dano += 25
                    monstro.machucado()
                    if monstro.skill.nome == "Devolver":
                        monstro.gauge += 25

        if self.nome == 'Louco':
            if not j.event_bossBattle:
                while 1:
                    alvo = random.choice(equipeInim)
                    if alvo.vivo:
                        break
                alvo.vida = 0
            else:
                DefineTextoMedidor("FAIL", False, False, pygame.mouse.get_pos(), j.txt_grupo)

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
            if not j.event_bossBattle:
                for monstro in equipe:
                    if monstro.vivo:
                        monstro.vida = int(monstro.vida / 2)
                        DefineTextoDano(int(monstro.vida), monstro, j.txt_grupo, "gray20", 3)
                        DefineAnimacaoAtaque(monstro, 5)
                        if monstro.skill.nome == "Devolver":
                            monstro.gauge += int(monstro.vida / 2)
                        j.dano += int(monstro.vida / 2)

                for monstro in equipeInim:
                    if monstro.vivo:
                        monstro.vida = int(monstro.vida / 2)
                        DefineTextoDano(int(monstro.vida), monstro, j.txt_grupo, "gray20", 3)
                        DefineAnimacaoAtaque(monstro, 5)
                        if monstro.skill.nome == "Devolver":
                            monstro.gauge += int(monstro.vida / 2)
                        j.dano += int(monstro.vida / 2)
            else:
                DefineTextoMedidor("FAIL", False, False, pygame.mouse.get_pos(), j.txt_grupo)

        if self.nome == 'Fisico':
            alvo = monsVez
            alvo.MODatk = 1.3
            alvo.updateStatus()
            alvo.CounterAtk = 0
            DefineTextoStatus("UP", alvo, j.txt_grupo, "black", 10)
            
        if self.nome == 'Resistencia':
            alvo = monsVez
            alvo.MODdef = 1.3
            alvo.updateStatus()
            alvo.CounterDef = 0
            DefineTextoStatus("UP", alvo, j.txt_grupo, "black", 11)

        if self.nome == 'Cafeina':
            if j.acoesEquipe < 4.5:
                j.acoesEquipe += 1
            else:
                DefineTextoMedidor("MAX", False, False, pygame.mouse.get_pos(), j.txt_grupo)

        if self.nome == 'Milagre':
            base = 1000
            for monstro in equipe:
                if monstro.vida < base and monstro.vivo:
                    alvo = monstro
                    base = monstro.vida
            cura = int(alvo.vidamax / 4)
            alvo.vida += cura
            if alvo.vida > alvo.vidamax:
                alvo.vida = alvo.vidamax
            DefineTextoStatus(f"{cura}", alvo, j.txt_grupo, "black", 16)
            DefineAnimacaoAtaque(alvo, 11)
            j.cura += cura
        
        if self.nome == 'Enamorados':
            while 1:
                alvo = random.choice(equipe)
                if alvo.vivo:
                    break
            while 1:
                alvo2 = random.choice(equipeInim)
                if alvo2.vivo:
                    break
            alvo.MODatk = 1.5
            alvo.MODdef = 1.5
            alvo.CounterDef = 0
            alvo.CounterAtk = 0
            alvo2.MODatk = 1.5
            alvo2.MODdef = 1.5
            alvo2.CounterDef = 0
            alvo2.CounterAtk = 0
            alvo.updateStatus()
            alvo2.updateStatus()
            DefineTextoStatus("UP", alvo, j.txt_grupo, "black", 10)
            DefineTextoStatus("UP", alvo, j.txt_grupo, "black", 11)
            DefineTextoStatus("UP", alvo2, j.txt_grupo, "black", 10)
            DefineTextoStatus("UP", alvo2, j.txt_grupo, "black", 11)
            
        if self.nome == 'Mundo':
            while 1:
                alvo = random.choice(equipe)
                if alvo.vivo:
                    break
            while 1:
                alvo2 = random.choice(selecao)
                if alvo2.custo >= alvo.custo and alvo2 not in equipe:
                    break
                    
            alvo2.ativar(alvo.x_pos, alvo.y_pos)
            alvo2.vida = alvo2.vidamax
            equipe.remove(alvo)
            equipe.append(alvo2)
            DefineAnimacaoAtaque(alvo2, 9)

        if self.nome == 'Mago':
            condicao = random.randint(1, 2)
            while 1:
                alvo = random.choice(equipeInim)
                if alvo.vivo:
                    break
            if alvo.condicao == 0:
                alvo.condicao = condicao
                alvo.updateCondicao()
            elif condicao == 2:
                DefineTextoStatus("       FALHOU", alvo, j.txt_grupo, "black", 6)
            elif condicao == 1:
                DefineTextoStatus("       FALHOU", alvo, j.txt_grupo, "black", 3)
        
        if self.nome == 'Estrela':
            alvo = monsVez
            alvo.ataque += 5
            alvo.ataqueNormal += 5
            DefineTextoStatus("    UP", alvo, j.txt_grupo, "black", 10)
        
        if self.nome == 'Fortuna':
            alvo = monsVez
            
            alvo.sorte += 2
            if alvo.sorte <= 25:
                DefineTextoStatus("    UP", alvo, j.txt_grupo, "black", 11)
            else:
                alvo.sorte = 25
                DefineTextoStatus("    MAX", alvo, j.txt_grupo, "black", 11)

        if self.nome == 'Aumento':
            med.energiaMax = 150
        
        if self.nome == 'Vampiro':
            j.event_vampirismo = True
        
        if self.nome == 'Fluxo':
            med.multiEnergia = 1.5
        
        if self.nome == 'Investimento':
            med.multiRubis = 1.2
        
        if self.nome == 'Subiu':
            for monstro in selecao:
                monstro.ataque += 5
                monstro.ataqueNormal += 5
                monstro.defesa += 3
                monstro.defesaNormal += 3
                monstro.sorte += 1

        if self.nome == 'Promocao':
            for monstro in selecao:
                monstro.custo = int(monstro.custo * 0.8)
        
        if self.nome == 'Chance':
            j.event_oneMore = True
        
        if self.nome == 'Carroagem':
            j.event_dropaCard = True
        
        if self.nome == 'Hierofante':
            for skill in skills:
                skill.custo = int(skill.custo * 0.8)

        if self.nome == 'Briga':
            soma = 0
            for monstro in equipe:
                soma += monstro.ataque
            
            dano = soma * 0.6

            for monstro in equipeInim:
                if monstro.vivo:
                    monstro.vida -= dano
                    monstro.machucado()
                    DefineTextoDano(dano, monstro, j.txt_grupo, "gray20", 7)
                    DefineAnimacaoAtaque(monstro, 4)
                    if monstro.skill.nome == "Devolver":
                        monstro.gauge += dano
                    j.dano += dano
        
        if self.nome == 'Julgamento':

            base = -1
            for monstro in equipe:
                if monstro.danoAcumulado > base:
                    alvo = monstro
                    base = monstro.danoAcumulado

            for monstro in equipeInim:
                if monstro.danoAcumulado > base:
                    alvo = monstro
                    base = monstro.danoAcumulado


            alvo.vida -= 60
            alvo.machucado()
            j.dano += 60
            if alvo.skill.nome == "Devolver":
                    alvo.gauge += 60
            DefineTextoDano("60", alvo, j.txt_dano, "black", 7)
            DefineAnimacaoAtaque(alvo, 8)
        
        if self.nome == 'Final':

            for monstro in equipeInim:
                monstro.vida -= med.energia - self.custo
                DefineTextoDano(f"{med.energia - self.custo}", monstro, j.txt_grupo, "gray20", 5)
                DefineAnimacaoAtaque(monstro, 5)
                monstro.machucado()
                if monstro.skill.nome == "Devolver":
                    monstro.gauge += med.energia - self.custo
                j.dano += med.energia - self.custo
            
            med.energia = 0
            med.valorE = med.energiaMax

        if self.nome == 'Visao':
            while 1:
                alvo = random.choice(equipeInim)
                if alvo.vivo:
                    break

            alvo.revelouMagia = True
            alvo.revelouFraqueza = True
            alvo.revelouVida = True
            DefineTextoStatus("        INFO", alvo, j.txt_grupo, "black", 11)
        
        if self.nome == 'Gratis':

            if len(deck) >= 1:
                numero = random.randint(0, len(deck) - 1)
                mao.append(deck.pop(numero))

            else:
                DefineTextoMedidor("IMPOSSIVEL", False, False, pygame.mouse.get_pos(), j.txt_grupo)

        
        if self.nome == 'Flush':
            while 1:
                alvo = random.choice(equipeInim)
                if alvo.vivo:
                    break
            
            dano = 20 * len(mao)

            alvo.vida -= dano
            alvo.machucado()
            if alvo.skill.nome == "Devolver":
                alvo.gauge += dano
            DefineTextoDano(f"{dano}", alvo, j.txt_dano, "black", 3)
            DefineAnimacaoAtaque(alvo, 3)
            j.dano += dano
        if self.nome == 'Polimerizacao':

            vivos = contarVivos(equipe)
            if vivos >= 2:
                if bombinha in equipe and linguico in equipe and azuliu not in equipe:
                    equipe.remove(linguico)
                    azuliu.ativar(linguico.x_pos, linguico.y_pos)
                    azuliu.vida = azuliu.vidamax
                    bombinha.vida = 0
                    equipe.append(azuliu)
                    DefineAnimacaoAtaque(linguico, 9)
                    DefineAnimacaoAtaque(bombinha, 9)
                    j.event_novoTurno = True
                
                elif adiburai in equipe and odiburoi in equipe and ediburei not in equipe:
                    equipe.remove(adiburai)
                    ediburei.ativar(adiburai.x_pos, adiburai.y_pos)
                    ediburei.vida = ediburei.vidamax
                    odiburoi.vida = 0
                    equipe.append(ediburei)
                    DefineAnimacaoAtaque(adiburai, 9)
                    DefineAnimacaoAtaque(odiburoi, 9)
                    j.event_novoTurno = True
                
                elif parceiro not in equipe:
                    while 1:
                        monstro = random.choice(equipe)
                        if monstro.vivo:
                            break
                    while 1:
                        monstro2 = random.choice(equipe)
                        if monstro2.vivo and monstro2 != monstro:
                            break
                    equipe.remove(monstro)
                    parceiro.ativar(monstro.x_pos, monstro.y_pos)
                    parceiro.vida = parceiro.vidamax
                    monstro2.vida = 0
                    equipe.append(parceiro)
                    DefineAnimacaoAtaque(monstro, 9)
                    DefineAnimacaoAtaque(monstro2, 9)
                    j.event_novoTurno = True
                else:
                    DefineTextoMedidor("IMPOSSIVEL", False, False, pygame.mouse.get_pos(), j.txt_grupo)
            else:
                DefineTextoMedidor("IMPOSSIVEL", False, False, pygame.mouse.get_pos(), j.txt_grupo)

        if self.nome == 'Mano':
            j.event_mano = True
        
        if self.nome == 'Justica':
            soma1 = 0
            soma2 = 0

            for monstro in equipe:
                soma1 += monstro.vida
            for monstro in equipeInim:
                soma2 += monstro.vida
            
            if soma1 < soma2:
                for monstro in equipe:
                    monstro.vida = monstro.vidamax
                    DefineTextoStatus(f"{int(monstro.vidamax)}", monstro, j.txt_grupo, "black", 16)
                    DefineAnimacaoAtaque(monstro, 11)
                    j.cura += monstro.vidamax
            else:
                for monstro in equipeInim:
                    monstro.vida = monstro.vidamax
                    DefineTextoStatus(f"{int(monstro.vidamax)}", monstro, j.txt_grupo, "black", 16)
                    DefineAnimacaoAtaque(monstro, 11)
                    j.cura += monstro.vidamax
                    
        if self.nome == 'Temperanca':

            for monstro in equipe:
                if monstro.condicao != 0:
                    DefineTextoStatus("           NORMAL", self, j.txt_grupo, "black", 16)
                    self.condicao = 0
                    self.CounterCon = 0

        if self.nome == 'Morte':
            
            while 1:
                monstro1 = random.choice(equipe)
                if monstro1.vivo:
                    break

            while 1:
                monstro = random.choice(equipeInim)
                if monstro.vivo:
                    monstro.fraqueza = monstro1.magia
                    break
            
            DefineTextoStatus("        CHANGE", monstro, j.txt_grupo, "black", monstro.fraqueza)
            monstro.revelouFraqueza = True

        if self.nome == 'Fraqueza':
            while 1:
                alvo = random.choice(equipeInim)
                if alvo.vivo:
                    break
            alvo.MODatk = 0.7
            alvo.updateStatus()
            alvo.CounterAtk = 0
            DefineTextoStatus("     DOWN", alvo, j.txt_grupo, "black", 12)
            
        if self.nome == 'Vulneravel':
            while 1:
                alvo = random.choice(equipeInim)
                if alvo.vivo:
                    break
            alvo.MODdef = 0.7
            alvo.updateStatus()
            alvo.CounterDef = 0
            DefineTextoStatus("     DOWN", alvo, j.txt_grupo, "black", 13)
        
        if self.nome == 'Sol':
            alvo = monsVez
            alvo.safe = True
            DefineTextoStatus("       SAFE", alvo, j.txt_grupo, "black", 16)
        
        if self.nome == 'Lua':
            if not j.event_bossBattle:
                while 1:
                    alvo = random.choice(equipeInim)
                    if alvo.vivo:
                        break
                
                if alvo in colecaoInimigos:
                    colecao = colecaoInimigos
                if alvo in colecaoInimigos2:
                    colecao = colecaoInimigos2
                if alvo in colecaoInimigos3:
                    colecao = colecaoInimigos3

                while 1:
                    alvo2 = random.choice(colecao)
                    if alvo2.custo >= alvo.custo and alvo2 not in equipeInim:
                        break
                        
                alvo2.ativar(alvo.x_pos, alvo.y_pos)
                alvo2.vida = alvo2.vidamax
                equipeInim.remove(alvo)
                equipeInim.append(alvo2)
                DefineAnimacaoAtaque(alvo2, 9)
            else:
                DefineTextoMedidor("FAIL", False, False, pygame.mouse.get_pos(), j.txt_grupo)

        if self.nome == 'Dealer':
            med.indice = 16
        
        if self.nome == 'Gambito':

            monstro1 = monsVez

            while 1:
                monstro = random.choice(equipeInim)
                if monstro.vivo:
                    break
            
            monstro.vida -= monstro1.vida * 1.5
            monstro.machucado()
            DefineTextoDano(monstro1.vida, monstro, j.txt_dano, "black", 3)
            monstro1.vida = 0
            DefineAnimacaoAtaque(monstro1, 9)
            j.event_novoTurno = True
            j.dano = monstro1.vida * 1.5

        if self.nome == 'Volta':
            j.turno -= 2
            j.event_novoTurno = True
        
        if self.nome == 'Weak':
            j.event_weak = True
                    
descricao_img = pygame.image.load("imagem/background/descricao.png").convert()
descricao_img.set_alpha(200)

# criacao das cartas

carta  = Card("Avareza", 20, 5, "+10 rubis")
carta1 = Card("Raio", 20, 5,"25 de dano a todos os inimigos")
carta2 = Card("Louco", 100, 140,"Mata um inimigo aleatorio")
carta3 = Card("Diabo", 35, 10,"A vida de TODOS será metade")
carta4 = Card("Energia", 0, 5,"+20 energia")
carta5 = Card("Troca", 0, 80,"Troca os rubis e energia")
carta6 = Card("Mensagem", 40, 5, "Imprime uma mensagem")
carta7 = Card("Fisico", 20, 5,"+ATQ para o aliado da vez")
carta8 = Card("Resistencia", 20, 5, "+DEF para o aliado da vez")
carta9 = Card("Cafeina", 30, 10,"+1 acao")
carta10 = Card("Milagre", 25, 10,"1/4 de cura ao aliado com menos vida")
carta11 = Card("Enamorados", 40, 15, "Fortalece 1 inimigo e 1 aliado")
carta12 = Card("Mundo", 75, 45, "Troca um aliado por um de custo >=")
carta13 = Card("Mago", 35, 10, "Status negativo aleatorio a um inimigo")
carta14 = Card("Estrela", 70, 30, "+ATQ para o aliado da vez (perma)")
carta15 = Card("Fortuna", 70, 25, "+SRT para o aliado da vez (perma)")
carta16 = Card("Julgamento", 40, 25, "60 de dano ao monstro que mais atacou") ###
carta17 = Card("Final", 30, 25, "Dano aos inimigos igual a energia, zera")
carta18 = Card("Visao", 20, 10, "Revela as informaçoes de um inimigo")
carta19 = Card("Gratis", 5, 10, "Compra uma carta")
carta20 = Card("Flush", 35, 35, "(20 x cartas na mao) de dano ao inimigo")
carta21 = Card("Briga", 50, 30, "Dano ao inimigos baseado no atq da equipe")
carta22 = Card("Polimerizacao", 90, 50, "Funde dois aliados")
carta23 = Card("Temperanca", 15, 15, "Cura as condicoes de status da equipe")
carta24 = Card("Justica", 60, 35, "Cura a equipe com menos vida")
carta25 = Card("Morte", 30, 20, "Troca a fraqueza de um inimigo")
carta26 = Card("Fraqueza", 30, 15, "-ATQ para um inimigo")
carta27 = Card("Vulneravel", 30, 15, "-DEF para um inimigo")
carta28 = Card("Sol", 35, 20, "O aliado da vez não morre esse round")
carta29 = Card("Lua", 25, 25, "Troca o inimigo por um de custo >=")
carta30 = Card("Gambito", 25, 20, "Dano pela vida do aliado da vez")
carta31 = Card("Volta", 25, 20, "Volta a vez pro aliado anterior")

# criacao dos aprimoramentos
# aprimoramentos sao um tipo de carta que nao sao incluidas num deck e tem efeito permanente

investimento = Card("Investimento", 0, 0, "Ganha 20% mais rubis")
promocao = Card("Promocao", 0, 0, "Os monstros na loja custam 20% menos")
vampiro = Card("Vampiro", 0, 0, "Atacar dará vida ao atacante aliado")
fluxo = Card("Fluxo", 0, 0, "Ataques concedem mais energia")
aumento = Card("Aumento", 0, 0, "Aumenta a energia máxima em 50%")
subiu = Card("Subiu", 0, 0, "A selecao ganha +5 de atq., def. e +2 de srt.")
chance = Card("Chance", 0, 0, "Ataques criticos concedem + uma ação")
carroagem = Card("Carroagem", 0, 0, "Derrotar alguem pode dropar uma carta")
mano = Card("Mano", 0, 0, "O ultimo aliado vivo ganha buffs")
hierofante = Card("Hierofante", 0, 0, "Diminui o custo das skills em 20%")
dealer = Card("Dealer", 0, 0, "Reduz o custo de compra de carta")
banco = Card("Banco", 0, 0, "Aumenta o maximo de rubis")

# lista que armazena os aprimoramentos

aprimoramentos = []

# conjunto de 3 aprimoramentos que serao selecionados aleatoriamente para serem escolhidos pelo player

leque = []

# colecao de aprimoramentos ativos

escolhidos = []

aprimoramentos.append(investimento)
aprimoramentos.append(promocao)
aprimoramentos.append(vampiro)
aprimoramentos.append(fluxo)
aprimoramentos.append(aumento)
aprimoramentos.append(subiu)
aprimoramentos.append(chance)
aprimoramentos.append(mano)
aprimoramentos.append(hierofante)
aprimoramentos.append(dealer)
aprimoramentos.append(carroagem)
aprimoramentos.append(banco)

# deck - conjunto de cartas ordinarias que foram compradas na loja e incluidas no deck

deck = []

# cartas iniciais que ja comecam incluidas no deck

deck.append(carta)
deck.append(carta4)
deck.append(carta7)
deck.append(carta8)
deck.append(carta1)

# mao- conjunto cartas que foram compradas do deck e estao em espera na mao.
# o maximo de cartas numa mao é 4.
# as cartas sao desenhadas a partir da mao

mao = []

# adicionaCarta - metodo que move uma carta aleatoria do deck para a mao

def adicionaCarta(deck, mao):
    nCartas = len(mao)
    if nCartas != 4:
        numero = random.randint(0, len(deck) - 1)
        mao.append(deck.pop(numero))

# cliqueCarta - detecta se uma carta na mao teve um input de clique
# ativa o efeito da carta e a retorna da mao pro deck
# recebe parametros que serao usados no metodo de ativar efeito das cartas

def cliqueCarta(mao, deck, posicao, equipeInim, equipe, equipeAtivos, monsVez):
     
    for cartas in mao:
        if cartas.checkForInput(posicao):
            if cartas.custo <= med.energia: # verifica se há energia o suficiente para ativar a carta
                med.valorE = cartas.custo
                j.event_perdeuEnergia = True
                cartas.ativarEfeito(equipeInim, equipe, equipeAtivos, monsVez) # ativa o efeito da carta
                mao.remove(cartas)
                deck.append(cartas)
            else:
                med.corEnergia = "red" # se nao há energia o suficiente, muda a cor da barra de energia de amarelo para vermelho
            

rubiImagem = pygame.image.load("imagem/medidor/rubi.png").convert_alpha()

# sorteiaAprimoramentos - retira uma amostra de 3 aprimoramentos da lista e as adiciona no leque de escolhas

def sorteiaAprimoramentos():

    leque.clear()
    amostra = random.sample(aprimoramentos, 3)
    leque.extend(amostra)

# cliqueAprimoramento - detecta se um input de clique foi acionado num aprimoramento e ativa seu efeito
# adiciona o aprimoramento a lista de escolhidos e remove ele da lista de aprimoramentos para que nao possa
# ser sorteado novamente no futuro

def cliqueAprimoramento(posicao):
    monsVez = 0
    for cartas in leque:
        if cartas.checkForInput(posicao):
            cartas.ativarEfeito(equipeInim, equipe, equipeAtivos, monsVez)
            cartas.selecionado = True
            j.selecionou = True
            aprimoramentos.remove(cartas)
            escolhidos.append(cartas)
            return True
    return False

# desenhaAprimoramentos - desenha os tres aprimoramentos sorteados no leque
# indica se um aprimoramento ja foi selecionado para impedir que os outros possam ser selecionados tambem
# altera a cor do texto dos aprimoramentos caso um tenha sido selecionado

def desenhaAprimoramentos(janela, fonte, leque):

    posicao = pygame.mouse.get_pos()
    y_axis = 200
    x_axis = 1360 / 3 - 200
    offset = 400
    for cards in leque:
        if cards.destacar(posicao):
            cor = "yellow"
        else:
            cor = "white"
        if j.selecionou:
            cor = "gray20"
        if cards.selecionado:
            cor = "orange"
        cards.x_pos = x_axis
        cards.y_pos = y_axis
        cards.rect = cards.image.get_rect(center=(cards.x_pos, cards.y_pos))
        desc = fonte.render(f"{cards.descricao}", True, cor)
        descRect = desc.get_rect(center=(x_axis, y_axis + 120))
        x_axis += offset
        cards.desenhaCards(janela)
        janela.blit(desc, descRect)
    
# desenhaPrecoCompra - desenha o preco de compra do deck ao lado do botao de comprar
# a cor do texto é vermelha se possui dinheiro suficiente, cinza se nao

def desenhaPrecoCompra(janela, fonte):

    janela.blit(rubiImagem, (1225, 560))
    if med.rubis >= med.custoComprar:
        txtPreco = fonte.render(f"{med.custoComprar}", True, "crimson")
    else:
        txtPreco = fonte.render(f"{med.custoComprar}", True, "gray")
    janela.blit(txtPreco, (1275, 565))

# desenhaDescricao - exibe um retangulo flutuante baseado na posicao do mouse
# para descrever o nome e o efeito da carta, bem como seu custo de energia

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
            return True

# desenhaMao - desenha as cartas contidas numa mao no canto inferior esquerdo da tela
# sao organizadas horizontamente

def desenhaMao(mao, largura, altura, janela, fonte):

    posicao = pygame.mouse.get_pos()
    y_axis = altura - 100
    x_axis = 110
    destacado = False
    nCartas = len(mao)
    if nCartas != 0:
        for i, cards in enumerate(mao):
            if cards.destacar(posicao):     # se a carta estiver com o mouse sobre ela,
                                            # altera suua posicao y para se destacar e indicar qual carta sera usada
                cards.y_pos = y_axis - 75
            else:
                cards.y_pos = y_axis
            if cards.recem: # se a carta foi recem comprada, ativa uma animacao de descida ate a posicao x y
                cards.y_pos -= cards.y_recem
                cards.y_recem -= 5
                if cards.y_recem <= 0:
                    cards.recem = False

            cards.x_pos = x_axis + 170 * i
            cards.rect = cards.image.get_rect(center=(cards.x_pos, cards.y_pos))
            cards.desenhaCards(janela) # desenha a carta da iteracao