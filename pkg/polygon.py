import numpy as np 
import pygame as pg
import math


def collidelines(l1, l2):
	#collide x:
	if math.copysign(1, l1[0][0] - l2[0][0]) != math.copysign(1, l1[1][0] - l2[1][0]):
		if math.copysign(1, l1[0][1] - l2[0][1]) != math.copysign(1, l1[1][1] - l2[1][1]):
			return True
	return False


class Polygon:
	def __init__(self, verteces):
		self.verteces = np.asarray(verteces)
		

	@property
	def rect(self):
		minvert = (np.min(self.verteces[:,0]), np.min(self.verteces[:,1]))
		maxvert = (self.verteces[:,0].max(), self.verteces[:,1].max())
		size = maxvert[0] - minvert[0], maxvert[1] - minvert[1]
		return pg.Rect(minvert, (size))
	

	def collidepoint(self, p):
		#create line
		line = p, (p[0] + self.rect.width, p[1])
		cords = []
		for i in range(len(self.verteces)):
			cords.append((self.verteces[i], self.verteces[i-1]))

		total = 0
		for cord in cords:
			total += collidelines(line, cord)

		return total%2 == 1





if __name__ == '__main__':
	l1 = [(0,0), (10,0)]
	l2 = [(5, 5), (5,-5)]
	# print(collidelines(l1,l2))

	v = [[0,2], [100,14], [10, 234]]
	p = Polygon(v)
	print(p.collidepoint((0,3)))

