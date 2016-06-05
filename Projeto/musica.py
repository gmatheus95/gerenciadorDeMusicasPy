class Musica:
    
    #construtor
    def __init__(self, faixa="0", nome="nome", album="album", banda="banda", duracao=0.1):
        self.__faixa = faixa
        self.__nome = nome
        self.__album = album
        self.__banda = banda
        self.__duracao = duracao        
    
    #gets e sets
    def setFaixa(self, faixa):
        self.__faixa = faixa
    
    def setNome(self, nome):
        self.__nome = nome
    
    def setAlbum(self, album):
        self.__album = album
        
    def setBanda(self, banda):
        self.__banda = banda
    
    def setDur(self, dur):
        self.__duracao = dur

    def getFaixa(self):
        return self.__faixa
    
    def getNome(self):
            return self.__nome
        
    def getAlbum(self):
            return self.__album
            
    def getBanda(self):
            return self.__banda
            
    def getDur(self):
            return self.__duracao
        
    faixa = property(getFaixa, setFaixa)
    nome = property(getNome, setNome)
    album = property(getAlbum, setAlbum)
    banda = property(getBanda, setBanda)
    duracao = property(getDuracao, setDuracao)
    
    #funcoes