import pygame
import pygame.image
import random
from carta import *
from monstro import *
from medidor import *
from button import *
from infotext import *
from eventos import *

pygame.init()

#tempo
clock = pygame.time.Clock()
fps = 60

#tela
largura = 1360
altura = 720

janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Chabude bude")

#fontes
fonte = pygame.font.Font("fonts/pixel.ttf", 18)
fonte1 = pygame.font.Font("fonts/pixel.ttf", 20)

#imagens
bg0_img = pygame.image.load("imagem/background/bg0.png")
action_img = pygame.image.load("imagem/background/action.png")

#spritegroup
j.txt_grupo = pygame.sprite.Group()

def desenhaAcoes(vivos, acoes):
    
    vezes = abs(acoes - vivos)
    x = 390
    y = 40
    for vez in range(vezes):
        janela.blit(action_img, (x, y))
        x += 60

#cursor
pygame.mouse.set_visible(False)
cursor0_img = pygame.image.load("imagem/background/cursor_normal.png")
cursor0_img = pygame.transform.scale_by(cursor0_img, 1.3)
cursor1_img = pygame.image.load("imagem/background/cursor_atk.png")
cursor1_img = pygame.transform.scale_by(cursor1_img, 1.3)
cursor2_img = pygame.image.load("imagem/background/cursor_info.png")
cursor2_img = pygame.transform.scale_by(cursor2_img, 1.3)

def desenhaCursor(posicao):
    if j.event_info == True:
        janela.blit(cursor2_img, posicao)
    elif j.event_atacar == True:
        janela.blit(cursor1_img, posicao)
    else:
        janela.blit(cursor0_img, posicao)

#VARIAVEIS DE VERIFICACAO --- //
clicou = False
monsVerif = 0
monsAlvo = 0
monsVez = equipe[0]
posMouse = pygame.mouse.get_pos()
xProx = 640
yProx = 320
espYProx = 50
espXProx = 220
turno = 0
acoesEquipe = 0
acoesEquipeInimiga = 0
cd_acaoInimiga = 0
tempoEspera_acaoInimiga = 80

gerarInimigos(9)

def atacar(atacante, alvo):

    if atacante.magia == alvo.fraqueza:
        mod = 1.5
    else:
        mod = 1

    dano = atacante.ataque * mod
    alvo.vida -= dano
    print(f"Vida do {alvo.nome} = {alvo.vida}")
    return dano

