import pygame as pg
import numpy as np
# import pkg.menu as menu
import copy
import re, os

pg.init()

#construct color dictionary
color_path = os.getcwd() + r'/data/resources/colors.csv'
color_path = r"D:\Users\Yuman\Desktop\Programmeren\Python\PyGame\game\data\resources\colors.csv"
color_dict = {}
with open(color_path, 'r') as f:
	for color in f.readlines():
		color = color.rstrip()
		splits = color.split(';')
		color_dict[splits[0].lower()] = (int(splits[1]), int(splits[2]), int(splits[3]))


class Text:
	def __init__(self, speaker='', text_parts=None, text_size=(1280,200)):
		self.speaker = speaker
		self.text_parts = [] if text_parts is None else text_parts
		self.text_size = text_size

		self.get_text_surf()



	def get_text_surf(self):
		text_surf = pg.Surface(self.text_size)
		text_surf.fill((255, 12, 90))
		text_surf.set_colorkey((255, 12, 90))

		x = 0
		y = 0
		for part in self.text_parts:
			for word in part.text.split():
				word = word + ' '
				word_width, word_height = part.font.size(word)

				if x + word_width > self.text_size[0]:
					x = 0
					y += word_height

				text_surf.blit(part.font.render(word, False, part.color), (x,y))
				x += word_width

		self.text_surf = text_surf


class Events:
	def __init__(self, events):
		#events is dictionary with key text index and value event: bkgr change, transition, chars
		self.events = events





class TextPart:
	def __init__(self, text, flags, text_size=(1280,200), font_size=30, default_font='mono', default_color=(255,255,255)):
		self.text = text
		self.flags = flags
		self.text_size = text_size
		self.bold = 'bold' in flags
		self.italics = 'italics' in flags
		self.underline = 'underline' in flags

		self.font_size = font_size

		self.color = list(filter(lambda x: 'color' in x, flags))
		if len(self.color) > 0:
			self.color = self.color[0].split('_')[1]
			try:
				self.color = color_dict[self.color]
			except:
				self.color = self.color.strip('(').strip(')').split(',')
				self.color = [c.strip() for c in self.color]
				self.color = [c for c in self.color if len(c) > 0]
				self.color = int(self.color[0]), int(self.color[1]), int(self.color[2])
		else:
			self.color = default_color

		self.font = list(filter(lambda x: 'font' in x, flags))
		if len(self.font) > 0:
			self.font = self.font[0].split('_')[1]
		else:
			self.font = default_font

		self.font = pg.font.Font(pg.font.match_font(default_font), self.font_size)
		self.font.set_italic(self.italics)
		self.font.set_bold(self.bold)
		self.font.set_underline(self.underline)



	def __repr__(self):
		return f'TEXT: {self.text} | FLAGS: {self.flags}'








class Parser:
	# @staticmethod
	def get_text(self, files, text_size=(1280,200), default_font='mono', font_size=30):
		self.files = files
		self.text_size = text_size
		self.default_font = default_font
		self.font_size = font_size

		self.allowed_flags = ['newtext', 'bold', 'italics', 'underline', 'color', 'font']

		raw_text = self.load_files(files)
		text_list = self.parse_text(raw_text)
		
		return text_list


	def load_files(self, files):
		text_list = []
		for file in files:
			with open(file, 'r') as f:
				lines = f.readlines()
				lines = [l.rstrip() for l in lines]
				lines = ' '.join(lines)
				text = lines.split(r'\newtext')
				text = [(r'\newtext' + t).strip() for t in text if len(t) > 0]
				text_list.append(text)

		return text


	def parse_text(self, raw_text):
		text_list = []
		for i, text in enumerate(raw_text):
			# print(text)
			
			#split on \, { and }
			splits = re.split(r'\\|{|}', text)
			splits = ['\\' + s if s in self.allowed_flags else s for s in splits]
			splits = [s for s in splits if len(s.strip()) > 0]


			#get speaker
			speaker_index = splits.index(r'\newtext') + 1
			speaker = splits[speaker_index]
			#and remove from splits
			del(splits[speaker_index])
			del(splits[speaker_index - 1])

			text_obj = Text(speaker=speaker, text_size=self.text_size)


			#get flags and text from splits
			flags = []
			skip_indices = []
			for i, s in enumerate(splits):
				if not i in skip_indices:
					if s.startswith('\\'):
						flags.append(s.strip(r'\\'))
						if flags[-1] in ['color', 'font']:
							flags[-1] = flags[-1] + '_' + splits[i+1]
							skip_indices.append(i+1)

					else:
						t = TextPart(s, flags, default_font=self.default_font, font_size=self.font_size, text_size=self.text_size)
						text_obj.text_parts.append(t)
						flags = []

			text_list.append(text_obj)

		[t.get_text_surf() for t in text_list]
		return text_list






if __name__ == '__main__':
	t = Parser().get_text([r"D:\Users\Yuman\Desktop\Programmeren\Python\PyGame\game\data\dialogue\test.txt"])
	[print(x.text_parts) for x in t]