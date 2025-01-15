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
from pygame.locals import *


pygame.init()

#tempo
clock = pygame.time.Clock()
fps = 70

#tela
largura = 1360
altura = 720

flags = DOUBLEBUF
janela = pygame.display.set_mode((largura, altura), DOUBLEBUF)
pygame.display.set_caption("Chabude bude")

#fontes
fonte = pygame.font.Font("fonts/pixel.ttf", 18)
fonte1 = pygame.font.Font("fonts/pixel.ttf", 20)
fonte2 = pygame.font.Font("fonts/pixel1.ttf", 20)
fonte3 = pygame.font.Font("fonts/pixel.ttf", 24)
fonte4 = pygame.font.Font("fonts/pixel.ttf", 35)

#imagens
i = random.randint(0, 2)
bg0_img = pygame.image.load(f"imagem/background/bg{i}.png").convert_alpha()
action_img = pygame.image.load("imagem/background/action.png").convert_alpha()
actionE_img = pygame.image.load("imagem/background/action_enemy.png").convert_alpha()

#spritegroup
j.txt_grupo = pygame.sprite.Group()

def desenhaAcoes(vivos, acoes, vezPlayer):
    
    vezes = acoes
    x = 200
    y = 20
    for vez in range(vezes):
        if vezPlayer:
            janela.blit(action_img, (x, y))
        else:
            janela.blit(actionE_img, (x, y))
        x += 90

img_guia = pygame.image.load("imagem/background/img_guia.png").convert_alpha()

def desenhaGuiaDeBatalha(MonsVez, alvo):

    janela.blit(img_guia, (700, 15))
    
    if j.textoAtualizou:
        
        if j.event_realizouAtaque:
            j.textoGuia = fonte3.render(f"{MonsVez.nome} atacou {alvo.nome}!", True, "white")
            if j.event_acertouCritico:
                j.textoGuia = fonte3.render(f"{MonsVez.nome} atacou {alvo.nome}! Ataque critico!", True, "red")
        elif j.event_realizouSkill:
            j.textoGuia = fonte3.render(f"{MonsVez.nome} usou sua skill {MonsVez.skill.nome}!", True, "yellow")
            if MonsVez == mago:
                j.textoGuia = fonte3.render(f"{MonsVez.nome} trocou seu tipo de ataque para {retornaNome(MonsVez.magia)}!", True, retornaCor(MonsVez.magia))
            if MonsVez == mestre:
                j.textoGuia = fonte3.render(f"{MonsVez.nome} está focado! Cuidado!", True, "red")
            if MonsVez == pepeteco:
                j.textoGuia = fonte3.render(f"{MonsVez.nome} sabotou o grupo!", True, "yellow")
            if MonsVez == bobonauta:
                j.textoGuia = fonte3.render(f"{MonsVez.nome} enfraqueceu a todos!", True, "yellow")
        elif j.event_primeiroTurno:
            j.textoGuia = fonte3.render(f"GAME!   START!", True, "white")
        elif j.event_vezJogador:
            j.textoGuia = fonte3.render(f"Vez de {MonsVez.nome}, o que você vai fazer?", True, "white")
        elif not j.event_vezJogador:
            j.textoGuia = fonte3.render(f"O inimigo {MonsVez.nome} vai atacar!", True, "white")
        j.textoAtualizou = False

    janela.blit(j.textoGuia, (740, 40))

        

#cursor
pygame.mouse.set_visible(False)
cursor0_img = pygame.image.load("imagem/background/cursor_normal.png").convert_alpha()
cursor0_img = pygame.transform.scale_by(cursor0_img, 1.3)
cursor1_img = pygame.image.load("imagem/background/cursor_atk.png").convert_alpha()
cursor1_img = pygame.transform.scale_by(cursor1_img, 1.3)
cursor2_img = pygame.image.load("imagem/background/cursor_info.png").convert_alpha()
cursor2_img = pygame.transform.scale_by(cursor2_img, 1.3)
cursor3_img = pygame.image.load("imagem/background/cursor_skill.png").convert_alpha()
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

