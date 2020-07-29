import pygame as pg
import numpy as np
import pkg.screen as screen
import pkg.widgets as widg
import pkg.game_state as game_state
import pkg.transition_anims as tr_anim
import pkg.text as txt
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
	menu.set_dialogue('prologue')
	if active_transition_animation is None:
		active_transition_animation = tr_anim.fade_out(start_time=time, menu=menu, direction=direction, duration=duration, **kwargs)
	menu.dialogue.text_index = 0
	menu.dialogue.handle_events(0)


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

		# print(m.dialogue.text_index)

		# print(1/dT)
		txt.color_key = (0,0,updt%255)
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

		# print(m.choice)
		mouse_event = list(filter(lambda x: x.type == pg.MOUSEBUTTONDOWN, events))
		key_event = list(filter(lambda x: x.type == pg.KEYDOWN, events))
		m.update(mouse_event=mouse_event, key_event=key_event)
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

		self.choice = None
		self.input = None
		self.dialogue = None

		self.game = game_state.GameState()

		# self.font = pg.font.match_font('roman')
		# self.font = pg.font.match_font('courier')
		self.font = rf'{data_dir}/resources/fonts/Osaka-Mono.ttf'

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
										font=self.font, 
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
										 font=self.font, 
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
										 font=self.font, 
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
										font=self.font, 
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
										 font=self.font, 
										 font_size=50, 
										 text='Back', 
										 justify_x='center', 
										 justify_y='center', 
										 command=command_shift_menu,
										 command_kwargs={'direction':'right', 'start_color':(120, 0, 250), 'target_color': (250, 0, 120)}) )


		

		

	def set_dialogue(self, filename):
		####====== MAIN GAME ======####
		offset = np.asarray((0, self.SIZE[1]))
		size = (self.SIZE[0], 220)
		pos = (0, self.SIZE[1]-size[1])
		self.dialogue = widg.Dialogue(parent=self,
									  pos=np.asarray(pos)+offset+self.menu_offset,
									  size=size,
									  font=self.font, 
									  font_size=30, 
									  alpha = 200,
									  font_color=(0,0,0),
									  text_file=dialogue_dir + filename + '.txt')

		# self.widgets.append(self.dialogue)

	def clear_dialogue(self):
		self.choice = None


	def set_background(self, file):
		self.background = pg.image.load(file).copy().convert_alpha()
		self.background = pg.transform.scale(self.background, self.SIZE)

	def clear_background(self):
		self.background = None

	def set_chars(self, chars):
		if len(chars[0]) == 0:
			self.char_surface = None
			return

		char_surface = pg.Surface(self.SIZE)
		char_surface.fill((120,0,0))
		char_surface.set_colorkey((120,0,0))
		for char, pos in zip(*chars):
			try:
				char_im = pg.image.load(rf'{data_dir}\images\characters\{char}.png')
				char_surface.blit(char_im, (pos*self.SIZE[0] - char_im.get_width()//2, 200))
			except:
				print('Could not find image ' + rf'{data_dir}\images\characters\{char}.png')

		self.char_surface = char_surface

	def clear_chars(self):
		self.char_surface = None

	def set_choices(self, choices, actions):
		offset = np.asarray((0, self.SIZE[1]))
		size = (self.SIZE[0], 220)
		pos = (0, 220)
		self.choice = widg.ChoiceDialogue(parent=self,
										   choices=choices,
										   actions=actions,
										   pos=np.asarray(pos)+offset,
										   size=size,
										   font=self.font,
										   font_size=30,
										   alpha=150,
										   font_color=(0,0,0),
										   justify_x='center',
										   justify_y='center',
										   choice_spacing=40)

		# self.widgets.append(self.choice)


	def clear_choices(self):
		self.choice = None


	def set_input(self, var, default_input, char_limit):
		offset = np.asarray((0, self.SIZE[1]))
		size = (self.SIZE[0], 50)
		pos = (0, 220)
		self.input = widg.Input(parent=self,
								var=var,
								default_input=default_input,
								char_limit=char_limit,
								pos=np.asarray(pos)+offset,
								size=size,
								font=self.font,
								font_size=30,
								alpha=150,
								font_color=(0,0,0),
								justify_x='center',
								justify_y='center',)

		# self.widgets.append(self.input)


	def clear_input(self):
		self.input = None


	def update_widget_pos(self):
		# print(self.menu_offset)
		for widget in self.widgets + self.default_widgets:
			widget.pos = widget.original_pos + self.menu_offset


	def update(self, *args, **kwargs):
		draw_surface = self.draw_surface

		self.update_widget_pos()
		for widget in (self.widgets + self.default_widgets):
			#draw widget if it is on screen
			# try: print(self.screen_rect.colliderect(self.choice.rect), self.choice.rect)
			# except: pass
			if self.screen_rect.colliderect(widget.rect):
				#update widget if it needs updating
				if widget.updatable:
					widget.update(*args, **kwargs)
				widget.draw(draw_surface)


	@property
	def default_widgets(self):
		default_widgets = [self.input, self.dialogue, self.choice]
		default_widgets = [x for x in default_widgets if x is not None]
		return default_widgets
	





s = screen.Screen((1280,720))
dialogue_dir = os.getcwd() + r'\data\dialogue\\'
active_transition_animation = None
menu = Menu()



