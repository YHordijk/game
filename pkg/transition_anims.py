import pygame as pg
import numpy as np
import pkg.menu as menu
import copy



class TransitionAnimation:
	def __init__(self, menu, start_time=0):
		self.menu = menu
		self.start_time = start_time
		self.original_offset = copy.copy(menu.menu_offset)


class shift_menus(TransitionAnimation):
	def __init__(self, direction='right', duration=0.4, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.direction = direction
		self.duration = duration


	def update(self, time, dT):
		menu = self.menu
		s = menu.SIZE

		progress = (time - self.start_time)/self.duration
		step_size = dT/self.duration
		if progress > 1:
			step_size -= progress - 1
			progress = 1


		if self.direction == 'right':
			d = np.array([s[0], 0]) + self.original_offset
			menu.menu_offset = self.original_offset + d * progress
		if self.direction == 'left':
			d = np.array([-s[0], 0]) + self.original_offset
			menu.menu_offset = self.original_offset + d * progress
		if self.direction == 'up':
			d = np.array([0, s[1]]) + self.original_offset
			menu.menu_offset = self.original_offset + d * progress
		if self.direction == 'down':
			d = np.array([0, -s[1]]) + self.original_offset
			menu.menu_offset = self.original_offset + d * progress


		if progress == 1:
			menu.menu_offset = d


class exp_shift_menus(TransitionAnimation):
	def __init__(self, direction='right', duration=0.4, speed=17, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.direction = direction
		self.duration = duration
		self.speed = speed

	def update(self, time, dT):
		menu = self.menu
		s = menu.SIZE

		progress = min((time - self.start_time)/self.duration, 1)

		step_size = dT/self.duration
		if progress > 1:
			step_size -= progress - 1
			progress = 1

		if self.direction == 'right':
			d = np.array([s[0], 0]) + self.original_offset
			menu.menu_offset = menu.menu_offset + (d - menu.menu_offset)*min(self.speed*dT,1)
		if self.direction == 'left':
			d = np.array([-s[0], 0]) + self.original_offset
			menu.menu_offset = menu.menu_offset + (d - menu.menu_offset)*min(self.speed*dT,1)
		if self.direction == 'up':
			d = np.array([0, s[1]]) + self.original_offset
			menu.menu_offset = menu.menu_offset + (d - menu.menu_offset)*min(self.speed*dT,1)
		if self.direction == 'down':
			d = np.array([0, -s[1]]) + self.original_offset
			menu.menu_offset = menu.menu_offset + (d - menu.menu_offset)*min(self.speed*dT,1)


		if progress == 1:
			menu.menu_offset = d