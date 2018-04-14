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

			event = handle_events()
			handle_keys()

			scr.fill(BLACK)

			collision = check_collision_bolt()
			if collision is not None:
				collision.die()

			for bolt in objects:
				if bolt.glyph == 2:
					if bolt.direction_fly == 0:
						bolt.clear(bolt.x, bolt.y)
						bolt.move(0, -1)
						#print bolt.x, bolt.y
					else:
						bolt.clear(bolt.x, bolt.y)
						bolt.move(0, 1)


			for elf in objects:
				direction = choose_dir_elves(elf)
				if elf.glyph == ELF_GLYPH:
					elf.clear(elf.x, elf.y)
					if direction == 'R':
						elf.direction_fly = 1
						elf.move(3, 1)

					if direction == 'L':
						elf.direction_fly = -1
						elf.move(-3, 1)

					elf.move(elf.direction_fly, 0)


			for obj in objects:
				obj.place()
				obj.check_off_boundaries()

			self.draw()

			pygame.display.flip()

			if event == 'quit':
				break
			
			clock.tick(60)

		self.quit()

	def quit(self):
		pygame.font.quit()
		pygame.quit
		exit(0)


	def draw(self):

		for row in range(WINDOW_W):
			for column in range(WINDOW_H):
				if MAP[column][row] == DWARF_GLYPH:
					scr.blit(DWARF_SYMBOL, (row * FONT_SIZE, column * FONT_SIZE))
				elif MAP[column][row] == BOLT_GLYPH:
					scr.blit(BOLT_SYMBOL, (row * FONT_SIZE, column * FONT_SIZE))
				elif MAP[column][row] == 3: # border
					scr.blit(HASH_SYMBOL, (row * FONT_SIZE, column * FONT_SIZE))
				elif MAP[column][row] == ELF_GLYPH:
					scr.blit(ELF_SYMBOL, (row * FONT_SIZE, column * FONT_SIZE))
				else:
					scr.blit(GROUND_SYMBOL, (row * FONT_SIZE, column * FONT_SIZE))


class Object(object):
	# A generic class
	# What can an object do?
	# Be drawn, move, die, collide

	def __init__(self, x, y, glyph, move_event, move_ms, shooter=None, direction_fly=None):
		self.x = x
		self.y = y
		self.glyph = glyph
		self.move_event = move_event
		self.move_ms = move_ms
		self.can_move = True
		self.shooter = shooter
		self.direction_fly = direction_fly 
		if self.shooter:
			self.shooter.owner = self

	def place(self):
		MAP[self.y][self.x] = self.glyph

	def clear(self, x, y):
		MAP[y][x] = 0

	def die(self):
		MAP[self.y][self.x] = 0
		objects.remove(self)

	def collide(self, other_x, other_y):
		dx = other_x - self.x
		dy = other_y - self.y

		return sqrt(dx ** 2 + dy ** 2)

	def check_off_boundaries(self):
		if self.y < 0 or self.y > WINDOW_H:
			self.die()

	def move(self, dx, dy):
		if self.can_move:
			if not (self.x + dx > WINDOW_W - 1) and not (self.x + dx < 0):
				self.can_move = False
				self.x += dx
				self.y += dy
				pygame.time.set_timer(self.move_event, self.move_ms)


class Shooter(object):
	def __init__(self, hp, can_shoot, shoot_event, shoot_event_ms):
		self.hp = hp
		self.can_shoot = can_shoot
		self.shoot_event = shoot_event
		self.shoot_event_ms = shoot_event_ms

	def shoot(self, direction):
		if self.can_shoot:
			self.can_shoot = False
			bolt = Object(self.owner.x, self.owner.y - 1, BOLT_GLYPH, BOLT_MOVE_EVENT, BOLT_MOVE_MS, direction_fly=direction)
			objects.append(bolt)
			pygame.time.set_timer(self.shoot_event, self.shoot_event_ms)


