from random import randint, random

class Noise:
	@staticmethod
	def dist(x1, y1, x2, y2):
		return ((x1 - x2)**2 + (y1 - y2)**2)**.5

	def maxdist(self, width, height):
		m = []
		for x in range(width):
			for y in range(height):
				m.append(max([Noise.dist(*point, x, y) for point in self.points]))
		return max(m)
	def closest(self, x, y):
		return min([Noise.dist(*point, x, y) for point in self.points])

	def __init__(self, width, height):
		self.points = [[randint((width//3) * x, (width//3) * (x + 1) - 1), randint((height//3) * y, (height//3) * (y + 1) - 1)] for y in range(0, 3) for x in range(0, 3) if random() > .8]
		self.points.append([randint(0, width-1), randint(0, height - 1)])
		diagmax = self.maxdist(width, height)
		self.grid = [[int(self.closest(x, y) / diagmax  * 7) for y in range(height)] for x in range(width)]

class _color:
	def __init__(self, color):
		self.color = color

		print(self.color)
	def __call__(self, text):
		return f"{self.color}{text}{Colors.C_RESET}"

class Colors:
	C_RESET   = "\u001b[31m"
	#C_BLACK   = "\u001b[30m"
	C_RED     = "\u001b[31m"
	C_GREEN   = "\u001b[32m"
	C_YELLOW  = "\u001b[33m"
	C_BLUE    = "\u001b[34m"
	C_MAGENTA = "\u001b[35m"
	C_CYAN    = "\u001b[36m"
	C_WHITE   = "\u001b[3m"

	def __init__(self):
		self.index = 0
		self.colors = [c for c in dir(Colors) if c[:2] == "C_"]
		self.l = len(self.colors)

	def getnoise(self, *args, **kwargs):
		self.noise = Noise(*args, **kwargs)
		
	def get(self, n):
		return _color(getattr(self, self.colors[n]))

	def __getattr__(self, attr):
		return _color(getattr(Colors, f"C_{attr.upper()}"))

	def __iter__(self):
		return self

	def __next__(self):
		self.index += 1
		return _color(getattr(self, f"{self.colors[randint(0, self.l-1)]}"))
	
if __name__ != "__main__":
	from sys import modules
	modules['colors'] = Colors()