def draw_aviso(janela, fonte, flag):
    if flag == 1:
        texto = fonte.render("Nenhum personagem selecionado", True, "yellow")
    else:
        texto = fonte.render("Deck nao pode ter menos que 4 cartas", True, "yellow")
    texto_rect = texto.get_rect(center=(1010, 565))
    janela.blit(texto, texto_rect)

def atacar(atacante, alvo):

    j.event_acertouCritico = False

    mod2 = 1
    mod = 1

    if random.randint(1, 15) >= 11 - (atacante.sorte * (4/10)):
        j.event_acertouCritico = True
        mod2 = 1.5
        if j.event_oneMore:
            if j.event_vezJogador and j.acoesEquipe < 5:
                j.acoesEquipe += 1
        
    if atacante.magia == alvo.fraqueza:
        mod = 1.5
        alvo.revelouFraqueza = True
        

    atacante.revelouMagia = True
    
    dano = int((atacante.ataque * mod * (50 / (alvo.defesa + 50)) * (random.randint(8, 12) / 10)) * atacante.MODatk2) * mod2
    atacante.danoAcumulado += dano
    if atacante.MODatk2 != 1:
        atacante.MODatk2 = 1
    alvo.vida -= dano
    alvo.machucado()

    if alvo.skill.nome == "Devolver":
        alvo.gauge += int(dano * 0.8)
                
    return dano

img_telaTiulo = pygame.image.load("imagem/background/telaTitulo.png").convert_alpha()

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

def desenhaMembros():

    espacamento = 150
    x = 860
    y = 490
    for monstro in equipe:
        rect = monstro.image.get_rect(center=(x, y))
        janela.blit(monstro.image, rect)
        x += espacamento

img_descricaoBox = pygame.image.load("imagem/background/description_box.png").convert_alpha()
def menuPrincipal():
    txtRounds = fonte3.render(f"Rounds concluídos: {j.round - 1}", True, "crimson")
    for botao in card_buttons:
        if botao.nome == 'cardframe':
            if botao.carta not in deck:
                botao.selected = False
                botao.image = pygame.image.load(f"imagem/background/{botao.nome}.png")                .convert_alpha()
            else:
                botao.selected = True
                botao.image = pygame.image.load("imagem/background/cardframe_selected.png")                .convert_alpha()

    wheelUp = False
    scrollou = False
    clicou = False
    j.mensagem = False
    j.flag = 0
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    j.event_ganhouRubi = True
                    med.valor = 100
                
        if clicou:
            j.mensagem = False
            if j.catalogoMonstro:
                selecionarPersonagem(char_buttons, posMouse)
            else:
                j.mensagem = not selecionarCarta(card_buttons, posMouse)
                j.flag = 2
                
            if main_go_button.checkForInput(posMouse) and len(equipe) != 0:
                DefinirPosicao(equipe)
                batalha()

            elif main_go_button.checkForInput(posMouse):
                j.mensagem = True
                j.flag = 1
            
            if monstro_button.checkForInput(posMouse):
                if not j.catalogoMonstro:
                    j.catalogoMonstro = True
                    j.buttonPosOffset = 0
                    scrollou = True
            
            if carta_button.checkForInput(posMouse):
                if j.catalogoMonstro:
                    j.catalogoMonstro = False
                    j.buttonPosOffset = 0
                    scrollou = True
            clicou = False
            
        if scrollou:
            if j.catalogoMonstro:
                scrollBotoes(char_buttons, wheelUp, -730)
            else:
                scrollBotoes(card_buttons, wheelUp, -2230)
            scrollou = False
        
        if j.event_ganhouRubi:
            med.rendaRubi(med.valor)
            DefineTextoMedidor(med.valor, False, True, (900, 35), j.txt_grupo)
            med.valor = 0
            j.event_ganhouRubi = False
            
        if j.event_perdeuRubi:
            med.prejuizoRubi(med.valor)
            DefineTextoMedidor(-med.valor, False, True, (900, 35), j.txt_grupo)
            med.valor = 0
            j.event_perdeuRubi = False


        janela.fill("white")
        janela.blit(img_descricaoBox, (680, 70))
        if j.catalogoMonstro:
            desenhaBotoes(janela, char_buttons)
        else:
            desenhaBotoes(janela, card_buttons)
        desenhaBotoes(janela, menu_buttons)
        desenhaMembros()
        if j.catalogoMonstro:
            desenhaDescricaoMenu(janela, char_buttons, posMouse, fonte, fonte3, equipe)
        else:
            desenhaDescricaoMenuCarta(janela, card_buttons, posMouse, fonte, fonte3, equipe)
        med.desenhaRubisMP(janela, fonte)
        if j.mensagem:
            draw_aviso(janela, fonte, j.flag)
        desenhaCursor(posMouse)
        desenhaTexto(j.txt_grupo, janela)
        janela.blit(txtRounds, (1050, 15))
        pygame.display.flip()

