from music import Music
from musicList import MusicList
from handlingMetadata import *
from db import DB

#this file contains the main static operations

#TODO: get the last user configurations from a DB (user built lists, song in execution when the application has been closed, volume, etc)

def initializeComponents():
    dbinstance = DB()
    dbinstance.create()
    songpaths = dbinstance.executeSelect('SELECT * FROM song')
    allSongs = []
    count = 0
    #adding songs from hard drive to objects (working!)
    for song in songpaths:
        fields = retrieveFields(song[1]) #path is in 1
        allSongs.append(Music(fields['track'], fields['title'], fields['album'], fields['band']))
        #print(allSongs[count].track + " - " + allSongs[count].title + " - " + allSongs[count].album + " - " + allSongs[count].band)
        count += 1
        #pensar como vai fazer pra puxar os albums (provavelmente vai ter que fazer objeto pra album!



#ver função glob
    

def importSong(paths):
    #criar objeto pra uso imediato e adicionar no bd
    pass

def playSong(song):
    #play song
    pass

def stopSong():
    #stop current song
    pass

def pauseSong():
    #pause current song
    pass

def nextSong(musiclist):
    #play next song
    pass


initializeComponents() #executa initializeComponents pra testar