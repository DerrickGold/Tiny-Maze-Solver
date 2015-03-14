#!/usr/local/bin/python3
class Maze:
	def __init__(self, fh): self.map, self.mazePath, self.P, self.V = self._readMaze(fh), list(), ' ', '0'

	#read line of "y x" coordinates, flip and return tuple of (x, y)
	def _getDim(self, fh): return tuple(reversed(tuple((int(i) * 2) - 1 for i in fh.readline().rstrip('\n').split(' '))))

	def _readMaze(self, fh):
        #width and height value
		self.dim, self.start, self.end = tuple(i + 1 for i in self._getDim(fh)), self._getDim(fh), self._getDim(fh)
        #read maze into a list of lists for modification
		return list(list(row.rstrip('\n')) for row in fh.readlines())

	def _solve(self, pos, fin):
        #base cases, first check that we are in the maze and if on a path
		if (pos[0] < 0 or pos[1] < 0 or self.map[self.dim[1] - pos[1]][pos[0]] != self.P \
			or pos[0] >= self.dim[0] or pos[1] >= self.dim[1]): return 0
        #once we hit the finish, the maze is done, we can start backtracking
		elif (pos[0] == fin[0] and pos[1] == fin[1]): self.mazePath.append(pos)
		else:
        	#recursive cases, mark our path and continue
			self.map[self.dim[1] - pos[1]][pos[0]] = self.V
        	#check right, left, up and down positions
			if(self._solve(([pos[0] + 1, pos[1]]), fin) or self._solve(([pos[0] - 1, pos[1]]), fin) \
				or self._solve(([pos[0], pos[1] + 1]), fin) or self._solve(([pos[0], pos[1] - 1]), fin)):
				self.mazePath.append(pos)
			else: return 0
		return 1

    #if the path has been solved, draw it out onto the maze
	def _setSoln(self):
		#clear the maze map of visited areas
		for y in range(self.dim[1]): self.map[y] = list(''.join(self.map[y]).replace(self.V, self.P))
		#then draw out solution on cleared map
		for p in range(len(self.mazePath)):
			if(p % 2 == 0): self.map[self.dim[1] - self.mazePath[p][1]][self.mazePath[p][0]] = self.V

	#neat trick for reducing lines, nest a function call as a parameter!
	def draw(self, n): print('\n'.join(''.join(*zip(*row)) for row in self.map))

	def solve(self): self._setSoln() if (self._solve(self.start, self.end)) else print("No solution found.")

#Program Start
try: maze = Maze(open(input("Please enter a filename: "), 'r'))
except: print("Missing file")
else: maze.draw(maze.solve())
