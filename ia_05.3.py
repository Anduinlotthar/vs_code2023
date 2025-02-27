# -*- coding: utf-8 -*-
# funciona un 80%
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime as dt
import wikipedia
import random

# Nombre del asistente
name = 'cortana'

# Inicializar reconocimiento de voz y síntesis de voz
listener = sr.Recognizer()
engine = pyttsx3.init()

# Configuración de la velocidad y voz del asistente
engine.setProperty('rate', 150)
engine.setProperty('voice', engine.getProperty('voices')[0].id)
wikipedia.set_lang('es')

# Traducción de los meses en español
spanish_month = {
    'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril',
    'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto',
    'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
}

# Respuesta aleatoria para iniciar la escucha


def random_choice():
    options = ['Te escucho', 'Dime tu orden', 'Estoy escuchándote', 'Dime']
    return random.choice(options)

# Método para que el asistente hable


def talk(text):
    engine.say(text)
    engine.runAndWait()

# Método para escuchar y reconocer la voz


def listen():
    try:
        with sr.Microphone() as source:
            print('Escuchando...')
            talk(random_choice())
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(
                voice, language='es-ES').lower()
            if name in command:
                command = command.replace(name, '').strip()
                print(f"Comando detectado: {command}")
                return command
    except sr.UnknownValueError:
        talk("No te he entendido, por favor repite.")
    except sr.RequestError:
        talk("Hubo un problema al conectarse al servicio de reconocimiento.")
    return ""

# Método que procesa los comandos


def process_command(command):
    if 'reproduce' in command:
        music = command.replace('reproduce', '').strip()
        talk(f'Reproduciendo {music} en YouTube.')
        pywhatkit.playonyt(music)
    elif 'hora' in command:
        hora = dt.datetime.now().strftime('%I:%M %p')
        talk(f'Son las {hora}')
    elif 'fecha' in command:
        fecha = dt.datetime.now().strftime('%d de %B de %Y')
        talk(f'La fecha es {fecha}')
    elif 'busca en wikipedia' in command:
        query = command.replace('busca en wikipedia', '').strip()
        talk(f'Buscando {query} en Wikipedia.')
        resultado = wikipedia.summary(query, sentences=3)
        talk(resultado)
    elif 'busca en google' in command:
        query = command.replace('busca en google', '').strip()
        talk(f'Buscando {query} en Google.')
        pywhatkit.search(query)
    else:
        talk("Disculpa, no te entiendo. ¿Podrías repetirlo?")

# Ejecución del asistente


def main():
    talk("Hola, soy tu asistente de voz. ¿En qué puedo ayudarte hoy?")
    while True:
        command = listen()
        if command:
            process_command(command)


if __name__ == "__main__":
    main()
