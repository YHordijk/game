


class GameState:
	def __init__(self):
		self.player = Character(gender='female', name='Cutie')
		self.happy_boy = Character(gender='male', name='Happy Boy')




class Character:
	def __init__(self, gender='male', hearts=0, name=''):
		self.gender = gender
		self.hearts = hearts
		self.name = name

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
			return 'miss'
		else: return 'uuuuh'


	
