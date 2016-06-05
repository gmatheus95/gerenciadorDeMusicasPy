from musica import Musica

class ListaDeMusicas:
    
    def __init__(self, nome, descricao ="", duracao = 0, listaMusicas = [], nMusicas = 0):
        self.__nome = nome
        self.__descricao = descricao
        self.__duracao = duracao
        self.__listaMusicas = listaMusicas
        self.__nMusicas = nMusicas
    
    def addMusica(self, musica):
        self.__listaMusicas.append(musica)
        self.__duracao += musica.duracao
        self.__nMusicas += 1
        
        
    def removeMusica(self, indice):
        #o vetor de musicas comeca com indice 0, entao a removida sera a musica de indice "indice-1"
        self.__duracao -= lista.__listaMusicas[indice-1].duracao
        self.__listaMusicas.remove(lista.__listaMusicas[indice-1])
        self.__nMusicas -= 1
        
    def mudaPosMusica(self, indiceMus, novoIndice):
        #esses indices serão sempre considerados partindo de 1 na interface do usuario e partindo de 0 para acesso a vetores
        musica = self.__listaMusicas[indiceMus-1]
        self.__listaMusicas.remove(lista.__listaMusicas[indiceMus-1])        
        self.__listaMusicas.insert(novoIndice-1, musica)
        
    def setNome(self, nome):
        self.__nome = nome
    
    def setDescricao(self, descricao):
        self.__descricao = descricao
    
    def getNome(self):
        return self.__nome
    
    def getDescricao(self):
        return self.__descricao
    
    def getDuracao(self):
        return self.__duracao
    
    def getListaMusicas(self):
        return self.__listaMusicas
    
    def getNumMusicas(self):
        return self.__numMusicas
    
    