import numpy as np
import math


# def map_colours(x, colour='RedBlue'):
# 	c = 


class ColourMap:
	def __init__(self, strength=1, cycles=1):
		self.strength = strength
		self.cycles = cycles

	def __getitem__(self, val):
		if type(val) is np.ndarray:
			return self.colour_array(val)

		else:
			cd = self.colours * self.cycles
			t = val*(len(cd)-1)
			i = math.floor(t)
			d = t - i
			if i < len(cd)-1:
				c0 = np.asarray(cd[i])
				c1 = np.asarray(cd[i+1])

				return np.round(c0 + (c1 - c0) * d).astype(int)
			else:
				return cd[i]

	def colour_array(self, val):
		val = (val - val.min())
		val = val/val.max()
		val = val

		p = np.empty(val.shape)
		cd = self.colours * self.cycles

		r, g, b = zip(*cd)
		r, g, b = np.asarray(r)*self.strength, np.asarray(g)*self.strength, np.asarray(b)*self.strength

		l = len(cd)-1

		t = val*l
		i = np.floor(t).astype(int)
		d = t - i

		r = np.round(r[i] + (r[np.minimum(i+1, l)] - r[i]) * d)
		g = np.round(g[i] + (g[np.minimum(i+1, l)] - g[i]) * d)
		b = np.round(b[i] + (b[np.minimum(i+1, l)] - b[i]) * d)

		p = b + g * 256 + r * 256**2
		return p.astype(int)

def get_cmap_names():
	return [o.__name__ for o in ColourMap.__subclasses__()]

def get_cmap_classes():
	return [o for o in ColourMap.__subclasses__()]


class CoolWarm(ColourMap):
	colours = [
	(58, 76, 192),
	(220, 220, 220),
	(79, 3, 38),
	]

class Viridis(ColourMap):
	colours = [
	(69, 6, 90),
	(56, 86, 139),
	(68, 190, 112),
	(243, 229, 30),
	]

class Ocean(ColourMap):
	colours = [
	(0, 124, 2),
	(0, 1, 86),
	(35, 145, 182),
	(255, 255, 255),
	]

class Hot(ColourMap):
	colours = [
	(0, 0, 0),
	(223, 0, 0),
	(255, 172, 0),
	(255,255,255),
	]

class Rainbow(ColourMap):
	colours = [
	(255, 0, 0),
	(255, 255, 0),
	(0, 255, 0),
	(0, 255, 255),
	(0, 0, 255),
	(255, 0, 0),
	]

class test(ColourMap):
	colours = [
	(252, 221, 79),
	(183, 73, 10),
	(15, 3, 65),
	]
