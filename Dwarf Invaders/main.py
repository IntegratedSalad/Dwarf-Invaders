#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import random
from math import sqrt

WINDOW_W = 50
WINDOW_H = 25
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (50, 50, 50)
GREEN = (0, 255, 0)
BROWN = (102, 51, 0)
LIGHT_BROWN = (153, 102, 51)
FONT_SIZE = 14
SCREEN_WIDTH = WINDOW_W * FONT_SIZE
SCREEN_HEIGHT = WINDOW_H * FONT_SIZE

class Game(object):
	def __init__(self):
		self.game_over = False

	def run(self):
		event = ""

		while not self.game_over or event == 'quit':

			clock.tick(FPS)
			event = handle_events()
			handle_keys()

			scr.fill(BLACK)

			for obj in objects:		
				if obj.check_off_boundaries() and obj is not None:
					obj.die()

				manage_elves(obj)
				manage_bolts(obj, self)
				obj.place()

			#MAP[15][15] = 3
			self.draw()
			fps = font.render("FPS: {0}".format(str(int(clock.get_fps()))), True, WHITE)
			scr.blit(fps, (0, 0))
			pygame.display.flip()


			if event == 'quit':
				break
		# losd menu
		self.quit()

	def quit(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.font.quit()
					pygame.quit
					exit(0)
			scr.fill(BLACK)
			losd = font.render("YOU LOSD XD", True, WHITE)
			scr.blit(losd, (SCREEN_WIDTH / 2 - 6 * FONT_SIZE, SCREEN_HEIGHT / 2))
			scr.blit(DWARF_SYMBOL, (SCREEN_WIDTH / 2 - 7 * FONT_SIZE, SCREEN_HEIGHT / 2))
			scr.blit(DWARF_SYMBOL, (SCREEN_WIDTH / 2 + 5 * FONT_SIZE, SCREEN_HEIGHT / 2))
			pygame.display.flip()



	def draw(self):

		for row in range(WINDOW_W):
			for column in range(WINDOW_H):
				if MAP[column][row] == DWARF_GLYPH:
					scr.blit(DWARF_SYMBOL, (row * FONT_SIZE, column * FONT_SIZE))
				elif MAP[column][row] == BOLT_GLYPH:
					scr.blit(BOLT_SYMBOL, (row * FONT_SIZE, column * FONT_SIZE))
				elif MAP[column][row] == HASH_GLYPH: # border
					scr.blit(HASH_SYMBOL, (row * FONT_SIZE, column * FONT_SIZE))
				elif MAP[column][row] == ELF_GLYPH:
					scr.blit(ELF_SYMBOL, (row * FONT_SIZE, column * FONT_SIZE))
				else:
					scr.blit(GROUND_SYMBOL, (row * FONT_SIZE, column * FONT_SIZE))


class Object(object):
	"""
	A generic class.
	What can an object do?
	Be placed, move, die, collide.
	"""

	def __init__(self, x, y, glyph, move_event, move_ms, shooter=None, direction_fly=None, to_hit=None):
		self.x = x
		self.y = y
		self.glyph = glyph
		self.move_event = move_event
		self.move_ms = move_ms
		self.can_move = True
		self.shooter = shooter
		self.direction_fly = direction_fly 
		self.to_hit = to_hit
		if self.shooter:
			self.shooter.owner = self

	def place(self):
		if self in objects:
			MAP[self.y][self.x] = self.glyph

	def clear(self, x, y):
		MAP[y][x] = 0

	def die(self):
		# if self.shooter:
			# if self.shooter.hp <0:
		#else:
		objects.remove(self)
		self.clear(self.x, self.y)
		self.shooter = None

	def collide(self, other_x, other_y):
		dx = other_x - self.x
		dy = other_y - self.y

		return sqrt(dx ** 2 + dy ** 2)

	def check_off_boundaries(self):
		return (self.y < 0 or self.y > WINDOW_H)

	def move(self, dx, dy):
		if self.can_move:
			if not (self.x + dx > WINDOW_W - 1) and not (self.x + dx < 0):
				self.can_move = False
				self.x += dx
				self.y += dy
				pygame.time.set_timer(self.move_event, self.move_ms)


class Shooter(object):
	def __init__(self, hp, can_shoot, shoot_event, shoot_event_ms, surpass_limits=False):
		self.hp = hp
		self.can_shoot = can_shoot
		self.shoot_event = shoot_event
		self.shoot_event_ms = shoot_event_ms
		self.surpass_limits = surpass_limits

	def shoot(self, direction, to_hits):
		if self.can_shoot:
			if direction == 0:
				d = -1
			else:
				d = 1
			self.can_shoot = False							
			bolt = Object(self.owner.x, self.owner.y + d, BOLT_GLYPH, BOLT_MOVE_EVENT, BOLT_MOVE_MS, direction_fly=direction, to_hit=to_hits)
			objects.append(bolt)
			pygame.time.set_timer(self.shoot_event, self.shoot_event_ms)

def init():
	global FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, font, scr, WHITE, GREY, \
	DWARF_SYMBOL, MAP, clock, objects, DWARF_OBJ, GROUND_SYMBOL, \
	DWARF_MOVE_EVENT,DWARF_MOVE_MS, DWARF_SHOOT_EVENT, DWARF_SHOOT_MS, BOLT_MOVE_EVENT, BOLT_MOVE_MS, BOLT_SYMBOL, DWARF_GLYPH, GROUND_GLYPH, \
	BOLT_GLYPH, ELF_GLYPH, ELF_SYMBOL, ELF_MOVE_MS, ELF_MOVE_EVENT, HASH_SYMBOL, HASH_GLYPH, ELF_SHOOT_EVENT, ELF_SHOOT_MS, FPS, FPS_TEXT

	pygame.init()
	pygame.font.init()
	clock = pygame.time.Clock()
	font = pygame.font.Font("Px437_IBM_BIOS.ttf", FONT_SIZE)
	pygame.display.set_caption("Dwarf Invaders")
	scr = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	MAP = [[0 for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)]

	DWARF_SYMBOL = font.render(u"☻", True, GREEN)
	GROUND_SYMBOL = font.render(u".", True, BROWN)
	HASH_SYMBOL = font.render(u"#", True, WHITE)
	BOLT_SYMBOL = font.render(u"|", True, LIGHT_BROWN)
	ELF_SYMBOL = font.render("e", True, GREEN)

	GROUND_GLYPH = 0
	DWARF_GLYPH = 1
	BOLT_GLYPH = 2
	HASH_GLYPH = 3
	ELF_GLYPH = 4

	# how fast can the dwarf move
	DWARF_MOVE_EVENT = pygame.USEREVENT + 1
	DWARF_MOVE_MS = 100
	pygame.time.set_timer(DWARF_MOVE_EVENT, DWARF_MOVE_MS)

	# how fast can the dwarf shoot
	DWARF_SHOOT_EVENT = pygame.USEREVENT + 2
	DWARF_SHOOT_MS = 1100
	pygame.time.set_timer(DWARF_SHOOT_EVENT, DWARF_SHOOT_MS)

	# how fast can the bolt move
	BOLT_MOVE_EVENT = pygame.USEREVENT + 3
	BOLT_MOVE_MS = 30
	pygame.time.set_timer(BOLT_MOVE_EVENT, BOLT_MOVE_MS)

	shooter_component = Shooter(hp=3, can_shoot=True, shoot_event=DWARF_SHOOT_EVENT, shoot_event_ms=DWARF_SHOOT_MS)
	DWARF_OBJ = Object(WINDOW_W / 2, WINDOW_H / 2 + 10, DWARF_GLYPH, DWARF_MOVE_EVENT, DWARF_MOVE_MS, shooter=shooter_component)
	objects = [DWARF_OBJ]
	FPS = 60

	ELF_ROWS = 3
	ELF_COLUMNS = 20

	create_elves(ELF_ROWS, ELF_COLUMNS)


def handle_keys():

	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_RIGHT]:
		DWARF_OBJ.clear(DWARF_OBJ.x, DWARF_OBJ.y) 
		DWARF_OBJ.move(1, 0)
	if pressed[pygame.K_LEFT]:
		DWARF_OBJ.clear(DWARF_OBJ.x, DWARF_OBJ.y) 
		DWARF_OBJ.move(-1, 0)
	if pressed[pygame.K_SPACE]:
		DWARF_OBJ.shooter.shoot(0, to_hits='elf')
		

