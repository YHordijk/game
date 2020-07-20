import pygame as pg
import numpy as np
# import pkg.menu as menu
import copy
import re, os

pg.init()

#construct color dictionary
color_path = os.getcwd() + r'/data/resources/colors.csv'
color_path = r"D:\Users\Yuman\Desktop\Programmeren\Python\PyGame\game\data\resources\colors.csv"
color_path = r"C:\Users\Yuman Hordijk\Desktop\Scripts\game\data\resources\colors.csv"
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
	def __init__(self, events=[]):
		#events is dictionary with key text index and value event: bkgr change, transition, chars
		self.events = events

	def get_events_at_index(self, index):
		return filter(lambda x: x[0] == index, self.events)

	def add_event(self, event, index):
		self.events.append((index, *event))





class TextPart:
	def __init__(self, text, flags, text_size=(1280,200), font_size=30, default_font='mono', default_text_color=(255,255,255)):
		self.text = text
		self.flags = flags
		self.text_size = text_size
		self.bold = 'bold' in flags
		self.italics = 'italics' in flags
		self.underline = 'underline' in flags

		self.font_size = font_size

		self.color = list(filter(lambda x: 'color' in x, flags))
		if len(self.color) > 0:
			self.color = self.color[0].split('|')[1]
			try:
				self.color = color_dict[self.color.lower()]
			except:
				self.color = self.color.strip('(').strip(')').split(',')
				self.color = [c.strip() for c in self.color]
				self.color = [c for c in self.color if len(c) > 0]
				self.color = int(self.color[0]), int(self.color[1]), int(self.color[2])
		else:
			self.color = default_text_color

		self.font = list(filter(lambda x: 'font' in x, flags))
		if len(self.font) > 0:
			self.font = self.font[0].split('_')[1]
		else:
			self.font = default_font

		self.font = pg.font.Font(pg.font.match_font(default_font), self.font_size)
		self.font.set_italic(self.italics)
		self.font.set_bold(self.bold)
		self.font.set_underline(self.underline)

		print(self)



	def __repr__(self):
		return f'TEXT: {self.text} | FLAGS: {self.flags}'








class Parser:
	


	# @staticmethod
	def get_text(self, files, text_size=(1280,200), default_font='mono', font_size=30, default_text_color=(0,0,0)):
		self.files = files
		self.text_size = text_size
		self.default_font = default_font
		self.default_text_color = default_text_color
		self.font_size = font_size

		# self.special_flags = ['background']

		# raw_text = self.load_files(files)
		text_list = self.parse_text(files[0])
		
		return text_list


	def parse_text(self, file):
		text_flags = ['\\bold', '\\italics', '\\underline', '\\color', '\\font']
		event_flags = ['\\background', '\\clearbackground', '\\chars', '\\clearchars']

		#load text and join all of the lines
		with open(file, 'r') as f:
			lines = f.readlines()
			lines = [l.rstrip() for l in lines]
			raw_text = ' '.join(lines)


		#find the flags
		pattern = r'\\[^. {}]+(?:\{[^}]*\})*'
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
		# [print(i) for i in text_parts_flags]




		
		events = Events()
		for i, p in enumerate(text_parts):
			for flag in text_parts_flags[i]:
				d = re.split(r'{', flag.group())
				d = [x.strip('}') for x in d]
				
				if d[0] == 'newtext':
					speaker = d[1]

				if d[0] in event_flags:
					events.add_event(d, i)

				if d[0] in text_flags:
					if any(map(lambda x: x in text_flags, d[1:])):
						print(d)



		# text_index = 0
		# #handle events first
		# for flag in flags:
		# 	d = re.split(r'{', flag.group())
		# 	d = [x.strip('}').strip('\\') for x in d]

		# 	if d[0] == 'newtext':
		# 		text_index += 1
		# 	if d[0] in event_flags:
		# 		events.add_event(d, text_index)


		# #gather text parts
		# text_list = []
		# for flag in flags:
		# 	d = re.split(r'{', flag.group())
		# 	d = [x.strip('}').strip('\\') for x in d]

		# 	if d[0] == 'newtext':
		# 		text_list.append(Text(speaker=d[1]))
		# 		text_start_index = flag.span()[0]
		# 		text_end_index = get_next_newtext(text_start_index)




		




	# def load_files(self, files):
	# 	text_list = []
	# 	for file in files:
	# 		with open(file, 'r') as f:
	# 			lines = f.readlines()
	# 			lines = [l.rstrip() for l in lines]
	# 			lines = ' '.join(lines)
	# 			text = lines.split(r'\newtext')
	# 			text = [(r'\newtext' + t).strip() for t in text if len(t) > 0]
	# 			text_list.append(text)

	# 	return text


	# def parse_text(self, raw_text):
	# 	events = Events()
	# 	text_list = []
	# 	for i, text in enumerate(raw_text):
	# 		# print(text)
			
	# 		#split on \, { and }
	# 		splits = re.split(r'\\|{|}', text)
	# 		splits = ['\\' + s if s in self.text_flags else s for s in splits]
	# 		splits = [s for s in splits if len(s.strip()) > 0]


	# 		#get speaker
	# 		speaker_index = splits.index(r'\newtext') + 1
	# 		speaker = splits[speaker_index]
	# 		#and remove from splits
	# 		del(splits[speaker_index])
	# 		del(splits[speaker_index - 1])

	# 		text_obj = Text(speaker=speaker, text_size=self.text_size)


	# 		#get flags and text from splits
	# 		flags = []
	# 		skip_indices = []
	# 		for j, s in enumerate(splits):
	# 			if not j in skip_indices:
	# 				if s.startswith('\\'):
	# 					# print(s)
	# 					if s == r'\background':
	# 						events.events.append((i, 'background', splits[j+1]))
	# 						skip_indices.append(j+1)

	# 					elif s == r'\chars':
	# 						chars = splits[j+1]
	# 						pos = splits[j+2]
	# 						events.events.append((i, 'chars', chars, pos))
								
	# 						skip_indices.append(j+1)
	# 						skip_indices.append(j+2)

	# 					elif s in [r'\clearchars', r'\clearbackground']:
	# 						# print(s)
	# 						events.events.append((i, s.strip('\\')))


	# 					else:
	# 						flags.append(s.strip(r'\\'))
	# 						if flags[-1] in ['color', 'font']:
	# 							flags[-1] = flags[-1] + '|' + splits[j+1]
	# 							skip_indices.append(j+1)
	# 				else:
	# 					t = TextPart(s, flags, default_text_color=self.default_text_color, default_font=self.default_font, font_size=self.font_size, text_size=self.text_size)
	# 					text_obj.text_parts.append(t)
	# 					flags = []

	# 		text_list.append(text_obj)

	# 	[t.get_text_surf() for t in text_list]
	# 	return text_list, events






if __name__ == '__main__':
	# t = Parser().get_text([r"D:\Users\Yuman\Desktop\Programmeren\Python\PyGame\game\data\dialogue\test.txt"])
	t = Parser().get_text([r"C:\Users\Yuman Hordijk\Desktop\Scripts\game\data\dialogue\test.txt"])
	# [print(x.text_parts) for x in t]