import pygame
import pygame.image
import random
from carta import *
from monstro import *
from medidor import *
from button import *
from infotext import *
from eventos import *
from ataque import *

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
fonte2 = pygame.font.Font("fonts/pixel1.ttf", 20)
fonte3 = pygame.font.Font("fonts/pixel.ttf", 24)
fonte4 = pygame.font.Font("fonts/pixel.ttf", 35)

#imagens
bg0_img = pygame.image.load("imagem/background/bg0.png")
action_img = pygame.image.load("imagem/background/action.png")
actionE_img = pygame.image.load("imagem/background/action_enemy.png")

#spritegroup
j.txt_grupo = pygame.sprite.Group()

def desenhaAcoes(vivos, acoes, vezPlayer):
    
    vezes = abs(acoes - vivos)
    x = 390
    y = 20
    for vez in range(vezes):
        if vezPlayer:
            janela.blit(action_img, (x, y))
        else:
            janela.blit(actionE_img, (x, y))
        x += 90

#cursor
pygame.mouse.set_visible(False)
cursor0_img = pygame.image.load("imagem/background/cursor_normal.png")
cursor0_img = pygame.transform.scale_by(cursor0_img, 1.3)
cursor1_img = pygame.image.load("imagem/background/cursor_atk.png")
cursor1_img = pygame.transform.scale_by(cursor1_img, 1.3)
cursor2_img = pygame.image.load("imagem/background/cursor_info.png")
cursor2_img = pygame.transform.scale_by(cursor2_img, 1.3)
cursor3_img = pygame.image.load("imagem/background/cursor_skill.png")
cursor3_img = pygame.transform.scale_by(cursor3_img, 1.3)

def desenhaCursor(posicao):
    if j.event_info == True:
        janela.blit(cursor2_img, posicao)
    elif j.event_atacar == True:
        janela.blit(cursor1_img, posicao)
    elif j.event_usarSkill:
        janela.blit(cursor3_img, posicao)
    else:
        janela.blit(cursor0_img, posicao)

def draw_aviso(janela, fonte):
    texto = fonte.render("Você não selecionou 3 personagens", True, "yellow")
    texto_rect = texto.get_rect(center=(1010, 565))
    janela.blit(texto, texto_rect)

def atacar(atacante, alvo):

    if atacante.magia == alvo.fraqueza:
        mod = 1.5
    else:
        mod = 1

    dano = atacante.ataque * mod
    alvo.vida -= dano
    print(f"Vida do {alvo.nome} = {alvo.vida}")
    alvo.machucado()
    return dano

img_telaTiulo = pygame.image.load("imagem/background/telaTitulo.png")

def menuTitulo():

    clicou = False
    while(1):

        posMouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicou = True

        if clicou:
            if t_start_button.checkForInput(posMouse):
                menuPrincipal()
            if t_quit_button.checkForInput(posMouse):
                pygame.quit()
            clicou = False

        janela.blit(img_telaTiulo, (0,0))
        desenhaBotoes(janela, titulo_buttons)
        desenhaCursor(posMouse)
        pygame.display.flip()

img_descricaoBox = pygame.image.load("imagem/background/description_box.png")
def menuPrincipal():

    wheelUp = False
    scrollou = False
    clicou = False
    mensagem = False
    while(1):

        posMouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicou = True
                if event.button == 5:
                    wheelUp = True
                    scrollou = True
                if event.button == 4:
                    wheelUp = False
                    scrollou = True
                
        if clicou:
            mensagem = False
            selecionarPersonagem(char_buttons, posMouse)

            if main_go_button.checkForInput(posMouse) and len(equipe) == 3:
                batalha()
            elif main_go_button.checkForInput(posMouse):
                mensagem = True
            clicou = False
            
        if scrollou:
            scrollBotoes(char_buttons, wheelUp)
            scrollou = False

        janela.fill("white")
        janela.blit(img_descricaoBox, (680, 70))
        desenhaBotoes(janela, char_buttons)
        desenhaBotoes(janela, menu_buttons)
        desenhaMonstrosMenuPrincipal(janela, selecao)
        desenhaDescricaoMenu(janela, char_buttons, posMouse, fonte, fonte3, equipe)
        if mensagem:
            draw_aviso(janela, fonte)
        desenhaCursor(posMouse)
        pygame.display.flip()