def batalha():

    #VARIAVEIS DE VERIFICACAO --- //
    j.event_bossBattle = False
    j.selecionou = False
    i = random.randint(0, 4)
    bg0_img = pygame.image.load(f"imagem/background/bg{i}.png").convert_alpha()
    if j.round == 4 or j.round == 8 or j.round == 12:
        bg0_img = gerarBoss(j.round)
        j.event_bossBattle = True
    else:
        gerarInimigos(j.round)
    clicou = False
    monsVerif = 0
    monsAlvo = 0
    monsVez = equipe[0]
    alvo = equipeInim[0]
    alvoGuia = alvo
    monsVezGuia = monsVez
    posMouse = pygame.mouse.get_pos()
    turno = 0
    j.acoesEquipeInimiga = 0
    cd_acaoInimiga = 0
    tempoEspera_acaoInimiga = 80
    j.event_primeiroTurno = True
    j.event_vezJogador = True
    j.textoAtualizou = True
    j.ataque_grupo.empty()
    j.txt_grupo.empty()
    j.txt_dano.empty()
    tamEquipe = len(equipe)
    tamEquipeInim = len(equipeInim)
    j.acoesEquipe = tamEquipe

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
        vivos = contarVivos(equipe)
        vivosInim = contarVivosInimigos(equipeInim)
        
        if vivosInim == 0:
            continuar()
        
        if vivos != 0 and j.acoesEquipe <= 0 and j.event_vezJogador:
            j.event_vezJogador = False
            j.acoesEquipeInimiga = contarVivosInimigos(equipeInim)
            if j.event_bossBattle:
                j.acoesEquipeInimiga = 2
            j.event_trocouTime = True
        
        if vivosInim != 0 and j.acoesEquipeInimiga <= 0 and not j.event_vezJogador:
            j.event_vezJogador = True
            j.acoesEquipe = contarVivos(equipe)
            j.event_trocouTime = True
        
        if j.event_vezJogador:

            if j.event_novoTurno and vivos > 0:
                if j.cdStandby > j.cdMaxStandby:
                    turno += 1
                    while 1:
                        monsVez = equipe[turno % tamEquipe]
                        if monsVez.vivo:
                            break
                        turno += 1
                    if j.event_mano and vivos == 1:
                        monsVez.MODdef = 1.8
                        monsVez.MODatk = 1.5
                        monsVez.CounterAtk = 0
                        monsVez.CounterDef = 0
                        DefineTextoStatus("UP", monsVez, j.txt_grupo, "black", 10)
                        DefineTextoStatus("UP", monsVez, j.txt_grupo, "black", 11)
                    monsVez.updateStatus()
                    monsVez.updateCondicao()
                    monsVezGuia = monsVez
                    if j.event_primeiroTurno:
                        j.event_primeiroTurno = False
                    j.event_novoTurno = False
                    j.event_realizouSkill = False
                    j.event_realizouAtaque = False
                    j.event_atacar = False
                    j.event_usarSkill = False
                    j.textoAtualizou = True
                    j.cdStandby = 0
                    j.event_standby = False
                    j.event_trocouTime = False

                    if monsVez.condicao == 2:
                        j.event_novoTurno = True
                        j.acoesEquipe -= 1
                else:
                    j.cdStandby += 1
                    j.event_standby = True
                    clicou = False

            elif vivos == 0 and not j.event_primeiroTurno:
                gameOver(j)
            
            if j.event_comprouCarta:
                if med.rubis >= med.custoComprar and len(mao) < 4:
                    adicionaCarta(deck, mao)
                    j.event_perdeuRubi = True
                    med.valor = med.custoComprar
                j.event_comprouCarta = False
            
            if clicou and not j.event_standby:
                med.corEnergia = "yellow"
                if vivos != 0:
                    cliqueCarta(mao, deck, posMouse, equipeInim, equipe, equipeAtivos, monsVez)                      #checagem ativacao de card
                
                    if atk_button.checkForInput(posMouse):
                        j.event_atacar = True
                        j.event_usarSkill = False
                        j.event_comprouCarta = False

                    elif com_button.checkForInput(posMouse):
                        j.event_comprouCarta = True
                        j.event_atacar = False
                        j.event_usarSkill = False

                    elif skl_button.checkForInput(posMouse):
                        if med.energia >= monsVez.skill.custo:
                            if monsVez.skill.auto == False:
                                j.event_usarSkill = True
                            else:
                                j.event_perdeuEnergia = True
                                med.valorE = monsVez.skill.custo
                                monsVez.ativarSkill(monsVez, equipeInim, equipe)
                                j.event_novoTurno = True
                                j.event_usarSkill = False
                                j.event_realizouSkill = True
                                j.acoesEquipe -= 1
                            j.event_atacar = False
                            j.event_comprouCarta = False
                        else:
                            med.corEnergia = "red"
                
                if j.event_atacar:
                    monsAlvo = cliqueMonstroBatalha(equipeInim, posMouse)
                    if monsAlvo != False:
                        dano = atacar(monsVez, monsAlvo)
                        j.event_ganhouEnergia = True
                        monsVezGuia = monsVez
                        alvoGuia =  monsAlvo
                        med.valorE = med.ganhoEnergia
                        if not j.event_acertouCritico:
                            DefineTextoDano(dano, monsAlvo, j.txt_grupo, "gray20", monsVez.magia)
                        else:
                            DefineTextoDano(dano, monsAlvo, j.txt_grupo, "red", monsVez.magia)
                        if j.event_vampirismo:
                            curaV = int(dano / 4)
                            DefineTextoStatus(curaV, monsVez, j.txt_grupo, "gray20", 16)
                            monsVez.vida += curaV
                            if monsVez.vida > monsVez.vidamax:
                                monsVez.vida = monsVez.vidamax
                        DefineAnimacaoAtaque(monsAlvo, monsVez.magia)
                        j.event_novoTurno = True
                        j.event_atacar = False
                        j.event_realizouAtaque = True
                        j.textoAtualizou = True
                        j.acoesEquipe -= 1
                
                if j.event_usarSkill:
                    if not monsVez.skill.benigno:
                        monsAlvo = cliqueMonstroBatalha(equipeInim, posMouse)
                    else:
                        monsAlvo = cliqueMonstroBatalha(equipe, posMouse)
                    if monsAlvo != False:
                        j.event_perdeuEnergia = True
                        med.valorE = monsVez.skill.custo
                        monsVez.ativarSkill(monsAlvo, equipeInim, equipe)
                        j.event_novoTurno = True
                        j.event_usarSkill = False
                        monsVezGuia = monsVez
                        j.event_realizouSkill = True
                        j.textoAtualizou = True
                        j.acoesEquipe -= 1

                clicou = False                             #reset
        
        if not j.event_vezJogador:
            if j.event_novoTurno and vivosInim > 0:
                if j.cdStandby > j.cdMaxStandby:
                    turno += 1
                    while 1:
                        monsVez = equipeInim[turno % tamEquipeInim]
                        if monsVez.vivo:
                            break
                        turno += 1
                    monsVez.updateStatus()
                    monsVez.updateCondicao()
                    monsVezGuia = monsVez
                    j.event_novoTurno = False
                    j.event_realizouAtaque = False
                    j.event_realizouSkill = False
                    j.event_trocouTime = False
                    j.textoAtualizou = True
                    j.cdStandby = 0
                    j.event_standby = False

                    if monsVez.condicao == 2:
                        j.event_novoTurno = True
                        j.acoesEquipeInimiga -= 1
                else:
                    j.cdStandby += 1
                    j.event_standby = True
                    clicou = False

            if cd_acaoInimiga > tempoEspera_acaoInimiga and not j.event_standby and monsVez.condicao != 2:

                comando = random.randint(0, 8)

                if monsVez == mago:
                    if j.acoesEquipeInimiga == 1:
                        comando = 1

                if monsVez.MODatk2 != 1:
                    comando = 1
                if comando < 7:
                    alvo = -1
                    contador = 0
                    while alvo == -1:
                        alvo = inimigoEscolheAlvo(equipe)
                        contador += 1
                        if contador >= 12:
                            gameOver(j)
                    dano = atacar(monsVez, alvo)
                    if not j.event_acertouCritico:
                        DefineTextoDano(dano, alvo, j.txt_grupo, "gray20", monsVez.magia)
                    else:
                        DefineTextoDano(dano, alvo, j.txt_grupo, "red", monsVez.magia)
                    DefineAnimacaoAtaque(alvo, monsVez.magia)
                    monsVezGuia = monsVez
                    alvoGuia = alvo
                    j.event_novoTurno = True
                    j.event_realizouAtaque = True
                    j.textoAtualizou = True
                    cd_acaoInimiga = 0
                    j.acoesEquipeInimiga -= 1
                
                if comando >= 7:
                    alvo = -1
                    contador = 0
                    if not monsVez.skill.auto:
                        if not monsVez.skill.benigno:
                            while alvo == -1:
                                alvo = inimigoEscolheAlvo(equipe)
                                contador += 1
                                if contador >= 12:
                                    gameOver(j)
                            monsVez.ativarSkill(alvo, equipe, equipeInim)
                        else:
                            while alvo == -1:
                                alvo = inimigoEscolheAlvo(equipeInim)

                            monsVez.ativarSkill(alvo, equipe, equipeInim)
                    else:
                        monsVez.ativarSkill(monsVez, equipe, equipeInim)
        
                    j.event_novoTurno = True
                    monsVezGuia = monsVez
                    j.textoAtualizou = True
                    j.event_usarSkill = False
                    j.event_realizouSkill = True
                    j.acoesEquipeInimiga -= 1
                    j.event_atacar = False


            elif not j.event_standby:
                cd_acaoInimiga += 1

        if j.event_ganhouRubi:
            med.rendaRubi(med.valor)
            DefineTextoMedidor(med.valor, True, False, (120, 165), j.txt_grupo)
            med.valor = 0
            j.event_ganhouRubi = False
            
        if j.event_perdeuRubi:
            med.prejuizoRubi(med.valor)
            DefineTextoMedidor(-med.valor, True, False, (120, 165), j.txt_grupo)
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

        
        atualizaBotoes()
        monsVezGuia = monsVez
        #RENDERIZACAO --- //
        janela.blit(bg0_img, (0,0))
        if vivos != 0 and not j.event_standby and not  (not j.event_vezJogador and j.event_bossBattle):
            desenharMonsVez(janela, monsVez)
        desenharMonstros(janela, equipe)
        desenharMonstros(janela, equipeInim)
        med.desenhaMedidores(janela, fonte)
        desenhaMao(mao, largura, altura, janela, fonte)
        desenharHud(janela, hud_buttons)
        desenhaPrecoCompra(janela, fonte1)
        desenhaGuiaDeBatalha(monsVezGuia, alvoGuia)
        if j.event_vezJogador:
            desenhaAcoes(vivos, j.acoesEquipe, j.event_vezJogador)
        else:
            desenhaAcoes(vivosInim, j.acoesEquipeInimiga, j.event_vezJogador)
        desenhaCursor(posMouse)
        if j.event_info:
            if not desenhaDescricao(janela, fonte):
                desenhaDescricaoMonstro(janela, fonte, fonte1, equipe, posMouse)
                desenhaDescricaoMonstroInim(janela, fonte, fonte1, equipeInim, posMouse)
            
        desenhaTexto(j.txt_grupo, janela)
        desenhaAtaque(j.ataque_grupo, janela)
        desenhaTexto(j.txt_dano, janela)
        pygame.display.flip()

