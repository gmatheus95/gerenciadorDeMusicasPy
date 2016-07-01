class Music:
    
    #construtor
    def __init__(self, track="", name="", album="", band="", duration=0):
        self.__track = track
        self.__name = name
        self.__album = album
        self.__band = band
        self.__duration = duration        
    

    #gets e sets
    def setTrack(self, track):
        self.__track = track
    
    def setName(self, name):
        self.__name = name
    
    def setAlbum(self, album):
        self.__album = album
        
    def setBand(self, band):
        self.__band = band
    
    def setDur(self, dur):
        self.__duration = dur

    def getTrack(self):
        return self.__track
    
    def getName(self):
            return self.__name
        
    def getAlbum(self):
            return self.__album
            
    def getBand(self):
            return self.__band
            
    def getDur(self):
            return self.__duration
        
    track = property(getTrack, setTrack)
    name = property(getName, setName)
    album = property(getAlbum, setAlbum)
    band = property(getBand, setBand)
    duration = property(getDur,setDur)
    
    #funcoes