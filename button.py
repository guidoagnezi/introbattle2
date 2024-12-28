import pygame

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


hud_buttons = []

hud_buttons.append(atk_button)
hud_buttons.append(com_button)
hud_buttons.append(skl_button)

def desenharHud(janela):
      
    janela.blit(hud0_img, (730, 530))
    
    for button in hud_buttons:
          button.desenhaBotao(janela)

def cliqueBotao(grupo, posicao):
      
      for button in grupo:
            button.checkForInput(posicao)