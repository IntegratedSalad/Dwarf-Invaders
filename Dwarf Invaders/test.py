import pygame

pygame.init()

DWARF_MOVE_EVENT = pygame.USEREVENT + 1
DWARF_MOVE_MS = 100
pygame.time.set_timer(DWARF_MOVE_EVENT, DWARF_MOVE_MS)
can = True

while True:
	for event in pygame.event.get():
		if event.type == DWARF_MOVE_EVENT  and can:
			pygame.time.set_timer(DWARF_MOVE_EVENT, 500)
			print 'D'
			can = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				print 'd'
				can = True
				pygame.time.set_timer(DWARF_MOVE_EVENT, 0)

