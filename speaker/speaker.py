from pickle import NONE
import speech_recognition as sr
import openai
import pyttsx3
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import os
import psutil
import signal
from secret import API_KEY
from spid import *
import os
openai.api_key=API_KEY

engine=pyttsx3.init()

r=sr.Recognizer()
mic=sr.Microphone(device_index=1)
#print(sr.Microphone.list_microphone_names())
print('                         ---------------------Microphone Devices available---------------------')
for i in sr.Microphone.list_microphone_names():
    print(i)
conversation=""
user="you"
bot_name="Jarvis"

####################################  SPOTIFY   ##################################################
#username = USERNAME
#clientID = CLIENTID
#clientSecret = CLIENTSECRET
#redirect_uri = URI

auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope,username=username)
spotify=spotipy.Spotify(auth_manager=auth_manager)
token_dict = auth_manager.get_access_token()
token = token_dict['access_token']
spotify = spotipy.Spotify(auth=token)
####################################  SPOTIFY   ##################################################

def play(user_in):

    
    devices=spotify.devices()
    for d in devices['devices']:
        print(d['name']+": "+d['id'])
    
    search_song=''
    if 'album' in user_in:
        search_song=user_in.split("album",1)[1]
        engine.say('playing album '+search_song)
        results=spotify.search(search_song, 1,0, "album")
        spotify.start_playback(device_id1,context_uri=results['albums']['items'][0]['uri'])
    else:
        search_song =user_in.split("play",1)[1]
        engine.say('playing song '+search_song)
        results = spotify.search(search_song, 1,0, "track")
        spotify.start_playback(device_id1,uris=[results['tracks']['items'][0]['uri']])
    
####################################  SPOTIFY   ##################################################

def conv(user_input):
    prompt=user+": "+user_input+"\n"+bot_name+": "
    global conversation
    conversation+=prompt
    response=openai.Completion.create(model='text-davinci-001',prompt=conversation,max_tokens=1000)
    response_str = response["choices"][0]["text"].replace("\n", "")
    response_str = response_str.split(user + ": ", 1)[0].split(bot_name + ": ", 1)[0]
    conversation += response_str + "\n"
    print(response_str)
    engine.say(response_str)

def open(user_in):
    #engine.say('opening')
    if "visual studio" in user_in:
        engine.say('opening visual studio')
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Visual Studio 2022.lnk')
    elif "brave" in user_in or "browser" in user_in:
        engine.say('opening brave')
        os.startfile("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Brave.lnk")

def EndProc(ProcessName):
    closed = False
    for proc in psutil.process_iter():
        try:
            procinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            if ProcessName.lower() in procinfo['name'].lower():
                try: 
                    os.kill(procinfo['pid'],signal.SIGTERM)
                except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess):
                    engine.say('Access Denied')

                closed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess):
            engine.say('No Such Process Exists sir')
        #print(closed)
    if closed:
        engine.say('closed ' + ProcessName)


def close(user_in):
    engine.say('closing')
    if "spotify" in user_in:
        engine.say('spotify')
        EndProc('Spotify')
    elif "brave" in user_in or "browser" in user_in:
        engine.say('brave')
        EndProc('brave')
    elif "whatsapp" in user_in:
        engine.say('Whatsapp')
        EndProc('WhatsApp')
    else:
        engine.say('app not found')


def search(user_in):
    s=user_in.split("search",1)[1]
    url = 'https://google.com/search?q=' + s
    engine.say('searching'+s)
    webbrowser.get().open(url)



while True:
    with mic as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source,duration=0.2)
        audio=r.listen(source)
    print("Not Listening")
    try:
        user_input=r.recognize_google(audio)
    except:
        continue
    user_in=user_input.lower()
    #print("ans: "+user_in)
    #if "google" not in user_in:
    #    continue
    if "play" in user_in:
        play(user_in)
    elif "image" in user_in:
        prompt=openai.Image.create(prompt=user_input,n=1,size="1024x1024")
        url=prompt['data'][0]['url']
        webbrowser.open(url)
        continue
    elif "open" in user_in or "":
        open(user_in)
    elif "close" in user_in:
        close(user_in)
    elif "search" in user_in:
        search(user_in)
    else:
        conv(user_input)
 
    engine.runAndWait()