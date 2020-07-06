import pygame as pg
import numpy as np
import pkg.screen as screen
import pkg.widgets as widg
import pkg.transition_anims as tr_anim
import copy, math, os





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


def _start_button_action(source):
	global active_transition_animation
	if active_transition_animation is None:
		active_transition_animation = tr_anim.exp_shift_menus(start_time=time, menu=menu, direction='right')


def _test_button_action(source):
	global active_transition_animation
	if active_transition_animation is None:
		active_transition_animation = tr_anim.exp_shift_menus(start_time=time, menu=menu, direction='left')



def mainloop(SIZE=(1280,720), FPS=120):
	global menu, active_transition_animation
	m = menu
	s = screen.Screen(SIZE)

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
		except: pass



		m.draw_surface.fill(m.bkgr_color)
		m.update(mouse_event=list(filter(lambda x: x.type == pg.MOUSEBUTTONDOWN, events)))
		s.update(m)



class Menu:
	def __init__(self, SIZE=(1280, 720), bkgr_color=(120,0,250)):
		self.SIZE = SIZE
		self.screen_rect = pg.Rect((0,0),SIZE)
		self.widgets = []
		self.draw_surface = pg.Surface(SIZE)
		self.bkgr_color = bkgr_color
		self.visible = True
		self.menu_offset = np.array([0,0])

		font = pg.font.match_font('roman')



		#add widgets

		####====== MAIN MENU ======####
		offset = np.asarray((0, 0))
		#title label
		size = (800, 200)
		pos = (self.SIZE[0]//2 - size[0]//2, self.SIZE[1]//2 - size[1]//2 - 150)
		self.widgets.append( widg.Label(pos=np.asarray(pos)+offset+self.menu_offset, 
										size=size, 
										font=font, 
										font_size=100, 
										text='Main Menu', 
										justify_x='center', 
										justify_y='center') )
		
		#button
		size = (200, 100)
		pos = (self.SIZE[0]//2 - size[0]//2, self.SIZE[1]//2 - size[1]//2 + 150)
		self.widgets.append( widg.Button(pos=np.asarray(pos)+offset+self.menu_offset, 
										 size=size, 
										 font=font, 
										 font_size=50, 
										 text='Start', 
										 justify_x='center', 
										 justify_y='center', 
										 command=_start_button_action) )

		#button
		size = (200, 100)
		pos = (self.SIZE[0]//2 - size[0]//2, self.SIZE[1]//2 - size[1]//2 + 300)
		self.widgets.append( widg.Button(pos=np.asarray(pos)+offset+self.menu_offset, 
										 size=size, 
										 font=font, 
										 font_size=50, 
										 text='Colours', 
										 justify_x='center', 
										 justify_y='center', 
										 command=_colour_button_action, 
										 enable_hover=False) )


		####====== Settings MENU ======####
		offset = np.asarray((-SIZE[0], 0))
		#label
		size = (SIZE[0]-500, 150)
		width = 150
		verts = [(width, 0), (size[0]+width, 0), (size[0], size[1]), (0, size[1])]
		pos = (self.SIZE[0]//2 - size[0]//2 - width//2, 50)
		self.widgets.append( widg.Label(pos=np.asarray(pos)+offset+self.menu_offset, 
										polygon=verts, 
										font=font, 
										font_size=100, 
										text='Settings', 
										justify_x='center', 
										justify_y='center') )
		#button
		size = (200, 100)
		pos = (self.SIZE[0]//2 - size[0]//2, self.SIZE[1]//2 - size[1]//2 + 200)
		self.widgets.append( widg.Button(pos=np.asarray(pos)+offset+self.menu_offset, 
										 size=size, 
										 font=font, 
										 font_size=50, 
										 text='Back', 
										 justify_x='center', 
										 justify_y='center', 
										 command=_test_button_action) )
		size = (self.SIZE[0], 200)
		pos = (0, self.SIZE[1]-200)
		self.widgets.append( widg.Dialogue(pos=np.asarray(pos)+offset+self.menu_offset,
										   size=size,
										   font=font, 
										   font_size=30, 
										   text_file=dialogue_dir + 'test.txt'))


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




dialogue_dir = os.getcwd() + r'\data\dialogue\\'
active_transition_animation = None
menu = Menu()