def handle_events():

	if pygame.event.get(pygame.QUIT): return 'quit'

	for event in pygame.event.get():

		if event.type == DWARF_MOVE_EVENT:
			DWARF_OBJ.can_move = True
			pygame.time.set_timer(DWARF_MOVE_EVENT, 0)

		elif event.type == DWARF_SHOOT_EVENT:
			DWARF_OBJ.shooter.can_shoot = True
			pygame.time.set_timer(DWARF_SHOOT_EVENT, 0)

		elif event.type == BOLT_MOVE_EVENT:
			for bolt in objects:
				if bolt.glyph == BOLT_GLYPH:
					bolt.can_move = True
					pygame.time.set_timer(bolt.move_event, 0)


		elif event.type == ELF_MOVE_EVENT:
			for elf in objects:
				if elf.glyph == ELF_GLYPH:
					elf.can_move = True
					pygame.time.set_timer(elf.move_event, 0)

		elif event.type == ELF_SHOOT_EVENT:
			for elf in objects:
				if elf.glyph == ELF_GLYPH:	
					elf.shooter.can_shoot = True
					pygame.time.set_timer(elf.shooter.shoot_event, 0)


def create_elves(E_ROWS, E_COLUMNS):
	global ELF_MOVE_EVENT, ELF_MOVE_MS, ELF_SHOOT_EVENT, ELF_SHOOT_MS, CAN_ELVES_SHOOT, CAN_ELVES_MOVE
	ELF_MOVE_EVENT = pygame.USEREVENT + 4
	ELF_MOVE_MS = 180
	ELF_SHOOT_EVENT = pygame.USEREVENT + 5
	ELF_SHOOT_MS = 200
	CAN_ELVES_SHOOT = True
	CAN_ELVES_MOVE = True

	pygame.time.set_timer(ELF_SHOOT_EVENT, ELF_SHOOT_MS)
	pygame.time.set_timer(ELF_MOVE_EVENT, ELF_MOVE_MS)

	for y in range(E_ROWS):
		for x in range(E_COLUMNS):
			shooter_elf_component = Shooter(hp=1, can_shoot=CAN_ELVES_SHOOT, shoot_event=ELF_SHOOT_EVENT, shoot_event_ms=ELF_SHOOT_MS, surpass_limits=True)
			elf = Object((2*x) + WINDOW_H / 2-2, 2*y, ELF_GLYPH, ELF_MOVE_EVENT, ELF_MOVE_MS, direction_fly=1, shooter=shooter_elf_component)
			objects.append(elf)


