import pygame, sys, random
from eventos import *

pygame.init()

class ParticlePrinciple(pygame.sprite.Sprite):
	def __init__(self):
		self.particles = []

	def emit(self):
		if self.particles:
			self.delete_particles()
			for particle in self.particles:
				particle[0][1] += particle[2][0]
				particle[0][0] += particle[2][1]
				particle[1] -= 0.2
				pygame.draw.circle(screen,pygame.Color('White'),particle[0], int(particle[1]))

	def add_particles(self):
		pos_x = pygame.mouse.get_pos()[0]
		pos_y = pygame.mouse.get_pos()[1] 
		radius = 10
		direction_x = random.randint(-3,3)
		direction_y = random.randint(-3,3)
		particle_circle = [[pos_x,pos_y],radius,[direction_x,direction_y]]
		self.particles.append(particle_circle)

	def delete_particles(self):
		particle_copy = [particle for particle in self.particles if particle[1] > 0]
		self.particles = particle_copy

class ParticleStar():
	def __init__(self):
		self.particles = []
		self.surface = pygame.image.load('imagem/medidor/particulaDefesa.png').convert_alpha()
		self.width = self.surface.get_rect().width
		self.height = self.surface.get_rect().height

	def emit(self):
		if self.particles:
			self.delete_particles()
			for particle in self.particles:
				particle[0].x += particle[1]
				particle[0].y += particle[2]
				particle[3] -= 0.2
				screen.blit(self.surface,particle[0])

	def add_particles(self, posicao):
		pos_x = posicao[0] - self.width / 2 + random.randint(-50, 50)
		pos_y = posicao[1] - self.height / 2
		direction_x = 0#random.randint(-3,3)
		direction_y = -1#random.randint(-1,1)
		lifetime = random.randint(4,10)
		particle_rect = pygame.Rect(int(pos_x),int(pos_y),self.width,self.height)
		self.particles.append([particle_rect,direction_x,direction_y,lifetime])

	def delete_particles(self):
		particle_copy = [particle for particle in self.particles if particle[3] > 0]
		self.particles = particle_copy

pygame.init()
screen = pygame.display.set_mode((1360,720))
clock = pygame.time.Clock()

particula = ParticlePrinciple()

particula2 = ParticleStar()

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT,80)

# def play():
#     while True:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()
#                 if event.type == PARTICLE_EVENT:
#                     # particula.add_particles()
#                     # particle2.add_particles(-30,pygame.Color("Red"))
#                     # particle2.add_particles(-18,pygame.Color("Orange"))
#                     # particle2.add_particles(-6,pygame.Color("Yellow"))
#                     # particle2.add_particles(6,pygame.Color("Green"))
#                     # particle2.add_particles(18,pygame.Color("Blue"))
#                     # particle2.add_particles(30,pygame.Color("Purple"))
#                     particula2.add_particles()
					
#             screen.fill((30,30,30))
#             #particula.emit()
#             particula2.emit()
#             pygame.display.update()
#             clock.tick(120)
# play()