def batalha():

    #VARIAVEIS DE VERIFICACAO --- //

    gerarInimigos(j.round)
    clicou = False
    monsVerif = 0
    monsAlvo = 0
    monsVez = equipe[0]
    posMouse = pygame.mouse.get_pos()
    turno = 0
    acoesEquipe = 0
    acoesEquipeInimiga = 0
    cd_acaoInimiga = 0
    tempoEspera_acaoInimiga = 80
    j.event_primeiroTurno = True
    j.event_vezJogador = True
    j.ataque_grupo.empty()
    j.txt_grupo.empty()

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
                    med.valor = 20
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
        
        if vivosInim == 0:
            continuar()
        
        if ativos != 0 and acoesEquipe > vivos - 1 and j.event_vezJogador:
            j.event_vezJogador = False
            acoesEquipeInimiga = 0
        
        if ativosInimigos != 0 and acoesEquipeInimiga > vivosInim - 1 and not j.event_vezJogador:
            j.event_vezJogador = True
            acoesEquipe = 0
        
        if j.event_vezJogador:

            if j.event_novoTurno and ativos > 0 and vivos > 0:
                print(f"Vivos: {vivos} Ativos: {ativos}")
                turno += 1
                monsVez = equipeAtivos[turno % vivos]
                monsVez.updateStatus()
                print(turno)
                if j.event_primeiroTurno:
                    j.event_primeiroTurno = False
                j.event_novoTurno = False
            elif ativos == 0 and not j.event_primeiroTurno:
                gameOver(j)

            if j.event_comprouCarta:
                if med.rubis >= med.custoComprar and len(mao) < 4:
                    adicionaCarta(deck, mao)
                    j.event_perdeuRubi = True
                    med.valor = med.custoComprar
                j.event_comprouCarta = False
            
            if clicou:
                if ativos != 0:
                    cliqueCarta(mao, deck, posMouse, equipeInim, equipe, equipeAtivos)                      #checagem ativacao de card

                monsVerif = cliqueMonstroLoja(equipe, posMouse) #checagem compra na loja

                if ativos != 3 and monsVerif != False:
                    print("FOI")
                    if ativos == 0:
                        xProx = 640
                        yProx = 320
                    if ativos == 1:
                        xProx = 400
                        yProx = 370
                    if ativos == 2:
                        xProx = 520
                        yProx = 420
                    if monsVerif.ativar(xProx, yProx, med.rubis):
                        print("ATIVOU")
                        equipeAtivos.append(monsVerif)
                        med.valor = monsVerif.getCusto()
                        j.event_perdeuRubi = True
                        j.event_novoTurno = True
                
                if atk_button.checkForInput(posMouse) and ativos != 0:
                    j.event_atacar = True
                    j.event_usarSkill = False
                    j.event_comprouCarta = False

                elif com_button.checkForInput(posMouse) and ativos != 0:
                    j.event_comprouCarta = True
                    j.event_atacar = False
                    j.event_usarSkill = False

                elif skl_button.checkForInput(posMouse) and ativos != 0:
                    if med.energia >= monsVez.skill.custo:
                        if monsVez.skill.status == False:
                            j.event_usarSkill = True
                        j.event_atacar = False
                        j.event_comprouCarta = False
                
                if j.event_atacar:
                    monsAlvo = cliqueMonstroBatalha(equipeInim, posMouse)
                    if monsAlvo != False:
                        dano = atacar(monsVez, monsAlvo)
                        j.event_ganhouEnergia = True
                        med.valorE = med.ganhoEnergia
                        DefineTextoDano(dano, monsAlvo, j.txt_grupo, retornaCor(monsVez), monsVez.magia)
                        DefineAnimacaoAtaque(monsAlvo, monsVez.magia)
                        j.event_novoTurno = True
                        j.event_atacar = False
                        acoesEquipe += 1
                
                if j.event_usarSkill:
                    monsAlvo = cliqueMonstroBatalha(equipeInim, posMouse)
                    if monsAlvo != False:
                        j.event_perdeuEnergia = True
                        med.valorE = monsAlvo.skill.custo
                        monsAlvo.ativarSkill(monsAlvo)
                        j.event_novoTurno = True
                        j.event_usarSkill = False
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
                            gameOver(j)
                    dano = atacar(monsVez, alvo)
                    DefineTextoDano(dano, alvo, j.txt_grupo, retornaCor(monsVez), monsVez.magia)
                    DefineAnimacaoAtaque(alvo, monsVez.magia)
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
            DefineTextoMedidor(med.valorE, False, True, (940, 510), j.txt_grupo)
            med.valorE = 0
            j.event_ganhouEnergia = False

        if j.event_perdeuEnergia:
            med.prejuizoEnergia(med.valorE)
            DefineTextoMedidor(-1 * med.valorE, False, True, (940, 510), j.txt_grupo)
            med.valorE = 0
            j.event_perdeuEnergia = False

        #RENDERIZACAO --- //
        janela.blit(bg0_img, (0,0))
        desenharLoja(janela, equipe, fonte, med.rubis)
        desenharMonstros(janela, equipe)
        desenharMonstros(janela, equipeInim)
        med.desenhaMedidores(janela, fonte)
        desenhaMao(mao, largura, altura, janela, fonte)
        desenharHud(janela, hud_buttons)
        desenhaPrecoCompra(janela, fonte1)
        if ativos != 0:
            desenharMonsVez(janela, monsVez)
        if j.event_vezJogador:
            desenhaAcoes(vivos, acoesEquipe, j.event_vezJogador)
        else:
            desenhaAcoes(vivosInim, acoesEquipeInimiga, j.event_vezJogador)
        desenhaCursor(posMouse)
        if j.event_info:
            desenhaDescricao(janela, fonte)
            if not desenhaDescricaoLoja(janela, fonte, fonte1, equipe, posMouse):
                desenhaDescricaoMonstro(janela, fonte, fonte1, equipeAtivos, posMouse)
            
        desenhaTexto(j.txt_grupo, janela)
        desenhaAtaque(j.ataque_grupo, janela)
        pygame.display.flip()