def batalha():

    #VARIAVEIS DE VERIFICACAO --- //
    clicou = False
    monsVerif = 0
    monsAlvo = 0
    monsVez = equipe[0]
    posMouse = pygame.mouse.get_pos()
    xProx = 640
    yProx = 320
    espYProx = 50
    espXProx = 220
    turno = 0
    acoesEquipe = 0
    acoesEquipeInimiga = 0
    cd_acaoInimiga = 0
    tempoEspera_acaoInimiga = 80

    while(1):

        clock.tick(fps)
        posMouse = pygame.mouse.get_pos()

        #INPUT --- //
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    j.event_comprouCarta = True
                if event.key == pygame.K_r:
                    j.event_ganhouRubi = True
                    med.valor = 1
                if event.key == pygame.K_e:
                    j.event_ganhouEnergia = True
                    med.valorE = 20
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicou = True
                elif event.button == 3:
                    j.event_info = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    j.event_info = False

        #ATUALIZACOES --- //

        vivos = contarVivos(equipeAtivos)
        vivosInim = contarVivosInimigos(equipeInim)
        ativos = contarAtivos(equipeAtivos)
        ativosInimigos = contarAtivos(equipeInim)
        

        if ativos != 0 and acoesEquipe > vivos - 1 and j.event_vezJogador:
            j.event_vezJogador = False
            acoesEquipeInimiga = 0
        
        if ativosInimigos != 0 and acoesEquipeInimiga > vivosInim - 1 and not j.event_vezJogador:
            j.event_vezJogador = True
            acoesEquipe = 0
        
        if j.event_vezJogador:

            if j.event_novoTurno and ativos > 0:
                turno += 1
                monsVez = equipeAtivos[turno % vivos]
                print(turno)
                if j.event_primeiroTurno:
                    j.event_primeiroTurno = False
                j.event_novoTurno = False

            if j.event_comprouCarta:
                if med.rubis >= med.custoComprar and len(mao) < 4:
                    adicionaCarta(deck, mao)
                    j.event_perdeuRubi = True
                    med.valor = med.custoComprar
                j.event_comprouCarta = False
            
            if clicou:
                cliqueCarta(mao, deck, posMouse, equipeInim, equipe)                      #checagem ativacao de card

                monsVerif = cliqueMonstroLoja(equipe, posMouse) #checagem compra na loja
                if ativos != 3 and monsVerif != False:
                    if monsVerif.ativar(xProx, yProx, med.rubis):
                        if ativos == 1:
                            xProx += espXProx * 0.8
                        else:
                            xProx -= espXProx * 1.3
                        yProx += espYProx
                        equipeAtivos.append(monsVerif)
                        med.valor = monsVerif.getCusto()
                        j.event_perdeuRubi = True
                        j.event_novoTurno = True
                
                if atk_button.checkForInput(posMouse) and ativos != 0:
                    j.event_atacar = True
                elif com_button.checkForInput(posMouse):
                    j.event_comprouCarta = True
                elif skl_button.checkForInput(posMouse):
                    pass
                
                if j.event_atacar:
                    monsAlvo = cliqueMonstroBatalha(equipeInim, posMouse)
                    if monsAlvo != False:
                        dano = atacar(monsVez, monsAlvo)
                        DefineTextoDano(dano, monsAlvo, j.txt_grupo, retornaCor(monsVez), monsVez.magia)
                        j.event_novoTurno = True
                        j.event_atacar = False
                        acoesEquipe += 1

                clicou = False                             #reset
        
        if not j.event_vezJogador:

            if j.event_novoTurno and ativosInimigos > 0:
                turno += 1
                while 1:
                    monsVez = equipeInim[turno % ativosInimigos]
                    if monsVez.vivo:
                        break
                    turno += 1
                    acoesEquipeInimiga += 1
                print(turno)
                j.event_novoTurno = False
            
            if cd_acaoInimiga > tempoEspera_acaoInimiga:
                
                comando = random.randint(0, 8)

                if comando <= 8:
                    alvo = -1
                    contador = 0
                    while alvo == -1:
                        alvo = inimigoEscolheAlvo(equipe)
                        contador += 1
                        if contador >= 12:
                            print("Perdeu!")
                            pygame.quit()

                    dano = atacar(monsVez, alvo)
                    DefineTextoDano(dano, alvo, j.txt_grupo, retornaCor(monsVez), monsVez.magia)
                    j.event_novoTurno = True
                    cd_acaoInimiga = 0
                    acoesEquipeInimiga += 1
            else:
                cd_acaoInimiga += 1

        if j.event_ganhouRubi:
            med.rendaRubi(med.valor)
            DefineTextoMedidor(med.valor, True, False, (325, 165), j.txt_grupo)
            med.valor = 0
            j.event_ganhouRubi = False
            
        if j.event_perdeuRubi:
            med.prejuizoRubi(med.valor)
            DefineTextoMedidor(-med.valor, True, False, (325, 165), j.txt_grupo)
            med.valor = 0
            j.event_perdeuRubi = False
        
        if j.event_ganhouEnergia:
            med.rendaEnergia(med.valorE)
            DefineTextoMedidor(med.valorE, False, True, (790, 475), j.txt_grupo)
            med.valorE = 0
            j.event_ganhouEnergia = False

        if j.event_perdeuEnergia:
            med.prejuizoEnergia(med.valorE)
            DefineTextoMedidor(-1 * med.valorE, False, True, (790, 475), j.txt_grupo)
            med.valorE = 0
            j.event_perdeuEnergia = False

        #RENDERIZACAO --- //
        janela.blit(bg0_img, (0,0))
        desenharLoja(janela, equipe, fonte, med.rubis)
        desenharMonstros(janela, equipe)
        desenharMonstros(janela, equipeInim)
        med.desenhaMedidores(janela, fonte)
        desenhaMao(mao, largura, altura, janela, fonte)
        desenharHud(janela)
        desenhaPrecoCompra(janela, fonte1)
        desenharMonsVez(janela, monsVez)
        if j.event_vezJogador:
            desenhaAcoes(vivos, acoesEquipe)
        else:
            desenhaAcoes(vivosInim, acoesEquipeInimiga)
        desenhaCursor(posMouse)
        if j.event_info:
            desenhaDescricao(janela, fonte)
            desenhaDescricaoMonstro(janela, fonte, fonte1, equipeAtivos, posMouse)
        desenhaTexto(j.txt_grupo, janela)
        pygame.display.flip()
        print(vivosInim)
batalha()