import datetime
import glob
import json
import multiprocessing
import os
import math
import random
import socket

import lxml
import requests
import subprocess
from time import sleep
from urllib.request import urlopen

try:
    import vlc
    import pafy
    from youtubesearchpython import VideosSearch
except Exception as e:
    print("[CRITICAL WARNING]: cannot play from youtube, error: ", e)

import wikipedia
import ipinfo
from bs4 import BeautifulSoup as soup
from pytube import YouTube
from word2number import w2n

from VoiceAssistant.nlu_stable2.config import *



#from VoiceAssistant.nlu_stable2.config import *


#p = Parser()




class TaskManager:

    def __init__(self):
        super().__init__()
        self.event = False
        self.jokelist = []
        self.f = r"https://official-joke-api.appspot.com/random_ten"
        try:
            self.VLC = vlc.Instance()
        except Exception as e:
            print(f"[ERROR] VLC couldn't be found. You will not be able to play music. If you already installed python-vlc, try installing a 64bit VLC.\n Error: {e}")


    def get_ip(self):
        """
        get your ip
        """
        self.response = requests.get('https://api64.ipify.org?format=json').json()
        print(self.response)
        return self.response["ip"]


    def get_location(self):
        """
        gets your city from your ip
        """
        self.ip_address = self.get_ip()
        self.response = requests.get(f'https://ipapi.co/{self.ip_address}/json/').json()
        return self.response.get("city")


    def weather(self):
        """
        Compulsory: You must sign-up to openweather and generate your api,
        and paste it in the config file that sits in this directory, otherwise it will not work

        1: Gets your ip address
        2: Gets your location from your ip address
        3: Pass your location to openweather api
        4: Get weather data
        """
        self.city_name = self.get_location()
        # base_url variable to store url
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
         
        # complete_url variable to store
        # complete url address
        self.complete_url = self.base_url + "appid=" + open_weather_api_token + "&q=" + self.city_name
         
        # get method of requests module
        # return response object
        self.response = requests.get(self.complete_url)
         
        # json method of response object
        # convert json format data into
        # python format data
        self.response = self.response.json()
         
        # Now x contains list of nested dictionaries
        # Check the value of "cod" key is equal to
        # "404", means city is found otherwise,
        # city is not found
        if self.response["cod"] != "404":
         
            # store the value of "main"
            # key in variable y
            self.y = self.response["main"]
         
            # store the value corresponding
            # to the "temp" key of y
            self.current_temperature = str(math.ceil((int(self.y["temp"]) - 273)))+ " Celcius"
         
            # store the value corresponding
            # to the "pressure" key of y
            
         
            # store the value corresponding
            # to the "humidity" key of y
            self.current_humidity = self.y["humidity"]
         
            # store the value of "weather"
            # key in variable z
            self.z = self.response["weather"]
         
            # store the value corresponding
            # to the "description" key at
            # the 0th index of z
            self.weather_description = self.z[0]["description"]

            return self.weather_description, self.current_temperature, self.current_humidity
 
        else:
            return "City Not Found", "City Not Found", "City Not Found"

    
    def take_note(self, text):
        """just pass the text to be saved or notted down"""

        self.date = str(datetime.datetime.now().date()) + "%" + str(datetime.datetime.now().hour) + "+" + str(
            datetime.datetime.now().minute) + "}"
        self.file_name = "notes/" + str(self.date).replace(":", "-") + "-note.txt"
        with open(self.file_name, "w") as f:
            f.write(text)
        # subprocess.Popen(["notepad.exe", self.file_name])


    def get_note(self, args):
        """
        available args:
            latest : reads latest note
            total : returns num of notes
            yesterday : returns yesterday's note

        """
        self.list_of_files = glob.glob('notes/*')  # * means all if need specific format then *.csv

        if "latest" in args.lower() or "last note" in args.lower():
            self.latest_file = max(self.list_of_files, key=os.path.getctime)
            self.latest_file = str(self.latest_file.replace("notes", ""))

            with open(f"notes{self.latest_file}", "r") as g:
                return g.read()

        elif "total" in args.lower() or "how many" in args.lower():
            return len(self.list_of_files)

        elif "yesterday" in args.lower():
            self.ys = str(datetime.datetime.now().day)
            self.ys = int(self.ys) - 1
            print(self.ys)
            self.mn = datetime.datetime.now().month
            self.yr = datetime.datetime.now().year
            print(f"{self.yr}-{self.mn}-{self.ys}")
            for i in self.list_of_files:
                if f"{self.yr}-{self.mn}-{self.ys}" in i:
                    with open(f"{i}", "r") as rf:
                        return rf
                else:
                    return "you haven't made any entries yesterday"

    # def get_note_time
    def get_note_time(self, filename, arg="ymd"):
        self.ymd = filename[:"%"]
        self.hour = filename["%":"+"]
        self.minute = filename["+":]

        if arg == "ymd":
            return self.ymd
        elif arg == "hr":
            return self.hour
        elif arg == "min":
            return self.hour

    
    def news(self, headlines):
        """

        --------------------------------------------------------------------------------------------
        :ARGS: Headlines(str)     [number of headlines you want]

        :PARSING: https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en
        change US in the above link to IN for Indian news, CA for Canada, and so on.

        Keep it just https://news.google.com/rss for dynanimic location selection based on your IP 
        address

        :OUTPUT: returns a list of headlines
        --------------------------------------------------------------------------------------------

        """

        self.nl = []
        try:
            self.int_num = int(w2n.word_to_num(headlines))
            print(self.int_num)
            self.newsurl = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
            self.root = urlopen(self.newsurl)
            self.xmlpage = self.root.read()
            self.root.close()
            self.souppage = soup(self.xmlpage, "xml")
            self.newslist = self.souppage.findAll("item")
            for news in self.newslist[:self.int_num]:
                # speak(news.pubDate.text)
                self.nl.append(news.title.text)
            return self.nl

        except Exception as e:
            return f"Looks like something went wrong. Try connecting to internet. {e}"

    
    def wiki(self, query):
        
        """
        
        Get summary of topics from wikipedia.
        Requested args: query(the topic you want to search)

        NOTE: INCREASE sentences=3 TO ANY NUMBER IF REQUIRED,
        HIGHER THE VALUE = LONGER INFO
        SMALLER THE VALUE = LESS INFO AND NOT MUCH USEFULL INFO
        IS RETRIEVED
        
        """
        try:
            return wikipedia.summary(query, sentences=3)
        except Exception as e:
            return e
 
    
    def parse_youtube_query(self, query):
        self.videosSearch = VideosSearch(query, limit = 2)
        self.link = self.videosSearch.result()['result'][1]['link']
  
        return self.link


  
    def play_v(self, url):
        # not my code, copied from stackoverflow
        try:
            video = pafy.new(url)
            best = video.getbestaudio()
            playurl = best.url

            player = Instance.media_player_new()
            Media = Instance.media_new(playurl)
            Media.get_mrl()
            player.set_media(Media)
            return player, video
        except Exception as e:
            print(e)
            return None, None


    def start_player(self, player, video):
        print(video.length)
        player.play()
        print("started playing from function")
        time.sleep(7)
        while True:
            if player.is_playing():
                print("is_playing==True")
                time.sleep(1)
            else:
                player.stop()
                break
        print("function ended")




