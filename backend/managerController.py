from backend.music import Music
from backend.album import Album
from backend.artist import Artist
from backend.musicList import MusicList
from backend.handlingMetadata import *
from backend.db import DB
from tkinter.filedialog import askopenfilenames
from tkinter import Tk

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
        self.__root = None
        self.__dbinstance = None

    def __addSongToEnvironment(self, song):
        # path is in 1
        fields = retrieveFields(song[1])
        self.allSongs.append(Music(song[0], fields['track'], fields['title'], fields['album'], fields['band'],
                                   fields['duration']))
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
            #print('\n' + self.allAlbums[index].getName() + "-" + self.allAlbums[index].getArtistName())

        # links the song to the artist
        if fields['band'] in self.dictArtists:
            self.allArtists[self.dictArtists[fields['band']]].addSong(song[0])
        else:
            index = len(self.allArtists)
            self.dictArtists[fields['band']] = index
            self.allArtists.append(Artist(fields['band']))
            self.allArtists[index].addSong(song[0])
            #print('\n' + self.allArtists[index].getName())
        '''
        print('\n' + self.allSongs[len(self.allSongs) - 1].track + " - " +
              self.allSongs[len(self.allSongs) - 1].title + " - " +
              self.allSongs[len(self.allSongs) - 1].album + " - " +
              self.allSongs[len(self.allSongs) - 1].band)
        '''



    def initialize_components(self):
        self.__dbinstance = DB()
        self.__dbinstance.create()
        songpaths = self.__dbinstance.executeSelect('SELECT * FROM song')
        # Iniatializes Tk() for importing purposes
        self.__root = Tk()
        self.__root.withdraw()
        # adding songs from hard drive to objects
        for song in songpaths:
            self.__addSongToEnvironment(song)

    # if exists, return 1, else, save in DB and return the created entry in DB to save in Environment
    def __addSongToDatabase(self, filepath):
        if (self.__dbinstance.executeSelect('SELECT * FROM song WHERE '
                                            'filepath = "' + filepath + '"') == None ):
            return 1
        else:
            print('INSERT INTO song(filepath) VALUES ("' + filepath + '")')
            self.__dbinstance.executeInsertUpdateDelete(
                'INSERT INTO song(filepath) VALUES ("' + filepath + '")')
            return self.__dbinstance.executeSelect('SELECT * FROM song WHERE '
                                                   'filepath = "' + filepath + '"')

    # Must save in DB and in Environment, if it already exists, it's ignored
    def import_song(self):

        filenames = askopenfilenames(parent=self.__root, title='Choose your songs',
                                     defaultextension='.mp3', filetypes=[('MP3 File', '*.mp3')])
        for filepath in filenames:
            song = self.__addSongToDatabase(filepath)
            print(song[0])
            if (song != 1):
                self.__addSongToEnvironment(song[0])



class ManagerControllerSingleton(ManagerController, metaclass=Singleton):
    pass

controller = ManagerControllerSingleton()
controller.initialize_components()
controller.import_song()