img_bg_gameover = pygame.image.load("imagem/background/bg_gameover.png").convert_alpha()

def reset():
    
    med.energiaMax = 100
    med.energia = 50
    med.rubis = 40
    med.custoComprar = 5

    j.event_primeiroTurno = True
    for monstros in selecao:
        monstros.vida = monstros.vidamax
        monstros.MODdef = 1
        monstros.MODatk = 1
        monstros.CounterAtk = 0
        monstros.CounterDef = 0
        monstros.gauge = 0
        monstros.danoAcumulado = 0
        monstros.custo = monstros.custoBase
        monstros.ataque = monstros.ataqueBase
        monstros.defesa = monstros.defesaBase
        monstros.sorte = monstros.sorteBase
        monstros.vida = monstros.vidaBase
        monstros.fraqueza = monstros.fraquezaBase
        monstros.CounterCon = 0
        monstros.condicao = 0
        monstros.ativo = False
        monstros.vivo = True
        monstros.idle()
        monstros.update_animation()
    
    for monstros in colecaoInimigos:
        monstros.vida = monstros.vidamax
        monstros.MODdef = 1
        monstros.MODatk = 1
        monstros.CounterAtk = 0
        monstros.CounterDef = 0
        monstros.CounterCon = 0
        monstros.condicao = 0
        monstros.gauge = 0
        monstros.danoAcumulado = 0
        monstros.ataque = monstros.ataqueBase
        monstros.ataqueNormal = monstros.ataqueBase
        monstros.defesa = monstros.defesaBase
        monstros.defesaNormal = monstros.ataqueNormal
        monstros.sorte = monstros.sorteBase
        monstros.vida = monstros.vidaBase
        monstros.fraqueza = monstros.fraquezaBase
        monstros.ativo = False
        monstros.vivo = True
        monstros.idle()
        monstros.update_animation()
    
    for monstros in colecaoInimigos2:
        monstros.vida = monstros.vidamax
        monstros.MODdef = 1
        monstros.MODatk = 1
        monstros.CounterAtk = 0
        monstros.CounterDef = 0
        monstros.CounterCon = 0
        monstros.condicao = 0
        monstros.gauge = 0
        monstros.danoAcumulado = 0
        monstros.ataque = monstros.ataqueBase
        monstros.ataqueNormal = monstros.ataqueBase
        monstros.defesa = monstros.defesaBase
        monstros.defesaNormal = monstros.ataqueNormal
        monstros.sorte = monstros.sorteBase
        monstros.vida = monstros.vidaBase
        monstros.fraqueza = monstros.fraquezaBase
        monstros.ativo = False
        monstros.vivo = True
        monstros.idle()
        monstros.update_animation()
    
    for monstros in colecaoInimigos3:
        monstros.vida = monstros.vidamax
        monstros.MODdef = 1
        monstros.MODatk = 1
        monstros.CounterAtk = 0
        monstros.CounterDef = 0
        monstros.CounterCon = 0
        monstros.condicao = 0
        monstros.gauge = 0
        monstros.danoAcumulado = 0
        monstros.ataque = monstros.ataqueBase
        monstros.ataqueNormal = monstros.ataqueBase
        monstros.defesa = monstros.defesaBase
        monstros.defesaNormal = monstros.ataqueNormal
        monstros.sorte = monstros.sorteBase
        monstros.vida = monstros.vidaBase
        monstros.fraqueza = monstros.fraquezaBase
        monstros.ativo = False
        monstros.vivo = True
        monstros.idle()
        monstros.update_animation()
    
    for skill in skills:
        skill.custo = skill.custoBase

    equipe.clear()
    j.event_realizouAtaque = False
    j.event_realizouSkill = False

    colecaoBoss.clear()

    colecaoBoss.append(pepeteco)
    colecaoBoss.append(mestre)
    colecaoBoss.append(mago)
    colecaoBoss.append(bobonauta)

    aprimoramentos.clear()

    aprimoramentos.append(investimento)
    aprimoramentos.append(promocao)
    aprimoramentos.append(vampiro)
    aprimoramentos.append(fluxo)
    aprimoramentos.append(aumento)
    aprimoramentos.append(subiu)
    aprimoramentos.append(mano)
    aprimoramentos.append(hierofante)

    for card in aprimoramentos:
        card.selecionado = False

    escolhidos.clear()

    med.energiaMax = 100
    med.multiEnergia = 1
    med.multiRubis = 1

    j.event_vampirismo = False
    j.event_dropaCard = False
    j.event_oneMore = False
    j.event_mano = False

    j.round = 1

    for botao in char_buttons:
        if botao.nome == 'cardframe':
            if botao.monstro not in equipe:
                botao.selected = False
                botao.image = pygame.image.load(f"imagem/background/{botao.nome}.png")                .convert_alpha()
            else:
                botao.selected = True
                botao.image = pygame.image.load("imagem/background/cardframe_selected.png")                .convert_alpha()
    
    deck.clear()
    deck.append(carta)
    deck.append(carta1)
    deck.append(carta8)
    deck.append(carta7)
    deck.append(carta4)

    mao.clear()

    for botao in card_buttons:
        if botao.nome == 'cardframe':
            if botao.carta not in deck:
                botao.selected = False
                botao.image = pygame.image.load(f"imagem/background/{botao.nome}.png")                .convert_alpha()
            else:
                botao.selected = True
                botao.image = pygame.image.load("imagem/background/cardframe_selected.png")                .convert_alpha()

