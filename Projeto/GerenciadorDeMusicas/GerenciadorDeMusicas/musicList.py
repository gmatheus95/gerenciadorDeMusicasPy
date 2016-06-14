from music import Music

class MusicList:
    
    def __init__(self, name, description ="", duration = 0, musList = [], nSongs = 0):
        self.__name = name
        self.__description = description
        self.__duration = duration
        self.__musList = musList
        self.__nSongs = nSongs
    
    def addMusica(self, musica):
        self.__musList.append(musica)
        self.__duration += musica.duration
        self.__nSongs += 1
        
        
    def removeMusica(self, indice):
        #o vetor de musicas comeca com indice 0, entao a removida sera a musica de indice "indice-1"
        self.__duration -= lista.__musList[indice-1].duration
        self.__musList.remove(lista.__musList[indice-1])
        self.__nSongs -= 1
        
    def mudaPosMusica(self, indiceMus, novoIndice):
        #esses indices ser�o sempre considerados partindo de 1 na interface do usuario e partindo de 0 para acesso a vetores
        music = self.__musList[indiceMus-1]
        self.__musList.remove(lista.__musList[indiceMus-1])        
        self.__musList.insert(novoIndice-1, music)
        
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