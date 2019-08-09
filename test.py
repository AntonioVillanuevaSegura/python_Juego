#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Escrito por Daniel Fuentes B.
# Licencia: X11/MIT license http://www.opensource.org/licenses/mit-license.php
# https://www.pythonmania.net/es/2010/04/07/tutorial-pygame-3-un-videojuego/
# Fuentes github https://github.com/dbfuentes/tutorial-pygame
#sudo pip install pygame
#ficheros audio ogg
##sudo apt-get install vorbis-tools 

# ---------------------------
# Importacion de los módulos
# ---------------------------

import pygame
from pygame.locals import *
import os
import sys

# -----------
# Constantes
# -----------

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
IMG_DIR = "."
SONIDO_DIR = "."

# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------


def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print("Error, no se puede cargar la imagen: " + ruta)
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha is True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image
    
def load_sound(nombre, dir_sonido):
    ruta = os.path.join(dir_sonido, nombre)
    # Intentar cargar el sonido
    try:
        sonido = pygame.mixer.Sound(ruta)
    except (pygame.error) as message:
        print("No se pudo cargar el sonido:", ruta)
        sonido = None
    return sonido

# -----------------------------------------------
# Creamos los sprites (clases) de los objetos del juego:


class Pelota(pygame.sprite.Sprite):
	"La bola y su comportamiento en la pantalla"

	def __init__(self, sonido_golpe, sonido_punto):
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image("bola.png", IMG_DIR, alpha=True)
		self.rect = self.image.get_rect()
		self.rect.centerx = SCREEN_WIDTH / 2
		self.rect.centery = SCREEN_HEIGHT / 2
		self.speed = [3, 3]
		self.sonido_golpe = sonido_golpe
		self.sonido_punto = sonido_punto
		
		#Contadores juego
		self.jugador1=0
		self.jugador2=0

	def update(self):
		"""mira los limites de la pantalla"""
		"""width"""
		if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
			self.speed[0] = -self.speed[0]
			self.sonido_golpe.play()  # Reproducir sonido de punto			
			
			#Contadores de juego 
			if self.rect.left < 0:
				self.jugador2+=1
			else:
				self.judador1+=1
			
		""" Height"""
		if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
			self.speed[1] = -self.speed[1]
			self.sonido_golpe.play()  # Reproducir sonido de punto				
			
		"""
		La función move_ip(x,y) mueve de forma relativa el sprite por pantalla,
		esto es, subirá o bajará x pixel y avanzará retrocederá y pixel 
		(en este caso utilizara la velocidad que definimos anteriormente para la bola, 
		moviendola 3pixeles hacia la derecha y abajo).
		"""	
		self.rect.move_ip((self.speed[0], self.speed[1]))		

	def colision(self, objetivo):
		"""Para saber si dos sprites/objetos han chocado usamos
			True en caso de que entren en contacto
		"""
		if self.rect.colliderect(objetivo.rect):
			self.speed[0] = -self.speed[0]	
			self.sonido_golpe.play()  # Reproducir sonido de punto	
			
	def getJugadores(self):
		"""retorna los contadores de los jugadores como una lista"""
		return [self.jugador1,self.jugador2]

class Paleta(pygame.sprite.Sprite):
	"Define el comportamiento de las paletas de ambos jugadores"

	def __init__(self, x):
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image("paleta.png", IMG_DIR, alpha=True)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = SCREEN_HEIGHT / 2

	def humano(self):
		# Controlar que la paleta no salga de la pantalla
		if self.rect.bottom >= SCREEN_HEIGHT:
			self.rect.bottom = SCREEN_HEIGHT
		elif self.rect.top <= 0:
			self.rect.top = 0        

	def cpu(self, objetivo):
		"""sera el segundo jugador controlado por el computador"""
		self.speed=[0,2.5]
		
		self.rect.centery = objetivo.rect.centery
		if self.rect.bottom >= SCREEN_HEIGHT:
			self.rect.bottom = SCREEN_HEIGHT
		elif self.rect.top <= 0:
			self.rect.top = 0            

# ------------------------------
# Funcion principal del juego
# ------------------------------


def main():
	pygame.init()
	# creamos la ventana y le indicamos un titulo:
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("Ejemplo de un Pong Simple")

	# cargamos los objetos
	fondo = load_image("fondo_tutorial3.jpg", IMG_DIR, alpha=False)
	fondo=pygame.transform.scale(fondo, (SCREEN_WIDTH,SCREEN_HEIGHT))
	sonido_golpe = load_sound("tennis.ogg", SONIDO_DIR)
	sonido_punto = load_sound("aplausos.ogg", SONIDO_DIR)
	
	
	bola = Pelota(sonido_golpe, sonido_punto)
	jugador1 = Paleta(40)#Persona
	jugador2 = Paleta(SCREEN_WIDTH - 40)#CPU 	

	clock = pygame.time.Clock() #crea un reloj que controle el tiempo del juego 

	pygame.key.set_repeat(1, 25)  # Activa repeticion de teclas
	pygame.mouse.set_visible(False)    
	
	
	fuente= pygame.font.SysFont("Arial", 30)
	marcador1 = fuente.render(str (bola.getJugadores()[0]),True, (200,200,200), (0,125,0) )
	marcador2 = fuente.render(str (bola.getJugadores()[1]),True, (200,200,200), (0,125,0) )	

	# el bucle principal del juego
	while True:
		"""sirve para poner el reloj a un paso de 60 FPS, 
		esto se hace para que nunca se pase de 60 frames por segundo, así no importará 
		si estamos ejecutando esto en un pentium II o en una supercomputadora, 
		la velocidad siempre será como máximo de 60 frames por segundo.
		el juego nunca correrá a más de 60 frames/cuadros por segundo (sirve para controlar el framerate).
		"""
		clock.tick(60)
		# Obtenemos la posicon del mouse
		pos_mouse = pygame.mouse.get_pos()
		mov_mouse = pygame.mouse.get_rel()                

		#Actualiza objetos en pantalla
		jugador1.humano()
		jugador2.cpu(bola)
		bola.update()

		# Comprobamos si colisionan los objetos
		bola.colision(jugador1)     
		bola.colision(jugador2)		

		# Posibles entradas del teclado y mouse
		for event in pygame.event.get():
			if event.type == pygame.QUIT:#salir
				sys.exit(0)
				
			elif event.type == pygame.KEYDOWN:
				if event.key == K_UP:#Arriba
					jugador1.rect.centery -= 5
				elif event.key == K_DOWN:#Abajo
					jugador1.rect.centery += 5
				elif event.key == K_ESCAPE:#Salir
					sys.exit(0)
	 
			elif event.type == pygame.KEYUP:
				if event.key == K_UP:
					jugador1.rect.centery += 0
				elif event.key == K_DOWN:
					jugador1.rect.centery += 0
					
			# Si el mouse no esta quieto mover la paleta a su posicion
			#elif mov_mouse[1] != 0:
			elif mov_mouse[1] != 0:            
				jugador1.rect.centery = pos_mouse[1]


		#actualizamos la pantalla
		screen.blit(fondo, (0, 0))#Fondo
		screen.blit(bola.image, bola.rect) #Pelota
		screen.blit(jugador1.image, jugador1.rect)# Paleta 1 humano
		screen.blit(jugador2.image, jugador2.rect)# Paleta 2 cpu	
		screen.blit(marcador1,(1,1)) #Marcador Jugador 1
		screen.blit(marcador2,(SCREEN_WIDTH-50,1)) #Marcador Jugador 2	
		pygame.display.flip()                    


if __name__ == "__main__":
    main()
