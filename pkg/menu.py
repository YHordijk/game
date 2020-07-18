import pygame as pg
import numpy as np
import pkg.screen as screen
import pkg.widgets as widg
import pkg.transition_anims as tr_anim
import copy, math, os


data_dir = os.path.join(os.getcwd(), 'data\\')



def _colour_button_action(source):
	if source.times_pressed % 4 == 0:
		source.colour = (255,255,255)
	elif source.times_pressed % 4 == 1:
		source.colour = (0,255,0)
	elif source.times_pressed % 4 == 2:
		source.colour = (0,0,255)
	elif source.times_pressed % 4 == 3:
		source.colour = (255,0,0)

	source.update_draw_surface()


def command_shift_menu(source, direction='right', duration=0.4, **kwargs):
	global active_transition_animation
	if active_transition_animation is None:
		active_transition_animation = tr_anim.exp_shift_menus(start_time=time, menu=menu, direction=direction, duration=duration, **kwargs)

def command_fade_menu(source, direction='right', duration=1, **kwargs):
	global active_transition_animation
	if active_transition_animation is None:
		active_transition_animation = tr_anim.fade_out(start_time=time, menu=menu, direction=direction, duration=duration, **kwargs)


def command_start_button(source, direction='right', duration=1, **kwargs):
	global active_transition_animation
	if active_transition_animation is None:
		active_transition_animation = tr_anim.fade_out(start_time=time, menu=menu, direction=direction, duration=duration, **kwargs)
	menu.widgets[-1].text_index = 0
	menu.widgets[-1].handle_events(0)


def mainloop(SIZE=(1280,720), FPS=120):
	global s, menu, active_transition_animation
	m = menu
	rungame = True
	clock = pg.time.Clock()

	global time, updt, dT
	updt = 0
	time = 0

	while rungame:

		events = pg.event.get()
		#pre-update
		for event in events:
			if event.type == pg.QUIT:
				  rungame = False

		dT = clock.tick_busy_loop(FPS)/1000
		time += dT
		updt += 1

		# print(1/dT)

		try: 
			active_transition_animation.update(time, dT)
			if time - active_transition_animation.start_time > active_transition_animation.duration:
				active_transition_animation = None
		except Exception as e: pass

		# print(m.bkgr_color)
		if m.background is not None:
			m.draw_surface.blit(m.background, (0,0))
		else:
			m.draw_surface.fill(m.bkgr_color)

		if m.char_surface is not None:
			m.draw_surface.blit(m.char_surface, (0,0))

		m.update(mouse_event=list(filter(lambda x: x.type == pg.MOUSEBUTTONDOWN, events)))
		s.update(m)



