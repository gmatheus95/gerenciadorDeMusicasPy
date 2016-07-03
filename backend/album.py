class Album:

    nAlbums = 0
    def __init__(self, name, artistName):
        self.__id = self.generateid()
        self.__name = name
        self.__artistName = artistName
        self.__numSongs = 0
        self.__songIDs = []

    def generateid(Album):
        Album.nAlbums += 1
        return Album.nAlbums

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

    def getArtistName(self):
        return self.__artistName

    def getSongs(self):
        return self.__songIDs
