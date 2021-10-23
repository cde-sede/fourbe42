#! /usr/bin/python3

import os, sys, time, glob, random, signal
import colors

sign = False
tab = []
default_path = os.environ.get('HOME')+'/.fourbe42/frames'
pid = os.getpid()
lockdir = os.path.join(os.environ.get('HOME'), '.fourbe42', f'{pid}')
lock = os.path.join(lockdir, 'lock.lock')

def check_lock():
	if not os.path.isdir(lockdir):
		return
	if not os.path.isfile(lock):
		open(lock, 'a').close()
	with open(lock, 'r') as f:
		data = f.read()
	if data == "exit\n":
		exit()

class Animation():
	def __path__(self, path=default_path):
		self.path=path

	def __name__(self, path=default_path):
		count = 0
		for c in path:
			if c == '/':
				count += 1
		counter = start = index = 0
		for c in self.path:
			if c == '/':
				counter += 1
				if counter == count:
					start = index
			index += 1
		self.name = path[start+1:]

	def __frame__(self, path=default_path):
		line_count = 0
		files = []
		for d in glob.glob(self.path+'/*.txt'):
			# print('['+d+']\n')
			files.append(d)
			file = open (d, 'r')
			for line in file:
				line_count += 1
			if self.heigth == None:
				self.heigth = line_count
		files.sort()
		for f in files:
			with open(f, 'r', encoding='utf-8') as f:
				self.frames.append(f.readlines())
				self.FrameNumber+=1 
					 

	def init(self, path=default_path):
		self.frames = []
		self.FrameNumber = 0
		self.heigth = None
		self.name = None
		self.path = None
		self.__path__(path)
		self.__name__(self.path)
		self.__frame__(self.path)

	def execute(self):
		global sign
		sign = False
		colors.getnoise(38, 85)
		noise = colors.noise
		newframes = []
		
		for frame in self.frames:
			newframes.append([])
			for x, line in enumerate(frame):
				for y, char in enumerate(line):
					newframes[-1].append(colors.get(noise.grid[x][y])(char))
		while sign == False:
			check_lock()
			for frame in newframes:
				print("".join(frame))
				time.sleep(0.15)
				os.system("clear")

def catch_signal(signal, contexte):
	global sign
	sign = True
	tab[random.randint(0,len(tab)-1)].execute()

def main():

	os.system(f'gnome-terminal -e "python3 watcher.py {pid}"')

	bdir = os.environ.get('HOME')+'/.fourbe42'
	for d in list(os.walk(bdir)):
		if d[0][len(bdir)+1:len(bdir)+2] != '.' and d[0][len(bdir)+1:len(bdir)+2] != '':
			print(d[0])
			a = Animation()
			a.init(d[0])
			tab.append(a)

	signal.signal(signal.SIGQUIT, catch_signal)
	signal.signal(signal.SIGINT, catch_signal)
	tab[random.randint(0, len(tab)-1)].execute()

if __name__ == '__main__':
	main()
