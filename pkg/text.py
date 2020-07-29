import pygame as pg
import numpy as np
# import pkg.menu as menu
import copy
import re, os

pg.init()

#construct color dictionary
color_path = os.getcwd() + r'/data/resources/colors.csv'
# color_path = r"D:\Users\Yuman\Desktop\Programmeren\Python\PyGame\game\data\resources\colors.csv"
# color_path = r"C:\Users\Yuman Hordijk\Desktop\Scripts\game\data\resources\colors.csv"
color_dict = {}
with open(color_path, 'r') as f:
	for color in f.readlines():
		color = color.rstrip()
		splits = color.split(';')
		color_dict[splits[0].lower()] = (int(splits[1]), int(splits[2]), int(splits[3]))


class Text:
	def __init__(self, speaker='', label=None, text_parts=None, text_size=(1280,200)):
		self.speaker = speaker
		self.label = label
		self.text_parts = [] if text_parts is None else text_parts
		self.text_size = text_size

		# self.get_text_surf()



	def get_text_surf(self):
		text_surf = pg.Surface(self.text_size)
		text_surf.fill((255,255,254))
		text_surf.set_colorkey((255,255,254))

		x = 0
		y = 0
		for part in self.text_parts:
			for word in part.text.split():
				word = word + ' '
				word_width, word_height = part.font.size(word)

				if x + word_width > self.text_size[0]:
					x = 0
					y += word_height

				text_surf.blit(part.font.render(word, True, part.color), (x,y))
				x += word_width

		self.text_surf = text_surf

	def add_part(self, part):
		self.text_parts.append(part)
		


class TextPart:
	def __init__(self, text, flags, text_size=(1280,200), font_size=30, default_font='mono', font_color=(0,0,0)):
		self.text = text
		self.flags = flags
		self.text_size = text_size
		self.font_color = font_color
		self.font_size = font_size
		self.parse_flags(flags)

		self.font = list(filter(lambda x: 'font' in x, flags))
		if len(self.font) > 0:
			self.font = self.font[0].split('_')[1]
		else:
			self.font = default_font

		self.font = pg.font.Font(pg.font.match_font(default_font), self.font_size)
		self.font.set_italic(self.italics)
		self.font.set_bold(self.bold)
		self.font.set_underline(self.underline)

		# print(self)

	def parse_flags(self, flags):
		color_flag = ''
		self.color = self.get_color(flags)
		if 'c' in flags:
			color_flag = re.search(r'c\([^()]*\)', flags).group()

		non_color_flags = flags.replace(color_flag, '')
		self.bold = 'b' in non_color_flags
		self.italics = 'i' in non_color_flags
		self.underline = 'u' in non_color_flags
		


	def get_color(self, flags):
		if 'c' in flags:
			# print(flags)
			# pass
			c = flags.split('(')[1].split(')')[0]
			try:
				c = color_dict[c]
			except:
				c = c.split(',')
				c = [x.strip() for x in c]
				c = [x for x in c if len(x) > 0]
				c = int(c[0]), int(c[1]), int(c[2])

		else:
			c = self.font_color
		return c


	def __repr__(self):
		return f'TEXT: {self.text} | FLAGS: {self.flags}'








class Parser:
	def get_text(self, parent, file, text_size=(1280,200), default_font='mono', font_size=30, font_color=(0,0,0)):
		self.file = file
		self.text_size = text_size
		self.default_font = default_font
		self.font_color = font_color
		self.font_size = font_size
		self.parent = parent

		text_list = self.parse_text(file)
		
		return text_list


	def parse_text(self, file):
		text_flags = ['\\s']
		event_flags = ['\\background', '\\clearbackground', '\\chars', '\\clearchars', '\\goto', '\\choice', '\\set', '\\input']

		#load text and join all of the lines
		with open(file, 'r') as f:
			lines = f.readlines()
			lines = [l.rstrip() for l in lines]
			raw_text = ' '.join(lines)


		#replace text flags:
		text_placeholders = {
			'they': self.parent.game.player.they,
			'them': self.parent.game.player.them,
			'their': self.parent.game.player.their,
			'honor': self.parent.game.player.honor,
			'nonmarital': self.parent.game.player.nonmarital,
		}

		pattern = r'(?<!\\)\$[^$]*(?<!\\)\$'
		for p in list(re.finditer(pattern, raw_text)):
			p = p.group()
			if p.strip('$') in text_placeholders.keys():
				new_string = text_placeholders[p.strip('$')]
			else:
				new_string = eval('self.parent.' + p.strip('$'))

			raw_text = raw_text.replace(p, str(new_string)) 

		raw_text = raw_text.replace('\\$', '$')



		#find the flags
		pattern = r'(?<!\\)\\{1}(?!\\)[^.$ {}]+(?:\{[^}]*\})*'
		flags = list(re.finditer(pattern, raw_text))


		def get_next_newtext(pos):
			for flag in filter(lambda x: x.group().startswith(r'\newtext'), flags):
				if pos < flag.span()[0]: return flag.span()[0]
			return len(raw_text)



		#find first newtext flags:
		newtext_instances = list(re.finditer(r'\\newtext', raw_text))
		newtext_indices = [x.span()[0] for x in newtext_instances]

		#cut text into parts
		text_parts = []
		for i in newtext_indices:
			text_parts.append(raw_text[i:get_next_newtext(i)])

		text_parts_flags = []
		for p in text_parts:
			text_parts_flags.append(list(re.finditer(pattern, p)))

		
		events = []
		text_obj_list = []
		for i, p in enumerate(text_parts):
			text_obj = Text(text_size=self.text_size)
			flag_spans = [flag.span() for flag in text_parts_flags[i]]
			non_flag_spans = []
			x = 0
			for j, s in enumerate(flag_spans):
				if x < s[0]:
					non_flag_spans.append((x,s[0]))
					x = s[1] + 1
				else:
					x = s[1] + 1

				if s[1] < len(p) and j == len(flag_spans)-1:
					non_flag_spans.append((x,len(p)))

			
			combined_spans = list(sorted(flag_spans + non_flag_spans, key=lambda x: x[0]))
			for span in combined_spans:
				is_flag = span in flag_spans
				if is_flag:
					d = re.split(r'{', p[span[0]:span[1]])
					d = [x.strip('}') for x in d]

					if d[0] in event_flags:
						if d[0] == '\\goto':
							events.append((i+1, *d))
							# events.add_event(d, min(i+1, len(text_parts)-1))
							print(min(i+1, len(text_parts)))
						else:
							events.append((i, *d))
							# events.add_event(d, i)


					elif d[0].startswith('\\newtext'):
							try:
								text_obj.label = d[0].split('[')[1].strip(']')
							except:
								text_obj.label = None
							text_obj.speaker = d[1]

					else:
						if d[0].startswith('\\s'):
							raw_flags = d[0].split('[')[1].strip(']')
							text_obj.add_part(TextPart(d[1], raw_flags))

				if not is_flag:
					text_obj.add_part(TextPart(p[span[0]:span[1]].replace(r'\\', '\\'), ''))



			text_obj.get_text_surf()
			text_obj_list.append(text_obj)
			
			# print(text_obj.text_parts)

		return text_obj_list, events


if __name__ == '__main__':
	t = Parser().get_text(r"D:\Users\Yuman\Desktop\Programmeren\Python\PyGame\game\data\dialogue\test.txt")
	# t = Parser().get_text([r"C:\Users\Yuman Hordijk\Desktop\Scripts\game\data\dialogue\test.txt"])
	# [print(x.text_parts) for x in t]