import pygame as pg
import numpy as np
import copy, os
import pkg.polygon as pol
import pkg.text as txt


data_dir = os.path.join(os.getcwd(), 'data\\')


class Widget:
	def __init__(self, parent=None, pos=None, polygon=None, size=None, colour=None, img=None, font=None, font_size=None, font_color=(0,0,0)):
		self.parent = parent
		self.pos = np.asarray(pos)
		self.original_pos = copy.copy(self.pos)
		self.size = size
		self.colour = colour
		self.colour_key = (255,0,123)
		self.img = img
		self.updatable = False
		if polygon is not None:
			self.polygon = pol.Polygon(polygon)

		if colour is None and img is None:
			self.colour = (255,255,255)

		if font_size is not None: self.font_size = font_size
		elif font_size is None and font is not None: self.font_size = max(self.rect.size[1], 12)

		self.font = pg.font.Font(font, self.font_size)
		self.font_color = font_color if font_color is not None else (255,255,255)


	@property
	def rect(self):
		try:
			return self.polygon.rect
		except:
			return pg.Rect(self.pos, self.size)
	
	

	def set_text(self, text):
		self.text = text
		self.update_draw_surface()


	def collidepoint(self, p):
		try:
			return self.polygon.collidepoint(p)
		except:
			return self.rect.collidepoint(p)


class Label(Widget):
	def __init__(self, text=None, text_margin=(0,0), justify_x='left', justify_y='top', *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.text = text

		self.text_margin = np.asarray(text_margin)

		self.justify_x = justify_x
		self.justify_y = justify_y


		self.update_draw_surface()


	def update_draw_surface(self):
		self.draw_surface = pg.surface.Surface(self.rect.size)
		self.draw_surface.fill(self.colour_key)

		if hasattr(self, 'polygon'):
			pg.draw.polygon(self.draw_surface, self.colour, self.polygon.verteces.tolist())
		else:
			pg.draw.rect(self.draw_surface, self.colour, ((0,0), self.rect.size))

		if not self.text is None:
			text = self.font.render(self.text, True, self.font_color)

			text_pos = [0,0]

			if self.justify_x == 'left':
				text_pos[0] = 0

			if self.justify_x == 'center':
				text_pos[0] = (self.rect.size[0] - text.get_size()[0])//2

			if self.justify_x == 'right':
				text_pos[0] = (self.rect.size[0] - text.get_size()[0])

			if self.justify_y == 'top':
				text_pos[1] = 0

			if self.justify_y == 'center':
				text_pos[1] = (self.rect.size[1] - text.get_size()[1])//2

			if self.justify_y == 'bottom':
				text_pos[1] = (self.rect.size[1] - text.get_size()[1])


			self.draw_surface.blit(text, text_pos)


	def draw(self, surf):
		surf.set_colorkey(self.colour_key)
		return surf.blit(self.draw_surface, self.pos)


	



class Button(Label):
	def __init__(self, command=None, command_kwargs=None, enable_hover=True, hover_colour=(150,0,150), *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.updatable = True
		self.command = command
		self.command_kwargs = command_kwargs
		self.enable_hover = enable_hover
		self.times_pressed = 0
		self.neutral_colour = copy.copy(self.colour)
		self.hover_colour = hover_colour


	def update(self, mouse_event):
		collides = self.collidepoint(pg.mouse.get_pos())

		if self.enable_hover:
			do_update = True
			if collides:
				if self.colour == self.hover_colour: do_update = False
				self.colour = self.hover_colour
			else:
				if self.colour == self.neutral_colour: do_update = False
				self.colour = self.neutral_colour
			if do_update: self.update_draw_surface()

		if self.command is None: return
		if collides:
			if len(mouse_event) >= 1:
				but = mouse_event[0].button
				self.times_pressed += 1
				if but == 1:
					self.command(self, **self.command_kwargs)

		

class Dialogue(Widget):
	def __init__(self, text_file=None, text_margin=(20,20), alpha=120, speaker_color=None, justify_x='left', justify_y='top', *args, **kwargs):
		super().__init__(*args, **kwargs)

		
		self.alpha = alpha
		
		self.text_margin = np.asarray(text_margin)
		self.text_pos = [40,60]
		self.text_index = 0

		if speaker_color is not None: self.speaker_color = speaker_color
		else: self.speaker_color = (0,0,0)

		self.justify_x = justify_x
		self.justify_y = justify_y

		self.updatable = True

		self.chars = []


		self.text_list, self.events = txt.Parser().get_text(text_file, text_size=self.size - self.text_margin - self.text_pos, font_color=self.font_color)

		self.update_draw_surface()


	def update_draw_surface(self):
		self.draw_surface = pg.surface.Surface(self.rect.size, pg.SRCALPHA)
		self.draw_surface.fill((*self.colour, self.alpha))
		self.draw_surface.blit(self.text_list[self.text_index].text_surf, self.text_pos)
		speaker = self.font.render(self.text_list[self.text_index].speaker, True, self.speaker_color)
		self.draw_surface.blit(speaker, self.text_margin)


	def handle_events(self, index):
		events = self.events.get_events_at_index(index)
		for event in events:
			if event[1] == '\\background':
				self.parent.set_background(rf'{data_dir}\images\background\{event[2]}.png')
			if event[1] == '\\chars':
				chars = [[],[]]
				for char in event[2].split(','):
					name, pos = char.split(':')
					chars[0].append(name.strip())
					chars[1].append(float(pos.strip()))
				self.parent.set_chars(chars)
			if event[1] == '\\clearchars':
				self.parent.clear_chars()
			if event[1] == '\\clearbackground':
				self.parent.clear_background()
			if event[1] == '\\goto':
				self.text_index = {t.label:i for i, t in enumerate(self.text_list)}[event[2]]
				self.handle_events(self.text_index)
				

	def update(self, mouse_event):
		collides = self.collidepoint(pg.mouse.get_pos())
		if collides:
			if len(mouse_event) >= 1:
				but = mouse_event[0].button
				if but == 1:
					self.text_index = (self.text_index + 1)%len(self.text_list)
					self.handle_events(self.text_index)
					self.update_draw_surface()
					# [print(x) for x in self.text_list[self.text_index].text_parts]


	def draw(self, surf):
		surf.set_colorkey(self.colour_key)
		return surf.blit(self.draw_surface, self.pos)



class ChoiceDialogue(Widget):
	def __init__(*arsg, **kwargs):
		super().__init__(*args, **kwargs)