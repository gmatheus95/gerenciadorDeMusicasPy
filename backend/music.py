class Music:
    
    #construtor
    def __init__(self, id="", path="", track="", title="-", album="", band="", duration=""):
        self.__id = id
        self.__path = path
        self.__track = track
        self.__title = title
        self.__album = album
        self.__band = band
        self.__duration = duration        
    

    #gets e sets
    def setTrack(self, track):
        self.__track = track
    
    def setTitle(self, title):
        self.__title = title

    def setPath(self, path):
        self.__path = path

    def setAlbum(self, album):
        self.__album = album

        
    def setBand(self, band):
        self.__band = band
    
    def setDur(self, dur):
        self.__duration = dur

    def getTrack(self):
        return self.__track

    def getPath(self):
        return self.__path
    
    def getTitle(self):
            return self.__title
        
    def getAlbum(self):
            return self.__album
            
    def getBand(self):
            return self.__band
            
    def getDur(self):
            return self.__duration

    track = property(getTrack, setTrack)
    title = property(getTitle, setTitle)
    album = property(getAlbum, setAlbum)
    band = property(getBand, setBand)
    duration = property(getDur,setDur)
    path = property(getPath, setPath)
    
    #funcoes
