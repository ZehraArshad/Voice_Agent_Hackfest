import pyttsx3
import threading

engine = pyttsx3.init()
engine_lock = threading.Lock()

def _speak_internal(text):
    with engine_lock:
        engine.say(text)
        engine.runAndWait()

def speak(text):
    t = threading.Thread(target=_speak_internal, args=(text,))
    t.start()
