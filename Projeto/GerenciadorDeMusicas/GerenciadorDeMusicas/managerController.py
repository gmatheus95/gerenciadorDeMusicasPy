from music import Music
from album import Album
from artist import Artist
from musicList import MusicList
from handlingMetadata import *
from db import DB

#this file contains the main static operations

#TODO: get the last user configurations from a DB (user built lists, song in execution when the application has been closed, volume, etc)

allSongs = []
allAlbums = []
allArtists = []
dictalbums = {}
dictartists = {}

def initializeComponents():
    dbinstance = DB()
    dbinstance.create()
    songpaths = dbinstance.executeSelect('SELECT * FROM song')
    # adding songs from hard drive to objects (working!)
    for song in songpaths:
        # path is in 1
        fields = retrieveFields(song[1])
        allSongs.append(Music(song[0], fields['track'], fields['title'], fields['album'], fields['band'], fields['duration']))
        # links the song to the album
        if fields['album'] in dictalbums:
            # the album already exists, so adds the song to the album
            # fields['album'] is the album's name
            # albums[x] is the dictionary that converts the name to the respective index
            # AllAlbums is the array of albums

            allAlbums[dictalbums[fields['album']]].addSong(song[0])
        else:
            # the album must be created and then the song linked
            index = len(allAlbums)
            dictalbums[fields['album']] = index
            allAlbums.append(Album(fields['album'], fields['band']))
            allAlbums[index].addSong(song[0])

        print('\n' + allAlbums[index].getName() + "-" + allAlbums[index].getArtistName())

        # links the song to the artist
        if fields['band'] in dictartists:
            allArtists[dictartists[fields['band']]].addSong(song[0])
        else:
            index = len(allArtists)
            dictartists[fields['band']] = index
            allArtists.append(Artist(fields['band']))
            allArtists[index].addSong(song[0])

        print('\n' + allArtists[index].getName())

        print('\n' + allSongs[len(allSongs)-1].track + " - " + allSongs[len(allSongs)-1].title + " - " + allSongs[len(allSongs)-1].album + " - " + allSongs[len(allSongs)-1].band)

    

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