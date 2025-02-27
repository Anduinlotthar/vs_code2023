# -*- coding: utf-8 -*-
# funciona un 80 %
import speech_recognition as speech
import pyttsx3
import pywhatkit
import datetime as time
import wikipedia
import requests
import random

# Nombre del asistente
name = 'cortana'  # TODO: Ingresa el nombre de tu asistente aquí

# Permite reconocer la voz
listener = speech.Recognizer()
engine = pyttsx3.init()

# Configuración del asistente
engine.setProperty('rate', 150)
voice_engine = engine.getProperty('voices')
engine.setProperty('voice', voice_engine[0].id)
wikipedia.set_lang('es')  # Lenguaje de Wikipedia en español

# Traducción de los meses
spanish_month = {
    'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril',
    'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto',
    'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
}

# Selecciona una palabra de forma aleatoria


def random_choice():
    lista = ['Te escucho', 'Dime tu orden', 'Estoy escuchándote', 'Dime']
    return random.choice(lista)

# Método que permite al asistente hablar


def talk(text):
    engine.say(text)
    engine.runAndWait()

# Método que permite al asistente escuchar


def listen():
    try:
        with speech.Microphone() as source:
            print('Escuchando...')
            talk(random_choice())
            voice = listener.listen(source)
            recognizer = listener.recognize_google(
                voice, language='es-MX').lower()
            # Depuración: ver el texto reconocido
            print(f"Texto reconocido: {recognizer}")

            if name in recognizer:
                return recognizer.replace(name, '').strip()
    except Exception as e:
        print(f'Error al escuchar: {e}')
        talk('Lo siento, no entendí. ¿Podrías repetirlo?')
        return ""
    return ""

# Obtener un chiste en español usando JokeAPI


def obtener_chiste():
    try:
        respuesta = requests.get("https://v2.jokeapi.dev/joke/Any?lang=es")
        if respuesta.status_code == 200:
            datos = respuesta.json()
            return datos["joke"] if datos["type"] == "single" else f"{
                datos['setup']}... {datos['delivery']}"
    except requests.RequestException:
        return "No se pudo obtener un chiste en este momento."

# Método que ejecuta al asistente


def run():
    recognizer = listen()
    if not recognizer:
        return

    # Reproduce un video en YouTube
    if 'reproduce' in recognizer:
        music = recognizer.replace('reproduce', '').strip()
        talk(f'Reproduciendo {music}')
        pywhatkit.playonyt(music)

    # Indica la hora actual
    elif 'hora' in recognizer:
        hora = time.datetime.now().strftime('%I:%M %p')
        talk(f'Son las {hora}')

    # Indica la fecha completa
    elif 'fecha' in recognizer:
        fecha = time.datetime.now().strftime('%d-%B-%Y')
        mes_translate = spanish_month[fecha.split('-')[1]]
        talk(
            f'La fecha es: {
                fecha.replace(
                    fecha.split("-")[1],
                    mes_translate)}')

    # Indica el día
    elif 'día' in recognizer:
        dia = time.datetime.now().strftime('%d')
        talk(f'Hoy es el día {dia}')

    # Indica el mes
    elif 'mes' in recognizer:
        mes = time.datetime.now().strftime('%B')
        mes_translate = spanish_month[mes]
        talk(f'Estamos en el mes de {mes_translate}')

    # Indica el año
    elif 'año' in recognizer:
        year = time.datetime.now().strftime('%Y')
        talk(f'Estamos en el año {year}')

    # Busca en Wikipedia
    elif 'busca en wikipedia' in recognizer:
        consulta = recognizer.replace('busca en wikipedia', '').strip()
        talk(f'Buscando en Wikipedia {consulta}')
        resultado = wikipedia.summary(consulta, sentences=3)
        talk(resultado)

    # Busca en Google
    elif 'busca en google' in recognizer:
        consulta = recognizer.replace('busca en google', '').strip()
        talk(f'Buscando en Google {consulta}')
        pywhatkit.search(consulta)

    # Cuenta un chiste
    elif 'chiste' in recognizer:
        chiste = obtener_chiste()
        talk(chiste)

    else:
        talk('Disculpa, no te entiendo')


# Ejecutar el asistente
if __name__ == "__main__":
    talk("Hola, soy tu asistente de voz. ¿En qué puedo ayudarte hoy?")
    while True:
        run()
