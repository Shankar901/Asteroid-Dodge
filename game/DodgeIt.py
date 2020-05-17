import pygame
from pygame.locals import *
import random
import time
import math
import os

pygame.init()

if not os.path.exists('LocalData'):
	os.mkdir('LocalData')

if not os.path.exists('LocalData/score.txt'):
	f = open('LocalData/score.txt', 'w')
	f.write(f"HighScore: 0")
	f.close()

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

flags = DOUBLEBUF
dodged = 0
with open('LocalData/score.txt', 'r') as f:
	high_score_phrase = f.read()
	high_score = int(high_score_phrase[high_score_phrase.find(' '):])

explosion = pygame.image.load('explosions/explosion.png')

count = 0

surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), flags)
pygame.display.set_caption('Asteroid Dodge')

icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
surface.set_alpha(None)

clock = pygame.time.Clock()

crash_sound = pygame.mixer.Sound('sounds/crash.wav')
music = pygame.mixer.music.load('sounds/bgmusic.mp3')

asteroid = pygame.image.load('images/asteroid.png')
asteroid2 = pygame.image.load('images/asteroid2 (2).png')
asteroid3 = pygame.image.load('images/asteroid3.png')
spaceship = pygame.image.load('images/transport.png')
background = pygame.image.load('images/space1.png')
background = background.convert()

ship_width = 64
paused = False

speed_y = 1
speed_x = 6

def pack(item, x, y):
	surface.blit(item, (x, y))

def switch_shuttle():
	global spaceship, speed_x, speed_y
	spaceship = pygame.image.load('images/transport.png')
	speed_y = 0.7
	speed_x = 8
	intro_screen()

def switch_razor():
	global spaceship, speed_x, speed_y
	spaceship = pygame.image.load('images/space-ship.png')
	speed_y = 1.7
	speed_x = 7.1
	intro_screen()

def switch_spacejet():
	global spaceship, speed_x, speed_y
	spaceship = pygame.image.load('images/ship.png')
	speed_y = 1.3
	speed_x = 7.4
	time.sleep(0.1)
	intro_screen()

def select_ship():
	shuttle_img = pygame.image.load('images/shuttle1.png')
	jet_img = pygame.image.load('images/ship1.png')
	razor_img = pygame.image.load('images/razor1.png')

	def display_font(text, x, y):
		Text = pygame.font.SysFont(None, 20)
		text_surface, text_rect = text_(text, Text, (255, 255, 255))
		text_rect.center = (x, y)
		surface.blit(text_surface, text_rect)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

		surface.fill((0, 0, 4))
		Text = pygame.font.SysFont("Big Space.ttf", 90)
		text_surface, text_rect = text_("Select Ship", Text, (255, 255, 255))
		text_rect.center = (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.25)
		surface.blit(text_surface, text_rect)
		button(30, 140, 30, 40, intro_screen, (50, 50, 50), (60, 60, 60), "Back")
		button(100, 170, 400, 40, switch_shuttle, (200, 60, 0), (210, 80, 0), "Shuttle")
		button(520, 170, 400, 40, switch_razor, (0, 200, 100), (0, 220, 120), "Razor")
		button(310, 170, 400, 40, switch_spacejet, (100, 0, 200), (120, 0, 220), "Space Jet")

		surface.blit(shuttle_img, (120, 250))
		display_font("Hor Speed: 8", 180, 470)
		display_font("Vert Speed: 0.7", 180, 490)

		surface.blit(jet_img, (330, 250))
		display_font("Hor Speed: 7.4", 390, 470)
		display_font("Vert Speed: 1.3", 390, 490)

		surface.blit(razor_img, (540, 250))
		display_font("Hor Speed: 7.1", 600, 470)
		display_font("Vert Speed: 1.7", 600, 490)

		pygame.display.update()


def ast_dodged(count):
	font = pygame.font.SysFont(None, 40)
	text = font.render(f"Score: {str(count)}", True, (51, 204, 255))
	surface.blit(text, (20, 20))

def button(x, w, y, h, func, color, bright_color, text):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if (x + w > mouse[0] and mouse[0] > x) and (y + h > mouse[1] and mouse[1] > y):
			pygame.draw.rect(surface, bright_color, (x, y, w, h))
			if click[0] == 1:
				func()
	else:
		pygame.draw.rect(surface, color, (x, y, w, h))

	Text = pygame.font.SysFont(None, 30)
	text_surface, text_rect = text_(text, Text, (255, 255, 255))
	text_rect.center = ( (x+(w/2)), (y+(h/2)) )
	surface.blit(text_surface, text_rect)

def dis_high_score(high_score):
	font = pygame.font.SysFont(None, 40)
	text = font.render(f"HighScore: {str(high_score)}", True, (51, 204, 255))
	surface.blit(text, (DISPLAY_WIDTH - 200, 20))

def display_asteroid(ast_x, ast_y, ast_speed, ast_height):
	global dodged
	global high_score
	if ast_y > DISPLAY_HEIGHT:
		ast_y = 0 - ast_height - 100
		ast_x = random.randrange(DISPLAY_WIDTH - 130)
		dodged += 1
		ast_speed += 0.3
	if high_score == 0 or dodged > high_score:
		high_score = dodged

	return ast_x, ast_y, ast_speed

def text_(text, font, color):
	text_surface = font.render(text, True, color)
	return text_surface, text_surface.get_rect()

