import requests
import pyttsx3
import pyaudio
import json
import os
from vosk import Model, KaldiRecognizer

# Инициализация синтезатора речи
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Инициализация распознавания речи
if not os.path.exists("model"):
    print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit(1)

model = Model("model")
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

# Функция для получения Lorem Ipsum текста
def get_lorem_ipsum():
    response = requests.get("https://loripsum.net/api/10/short/headers")
    if response.status_code == 200:
        return response.text
    else:
        return "Не удалось получить Lorem Ipsum текст."

# Основной цикл для распознавания команд
print("Голосовой ассистент запущен...")

while True:
    data = stream.read(4000)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        command = result.get("text", "").lower()
        
        if "создать" in command:
            text = get_lorem_ipsum()
            speak("Lorem Ipsum текст создан.")
        elif "прочесть" in command:
            text = get_lorem_ipsum()
            speak(text)
        elif "сохранить" in command:
            text = get_lorem_ipsum()
            with open("lorem_ipsum.html", "w") as file:
                file.write(text)
            speak("Lorem Ipsum текст сохранен как HTML файл.")
        elif "текст" in command:
            text = get_lorem_ipsum()
            with open("lorem_ipsum.txt", "w") as file:
                file.write(text)
            speak("Lorem Ipsum текст сохранен как текстовый файл.")
        else:
            speak("Команда не распознана. Попробуйте еще раз.")
