class Artist:

    nArtists = 0
    def __init__(self, name):
        self.__id = self.generateid()
        self.__name = name
        self.__numSongs = 0
        self.__songIDs = []

    def generateid(Artist):
        Artist.nArtists += 1
        return Artist.nArtists

    def getId(self):
        return self.__id

    def addSong(self, songid):
        self.__songIDs.append(songid)

    def removeSong(self, songid):
        self.__songIDs.remove(songid)

    def nSongs(self):
        return len(self.__songIDs)

    def getAllSongs(self):
        return self.__songIDs

    def getName(self):
        return self.__name

    def getSongs(self):
        return self.__songIDs

'''     mudar nome de artista precisa pensar melhor
    def changeName(self, newname):
        self.__name = newname
        return __songIDs
'''
