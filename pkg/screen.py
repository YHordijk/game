import pygame as pg
import numpy as np


class Screen:
	def __init__(self, SIZE=(1280,720), bkgr_color=(0,0,0)):
		self.SIZE = SIZE
		self.disp = pg.display.set_mode(SIZE)
		self.bkgr_color = bkgr_color
		self.disp.fill(self.bkgr_color)

	def update(self, menu):
		try:
			self.disp.blit(menu.draw_surface, (0,0))
			# if menu.draw_mask:
			self.disp.blit(menu.mask_surface, (0,0))
			pg.display.update()
		except:
			raise Exception('Menu does not contain draw_surface')

	def clear(self):
		self.disp.fill(self.bkgr_color)


if __name__ == '__main__':
	s = Screen()
	print(type(s.disp))