def crash(x, y):
	global dodged
	dodged = 0
	surface.blit(explosion, (x, y))
	crash_sound.play()
	pygame.display.update()
	time.sleep(0.2)
	pygame.mixer.music.pause()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

		surface.fill((0, 0, 4))

		Text = pygame.font.SysFont(None, 90)
		text_surface, text_rect = text_("Game Over", Text, (255, 0, 100))
		text_rect.center = (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.35)
		surface.blit(text_surface, text_rect)

		button(550, 220, 30, 40, intro_screen, (0, 230, 235), (0, 240, 250), "Main Menu")
		button(310, 170, 310, 40, main_loop, (0, 210, 50), (0, 240, 90), "Restart")
		button(310, 170, 360, 40, quit, (200, 0, 50), (240, 0, 90), "Exit")
		pygame.display.update()
		clock.tick(40)


def new_game():
	global high_score
	high_score = 0
	main_loop()

def intro_screen():
	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

		surface.fill((0, 0, 4))
		Text = pygame.font.SysFont(None, 100)
		text_Surface, text_rect = text_("Asteroid Dodge", Text, (200, 200, 255))
		text_rect.center = (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.35)
		surface.blit(text_Surface, text_rect)

		button(310, 170, 300, 40, new_game, (0, 100, 180), (0, 120, 240), "New Game")
		button(310, 170, 350, 40, main_loop, (0, 210, 50), (0, 240, 90), "Continue")
		button(550, 220, 530, 40, select_ship, (235, 230, 0), (250, 240, 0), "Change Ship")
		button(30, 170, 530, 40, quit, (200, 0, 50), (240, 0, 90), "Exit")
		pygame.display.update()
		clock.tick(40)

def continue_game():
	global paused
	pygame.mixer.music.unpause()
	paused = False

def pause():
	global paused
	pygame.mixer.music.pause()
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					pygame.mixer.music.unpause()
					paused = False

		surface.fill((0, 0, 4))
		Text = pygame.font.SysFont(None, 100)
		text_Surface, text_rect = text_("Paused", Text, (255, 255, 255))
		text_rect.center = (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.35)
		surface.blit(text_Surface, text_rect)

		button(310, 170, 310, 40, continue_game, (0, 210, 50), (0, 240, 90), "Continue")
		button(310, 170, 360, 40, quit, (200, 0, 50), (240, 0, 90), "Quit")
		pygame.display.update()
		clock.tick(40)

def main_loop():

	global paused

	bg_y = 600 - background.get_height()
	all_astx = (
		random.randrange(0, DISPLAY_WIDTH - 128),
		random.randrange(0, DISPLAY_WIDTH - 128),
		random.randrange(200, DISPLAY_WIDTH - 200)
	)
	all_asty = (-600, -800, -900)
	all_ast_speeds = (7, 5, 6)
	all_ast_widths = (64, 128, 128)
	all_ast_heights = all_ast_widths

	ast_x, ast_x2, ast_x3 = all_astx
	ast_y, ast_y2, ast_y3 = all_asty
	ast_speed1, ast_speed2, ast_speed3 = all_ast_speeds

	x, y = DISPLAY_WIDTH * 0.45, DISPLAY_HEIGHT * 0.8
	x_change = 0
	y_change = 0
	bg_y_change = 0

	pygame.mixer.music.play(-1)
	running = True
	while running:

		surface.fill((0,0,0))
		surface.blit(background, (800 - background.get_width(), bg_y))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = -speed_x
				elif event.key == pygame.K_RIGHT:
					x_change = speed_x
				elif event.key == pygame.K_UP:
					y_change = -speed_y
					bg_y_change += 0.001
				elif event.key == pygame.K_DOWN:
					y_change = speed_y
				elif event.key == pygame.K_SPACE:
					paused = True
					pause()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					x_change = 0
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					y_change = 0
					bg_y_change -= 0.001

		ast_x, ast_y, ast_speed1 = display_asteroid(ast_x, ast_y, ast_speed1, all_ast_heights[0])

		if dodged >= 20:
			ast_x2, ast_y2, ast_speed2 = display_asteroid(ast_x2, ast_y2, ast_speed2, all_ast_heights[1])

		if dodged >= 40:
			ast_x3, ast_y3, ast_speed3 = display_asteroid(ast_x3, ast_y3, ast_speed3, all_ast_heights[2])

		bg_y_change += 0.0001
		if math.sqrt((x - ast_x) ** 2 + (y - ast_y) ** 2) < 64:
			crash(x, y)

		if dodged >= 20:
			if math.sqrt((x - 30 - ast_x2) ** 2 + (y - ast_y2) ** 2) < 100:
				crash(x, y)

		if dodged >= 40:
			if math.sqrt((x - 30 - ast_x3) ** 2 + (y - ast_y3) ** 2) < 100:
				crash(x, y)

		if x > DISPLAY_WIDTH - ship_width:
			x = DISPLAY_WIDTH - ship_width

		if x < 0:
			x = 0

		if y > DISPLAY_HEIGHT - ship_width:
			y = DISPLAY_HEIGHT - ship_width

		if y < DISPLAY_HEIGHT * 0.7:
			y = DISPLAY_HEIGHT * 0.7

		with open('LocalData/score.txt', 'w') as f:
			f.write(f"HighScore: {str(high_score)}")

		pygame.mixer.music.set_volume(0.2)

		x += x_change
		y += y_change
		bg_y += bg_y_change
		ast_y += ast_speed1
		ast_y2 += ast_speed2
		ast_y3 += ast_speed3

		pack(asteroid, ast_x, ast_y)

		if dodged >= 20:
			pack(asteroid2, ast_x2, ast_y2)
		if dodged >= 40:
			pack(asteroid3, ast_x3, ast_y3)
		pack(spaceship, x, y)
		ast_dodged(dodged)
		dis_high_score(high_score)

		pygame.display.update()
		clock.tick(80)

intro_screen()
