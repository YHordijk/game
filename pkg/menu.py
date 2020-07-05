import pygame as pg
import numpy as np
import pkg.screen as screen
import pkg.widgets as widg
import pkg.transition_anims as tr_ani
import copy, math


class TransitionAnimation:
	def __init__(self, start_time=0):
		self.start_time = start_time


class shift_menus(TransitionAnimation):
	def __init__(self, menu1, menu2, direction='right', duration=0.4, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.menu1 = menu1
		self.menu2 = menu2
		self.direction = direction
		self.duration = duration

		if direction == 'right':
			for widget in menu2.widgets:
				widget.pos = (widget.original_pos[0] - menu2.SIZE[0], widget.original_pos[1])

	def update(self):
		s = self.menu1.SIZE

		progress = min((time - self.start_time)/self.duration, 1)

		self.menu1.hidden = False
		self.menu2.hidden = False
		print(progress)

		for widget in self.menu1.widgets:
			if self.direction == 'right':
				target_pos = np.array([widget.original_pos[0] + s[0], widget.original_pos[1]])
				widget.pos[0] = (target_pos[0] - widget.original_pos[0]) * progress

		for widget in self.menu2.widgets:
			if self.direction == 'right':
				target_pos = np.array([widget.original_pos[0], widget.original_pos[1]])
				widget.pos = (target_pos - widget.pos) * 0.2


		if time >= self.duration + self.start_time:
			global active_transition_animation
			active_transition_animation = None
			self.menu1.hidden = True




def _start_button_action(source):
	print('Pressed start button!')

	if source.times_pressed % 4 == 0:
		source.color = (255,255,255)
	elif source.times_pressed % 4 == 1:
		source.color = (0,255,0)
	elif source.times_pressed % 4 == 2:
		source.color = (0,0,255)
	elif source.times_pressed % 4 == 3:
		source.color = (255,0,0)

	source.update_draw_surface()


def _start_button_action(source):
	global active_menu, active_transition_animation
	new_menu = menus['testmenu']
	active_transition_animation = shift_menus(start_time=time, menu1=active_menu, menu2=new_menu, direction='right')
	active_menu = new_menu


def _test_button_action(source):
	global active_menu, active_transition_animation
	new_menu = menus['mainmenu']
	active_transition_animation = shift_menus(start_time=time, menu1=active_menu, menu2=new_menu, direction='right')
	active_menu = new_menu






class Menu:
	def __init__(self, widgets=[], SIZE=(1280, 720), bkgr_color=(0,0,0)):
		self.SIZE = SIZE
		self.widgets = widgets
		self.draw_surface = pg.Surface(SIZE)
		self.bkgr_color = bkgr_color
		self.hidden = True



	def add_widget(self, widget):
		self.widgets.append(widget)


	def update(self, *args, **kwargs):
		draw_surface = self.draw_surface
		# draw_surface.fill(self.bkgr_color)
		for widget in self.widgets:
			if widget.updatable:
				widget.update(*args, **kwargs)
			widget.draw(draw_surface)



class MainMenu(Menu):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		#add widgets
		self.widgets = []
		#title label
		size = (800, 200)
		font = pg.font.match_font('mono')
		self.widgets.append( widg.Label(pos=(self.SIZE[0]//2 - size[0]//2, self.SIZE[1]//2 - size[1]//2 - 150), size=size, font=font, font_size=100, text='Main Menu', justify_x='center', justify_y='center') )
		
		#button
		size = (200, 100)
		font = pg.font.match_font('mono')
		self.widgets.append( widg.Button(pos=(self.SIZE[0]//2 - size[0]//2, self.SIZE[1]//2 - size[1]//2 + 150), size=size, font=font, font_size=50, text='Start', justify_x='center', justify_y='center', action=_start_button_action) )


	def update(self, *args, **kwargs):
		draw_surface = self.draw_surface
		# draw_surface.fill(self.bkgr_color)

		for widget in self.widgets:
			if widget.updatable:
				widget.update(*args, **kwargs)
			widget.draw(draw_surface)


class TestMenu(Menu):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		
		font = pg.font.match_font('roman')

		#add widgets
		self.widgets = []
		#title label
		size = (800, 200)
		self.widgets.append( widg.Label(pos=(self.SIZE[0]//2 - size[0]//2, self.SIZE[1]//2 - size[1]//2), size=size, font=font, font_size=100, text='Second Menu', justify_x='center', justify_y='center') )
		#button
		size = (200, 100)
		self.widgets.append( widg.Button(pos=(self.SIZE[0]//2 - size[0]//2, self.SIZE[1]//2 - size[1]//2 + 200), size=size, font=font, font_size=50, text='Back', justify_x='center', justify_y='center', action=_test_button_action) )




def mainloop(SIZE=(1280,720), FPS=120):

	s = screen.Screen(SIZE)

	rungame = True
	clock = pg.time.Clock()

	global time, updt, dT
	updt = 0
	time = 0

	while rungame:

		events = pg.event.get()
		# s.clear()
		#pre-update
		for event in events:
			if event.type == pg.QUIT:
				  rungame = False

		dT = clock.tick_busy_loop(FPS)/1000
		time += dT
		updt += 1



		if active_transition_animation is not None:
			active_transition_animation.update()


		for key, val in menus.items():
			if not val.hidden:
				val.draw_surface.fill(val.bkgr_color)
				val.update(mouse_event=list(filter(lambda x: x.type == pg.MOUSEBUTTONDOWN, events)))
				s.update(val)


menus = {'mainmenu': MainMenu(), 'testmenu': TestMenu()}

active_menu = menus['mainmenu']
active_menu.hidden = False
active_transition_animation = None