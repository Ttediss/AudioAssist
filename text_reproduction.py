import pyttsx3

class voice_acting:
    def settings(property, value):
        engine.setProperty(property, value)
    def say(text):
        engine.say(text)
        engine.runAndWait()

engine = pyttsx3.init()

