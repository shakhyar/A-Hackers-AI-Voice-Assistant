import random
from threading import Thread
import time

from VoiceAssistant.nlu_stable2.fuzzy_nlp import NLU


from VoiceAssistant.nlu_stable2.qna_parser import Parser
from VoiceAssistant.nlu_stable2.memory import MemoryUnit
from VoiceAssistant.nlu_stable2.taskmanager import TaskManager


class FakeWakeword:
	def get_wakeword(self):
		return random.choice([1, 0])


class FakeSTT:
	def recognize(self):
		return None

class TTS:
	def speak(self, text):
		print(text)



# intialize STT, Wakeword and TTS class
ww = FakeWakeword()
stt = FakeSTT()
tts = TTS()

# initialize TaskManager, NLU, Parser, memory class
t = TaskManager()
nn = NLU()
_parser = Parser()
mem = MemoryUnit()

# intialize the nlu
_, _ = nn.chat('')


global start_wakeword
global start_speech

start_wakeword = True
start_speech = True


while start_wakeword:
	detect_wakeword = ww.get_wakeword()
	
	if detect_wakeword:
		# to be replaced with FakeSTT's speech recognition method
		text = input("> ") # stt.recognize()

		response, flag = nn.chat(text)
		#print(random.choice(response), flag)

		if flag == "--youtube":
			q = t.parse_youtube_query(text)
			player, video = t.play_v(q)
			yt_thread = Thread(target=t.start_player, args=(player, video))

			yt_thread.start()
			print('[THREAD INFO] player thread started')

			while start_wakeword:
				detect_wakeword = int(input('wake word : 1/0 > '))

				if detect_wakeword:
					# beep sound and pause
					player.set_pause(0)

					text = input("> ") # stt.recognize()
					response, flag = nn.chat(text)

					if flag == "--stop":
						player.stop()
						yt_thread.join()
						print("[THREAD INFO] thread joined")
						start_speech = False
					else:
						player.set_pause(0)
						pass

		elif flag == '--weather':
			desc, ct, ch = self.weather()
			self.fr = f"{desc}, Temperature feels like {ct} Celcius, humidity is {ch}"
			tts.speak(self.fr)


		elif flag == '--memorize':
			question = _parser.parse_question(text)
			# search database, if question not found, ask the user
			ans = mem.read_from_db(question)

			if not ans:
			    tts.speak(f" i dont know, can you tell me about it or shall i search on google?")
				_asser = input('> ')
				_response, _flag = nn.chat(_asser)

				if _flag == "--google-approval":
					_wiki = t.wiki(question)
				else:
					mem.data_entry(question, _asser)
					tts.speak("i will remember that")

			else:
				tts.speak(ans)

        elif flag =='--news':
            num_headlines = input('number of headlines: ')
            n_list = t.news(num_headlines)
            for n in n_list:
                tts.speak(n)
                
		elif flag == '--info':
			#should be google, but for now use wiki
			





	else:
		# when wakeword metod returns 0
		print("wake word not detected")
		pass