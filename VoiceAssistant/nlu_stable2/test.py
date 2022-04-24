
from taskmanager import TaskManager

t = TaskManager()

print(t.weather())




"""
# youtube multi thread test

from threading import Thread
import time

t = TaskManager()

#print(t.news("tell me two news")) worksssss

url = "https://www.youtube.com/watch?v=8d0f9G7lmzg"
global stop_thread
global r
r = True
player, video = t.play_v(url)
stop_thread = False

def v():
	print(video.length)
	player.play()
	print("started playing from function")
	time.sleep(7)
	while True:
		if player.is_playing():
			print("is_playing==True")
			time.sleep(1)
		else:
			player.stop()
			break
	print("function ended")

t1 = Thread(target=v)
t1.start()
print("thread started")

while r:
	# pretending to be main speech recognition loop
	x = input("y/n ")
	if x == "y":
		player.stop()
		t1.join()

		print("thread joined")
"""
#TOOD: make the play function auto sleep, and perform event loop
#TODO: run the function daemon in a different thread, and kill the thread if requested