def choose_dir_elves(elf):
	if elf.x == WINDOW_W - 1:
		return 'L'

	elif elf.x <= 1:
		return 'R'

def check_collision_bolt(bolt):
	for other in objects:

		if bolt.collide(other.x, other.y) < 1:
			if bolt.to_hit == 'elf' and other.glyph == ELF_GLYPH:
				return other

			if bolt.to_hit == 'dwarf' and other.glyph == DWARF_GLYPH:
				return other


def choose_elf_to_shoot():
	chance = random.randint(0, 10000)
	chance_limit = 65
	elf = random.choice(objects)
	if elf.glyph == ELF_GLYPH and chance <chance_limit:
		return elf.shooter


def manage_elves(obj):
	direction = choose_dir_elves(obj)
	shooting_elf = choose_elf_to_shoot()
	if obj.glyph == ELF_GLYPH:
		obj.clear(obj.x, obj.y)
		if direction == 'R':
			obj.direction_fly = 1
			obj.move(3, 1)

		if direction == 'L':
			obj.direction_fly = -1
			obj.move(-3, 1)

		obj.move(obj.direction_fly, 0)
		if shooting_elf is not None:
			shooting_elf.shoot(1, 'dwarf')

def manage_bolts(obj, game):

	if obj.glyph == BOLT_GLYPH:
		collision = check_collision_bolt(obj)
		if collision is not None:
			obj.die()
			collision.die()

		if collision is not None and collision.glyph is DWARF_GLYPH:
			game.game_over = True 

		else:

			if obj.direction_fly == 0:
				obj.clear(obj.x, obj.y)
				obj.move(0, -1)

			elif obj.direction_fly == 1:
				obj.clear(obj.x, obj.y)
				obj.move(0, 1)


if __name__ == '__main__':
	init()
	game = Game()
	game.run()



#TODO:
#	1.Optimize DONE
#	2.Add crates and bonuses
#	3.Add UI