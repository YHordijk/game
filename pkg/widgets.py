import pygame as pg
import numpy as np
import copy



class Widget:
	def __init__(self, pos=None, size=None, colour=None, img=None):
		self.pos = np.asarray(pos)
		self.original_pos = copy.copy(self.pos)
		self.size = size
		self.colour = colour
		self.img = img
		self.updatable = False

		if colour is None and img is None:
			self.colour = (255,255,255)

	@property
	def rect(self):
		return pg.Rect(self.pos, self.size)
	

	def set_text(self, text):
		self.text = text
		self.update_draw_surface()


class Label(Widget):
	def __init__(self, text=None, font=None, font_size=None, font_colour=None, justify_x='left', justify_y='top', *args, **kwargs):
		super().__init__(*args, **kwargs)

		if font_size is not None: self.font_size = font_size
		elif font_size is None and font is not None: self.font_size = max(self.size[1], 12)

		self.font = pg.font.Font(font, self.font_size)
		
		self.text = text

		if font_colour is not None: self.font_colour = font_colour
		else: self.font_colour = (0,0,0)

		self.justify_x = justify_x
		self.justify_y = justify_y


		self.update_draw_surface()


	def update_draw_surface(self):
		self.draw_surface = pg.surface.Surface(self.size)
		self.draw_surface.fill(self.colour)
		pg.draw.rect(self.draw_surface, self.colour, self.rect)
		if not self.text is None:
			text = self.font.render(self.text, True, self.font_colour)

			text_pos = [0,0]

			if self.justify_x == 'left':
				text_pos[0] = 0

			if self.justify_x == 'center':
				text_pos[0] = (self.size[0] - text.get_size()[0])//2

			if self.justify_x == 'right':
				text_pos[0] = (self.size[0] - text.get_size()[0])

			if self.justify_y == 'top':
				text_pos[1] = 0

			if self.justify_y == 'center':
				text_pos[1] = (self.size[1] - text.get_size()[1])//2

			if self.justify_y == 'bottom':
				text_pos[1] = (self.size[1] - text.get_size()[1])


			self.draw_surface.blit(text, text_pos)


	def draw(self, surf):
		return surf.blit(self.draw_surface, self.pos)


	



class Button(Label):
	def __init__(self, command=None, enable_hover=True, hover_colour=(150,0,150), *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.updatable = True
		self.command = command
		self.enable_hover = enable_hover
		self.times_pressed = 0
		self.neutral_colour = copy.copy(self.colour)
		self.hover_colour = hover_colour

	def update(self, mouse_event):
		if self.enable_hover:

			do_update = True
			if self.rect.collidepoint(pg.mouse.get_pos()):
				if self.colour == self.hover_colour: do_update = False
				self.colour = self.hover_colour
			else:
				if self.colour == self.neutral_colour: do_update = False
				self.colour = self.neutral_colour
			if do_update: self.update_draw_surface()



		if self.rect.collidepoint(pg.mouse.get_pos()):
			if len(mouse_event) >= 1:
				but = mouse_event[0].button
				self.times_pressed += 1
				if but == 1:
					self.command(self)

		

