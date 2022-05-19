import speech_recognition as sr
import pyttsx3

class VoiceAssistant:
    def __init__(self):
        self.stt = sr.Recognizer()
        self.tts = pyttsx3.init()
        self.tts.setProperty('volume', 0.5)
        self.tts.setProperty('rate', 200)

    def listen(self):
        with sr.Microphone() as source:
            try:
                audio = self.stt.listen(source)
                text = self.stt.recognize_google(audio, language='pl_PL')
            except sr.UnknownValueError:
                return 'Do not understand'
            except sr.RequestError as e:
                return 'Error: ' + e

        return text

    def speak(self, text):
        self.tts.say(text)
        self.tts.runAndWait()