def init():
	global FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, font, scr, WHITE, GREY, \
	DWARF_SYMBOL, MAP, clock, objects, DWARF_OBJ, GROUND_SYMBOL, \
	DWARF_MOVE_EVENT,DWARF_MOVE_MS, DWARF_SHOOT_EVENT, DWARF_SHOOT_MS, BOLT_MOVE_EVENT, BOLT_MOVE_MS, BOLT_SYMBOL, DWARF_GLYPH, GROUND_GLYPH, \
	BOLT_GLYPH, ELF_GLYPH, ELF_SYMBOL, ELF_MOVE_MS, ELF_MOVE_EVENT

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
	ELF_GLYPH = 4
	HASH_GLYPH = 5

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
	BOLT_MOVE_MS = 100
	pygame.time.set_timer(BOLT_MOVE_EVENT, BOLT_MOVE_MS)

	#how fast can the elf move
	ELF_MOVE_EVENT = pygame.USEREVENT + 4
	ELF_MOVE_MS = 300
	pygame.time.set_timer(ELF_MOVE_EVENT, ELF_MOVE_MS)

	shooter_component = Shooter(hp=5, can_shoot=True, shoot_event=DWARF_SHOOT_EVENT, shoot_event_ms=DWARF_SHOOT_MS)
	#shooter_elf_component = Shooter(hp=5, can_shoot=True, shoot_event=ELF, shoot_event_ms=DWARF_SHOOT_MS)
	DWARF_OBJ = Object(WINDOW_W / 2, WINDOW_H / 2 + 10, DWARF_GLYPH, DWARF_MOVE_EVENT, DWARF_MOVE_MS, shooter=shooter_component)
	objects = [DWARF_OBJ]
	create_elves()


def handle_keys():

	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_RIGHT]:
		DWARF_OBJ.clear(DWARF_OBJ.x, DWARF_OBJ.y) 
		DWARF_OBJ.move(1, 0)
	if pressed[pygame.K_LEFT]:
		DWARF_OBJ.clear(DWARF_OBJ.x, DWARF_OBJ.y) 
		DWARF_OBJ.move(-1, 0)
	if pressed[pygame.K_SPACE]:
		DWARF_OBJ.shooter.shoot(0)

def handle_events():

	if pygame.event.get(pygame.QUIT): return 'quit'

	for event in pygame.event.get():

		if event.type == DWARF_MOVE_EVENT:
			DWARF_OBJ.can_move = True
			pygame.time.set_timer(DWARF_MOVE_EVENT, 0)

		if event.type == DWARF_SHOOT_EVENT:
			DWARF_OBJ.shooter.can_shoot = True
			pygame.time.set_timer(DWARF_SHOOT_EVENT, 0)

		if event.type == BOLT_MOVE_EVENT:
			for bolt in objects:
				if bolt.glyph == BOLT_GLYPH:
					bolt.can_move = True
					pygame.time.set_timer(bolt.move_event, 0)

		if event.type == ELF_MOVE_EVENT:
			for elf in objects:
				if elf.glyph == ELF_GLYPH:	
					elf.can_move = True
					pygame.time.set_timer(elf.move_event, 0)

def create_elves():
	for y in range(5):
		for x in range(15):
			elf = Object((2*x) + WINDOW_H / 2-2, y, ELF_GLYPH, ELF_MOVE_EVENT, ELF_MOVE_MS, direction_fly=1)
			objects.append(elf)


def choose_dir_elves(elf):
	if elf.x == WINDOW_W - 1:
		return 'L'

	if elf.x <= 1:
		return 'R'

def check_collision_bolt():
	for bolt in objects:
		for other in objects:
			if bolt.glyph == BOLT_GLYPH and other.glyph == ELF_GLYPH: #other.glyph == ELF_GLYPH: #other.shooter:
				if bolt.collide(other.x, other.y) < 1:
					bolt.die()
					return other

if __name__ == '__main__':
	init()
	game = Game()
	game.run()