import pygame
from eventos import *
from monstro import *
from carta import *
pygame.init()

# Metodos que criam e verificam as situacoes dos botoes ordinarios do jogo
# Button - objeto que define retangulos, a posicao do retangulo na tela e verifica os inputs

pygame.display.set_mode((1,1), pygame.NOFRAME)
class Button():
        
    def __init__(self, nome, x_pos, y_pos):
            self.nome = nome
            self.image = pygame.image.load(f"imagem/background/{nome}.png").convert_alpha()
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.monstro = 0
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
            self.selected = False # definir se o botao do tipo "cardframe" esta selecionado

      # desenhaBotao - desenha o botao na janela

    def desenhaBotao(self, janela):
            janela.blit(self.image, self.rect)
      
      # desenhaEstampa - se for um botao do tipo "cardframe", desenha a estampa da carta ou monstro que armazena

    def desenhaEstampa(self, janela):
          if self.monstro != 0:
            rect = self.monstro.image.get_rect(center=(self.x_pos, self.y_pos + j.buttonPosOffset))
            janela.blit(self.monstro.image, rect)
          else:
            rect = self.carta.entalho.get_rect(center=(self.x_pos, self.y_pos + j.buttonPosOffset))
            janela.blit(self.carta.entalho, rect)    

      # checkForInput - recebe uma posicao em tupla (coordenadas) para checar se um clique aconteceu dentro do retangulo
      # do botao

    def checkForInput(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                return True
      # destacar - recebe uma posicao em tupla (coordenadas) para checar se a posicao do mouse se encontra dentro do retangulo
      # do botao

    def destacar(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom): 
                return True
            else:
                return False

# inicializacao dos botoes da batalha

atk_button = Button("atk_button", 885, 580)
atk_button.image = pygame.transform.scale_by(atk_button.image, 1.2).convert()
atk_button.rect = atk_button.image.get_rect(center=(atk_button.x_pos, atk_button.y_pos))
com_button = Button("com_button", 1175, 580)
com_button.image = pygame.transform.scale_by(com_button.image, 1.2).convert()
com_button.rect = com_button.image.get_rect(center=(com_button.x_pos, com_button.y_pos))
skl_button = Button("skl_button", 885, 650)
skl_button.image = pygame.transform.scale_by(skl_button.image, 1.2).convert()
skl_button.rect = skl_button.image.get_rect(center=(skl_button.x_pos, skl_button.y_pos))
pas_button = Button("pas_button", 1175, 650)
pas_button.image = pygame.transform.scale_by(pas_button.image, 1.2).convert()
pas_button.rect = pas_button.image.get_rect(center=(pas_button.x_pos, pas_button.y_pos))

atk_button.image_on = atk_button.image
atk_button.rect_on = atk_button.rect
com_button.image_on = com_button.image
com_button.rect_on = com_button.rect
skl_button.image_on = skl_button.image
skl_button.rect_on = skl_button.rect
pas_button.image_on = pas_button.image
pas_button.rect_on = pas_button.rect

atk_button.image_off = pygame.image.load("imagem/background/atk_button_off.png").convert()
skl_button.image_off = pygame.image.load("imagem/background/skl_button_off.png").convert()
com_button.image_off = pygame.image.load("imagem/background/com_button_off.png").convert()
pas_button.image_off = pygame.image.load("imagem/background/pas_button_off.png").convert()
atk_button.image_off = pygame.transform.scale_by(atk_button.image_off, 1.2).convert()
atk_button.rect_off = atk_button.image_off.get_rect(center=(atk_button.x_pos, atk_button.y_pos))
com_button.image_off = pygame.transform.scale_by(com_button.image_off, 1.2).convert()
com_button.rect_off = com_button.image_off.get_rect(center=(com_button.x_pos, com_button.y_pos))
skl_button.image_off = pygame.transform.scale_by(skl_button.image_off, 1.2).convert()
skl_button.rect_off = skl_button.image_off.get_rect(center=(skl_button.x_pos, skl_button.y_pos))
pas_button.image_off = pygame.transform.scale_by(pas_button.image_off, 1.2).convert()
pas_button.rect_off = pas_button.image_off.get_rect(center=(pas_button.x_pos, pas_button.y_pos))

hud0_img = pygame.image.load("imagem/background/hud0.png").convert()

# inicializacao dos botoes do menu inicial

t_start_button = Button("start_button", 675, 360)
t_start_button.image = pygame.transform.scale_by(t_start_button.image, 1.2).convert()
t_start_button.rect = t_start_button.image.get_rect(center=(t_start_button.x_pos, t_start_button.y_pos))

t_quit_button = Button("sair_button", 675, 440)
t_quit_button.image = pygame.transform.scale_by(t_quit_button.image, 1.2).convert()
t_quit_button.rect = t_quit_button.image.get_rect(center=(t_quit_button.x_pos,t_quit_button.y_pos))

# inicializacao dos botoes "cardframe" que armazenam monstros

main_char_button = Button("cardframe", 130, 180)
main_char_button.monstro = ico
main_char_button1 = Button("cardframe", 340, 180)
main_char_button1.monstro = linguico
main_char_button2 = Button("cardframe", 550, 180)
main_char_button2.monstro = amigo
main_char_button3 = Button("cardframe", 130, 470)
main_char_button3.monstro = filho
main_char_button4 = Button("cardframe", 340, 470)
main_char_button4.monstro = gelo
main_char_button5 = Button("cardframe", 550, 470)
main_char_button5.monstro = horroroso
main_char_button6 = Button("cardframe", 130, 760)
main_char_button6.monstro = bombinha
main_char_button7 = Button("cardframe", 340, 760)
main_char_button7.monstro = camboja
main_char_button8 = Button("cardframe", 550, 760)
main_char_button8.monstro = monge
main_char_button9 = Button("cardframe", 130, 1050)
main_char_button9.monstro = bireco
main_char_button10 = Button("cardframe", 340, 1050)
main_char_button10.monstro = adiburai
main_char_button11 = Button("cardframe", 550, 1050)
main_char_button11.monstro = demonio
main_char_button12 = Button("cardframe", 340, 1340)
main_char_button12.monstro = odiburoi
main_char_button13 = Button("cardframe", 130, 1340)
main_char_button13.monstro = kamirider

# inicializacao dos botoes "cardframe" que armazenam cartas

main_card_button = Button("cardframe", 130, 180)
main_card_button.carta = carta
main_card_button1 = Button("cardframe", 340, 180)
main_card_button1.carta = carta1
main_card_button2 = Button("cardframe", 550, 180)
main_card_button2.carta = carta2
main_card_button3 = Button("cardframe", 130, 470)
main_card_button3.carta = carta3
main_card_button4 = Button("cardframe", 340, 470)
main_card_button4.carta = carta4
main_card_button5 = Button("cardframe", 550, 470)
main_card_button5.carta = carta5
main_card_button6 = Button("cardframe", 130, 760)
main_card_button6.carta = carta6
main_card_button7 = Button("cardframe", 340, 760)
main_card_button7.carta = carta7
main_card_button8 = Button("cardframe", 550, 760)
main_card_button8.carta = carta8
main_card_button9 = Button("cardframe", 130, 1050)
main_card_button9.carta = carta9
main_card_button10 = Button("cardframe", 340, 1050)
main_card_button10.carta = carta10
main_card_button11 = Button("cardframe", 550, 1050)
main_card_button11.carta = carta11
main_card_button12 = Button("cardframe", 130, 1340)
main_card_button12.carta = carta12
main_card_button13 = Button("cardframe", 340, 1340)
main_card_button13.carta = carta13
main_card_button14 = Button("cardframe", 550, 1340)
main_card_button14.carta = carta14
main_card_button15= Button("cardframe", 130, 1630)
main_card_button15.carta = carta15
main_card_button16 = Button("cardframe", 340, 1630)
main_card_button16.carta = carta16
main_card_button17 = Button("cardframe", 550, 1630)
main_card_button17.carta = carta17
main_card_button18 = Button("cardframe", 130, 1920)
main_card_button18.carta = carta18
main_card_button19 = Button("cardframe", 340, 1920)
main_card_button19.carta = carta19
main_card_button20 = Button("cardframe", 550, 1920)
main_card_button20.carta = carta20
main_card_button21= Button("cardframe", 130, 2210)
main_card_button21.carta = carta21
main_card_button22= Button("cardframe", 340, 2210)
main_card_button22.carta = carta22
main_card_button23= Button("cardframe", 550, 2210)
main_card_button23.carta = carta23
main_card_button24= Button("cardframe", 130, 2500)
main_card_button24.carta = carta24
main_card_button25= Button("cardframe", 340, 2500)
main_card_button25.carta = carta25
main_card_button26= Button("cardframe", 550, 2500)
main_card_button26.carta = carta26
main_card_button27= Button("cardframe", 130, 2790)
main_card_button27.carta = carta27
main_card_button28= Button("cardframe", 340, 2790)
main_card_button28.carta = carta28
main_card_button29= Button("cardframe", 550, 2790)
main_card_button29.carta = carta29
main_card_button30= Button("cardframe", 130, 3080)
main_card_button30.carta = carta30
main_card_button31= Button("cardframe", 340, 3080)
main_card_button31.carta = carta31
main_card_button32= Button("cardframe", 550, 3080)
main_card_button32.carta = carta32
main_card_button33= Button("cardframe", 130, 3370)
main_card_button33.carta = carta33
main_card_button34= Button("cardframe", 340, 3370)
main_card_button34.carta = carta34
main_card_button35= Button("cardframe", 550, 3370)
main_card_button35.carta = carta35

# inicializacao dos botoes do Menu Principal
main_go_button = Button("go_button", 1150, 650)
monstro_button = Button("monstro_button", 760, 650)
carta_button = Button("carta_button", 860, 650)
ranking_button = Button("ranking_button", 960, 650)

# inicializacao dos botoes da tela de gameover

gameover_reset = Button("voltar_button", 680, 600)

# inicializacao dos botos da tela de continue

continue_button = Button("continue_button", 680, 500)
return_button = Button("return_button", 680, 600)

# lista de botoes da hud de batalha

hud_buttons = []

hud_buttons.append(atk_button)
hud_buttons.append(com_button)
hud_buttons.append(skl_button)
hud_buttons.append(pas_button)

# lista de botoes do menu inicial

titulo_buttons = []

titulo_buttons.append(t_start_button)
titulo_buttons.append(t_quit_button)

# lista de botoes "cardframe" que armazenam monstros

char_buttons = []

char_buttons.append(main_char_button)
char_buttons.append(main_char_button1)
char_buttons.append(main_char_button2)
char_buttons.append(main_char_button3)
char_buttons.append(main_char_button4)
char_buttons.append(main_char_button5)
char_buttons.append(main_char_button6)
char_buttons.append(main_char_button7)
char_buttons.append(main_char_button8)
char_buttons.append(main_char_button9)
char_buttons.append(main_char_button10)
char_buttons.append(main_char_button11)
char_buttons.append(main_char_button12)
char_buttons.append(main_char_button13)

# lista de botoes "cardframe" que armazenam cartas

card_buttons = []

card_buttons.append(main_card_button)
card_buttons.append(main_card_button1)
card_buttons.append(main_card_button2)
card_buttons.append(main_card_button3)
card_buttons.append(main_card_button4)
card_buttons.append(main_card_button5)
card_buttons.append(main_card_button6)
card_buttons.append(main_card_button7)
card_buttons.append(main_card_button8)
card_buttons.append(main_card_button9)
card_buttons.append(main_card_button10)
card_buttons.append(main_card_button11)
card_buttons.append(main_card_button12)
card_buttons.append(main_card_button13)
card_buttons.append(main_card_button14)
card_buttons.append(main_card_button15)
card_buttons.append(main_card_button16)
card_buttons.append(main_card_button17)
card_buttons.append(main_card_button18)
card_buttons.append(main_card_button19)
card_buttons.append(main_card_button20)
card_buttons.append(main_card_button21)
card_buttons.append(main_card_button22)
card_buttons.append(main_card_button23)
card_buttons.append(main_card_button24)
card_buttons.append(main_card_button25)
card_buttons.append(main_card_button26)
card_buttons.append(main_card_button27)
card_buttons.append(main_card_button28)
card_buttons.append(main_card_button29)
card_buttons.append(main_card_button30)
card_buttons.append(main_card_button31)
card_buttons.append(main_card_button32)
card_buttons.append(main_card_button33)
card_buttons.append(main_card_button34)
card_buttons.append(main_card_button35)

# lista de botoes ordinarios do Menu Principal

menu_buttons = []

menu_buttons.append(main_go_button)
menu_buttons.append(monstro_button)
menu_buttons.append(carta_button)
menu_buttons.append(ranking_button)

# lista de botoes da tela de gameover

gameover_buttons = []

gameover_buttons.append(gameover_reset)

# lista de botoes da tela de continue

continue_buttons = []

continue_buttons.append(continue_button)
continue_buttons.append(return_button)

# desenharHud - desenha os botoes da hud de batalha

def desenharHud(janela, grupo):

    janela.blit(hud0_img, (730, 530))
    
    for button in grupo:
          button.desenhaBotao(janela)

# desenhaBotoes - desenha botoes de uma lista genericamente

def desenhaBotoes(janela, grupo):
      
      for button in grupo:
            button.desenhaBotao(janela)
            if (grupo == char_buttons or grupo == card_buttons) and button.nome == "cardframe":
                  button.desenhaEstampa(janela)

# cliqueBotao - verifica se aconteceu um input sobre um botao

def cliqueBotao(grupo, posicao):
      
      for button in grupo:
            button.checkForInput(posicao)

# scrollBotoes - altera o offset vertical do retangulo dos botoes quando o scroll do mouse é acionado.
# muda a posicao do retangulo

def scrollBotoes(grupo, wheelUp, limite):

      valor = 45
      if wheelUp == False and j.buttonPosOffset < 0:
            j.buttonPosOffset += valor

      elif wheelUp and j.buttonPosOffset > limite:
            j.buttonPosOffset -= valor

      for botao in grupo:
            botao.rect = botao.image.get_rect(center=(botao.x_pos, botao.y_pos + j.buttonPosOffset))

# selecionarPersonagem - adiciona o monstro armazenado no botao "cardframe" a lista da equipe
# se ja estiver selecionado, remove o monstro da lista da equipe

def selecionarPersonagem(grupo, position):
      j.monstroComprados = 0
      for botao in grupo:
            if botao.checkForInput(position) and botao.nome == "cardframe":
                  if botao.selected == False and len(equipe) != 3 and med.rubis >= botao.monstro.custo:
                        botao.image = pygame.image.load("imagem/background/cardframe_selected.png")                        .convert_alpha()
                        equipe.append(botao.monstro)
                        j.monstroComprados = 1
                        j.event_perdeuRubi = True
                        med.valor = botao.monstro.custo
                        botao.selected = True
                  elif botao.selected == True:
                        botao.image = pygame.image.load(f"imagem/background/{botao.nome}.png")                        .convert_alpha()
                        equipe.remove(botao.monstro)
                        j.monstroComprados = 0
                        botao.selected = False

# selecionarCarta - adiciona a carta armazenado no botao "cardframe" ao deck
# se ja estiver selecionado, remove a carta do deck

def selecionarCarta(grupo, position):
      j.cartasCompradas = 0
      for botao in grupo:
            if botao.checkForInput(position) and botao.nome == "cardframe":
                  if botao.selected == False and med.rubis >= botao.carta.preco:
                        botao.image = pygame.image.load("imagem/background/cardframe_selected.png")                        .convert_alpha()
                        deck.append(botao.carta)
                        j.cartasCompradas = 1
                        j.event_perdeuRubi = True
                        med.valor = botao.carta.preco
                        botao.selected = True
                        return True
                  elif botao.selected == True and len(deck) > 4:
                        botao.image = pygame.image.load(f"imagem/background/{botao.nome}.png")                        .convert_alpha()
                        deck.remove(botao.carta)
                        j.cartasCompradas = 0
                        botao.selected = False
                        return True
                  elif len(deck) == 4:
                        return False
      return True

img_rubi = pygame.image.load("imagem/medidor/rubi.png").convert_alpha()

# desenhaDescricaoMenu - desenha a descricao e parametros do monstro no menu principal

def desenhaDescricaoMenu(janela, grupo, posicao, fonte, fonte2, equipe):

      for botao in grupo:
            if botao.nome == "cardframe" and botao.destacar(posicao):

                  cor = retornaCor(botao.monstro.magia)
                  txtNome = fonte2.render(f"{botao.monstro.nome}", True, "white")
                  txtVida = fonte.render(f"Vida: {botao.monstro.vidamax}", True, "white")
                  # txtDescricao = fonte.render(botao.monstro.descricao, True, "white")
                  txtCusto = fonte2.render(f"{int(botao.monstro.custo)}", True, "crimson")
                  txtAtaque = fonte.render(f"Ataque: {int(botao.monstro.ataque)}", True, "white")
                  txtDefesa = fonte.render(f"Defesa: {int(botao.monstro.defesa)}", True, "white")
                  txtSorte = fonte.render(f"Sorte: {int(botao.monstro.sorte)}", True, "white")  
                  txtMagia = fonte.render(f"Tipo de ataque:", True, cor)
                  txtFraqueza = fonte.render(f"Fraqueza:", True, retornaCor(botao.monstro.fraqueza))
                  txtCustoSkill = fonte.render(f"Custo da Skill: {botao.monstro.skill.custo}", True, "yellow")
                  txtSkill = fonte.render(f"Skill: {botao.monstro.skill.nome} - {botao.monstro.skill.descricao}", True, "gray")
                  rect = botao.monstro.image.get_rect(center=(800, 180))
                  rect1 = txtNome.get_rect(center=(800, 250))
                  janela.blit(botao.monstro.image, rect)
                  janela.blit(txtNome, rect1)
                  # janela.blit(txtDescricao ,)
                  janela.blit(txtVida, (890, 130))
                  janela.blit(txtAtaque, (890, 170))
                  janela.blit(txtSorte, (1020, 170))
                  janela.blit(txtDefesa,(890, 210))
                  janela.blit(txtMagia, (890, 250))
                  janela.blit(retornaImagem(botao.monstro.magia), (1040, 255))
                  if botao.monstro.fraqueza != 0:
                        janela.blit(txtFraqueza, (1090, 250))
                        janela.blit(retornaImagem(botao.monstro.fraqueza), (1192, 255))
                  janela.blit(txtSkill, (740, 310))
                  janela.blit(txtCustoSkill, (740, 350))
                  janela.blit(img_rubi, (1170, 130))
                  janela.blit(txtCusto, (1220, 130))

# desenhaDescricaoMenuCarta - desenha a descricao e parametros da carta no menu principal

def desenhaDescricaoMenuCarta(janela, grupo, posicao, fonte, fonte2, equipe):
      
      for botao in grupo:
            if botao.nome == "cardframe" and botao.destacar(posicao):

                  rect = botao.carta.entalho.get_rect(center=(810, 190))
                  txtCusto = fonte.render(f"{botao.carta.preco}", True, "crimson")
                  txtDescricao = fonte.render(f"{botao.carta.descricao}", True, "white")
                  txtCusto2 = fonte.render(f"Custo: {botao.carta.custo} energia", True, "yellow")
                  txtNome = fonte2.render(f"{botao.carta.nome}", True, "white")
                  rect1 = txtNome.get_rect(center=(810, 300))
                  txtDeck = fonte.render(f"No deck", True, "white")
                  janela.blit(botao.carta.entalho, rect)
                  janela.blit(txtNome, rect1)
                  janela.blit(txtDescricao, (890, 180))
                  if botao.selected:
                        janela.blit(txtDeck, (890, 240))
                  janela.blit(txtCusto2, (890, 210))
                  janela.blit(img_rubi, (1170, 130))
                  janela.blit(txtCusto, (1220, 130))

# draw_aviso - desenha a mensagem de aviso de equipe incompleta - nao usado

def draw_aviso(janela, fonte):
    texto = fonte.render("Você não selecionou 3 personagens", True, "white")
    texto_rect = texto.get_rect(center=(750, 650))
    janela.blit(texto, texto_rect)

# atualizaBotoes - altera a imagem dos botoes da hud em batalha para indicar se ele esta ou nao ativo

def atualizaBotoes():
      
      if (not j.event_vezJogador or j.event_standby) and not j.botoesOff:

            atk_button.image = atk_button.image_off
            skl_button.image = skl_button.image_off
            com_button.image = com_button.image_off
            pas_button.image = pas_button.image_off
            atk_button.rect  = atk_button.rect_off
            skl_button.rect  = skl_button.rect_off
            com_button.rect  = com_button.rect_off
            pas_button.rect  = pas_button.rect_off
            j.botoesOff = True
      
      elif j.event_vezJogador and not j.event_standby and j.botoesOff:
            atk_button.image = atk_button.image_on
            skl_button.image = skl_button.image_on
            com_button.image = com_button.image_on
            pas_button.image = pas_button.image_on
            atk_button.rect  = atk_button.rect_on
            skl_button.rect  = skl_button.rect_on
            com_button.rect  = com_button.rect_on
            pas_button.rect  = pas_button.rect_on
            j.botoesOff = False
      

# animacaoSelected - ativa a atualizacao da imagem do monstro no menu principal se o botao que o armazena estivar selecionado

def animacaoSelected():

      for botao in char_buttons:
            if botao.selected:
                  botao.monstro.update_animation()