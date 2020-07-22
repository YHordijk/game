


class GameState:
	def __init__(self):
		self.player = Character(gender='female')
		self.happy_boy = Character(gender='male')




class Character:
	def __init__(self, gender='male'):
		self.gender = gender
		self.hearts = 0

	@property
	def they(self):
		if self.gender == 'male':
			return 'he'
		elif self.gender == 'female':
			return 'she'
		else: return 'they'

	@property
	def them(self):
		if self.gender == 'male':
			return 'him'
		elif self.gender == 'female':
			return 'her'
		else: return 'them' 

	@property
	def their(self):
		if self.gender == 'male':
			return 'his'
		elif self.gender == 'female':
			return 'her'
		else: return 'their'

	@property
	def honor(self):
		if self.gender == 'male':
			return 'sir'
		elif self.gender == 'female':
			return 'madam'
		else: return 'uuuuh'

	@property
	def nonmarital(self):
		if self.gender == 'male':
			return 'mister'
		elif self.gender == 'female':
			return 'misses'
		else: return 'uuuuh'


	