#######################################[    WARNING    ]####################################################    

    # The joke server is down for now, tested on 16 April 2022.
    # The below method wont work until they fix their server again.
    
    # For now, this function will raise an error.
    # So dont call this method.
    
    # I am not using this method in the main script.
    # If the server comes back online again, i will add this to the 
    # main inference loop.
    
    # If you still want to use jokes, create a similar joke method
    # that gets any random joke from your desired api
    # if that works out, give a pull request!


    def joke(self):
        """
        return any joke
        """
        if len(self.jokelist) == 0:
            try:
                self._data = requests.get(self.f)
                self._data = json.loads(self._data.text)
            
                print("from web")
                for jokes in self._data:
                    self.jokelist.append(jokes["setup"]+" "+jokes["punchline"])
                return random.choice(self.jokelist)
            
            except Exception as e:
                return f"unable to get jokes right now, error: [{e}]"

        else:
            print("from storage")
            return random.choice(self.jokelist)

############################################################################################################

    def all_event_loop(self, response, flags):
        if flag == '--weather':
            desc, ct, ch = self.weather()
            self.fr = f"{desc}, Temperature feels like {ct} Celcius, humidity is {ch}"
            return self.fr
        # NOTES FOR LATER : return the text to be said, and do the things here, and the string will be said in the loop.
        
        elif 
        