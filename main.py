from contextlib import nullcontext
import json
import os.path
import time
import datetime
import pyaudio
from sympy import true
from vosk import Model, KaldiRecognizer
import pyttsx3
from func_command import Caterpillars, Manipulator, Camera, Date
from Interface import AmurGUI
import sys
import threading


class VoiceAssistant:
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""

    # private
    __ttsEngine = nullcontext
    __rec = nullcontext
    __stream = nullcontext

    # setup_assistant_voices
    def __init__(self):
        model = Model("osk-model-small-ru-0.4")
        self.__rec = KaldiRecognizer(model, 16000)
        p = pyaudio.PyAudio()
        self.__stream = p.open(format=pyaudio.paInt16, channels=1,
                        rate=16000, input=True, frames_per_buffer=8000)
        self.__stream.start_stream()

        self.__ttsEngine = pyttsx3.init()
        voices = self.__ttsEngine.getProperty("voices")

        if self.speech_language == "en":
            self.recognition_language = "en-US"
            if self.sex == "female":
                self.__ttsEngine.setProperty("voice", voices[1].id)
            else:
                self.__ttsEngine.setProperty("voice", voices[2].id)
        else:
            self.recognition_language = "ru-RU"
            # ttsEngine.setProperty("voice", voices[56].id)

    def play_speech(self, text_to_speech):
        self.__ttsEngine.say(text_to_speech)
        self.__ttsEngine.runAndWait()


    def listen(self):
        while True:
            data = self.__stream.read(4000, exception_on_overflow=False)
            if (self.__rec.AcceptWaveform(data)) and (len(data) > 0):
                answer = json.loads(self.__rec.Result())
                if answer['text']:
                    yield answer['text']


data_text = "%Y.%m.%d-%H:%M:%S"


def log_text(text):
    str = datetime.datetime.today().strftime(data_text) + ' ' + text
    print(str)
    Log.writelines(str + '\n')


def listen_handler():
    for text in assistant.listen():
        log_text(text)
        if "амур триста семь" in text or "амур" in text:
            gui.Print(datetime.datetime.today().strftime(
                data_text) + ' ' + text)
            if "привет" in text:
                answer = " АМУР: приветствую вас, сэр!"
                gui.Print(datetime.datetime.today().strftime(
                    data_text) + answer)
                assistant.play_speech("приветствую вас, сэр!")
                log_text(answer)

            elif "состояние" in text:
                answer = " АМУР: я нахожусь в стадии разработки"
                gui.Print(datetime.datetime.today().strftime(
                    data_text) + answer)
                assistant.play_speech("я нахожусь в стадии разработки")
                log_text(answer)
            elif "отбой" in text:
                answer = ' АМУР: всего доброго сэр!\n'
                gui.Print(datetime.datetime.today().strftime(
                    data_text) + " АМУР: всего доброго сэр!")
                assistant.play_speech("всего доброго сэр!")
                log_text(answer)
                Log.close()
                sys.exit()
            else:
                answer = " АМУР: я не понимаю вас"
                gui.Print(datetime.datetime.today().strftime(data_text) + answer)
                assistant.play_speech("я не понимаю вас")
                log_text(answer)


if __name__ == "__main__":

    assistant = VoiceAssistant()
    assistant.name = "Jarvis"
    assistant.sex = "male"
    assistant.speech_language = "ru"
    gui = AmurGUI()


    Log = open('Log.txt', 'a')
    a = os.path.getsize('Log.txt')
    if a > 10485760:  # a>1 Mbyte
        Log.close()
        os.rename('Log.txt', 'Log_old.txt')
        Log = open('Log.txt', 'w+')
    print(a)

    hello = " Приветствую вас!"
    working = " Работаем!"

    log_text(hello)
    assistant.play_speech(hello)
    log_text(working)
    assistant.play_speech(working)

    t1 = threading.Thread(target=listen_handler)
    t1.start()
    gui.window_handler()
    gui.window.close()

    # t1 = threading.Thread( target = listen_handler)
    # t1.start()
