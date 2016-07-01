from Projeto.GerenciadorDeMusicas.GerenciadorDeMusicas.backend.music import Music
from Projeto.GerenciadorDeMusicas.GerenciadorDeMusicas.backend.album import Album
from Projeto.GerenciadorDeMusicas.GerenciadorDeMusicas.backend.artist import Artist
from Projeto.GerenciadorDeMusicas.GerenciadorDeMusicas.backend.musicList import MusicList
from Projeto.GerenciadorDeMusicas.GerenciadorDeMusicas.backend.handlingMetadata import *
from Projeto.GerenciadorDeMusicas.GerenciadorDeMusicas.backend.db import DB

# this file contains the main static operations


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ManagerController:
    def __init__(self):
        self.allSongs = []
        self.allAlbums = []
        self.allArtists = []
        self.dictAlbums = {}
        self.dictArtists = {}

    def initialize_components(self):
        dbinstance = DB()
        dbinstance.create()
        songpaths = dbinstance.executeSelect('SELECT * FROM song')
        # adding songs from hard drive to objects (working!)
        for song in songpaths:
            # path is in 1
            fields = retrieveFields(song[1])
            self.allSongs.append(Music(song[0], fields['track'], fields['title'], fields['album'], fields['band'], fields['duration']))
            # links the song to the album
            if fields['album'] in self.dictAlbums:
                # the album already exists, so adds the song to the album
                # fields['album'] is the album's name
                # albums[x] is the dictionary that converts the name to the respective index
                # self.allAlbums is the array of albums
    
                self.allAlbums[self.dictAlbums[fields['album']]].addSong(song[0])
            else:
                # the album must be created and then the song linked
                index = len(self.allAlbums)
                self.dictAlbums[fields['album']] = index
                self.allAlbums.append(Album(fields['album'], fields['band']))
                self.allAlbums[index].addSong(song[0])
                print('\n' + self.allAlbums[index].getName() + "-" + self.allAlbums[index].getArtistName())
    
            # links the song to the artist
            if fields['band'] in self.dictArtists:
                self.allArtists[self.dictArtists[fields['band']]].addSong(song[0])
            else:
                index = len(self.allArtists)
                self.dictArtists[fields['band']] = index
                self.allArtists.append(Artist(fields['band']))
                self.allArtists[index].addSong(song[0])
                print('\n' + self.allArtists[index].getName())
    
            print('\n' + self.allSongs[len(self.allSongs)-1].track + " - " + self.allSongs[len(self.allSongs)-1].title + " - " + self.allSongs[len(self.allSongs)-1].album + " - " + self.allSongs[len(self.allSongs)-1].band)
    
    def import_song(self, paths):
        # criar objeto pra uso imediato e adicionar no bd
        pass


class ManagerControllerSingleton(ManagerController, metaclass=Singleton):
    pass

controller = ManagerControllerSingleton()
controller.initialize_components()
