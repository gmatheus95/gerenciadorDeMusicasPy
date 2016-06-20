from music import Music

class MusicList:
    
    def __init__(self, name, description ="", duration = 0, musList = [], nSongs = 0):
        self.__name = name
        self.__description = description
        self.__duration = duration
        self.__musList = musList #list of Musics
        self.__nSongs = nSongs
    
    def addMusica(self, musica):
        self.__musList.append(musica)
        self.__duration += musica.duration
        self.__nSongs += 1
        
        
    def removeMusica(self, index):
        #the music array starts in 0, so the song to be removed is the song[index-1]
        self.__duration -= self.__musList[index-1].duration
        self.__musList.remove(self.__musList[index-1])
        self.__nSongs -= 1
        
    def mudaPosMusica(self, indexMus, novoindex):
        #these index starts in 1 in User Interface and in 0 in code to properly access the arrays
        music = self.__musList[indexMus-1]
        self.__musList.remove(self.__musList[indexMus-1])        
        self.__musList.insert(novoindex-1, music)
        
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
    
    def getmusList(self):
        return self.__musList
    
    def getNSongs(self):
        return self.__nSongs
        