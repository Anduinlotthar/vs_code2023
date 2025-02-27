import speech_recognition as speech
import pyttsx3
import pywhatkit
import datetime as time
import wikipedia
import random

# Nombre del asistente
name = 'cortana'  # TODO: Debes ingresar el nombre de tu asistente aqui

# Permite reconocer la voz
listener = speech.Recognizer()

engine = pyttsx3.init()

"""RATE DEL ASISTENTE"""
rate = engine.getProperty('rate')
engine.setProperty('rate', 150)

"""VOZ DEL ASISTENTE"""
voice_engine = engine.getProperty('voices')
engine.setProperty('voice', voice_engine[0].id)

"""LENGUAJE DE WIKIPEDIA"""
wikipedia.set_lang('es')

# Traduccion de los meses
spanish_month = {
    'January': 'Enero',
    'February': 'Febrero',
    'March': 'Marzo',
    'April': 'Abril',
    'May': 'Mayo',
    'June': 'Junio',
    'July': 'Julio',
    'August': 'Agosto',
    'September': 'Septiembre',
    'October': 'Octubre',
    'November': 'Noviembre',
    'December': 'Diciembre'
}

# Selecciona una palabra de forma aleatoria


def random_choice():
    lista = ['Te escucho', 'Dime tu orden', 'Estoy escuchándote', 'Dime']
    seleccion = random.choice(lista)
    return seleccion

# Meotodo que permite al asistente hablar


def talk(text):
    engine.say(text)
    engine.runAndWait()

# Metodo que permite al asistente escuchar

# Metodo que permite al asistente escuchar


def listen():
    recognizer = ''  # Asignar valor predeterminado
    try:
        with speech.Microphone() as source:
            select = random_choice()
            print('Escuchando...')
            talk(select)
            voice = listener.listen(source)
            recognizer = listener.recognize_google(
                voice, language='es-MX').lower().strip()

            if name in recognizer:
                recognizer = recognizer.replace(name, '')
    except BaseException:
        print('Algo ha salido mal')
        pass
    return recognizer


# Diccionario de comandos con variaciones
COMMANDS = {
    "reproduce": ["reproduce", "pon", "quiero escuchar", "quiero musica"],
    "busca_google": ["busca en google", "busca", "quiero buscar", "necesito información sobre"],
    "hora": ["hora", "qué hora es", "dime la hora"],
    "fecha": ["fecha", "qué fecha es", "dime la fecha"],
    "día": ["día", "qué día es", "dime el día"],
    "mes": ["mes", "qué mes es", "dime el mes"],
    "año": ["año", "qué año es", "dime el año"],
    "wikipedia": ["busca en wikipedia", "dime sobre", "qué es"]
}

# Función para detectar el comando


def detect_command(command):
    for action, keywords in COMMANDS.items():
        if any(keyword in command for keyword in keywords):
            return action
    return None

# Metodo que ejecuta al asistente


def run():
    recognizer = listen()

    print(f'Comando recibido: {recognizer}')

    # Detectar el comando usando el diccionario de comandos
    command_action = detect_command(recognizer)

    if command_action == "reproduce":
        music = recognizer.replace('reproduce', '').strip()
        talk(f'reproduciendo {music}')
        pywhatkit.playonyt(music)

    elif command_action == "hora":
        hora = time.datetime.now().strftime('%I:%M %p')
        talk(f'Son las {hora}')

    elif command_action == "fecha":
        fecha = time.datetime.now().strftime('%d-%b-%Y')
        talk(f'La fecha es: {fecha}')

    elif command_action == "día":
        dia = time.datetime.now().strftime('%d')
        talk(f'Hoy es el día {dia}')

    elif command_action == "mes":
        mes = time.datetime.now().strftime('%B')
        mes_translate = spanish_month[mes]
        talk(f'Estamos en el mes de {mes_translate}')

    elif command_action == "año":
        year = time.datetime.now().strftime('%Y')
        talk(f'Estamos en el {year}')

    elif command_action == "wikipedia":
        consulta = recognizer.replace('busca en wikipedia', '').strip()
        talk(f'buscando en wikipedia {consulta}')
        resultado = wikipedia.summary(consulta, sentences=3)
        talk(resultado)

    elif command_action == "busca_google":
        consulta = recognizer.replace('busca en google', '').strip()
        talk(f'buscando en google {consulta}')
        pywhatkit.search(consulta)

    # COMANDO DE DESPEDIDA
    elif 'adiós' in recognizer or 'nos vemos' in recognizer:
        talk('¡Hasta luego! Que tengas un buen día.')
        exit(0)  # Termina el programa

    else:
        talk('Disculpa, no te entiendo')


# Ejecutar el asistente
if __name__ == "__main__":
    while True:
        run()
