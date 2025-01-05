import pygame
from eventos import *
from monstro import *

class Button():
        
    def __init__(self, nome, x_pos, y_pos):
            self.nome = nome
            self.image = pygame.image.load(f"imagem/background/{nome}.png")
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
            self.selected = False

    def desenhaBotao(self, janela):
            janela.blit(self.image, self.rect)

    def checkForInput(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                print(f"Button Press! {self.nome}")
                return True
            
    def destacar(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom): 
                return True
            else:
                return False
            
atk_button = Button("atk_button", 885, 580)
atk_button.image = pygame.transform.scale_by(atk_button.image, 1.2)
atk_button.rect = atk_button.image.get_rect(center=(atk_button.x_pos, atk_button.y_pos))
com_button = Button("com_button", 1175, 580)
com_button.image = pygame.transform.scale_by(com_button.image, 1.2)
com_button.rect = com_button.image.get_rect(center=(com_button.x_pos, com_button.y_pos))
skl_button = Button("skl_button", 885, 650)
skl_button.image = pygame.transform.scale_by(skl_button.image, 1.2)
skl_button.rect = skl_button.image.get_rect(center=(skl_button.x_pos, skl_button.y_pos))

hud0_img = pygame.image.load("imagem/background/hud0.png")

t_start_button = Button("start_button", 675, 360)
t_start_button.image = pygame.transform.scale_by(t_start_button.image, 1.2)
t_start_button.rect = t_start_button.image.get_rect(center=(t_start_button.x_pos, t_start_button.y_pos))

t_quit_button = Button("sair_button", 675, 440)
t_quit_button.image = pygame.transform.scale_by(t_quit_button.image, 1.2)
t_quit_button.rect = t_quit_button.image.get_rect(center=(t_quit_button.x_pos,t_quit_button.y_pos))

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
main_char_button6.monstro = adiburai
main_char_button7 = Button("cardframe", 340, 760)
main_char_button7.monstro = demonio

main_custo10 = Button("custo_10", 190, 40)
main_custo20 = Button("custo_20", 190, 330)
main_custo40 = Button("custo_40", 190, 620)

main_go_button = Button("go_button", 1150, 650)

gameover_reset = Button("voltar_button", 680, 460)

continue_button = Button("continue_button", 680, 400)
return_button = Button("return_button", 680, 500)

hud_buttons = []

hud_buttons.append(atk_button)
hud_buttons.append(com_button)
hud_buttons.append(skl_button)

titulo_buttons = []

titulo_buttons.append(t_start_button)
titulo_buttons.append(t_quit_button)

char_buttons = []

char_buttons.append(main_char_button)
char_buttons.append(main_char_button1)
char_buttons.append(main_char_button2)
char_buttons.append(main_char_button3)
char_buttons.append(main_char_button4)
char_buttons.append(main_char_button5)
char_buttons.append(main_char_button6)
char_buttons.append(main_char_button7)
char_buttons.append(main_custo10)
char_buttons.append(main_custo20)
char_buttons.append(main_custo40)

menu_buttons = []

menu_buttons.append(main_go_button)

gameover_buttons = []

gameover_buttons.append(gameover_reset)

continue_buttons = []

continue_buttons.append(continue_button)
continue_buttons.append(return_button)

def desenharHud(janela, grupo):

    janela.blit(hud0_img, (730, 530))
    
    for button in grupo:
          button.desenhaBotao(janela)

def desenhaBotoes(janela, grupo):
      
      for button in grupo:
            button.desenhaBotao(janela)


def cliqueBotao(grupo, posicao):
      
      for button in grupo:
            button.checkForInput(posicao)

def scrollBotoes(grupo, wheelUp):

      valor = 30
      if wheelUp == False and j.buttonPosOffset < 0:
            j.buttonPosOffset += valor

      elif wheelUp and j.buttonPosOffset > -180:
            j.buttonPosOffset -= valor

      for botao in grupo:
            botao.rect = botao.image.get_rect(center=(botao.x_pos, botao.y_pos + j.buttonPosOffset))

def selecionarPersonagem(grupo, position):
      
      for botao in grupo:
            if botao.checkForInput(position) and botao.nome == "cardframe":
                  if botao.selected == False and len(equipe) != 3:
                        botao.image = pygame.image.load("imagem/background/cardframe_selected.png")
                        equipe.append(botao.monstro)
                        botao.selected = True
                  elif botao.selected == True:
                        botao.image = pygame.image.load(f"imagem/background/{botao.nome}.png")
                        equipe.remove(botao.monstro)
                        botao.selected = False


img_rubi = pygame.image.load("imagem/medidor/rubi.png")

def desenhaDescricaoMenu(janela, grupo, posicao, fonte, fonte2, equipe):
      
      espacamento = 150
      x = 860
      y = 490
      for monstro in equipe:
            rect = monstro.image.get_rect(center=(x, y))
            janela.blit(monstro.image, rect)
            x += espacamento

      for botao in grupo:
            if botao.nome == "cardframe" and botao.destacar(posicao):

                  if botao.monstro.magia == 3:
                        magia = "Corte"
                  if botao.monstro.magia == 4:
                        magia = "Impacto"
                  if botao.monstro.magia == 5:
                        magia = "Fogo"
                  if botao.monstro.magia == 6:
                        magia = "Agua"
                  if botao.monstro.magia == 7:
                        magia = "Raio"
                  if botao.monstro.magia == 8:
                        magia = "Neutro"
                  
                  cor = retornaCor(botao.monstro)
                  if cor == "gray20":
                        cor = "gray"
            
                  txtNome = fonte2.render(f"{botao.monstro.nome}", True, "white")
                  txtVida = fonte.render(f"Vida: {botao.monstro.vidamax}", True, "white")
                  # txtDescricao = fonte.render(botao.monstro.descricao, True, "white")
                  txtCusto = fonte2.render(f"{int(botao.monstro.custo)}", True, "crimson")
                  txtAtaque = fonte.render(f"Atq: {int(botao.monstro.ataque)}", True, "white")
                  txtDefesa = fonte.render(f"Def: {int(botao.monstro.defesa)}", True, "white")
                  txtMagia = fonte.render(f"Tipo de ataque: {magia}", True, cor)
                  txtCustoSkill = fonte.render(f"Custo da Skill: {botao.monstro.skill.custo}", True, "yellow")
                  txtSkill = fonte.render(f"Skill: {botao.monstro.skill.nome} - {botao.monstro.skill.descricao}", True, "gray")
                  rect = botao.monstro.image.get_rect(center=(800, 180))
                  rect1 = txtNome.get_rect(center=(800, 250))
                  janela.blit(botao.monstro.image, rect)
                  janela.blit(txtNome, rect1)
                  # janela.blit(txtDescricao ,)
                  janela.blit(txtVida, (890, 130))
                  janela.blit(txtAtaque, (890, 170))
                  janela.blit(txtDefesa,(890, 210))
                  janela.blit(txtMagia, (890, 250))
                  janela.blit(txtSkill, (740, 310))
                  janela.blit(txtCustoSkill, (740, 350))
                  janela.blit(img_rubi, (1170, 130))
                  janela.blit(txtCusto, (1220, 130))


def draw_aviso(janela, fonte):
    texto = fonte.render("Você não selecionou 3 personagens", True, "white")
    texto_rect = texto.get_rect(center=(750, 650))
    janela.blit(texto, texto_rect)
      
