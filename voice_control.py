import pyaudio
import json
from contextlib import nullcontext
import pyttsx3
from vosk import Model, KaldiRecognizer
from sympy import false, true


class VoiceAssistant:
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""
    robotName = ["амур триста семь"]   # имя робота по умолчанию

    commands = nullcontext     # требуется присвоить список команд
    log_comand = nullcontext   # для логирования текста
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

	# обработчик аудиосообщений, требуется запустить в отдельном потоке
    def listen_handler(self):
        for text in self.listen():
            self.log_comand(text)
            if self.__have_str(text, self.robotName):
                self.__execute_command_with_name(text, text)


    def __execute_command_with_name(self,command_name: str, *args: str):
        for key in self.commands.keys():
            for one_key in key:
                if one_key in command_name:
                    self.commands[key](*args)
                    return
                else:
                    pass  
        print("Command not found")
        answer = " АМУР: я не понимаю вас"
        self.play_speech("я не понимаю вас")
        self.log_comand(answer)
    
    def __have_str(self, str, words):
        for word in words:
            if  word in str :
                return true
        return false


# ковёр

# def listen_handler():
#     for text in assistant.listen():
#         log_text(text)

#         if have_str(text,assistant.robotName):
#             gui.Print(datetime.datetime.today().strftime(
#                 data_text) + ' ' + text)

#             execute_command_with_name(text, "command options")

#             if "привет" in text:
#                 answer = " АМУР: приветствую вас, сэр!"
#                 assistant.play_speech("приветствую вас, сэр!")
#                 log_text(answer)

#             elif "состояние" in text:
#                 answer = " АМУР: я нахожусь в стадии разработки"
#                 assistant.play_speech("я нахожусь в стадии разработки")
#                 log_text(answer)
#             elif "отбой" in text:
#                 answer = ' АМУР: всего доброго сэр!\n'
#                 assistant.play_speech("всего доброго сэр!")
#                 log_text(answer)
#                 Log.close()
#                 sys.exit()
#             else:
#                 answer = " АМУР: я не понимаю вас"
#                 assistant.play_speech("я не понимаю вас")
#                 log_text(answer)

# def have_str(str, words):
#     for word in words:
#         if  word in str :
#             return true
#     return false

# def execute_command_with_name(command_name: str, *args: list):
#     """
#     Выполнение заданной пользователем команды с дополнительными аргументами
#     :param command_name: название команды
#     :param args: аргументы, которые будут переданы в функцию
#     :return:
#     """
#     for key in commands.keys():
#         for one_key in key:
#             if one_key in command_name:
#                 commands[key](*args)
#                 return
#             else:
#                 pass  # print("Command not found")


# def listen_handler_old():
#     for text in assistant.listen():
#         log_text(text)

#         if have_str(text,assistant.robotName):
#             gui.Print(datetime.datetime.today().strftime(
#                 data_text) + ' ' + text)

#             execute_command_with_name(text, "command options")

#             if "привет" in text:
#                 answer = " АМУР: приветствую вас, сэр!"
#                 assistant.play_speech("приветствую вас, сэр!")
#                 log_text(answer)

#             elif "состояние" in text:
#                 answer = " АМУР: я нахожусь в стадии разработки"
#                 assistant.play_speech("я нахожусь в стадии разработки")
#                 log_text(answer)
#             elif "отбой" in text:
#                 answer = ' АМУР: всего доброго сэр!\n'
#                 assistant.play_speech("всего доброго сэр!")
#                 log_text(answer)
#                 Log.close()
#                 sys.exit()
#             else:
#                 answer = " АМУР: я не понимаю вас"
#                 assistant.play_speech("я не понимаю вас")
#                 log_text(answer)