img_bg_gameover = pygame.image.load("imagem/background/bg_gameover.png")


def reset():
    
    med.energiaMax = 100
    med.energia = 50
    med.rubis = 40
    med.custoComprar = 5
    
    for carta in mao:
        mao.remove(carta)
        deck.append(carta)

    j.event_primeiroTurno = True
    for monstros in selecao:
        monstros.vida = monstros.vidamax
        monstros.MODdef = 1
        monstros.MODatk = 1
        monstros.CounterAtk = 0
        monstros.CounterDef = 0
        monstros.ativo = False
        monstros.vivo = True
        monstros.idle()
        monstros.update_animation()
        print(f"{monstros.nome} - Vida: {monstros.vida}")
    
    for monstros in colecaoInimigos:
        monstros.vida = monstros.vidamax
        monstros.MODdef = 1
        monstros.MODatk = 1
        monstros.CounterAtk = 0
        monstros.CounterDef = 0
        monstros.ativo = False
        monstros.vivo = True
        monstros.idle()
        monstros.update_animation()
        print(f"{monstros.nome} - Vida: {monstros.vida}")
    
    equipeAtivos.clear()

    j.round = 0

def continuar():

    j.ataque_grupo.empty()
    j.txt_grupo.empty()
    equipeAtivos.clear()

    for monstros in colecaoInimigos:
        monstros.vida = monstros.vidamax
        monstros.MODdef = 1
        monstros.MODatk = 1
        monstros.CounterAtk = 0
        monstros.CounterDef = 0
        monstros.ativo = False
        monstros.vivo = True
        monstros.idle()
        monstros.update_animation()
        print(f"{monstros.nome} - Vida: {monstros.vida}")

    for monstros in selecao:
        monstros.vida = monstros.vidamax
        monstros.MODdef = 1
        monstros.MODatk = 1
        monstros.CounterAtk = 0
        monstros.CounterDef = 0
        monstros.ativo = False
        monstros.vivo = True
        monstros.idle()
        monstros.update_animation()
        print(f"{monstros.nome} - Vida: {monstros.vida}")

    j.round += 1
    img_bg_gameover.set_alpha(20)
    transparencia = 40
    clicou = False
    txtContinue = fonte4.render("Round completo! Continue lutando!!", True, "white")
    txtContinue_rect = txtContinue.get_rect(center=(680, 300))
    while(1):

        posMouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicou = True

        if clicou:
            if continue_button.checkForInput(posMouse):
                menuPrincipal()
            if return_button.checkForInput(posMouse):
                reset()
                menuPrincipal()
            clicou = False
        
        if transparencia % 40 == 0:
            janela.blit(img_bg_gameover, (0, 0))
        if transparencia >= 800:
            desenhaBotoes(janela, continue_buttons)
            janela.blit(txtContinue, txtContinue_rect)
        desenhaCursor(posMouse)
        pygame.display.flip()
        
        transparencia += 2


def gameOver(jogo):

    reset()
    img_bg_gameover.set_alpha(20)
    transparencia = 40
    clicou = False
    txtFim = fonte4.render("Todos os lutadores PERECERAM, aceite seu fim.", True, "white")
    txtFim_rect = txtFim.get_rect(center=(680, 360))
    while(1):

        posMouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicou = True

        if clicou:
            if gameover_reset.checkForInput(posMouse):
                menuPrincipal()
            clicou = False
        
        if transparencia % 40 == 0:
            janela.blit(img_bg_gameover, (0, 0))
        if transparencia >= 800:
            desenhaBotoes(janela, gameover_buttons)
            janela.blit(txtFim, txtFim_rect)
        desenhaCursor(posMouse)
        pygame.display.flip()
        
        transparencia += 2

menuTitulo()