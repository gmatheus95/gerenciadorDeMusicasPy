from music import Music
from musicList import MusicList
from db import DB
import sqlite3

#this file contains the main static operations

#TODO: get the last user configurations from a DB (user built lists, song in execution when the application has been closed, volume, etc)

def initializeComponents():
    database = DB()
    database.create()
    nsongs = database.executeSelect('SELECT COUNT (id) FROM song')
    songs = database.executeSelect('SELECT * FROM song')
    allSongs = []
    for i in range(0,nsongs):
        #TODO: retrieve songs' information through windows and save in allSongs music array
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