def desenhaGameover(janela):

    txtEquipe = fonte3.render("Equipe", True, "white")
    txtAprimoramentos = fonte3.render("Aprimoramentos", True, "white")
    espacamento = 200
    x = largura / 3
    y = 90
    for monstro in equipe:
        rect = monstro.image.get_rect(center=(x, y))
        janela.blit(monstro.image, rect)
        x += espacamento
    rect = txtEquipe.get_rect(center=(100, y))
    janela.blit(txtEquipe, rect)
    espacamento = 200
    x = largura / 3
    y = 280
    for card in escolhidos:
        rect = card.entalho.get_rect(center=(x, y))
        janela.blit(card.image, rect)
        janela.blit(card.entalho, rect)
        x += espacamento
    rect = txtEquipe.get_rect(center=(100, y))
    janela.blit(txtAprimoramentos, rect)

def continuar():
    if j.round == 12:
        gameOver(j)
    if j.round == 1:
        j.event_bossBattle = True
    j.ataque_grupo.empty()
    j.txt_grupo.empty()
    equipeAtivos.clear()
    
    for monstros in colecaoInimigos:
        monstros.vida = monstros.vidamax
        monstros.MODdef = 1
        monstros.MODatk = 1
        monstros.CounterAtk = 0
        monstros.CounterDef = 0
        monstros.CounterCon = 0
        monstros.condicao = 0
        monstros.gauge = 0
        monstros.danoAcumulado = 0
        monstros.ataque = monstros.ataqueBase
        monstros.ataqueNormal = monstros.ataqueBase
        monstros.defesa = monstros.defesaBase
        monstros.defesaNormal = monstros.ataqueNormal
        monstros.sorte = monstros.sorteBase
        monstros.vida = monstros.vidaBase
        monstros.fraqueza = monstros.fraquezaBase
        monstros.ativo = False
        monstros.vivo = True
        monstros.idle()
        monstros.update_animation()
    
    for monstros in colecaoInimigos2:
        monstros.vida = monstros.vidamax
        monstros.MODdef = 1
        monstros.MODatk = 1
        monstros.CounterAtk = 0
        monstros.CounterDef = 0
        monstros.CounterCon = 0
        monstros.condicao = 0
        monstros.gauge = 0
        monstros.danoAcumulado = 0
        monstros.ataque = monstros.ataqueBase
        monstros.ataqueNormal = monstros.ataqueBase
        monstros.defesa = monstros.defesaBase
        monstros.defesaNormal = monstros.ataqueNormal
        monstros.sorte = monstros.sorteBase
        monstros.vida = monstros.vidaBase
        monstros.fraqueza = monstros.fraquezaBase
        monstros.ativo = False
        monstros.vivo = True
        monstros.idle()
        monstros.update_animation()

    for monstros in selecao:
        monstros.vida = monstros.vidamax
        monstros.MODdef = 1
        monstros.MODatk = 1
        monstros.CounterAtk = 0
        monstros.CounterDef = 0
        monstros.condicao = 0
        monstros.CounterCon = 0
        monstros.danoAcumulado = 0
        monstros.ativo = False
        monstros.vivo = True
        monstros.idle()
        monstros.update_animation()

    for botao in char_buttons:
        if botao.nome == 'cardframe':
            if botao.monstro not in equipe:
                botao.selected = False
                botao.image = pygame.image.load(f"imagem/background/{botao.nome}.png")           .convert_alpha()
            else:
                botao.selected = True
                botao.image = pygame.image.load("imagem/background/cardframe_selected.png")                .convert_alpha()
    
    for carta in mao:
        mao.remove(carta)
        deck.append(carta)
    
    for carta in mao:
        mao.remove(carta)
        deck.append(carta)
    
    for carta in mao:
        mao.remove(carta)
        deck.append(carta)

    j.round += 1
    img_bg_gameover.set_alpha(20)
    transparencia = 40
    clicou = False
    txtContinue = fonte4.render("Round completo! Continue lutando!!", True, "white")
    txtContinue_rect = txtContinue.get_rect(center=(680, 420))
    j.event_realizouAtaque = False
    j.event_realizouSkill = False
    
    if j.event_bossBattle:
        sorteiaAprimoramentos()

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
            if j.event_bossBattle and not j.selecionou:
                cliqueAprimoramento(posMouse)
            clicou = False

        if transparencia % 40 == 0 and transparencia <= 1200:
            janela.blit(img_bg_gameover, (0, 0))

        if transparencia >= 1200:
            janela.fill("black")
            desenhaBotoes(janela, continue_buttons)
            if j.event_bossBattle:
                desenhaAprimoramentos(janela, fonte, leque)
            else:
                desenhaGameover(janela)
            janela.blit(txtContinue, txtContinue_rect)
        desenhaCursor(posMouse)
        pygame.display.flip()
        
        transparencia += 2


def gameOver(jogo):

    img_bg_gameover.set_alpha(20)
    transparencia = 40
    clicou = False
    txtFim = fonte4.render("Todos os lutadores PERECERAM, aceite seu fim.", True, "white")
    if j.round == 12:
        txtFim = fonte4.render("Parabéns! Você concluiu os 12 rounds", True, "white")
    txtFim_rect = txtFim.get_rect(center=(680, 420))
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
                reset()
                menuPrincipal()
            clicou = False
        
        if transparencia % 40 == 0:
            janela.blit(img_bg_gameover, (0, 0))
        if transparencia >= 800:
            desenhaBotoes(janela, gameover_buttons)
            janela.blit(txtFim, txtFim_rect)
            desenhaGameover(janela)
        desenhaCursor(posMouse)
        pygame.display.flip()
        
        transparencia += 2

menuTitulo()