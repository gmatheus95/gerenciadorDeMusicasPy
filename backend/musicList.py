from backend.music import Music

class MusicList:
    
    def __init__(self, name, description="", duration=0, songList=[], nSongs=0):
        self.__name = name
        self.__description = description
        self.__duration = duration
        self.__songList = songList #list of Musics
        self.__nSongs = nSongs
    
    def addsong(self, music):
        self.__songList.append(music)
        self.__duration += music.duration
        self.__nSongs += 1
        
        
    def removesong(self, index):
        #the music array starts in 0, so the song to be removed is the song[index-1]
        self.__duration -= self.__songList[index-1].duration
        self.__songList.remove(self.__songList[index-1])
        self.__nSongs -= 1
        
    def changeSongPos(self, songIndex, newIndex):
        #these index starts in 1 in User Interface and in 0 in code to properly access the arrays
        music = self.__songList[songIndex-1]
        self.__songList.remove(self.__musList[songIndex-1])
        self.__songList.insert(newIndex-1, music)
        
    def setname(self, name):
        self.__name = name
    
    def setdescription(self, description):
        self.__description = description
    
    def getname(self):
        return self.__name
    
    def getdescription(self):
        return self.__description
    
    def getduration(self):
        return self.__duration
    
    def getSongList(self):
        return self.__songList
    
    def getNSongs(self):
        return self.__nSongs
        