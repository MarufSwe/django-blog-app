import speech_recognition as sr
import pyttsx3
# import pywhatkit
# import datetime
# import wikipedia
import discord

# import os

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[10].id)


# convert my voice to virtual voice
def talk(text):
    engine.say(text)
    engine.runAndWait()


# voice command here (speak)
def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)  # listener listen the user-voice by source
            user_command = listener.recognize_google(
                voice)  # by google-api, listener send audio & google back it like text
            print('user_command: ', user_command)
    except:
        pass
    return user_command


def run_assistant():
    command = take_command()
    print('get_user_command: ', command)

    # for Discord BOT
    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')
        channel = client.get_channel(1069591088677015604)  # bot channel id
        await channel.send(command)
        talk(command)
        print(command)

    client.run("MTA2OTU1ODY0MTk2MDY5Mzg2MQ.GV8nse.mIVp19yhUzmuA_sRsfjIeOFieuO23tmv_uAUwU")  # bot Token
    # client.run("OTg2NDkzMjEyODMzMjE4NTgx.GtGJAO.OGi6Y_rwqg_7Zb29ZqFfTS_yWvMItL1RHhZsOs")  # My real Token
    # client.run("token is here", bot=False)


while True:
    run_assistant()
