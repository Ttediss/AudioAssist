import os.path
import time
import datetime
from sympy import false, true
from vosk import Model, KaldiRecognizer
from func_command import Caterpillars, Manipulator, Camera, Date
import sys
import threading

from GUInterface import AmurGUI
from voice_control import VoiceAssistant


data_text = "%Y.%m.%d-%H:%M:%S"



def play_greetings(arg: str):
    answer = " АМУР: приветствую вас, сэр!"
    assistant.play_speech("приветствую вас, сэр!")
    log_text(answer)

def play_quit(arg: str):
    answer = " АМУР: всего доброго сэр!"
    assistant.play_speech("всего доброго сэр!\n")
    gui.window.close()
    log_text(answer)


def delivery_item(arg: str):
    answer = " АМУР: эта команда пока не работает!"
    assistant.play_speech("эта команда пока не работает!")
    log_text(answer)

def play_status(arg: str):
    answer = " АМУР: я нахожусь в стадии разработки"
    assistant.play_speech("я нахожусь в стадии разработки")
    log_text(answer)

def search_code(arg: str):
    answer = " АМУР: эта команда пока не работает"
    assistant.play_speech("эта команда пока не работает")
    log_text(answer)



# для добавления новой команды нужно добавить ключевые слова и метод, реализующий функционал
commands = {
    ("привет","здравствуй"): play_greetings,
    ( "пока","отбой","стоп"): play_quit,
    ( "найди","поиск"): search_code,
    ("статус", "состояние"): play_status,
    ("доставь", "отнеси "): delivery_item,
}

def log_text(text):
    str = datetime.datetime.today().strftime(data_text) + ' ' + text
    print(str)
    Log.writelines(str + '\n')


if __name__ == "__main__":

    assistant = VoiceAssistant()
    assistant.name = "Jarvis"
    assistant.sex = "male"
    assistant.speech_language = "ru"

    assistant.robotName.append( "амур" )
    assistant.robotName.append( "амор" )
    assistant.robotName.append( "мур" )
    assistant.log_comand = log_text
    assistant.commands = commands
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

    t1 = threading.Thread(target=assistant.listen_handler)
    t1.start()
    gui.window_handler()
    gui.window.close()
    
    # t1 = threading.Thread( target = listen_handler)
    # t1.start()
