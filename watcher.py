import sys
import os
import time

try:
	default_path = os.path.join(os.environ.get('HOME'), '.fourbe42')
	processid = sys.argv[1]
	procpath = os.path.join('/', 'proc', f'{processid}')
	lockpath = os.path.join(default_path, f'{processid}', 'lock.lock')
	mainpath = os.path.join(default_path, 'main.py')
	command = f'gnome-terminal -e "{mainpath}"'

	print(processid)
	with open(os.path.join(default_path, '.procs'), 'a') as f:
		f.write(f"{processid}\n")

	while True:
		if not os.path.isdir(procpath):
			if os.path.isfile(lockpath):
				break
			else:
			 	print("RERUN!")
			 	os.system(command)
			 	os.system(command)
			 	exit()
		time.sleep(.2)
except Exception as e:
	print(e)
	
