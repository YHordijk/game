import pygame as pg
import numpy as np
import pkg.menu as menu
import copy



class TransitionAnimation:
	def __init__(self, menu, direction=None, start_time=0, start_color=None, target_color=None):
		self.direction = direction
		self.menu = menu
		self.start_time = start_time
		self.original_offset = copy.copy(menu.menu_offset)
		self.start_color = start_color
		self.target_color = target_color

		s = self.menu.SIZE
		if self.direction == 'left':
			self.d = np.array([ s[0], 0])
		elif self.direction == 'right':
			self.d = np.array([-s[0], 0])
		elif self.direction == 'up':
			self.d = np.array([0,  s[1]])
		elif self.direction == 'down':
			self.d = np.array([0, -s[1]])
		elif self.direction == None:
			self.d = np.array([0, 0])


class shift_menus(TransitionAnimation):
	def __init__(self, duration=0.4, *args, **kwargs):
		super().__init__(*args, **kwargs)
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
	def __init__(self, duration=0.4, speed=50, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.duration = duration
		self.speed = speed

	def update(self, time, dT):
		menu = self.menu
		progress = min((time - self.start_time)/self.duration, 1)
		menu.menu_offset = self.original_offset + self.d * (1-(self.speed**(1-progress)-1)/(self.speed-1))

		if progress == 1:
			menu.menu_offset = self.d + self.original_offset

		if not self.start_color is None and not self.target_color is None:
			s = self.start_color
			t = self.target_color

			menu.bkgr_color = int(t[0] + (s[0] - t[0])*progress), int(t[1] + (s[1] - t[1])*progress), int(t[2] + (s[2] - t[2])*progress)
			print(menu.bkgr_color)


class fade_out(TransitionAnimation):
	def __init__(self, fade_color=(0,0,0), fade_in=False, duration=1, pause=0, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fade_color = fade_color
		self.duration = duration

		self.fade_in = fade_in
		self.pause = pause


	def update(self, time, dT):
		menu = self.menu
		menu.draw_mask = True
		s = menu.SIZE

		progress = min((time - self.start_time)/(self.duration), 1)
		alpha = 510 * abs(progress/self.duration - int(progress/self.duration + 0.5))

		if progress >= 0.5:
			menu.menu_offset = self.d + self.original_offset

		if progress == 1:
			alpha = 0
			menu.draw_mask = False

		menu.mask_surface.fill((0,0,0,0))
		fade_surf = pg.Surface(self.menu.SIZE, pg.SRCALPHA)
		fade_surf.fill((*self.fade_color, alpha))
		menu.mask_surface.blit(fade_surf, (0,0))
