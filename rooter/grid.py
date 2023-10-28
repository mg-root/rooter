from rooter import rooter

class Grid:
	def __init__(self, size: str, frame_size: int):
		self.__x,self.__y = map(int, size.split('x'))
		self.__frame_size = frame_size
		self.__frames = [[' ' * self.__frame_size for _ in range(self.__x)] for _ in range(self.__y)]

	def generate(self):
		top = '┏' + ('━' * self.__frame_size + '┳') * (self.__x-1) + '━' * self.__frame_size + '┓'
		bottom = '┗' + ('━' * self.__frame_size + '┻') * (self.__x-1) + '━' * self.__frame_size + '┛'

		lines = []
		for y in range(self.__y):
			line = '┃'
			for x in range(self.__x):
				line += self.__frames[y][x] + '┃'
			lines.append(line)

			if y != self.__y-1:
				lines.append('┣' + ('━' * self.__frame_size + '╋') * (self.__x-1) + '━' * self.__frame_size + '┫')

		return '\n'.join([top] + lines + [bottom])
	
	def set(self, y: int, x: int, value, color=None):
		color = rooter.getColor(color)
		if y < self.__y:
			if x < self.__x:
				self.__frames[y][x] = color + value + ' ' * (self.__frame_size - len(value)) + rooter.reset
			else:
				raise IndexError('<x> is out of frame.')
		else:
			raise IndexError('<y> is out of frame.')
		
	def setPoints(self, y: list, x: list, value):
		for i in range(len(y)):
			if y[i] < self.__y:
				if x[i] < self.__x:
					self.__frames[y[i]][x[i]] = value
				else:
					raise IndexError('<x> is out of frame.')
			else:
				raise IndexError('<y> is out of frame.')

	def setLines(self, y: list, value):
		for y in y:
			if y < self.__y:
				for x in range(self.__x):
					self.set(y, x, value)
			else:
				raise IndexError('<y> is out of range.')
		
	def setColumns(self, x: list, value):
		for x in x:
			if x < self.__x:
				for y in range(self.__y):
					self.set(y, x, value)
			else:
				raise IndexError('<x> is out of range.')

	def show(self):
		print(self.generate())