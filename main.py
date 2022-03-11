import json
import os.path
import time
import datetime
import pyaudio
from vosk import Model, KaldiRecognizer
import pyttsx3
from func_command import Caterpillars, Manipulator, Camera, Date
from Interface import Print
import sys

class VoiceAssistant:
	name = ""
	sex = ""
	speech_language = ""
	recognition_language = ""

def setup_assistant_voices():
	voices = ttsEngine.getProperty("voices")

	if assistant.speech_language == "en":
		assistant.recognition_language = "en-US"
		if assistant.sex == "female":
			ttsEngine.setProperty("voice", voices[1].id)
		else:
			ttsEngine.setProperty("voice", voices[2].id)
	else:
		assistant.recognition_language = "ru-RU"
		#ttsEngine.setProperty("voice", voices[56].id)

def play_voice_assistant_speech(text_to_speech):
	ttsEngine.say(text_to_speech)
	ttsEngine.runAndWait()

model = Model("osk-model-small-ru-0.4")
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data)>0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']
if __name__ == "__main__":
	ttsEngine = pyttsx3.init()

	assistant = VoiceAssistant()
	assistant.name = "Jarvis"
	assistant.sex = "male"
	assistant.speech_language = "ru"

	setup_assistant_voices()


	Log = open('Log.txt', 'a')
	a = os.path.getsize('Log.txt')
	if a > 10485760: # a>1 Mbyte
		Log.close()
		os.rename('Log.txt', 'Log_old.txt')
		Log = open('Log.txt', 'w+')
	#print(a)

	hello = " Приветствую вас!"
	working = " Работаем!"
	# window()
	Print(hello)
	Print(working)


	print(hello)
	print(working)
	play_voice_assistant_speech(hello)
	Log.writelines(datetime.datetime.today().strftime("%Y.%m.%d-%H:%M:%S") + hello+'\n')
	play_voice_assistant_speech(working)
	Log.writelines(datetime.datetime.today().strftime("%Y.%m.%d-%H:%M:%S") + working+'\n')


	for text in listen():

		print(datetime.datetime.today().strftime("%Y.%m.%d-%H:%M:%S") + ' ' + text)
		Log.writelines(datetime.datetime.today().strftime("%Y.%m.%d-%H:%M:%S") + ' ' + text + '\n')
		if "амур триста семь" in text:
			Print(datetime.datetime.today().strftime("%Y.%m.%d-%H:%M:%S") +' '+  text)
			if "привет" in text:

				print(datetime.datetime.today().strftime("%Y.%m.%d-%H:%M:%S") + " АМУР: приветствую вас, сэр!")
				Print(datetime.datetime.today().strftime("%Y.%m.%d-%H:%M:%S") + " АМУР: приветствую вас, сэр!")
				play_voice_assistant_speech("приветствую вас, сэр!")
				Log.writelines(datetime.datetime.today().strftime("%Y.%m.%d-%H:%M:%S") + ' АМУР:  приветствую вас, сэр!\n')

			elif "состояние" in text:

				print(datetime.datetime.today().strftime("%Y.%m.%d-%H:%M:%S") + " АМУР: я нахожусь в стадии разработки")
				Print(datetime.datetime.today().strftime("%Y.%m.%d-%H:%M:%S") + " АМУР: я нахожусь в стадии разработки")
				play_voice_assistant_speech("я нахожусь в стадии разработки")
				Log.writelines(datetime.datetime.today().strftime("%Y.%m.%d-%H:%M:%S") + ' АМУР: я нахожусь в стадии разработки\n')
			elif "отбой" in text:

				print(datetime.datetime.today().strftime("%Y.%m.%d-%H:%M:%S") + " АМУР: всего доброго сэр!")
				Print(datetime.datetime.today().strftime("%Y.%m.%d-%H:%M:%S") + " АМУР: всего доброго сэр!")
				play_voice_assistant_speech("всего доброго сэр!")
				Log.writelines(datetime.datetime.today().strftime("%Y.%m.%d-%H:%M:%S") + ' АМУР: всего доброго сэр!\n')
				Log.close()
				sys.exit()