class Menu:
	def __init__(self, SIZE=(1280, 720), bkgr_color=(120,0,250), background=None):
		self.SIZE = SIZE
		self.screen_rect = pg.Rect((0,0),SIZE)
		self.widgets = []
		self.draw_surface = pg.Surface(SIZE)
		self.mask_surface = pg.Surface(SIZE, pg.SRCALPHA)
		self.draw_mask = False
		self.bkgr_color = bkgr_color
		self.background = background
		self.menu_offset = np.array([0,0])

		font = pg.font.match_font('roman')

		self.char_surface = None



		#add widgets

		####====== MAIN MENU ======####
		offset = np.asarray((0, 0))
		#title label
		size = (800, 200)
		pos = (self.SIZE[0]//2 - size[0]//2, self.SIZE[1]//2 - size[1]//2 - 150)
		self.widgets.append( widg.Label(parent=self,
										pos=np.asarray(pos)+offset+self.menu_offset, 
										size=size, 
										font=font, 
										font_size=100, 
										text='Main Menu', 
										justify_x='center', 
										justify_y='center') )
		
		#play button
		size = (200, 100)
		pos = (self.SIZE[0]//2 - size[0]//2, self.SIZE[1]//2 - size[1]//2 + 125)
		self.widgets.append( widg.Button(parent=self,
										 pos=np.asarray(pos)+offset+self.menu_offset, 
										 size=size, 
										 font=font, 
										 font_size=50, 
										 text='Start', 
										 justify_x='center', 
										 justify_y='center', 
										 command=command_start_button,
										 command_kwargs={'direction':'down'}) )


		#settings button
		size = (200, 100)
		pos = (self.SIZE[0]//2 - size[0]//2, self.SIZE[1]//2 - size[1]//2 + 275)
		self.widgets.append( widg.Button(parent=self,
										 pos=np.asarray(pos)+offset+self.menu_offset, 
										 size=size, 
										 font=font, 
										 font_size=50, 
										 text='Settings', 
										 justify_x='center', 
										 justify_y='center',
										 command=command_shift_menu,
										 command_kwargs={'direction':'left', 'start_color':(250, 0, 120), 'target_color': (120, 0, 250)}, 
										 enable_hover=True) )


		####====== Settings MENU ======####
		offset = np.asarray((-SIZE[0], 0))
		#label
		size = (SIZE[0]-500, 150)
		width = 150
		verts = [(width, 0), (size[0]+width, 0), (size[0], size[1]), (0, size[1])]
		pos = (self.SIZE[0]//2 - size[0]//2 - width//2, 50)
		self.widgets.append( widg.Label(parent=self,
										pos=np.asarray(pos)+offset+self.menu_offset, 
										polygon=verts, 
										font=font, 
										font_size=100, 
										text='Settings', 
										justify_x='center', 
										justify_y='center') )
		#back button
		size = (200, 100)
		pos = (self.SIZE[0]//2 - size[0]//2, self.SIZE[1]//2 - size[1]//2 + 200)
		self.widgets.append( widg.Button(parent=self,
										 pos=np.asarray(pos)+offset+self.menu_offset, 
										 size=size, 
										 font=font, 
										 font_size=50, 
										 text='Back', 
										 justify_x='center', 
										 justify_y='center', 
										 command=command_shift_menu,
										 command_kwargs={'direction':'right', 'start_color':(120, 0, 250), 'target_color': (250, 0, 120)}) )


		####====== MAIN GAME ======####
		offset = np.asarray((0, SIZE[1]))
		size = (self.SIZE[0], 200)
		pos = (0, self.SIZE[1]-200)
		self.widgets.append( widg.Dialogue(parent=self,
										   pos=np.asarray(pos)+offset+self.menu_offset,
										   size=size,
										   font=font, 
										   font_size=30, 
										   alpha = 200,
										   default_text_color=(0,0,0),
										   text_files=[dialogue_dir + 'test.txt']))


	def set_background(self, file):
		self.background = pg.image.load(file).copy().convert_alpha()
		self.background = pg.transform.scale(self.background, self.SIZE)

	def clear_background(self):
		print('hello')
		self.background = None


	def update_widget_pos(self):
		for widget in self.widgets:
			widget.pos = widget.original_pos + self.menu_offset


	def update(self, *args, **kwargs):
		draw_surface = self.draw_surface
		self.update_widget_pos()
		for widget in self.widgets:
			#draw widget if it is on screen
			if self.screen_rect.colliderect(widget.rect):
				#update widget if it needs updating
				if widget.updatable:
					widget.update(*args, **kwargs)
				widget.draw(draw_surface)


	def set_chars(self, chars):
		if len(chars[0]) == 0:
			self.char_surface = None
			return

		char_surface = pg.Surface(self.SIZE)
		char_surface.fill((120,0,0))
		char_surface.set_colorkey((120,0,0))

		for char, pos in zip(*chars):
			char_im = pg.image.load(rf'{data_dir}\images\characters\{char}.png')
			char_surface.blit(char_im, (pos*self.SIZE[0], 200))

		self.char_surface = char_surface


	def clear_chars(self):
		self.char_surface = None





s = screen.Screen((1280,720))
dialogue_dir = os.getcwd() + r'\data\dialogue\\'
active_transition_animation = None
menu = Menu()



