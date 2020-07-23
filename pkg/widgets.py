import pygame as pg
import numpy as np
import copy, os
import pkg.polygon as pol
import pkg.text as txt


data_dir = os.path.join(os.getcwd(), 'data\\')


class Widget:
	def __init__(self, parent=None, pos=None, polygon=None, size=None, colour=None, img=None, font=None, font_size=None, font_color=(0,0,0), alpha=255, justify_x='left', justify_y='top'):
		self.parent = parent
		self.pos = np.asarray(pos)
		self.alpha = alpha
		self.original_pos = copy.copy(self.pos)
		self.size = size
		self.colour = colour
		self.colour_key = (255,255,254)
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

		self.justify_x = justify_x
		self.justify_y = justify_y


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
		self.draw_surface = pg.surface.Surface(self.rect.size, pg.SRCALPHA)
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


	def update(self, mouse_event, key_event):
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
	def __init__(self, text_file=None, text_margin=(20,20), speaker_color=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.text_file = text_file
		self.text_margin = np.asarray(text_margin)
		self.text_pos = [40,60]
		self.text_index = 0

		if speaker_color is not None: self.speaker_color = speaker_color
		else: self.speaker_color = (0,0,0)

		self.updatable = True

		self.chars = []

		self.events = []
		self.text_list = []
		self.get_text_events()


	def get_events_at_index(self, index):
		return filter(lambda x: x[0] == index, self.events)


	def get_text_events(self):
		self.text_list.clear()
		self.events.clear()
		self.text_list, self.events = txt.Parser().get_text(self.parent, self.text_file, text_size=self.size - self.text_margin - self.text_pos, font_color=self.font_color)

		self.update_draw_surface()


	def update_draw_surface(self):
		self.draw_surface = pg.surface.Surface(self.rect.size, pg.SRCALPHA)
		self.draw_surface.fill((*self.colour, self.alpha))
		self.draw_surface.blit(self.text_list[self.text_index].text_surf, self.text_pos)
		speaker = self.font.render(self.text_list[self.text_index].speaker, True, self.speaker_color)
		self.draw_surface.blit(speaker, self.text_margin)


	def goto(self, label):
		self.text_index = {t.label:i for i, t in enumerate(self.text_list)}[label]
		self.handle_events(self.text_index)
		self.update_draw_surface()


	def handle_events(self, index):
		events = self.get_events_at_index(index)
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
				self.goto(event[2])
			if event[1] == '\\choice':
				choices = []
				actions = []
				for c in event[2].split(','):
					d = c.split(':')
					choices.append(d[0].strip())
					actions.append(d[1].strip())

				self.parent.set_choices(choices, actions)
			if event[1] == '\\set':
				exec('self.parent.' + event[2])
				self.get_text_events()
			if event[1] == '\\input':
				ds = event[2].split(',')
				ds = [x.strip() for x in ds]
				var = 'self.parent.' + ds[0]

				default_input = ''
				char_limit = 0
				for d in ds:
					d = d.split('=')
					if d[0].strip() == 'default':
						default_input = d[1].strip()
					elif d[0].strip() == 'limit':
						char_limit = int(d[1].strip())


				self.parent.set_input(var, default_input, char_limit)

				

	def update(self, mouse_event, key_event):
		collides = self.collidepoint(pg.mouse.get_pos())
		if collides:
			if len(mouse_event) >= 1:
				but = mouse_event[0].button
				if but == 1:
					self.text_index = (self.text_index + 1)%len(self.text_list)
					self.handle_events(self.text_index)
					self.update_draw_surface()


	def draw(self, surf):
		surf.set_colorkey(self.colour_key)
		return surf.blit(self.draw_surface, self.pos)



class ChoiceDialogue(Widget):
	def __init__(self, choices=[], actions=[], choice_spacing=10, choice_margin=30, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.choices = choices
		self.actions = actions

		self.choice_spacing = choice_spacing
		self.choice_margin = choice_margin

		self.choice_alpha = [self.alpha for _ in range(len(self.choices))]

		self.updatable = True

		self.parent.dialogue.updatable = False

		# self.choice_rects = self.get_choice_rects()

		self.update_draw_surface()


	def update_draw_surface(self):
		draw_surface = pg.surface.Surface(self.rect.size, pg.SRCALPHA)
		# draw_surface.fill((*self.colour, self.alpha))
		

		text_height = self.font.get_height()

		y = 0
		for i, choice in enumerate(self.choices):
			rect = self.choice_rects[i]
			choice_surf = pg.surface.Surface(rect.size, pg.SRCALPHA)
			choice_surf.fill((*self.colour, self.choice_alpha[i]))
			text = self.font.render(choice, True, self.font_color)

			text_pos = [0,0]
			if self.justify_x == 'left':
				text_pos[0] = 0
			if self.justify_x == 'center':
				text_pos[0] = (rect.size[0] - text.get_size()[0])//2
			if self.justify_x == 'right':
				text_pos[0] = (rect.size[0] - text.get_size()[0])

			if self.justify_y == 'top':
				text_pos[1] = 0
			if self.justify_y == 'center':
				text_pos[1] = (rect.size[1] - text.get_size()[1])//2
			if self.justify_y == 'bottom':
				text_pos[1] = (rect.size[1] - text.get_size()[1])

			choice_surf.blit(text, text_pos)
			draw_surface.blit(choice_surf, (0,y))

			y += self.font.get_height() + self.choice_spacing


		self.draw_surface = draw_surface

	@property
	def choice_rects(self):
		rects = []
		p = self.pos
		y = 0
		for i in range(len(self.choices)):
			rects.append(pg.Rect(p[0], p[1]+y, self.size[0], self.font.get_height() + self.choice_margin))
			y += self.font.get_height() + self.choice_spacing

		return rects


	def update(self, mouse_event, key_event):
		mouse_pos = pg.mouse.get_pos()
		for i in range(len(self.choices)):
			collides = self.choice_rects[i].collidepoint(mouse_pos)
			if collides:
				self.choice_alpha[i] = min(255, 2*self.alpha)
				if len(mouse_event) >= 1:
					but = mouse_event[0].button
					if but == 1:
						self.handle_choice_action(self.actions[i])
						self.parent.clear_choices()
						self.parent.dialogue.updatable = True
						self.parent.dialogue.text_index = (self.parent.dialogue.text_index + 1)%len(self.parent.dialogue.text_list)
						self.parent.dialogue.handle_events(self.parent.dialogue.text_index)
						self.parent.dialogue.update_draw_surface()
			else:
				self.choice_alpha[i] = self.alpha

			self.update_draw_surface()


	def handle_choice_action(self, actions):
		actions = actions.split(')')
		actions = [a + ')' for a in actions if len(a) > 0]
		for action in actions:
			if action.startswith('set'):
				a = action.strip('set(').strip(')')
				exec('self.parent.' + a)
				self.parent.dialogue.get_text_events()

			elif action.startswith('goto'):
				a = action.strip('goto(').strip(')').strip()
				self.parent.dialogue.goto(a)
				self.parent.dialogue.text_index -= 1



	def draw(self, surf):
		surf.set_colorkey(self.colour_key)
		return surf.blit(self.draw_surface, self.pos)




class Input(Widget):
	def __init__(self, var='', default_input='', char_limit=0, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.var = var
		self.updatable = True
		self.char_limit = char_limit
		self.parent.dialogue.updatable = False
		self.input = ''
		self.default_input = default_input
		self.update_draw_surface()


	def update(self, mouse_event, key_event):
		if len(key_event) > 0:
			keys = [e.key for e in key_event]

			capslock = bool(pg.key.get_mods() & pg.KMOD_CAPS)
			shift = bool(pg.key.get_mods() & pg.KMOD_SHIFT)
			capitalize = capslock != shift
			forbidden_keys = (13,8,304,303,301)

			for key in keys:
				#enter key 13
				#backspace 8
				#shift 304 and 303
				#capslock: capslock = pg.key.get_mods() & pg.KMOD_CAPS
				if key == 13:
					if len(self.input.strip()) == 0:
						self.input = self.default_input
					exec(f'{self.var} = "{self.input}"')
					self.parent.clear_input()
					self.parent.dialogue.updatable = True
					self.parent.dialogue.text_index = (self.parent.dialogue.text_index + 1)%len(self.parent.dialogue.text_list)
					self.parent.dialogue.handle_events(self.parent.dialogue.text_index)
					self.parent.dialogue.get_text_events()
					return
				elif key == 8:
					self.input = self.input[:-1]
				if not self.char_limit == 0 and len(self.input) < self.char_limit:
					if chr(key).isalpha() and not key in forbidden_keys:
						self.input = self.input + (chr(key), chr(key).upper())[capitalize]

			self.update_draw_surface()


	def draw(self, surf):
		surf.set_colorkey(self.colour_key)
		return surf.blit(self.draw_surface, self.pos)

	def update_draw_surface(self):
		draw_surface = pg.surface.Surface(self.rect.size, pg.SRCALPHA)
		draw_surface.fill((*self.colour, self.alpha))

		text = self.font.render(self.input, True, self.font_color)
		text_pos = [0,0]
		rect = self.rect

		if self.justify_x == 'left':
			text_pos[0] = 0
		elif self.justify_x == 'center':
			text_pos[0] = (rect.size[0] - text.get_size()[0])//2
		elif self.justify_x == 'right':
			text_pos[0] = (rect.size[0] - text.get_size()[0])

		if self.justify_y == 'top':
			text_pos[1] = 0
		elif self.justify_y == 'center':
			text_pos[1] = (rect.size[1] - text.get_size()[1])//2
		elif self.justify_y == 'bottom':
			text_pos[1] = (rect.size[1] - text.get_size()[1])

		draw_surface.blit(text, text_pos)

		self.draw_surface = draw_surface