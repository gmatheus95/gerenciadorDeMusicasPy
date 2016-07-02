import sqlite3


class DB:
    def __init__(self):
        self.__conn=sqlite3.connect("db_musManager.db")
        self.__conn.execute('pragma foreign_keys=ON')
        
    def create(self):
        cursor = self.__conn.cursor()
        
        #cursor.execute('''DROP TABLE IF EXISTS song''')
        #cursor.execute('''DROP TABLE IF EXISTS musiclist''')
        #cursor.execute('''DROP TABLE IF EXISTS song_muslist''')

        #table song
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS song
                        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, filepath TEXT NOT NULL)''')

        #table musicList

        cursor.execute('''CREATE TABLE IF NOT EXISTS musiclist
                        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, nsongs INTEGER NOT NULL, totaldur REAL NOT NULL, name TEXT NOT NULL, description TEXT)''')

        #table song_muslist
        cursor.execute('''CREATE TABLE IF NOT EXISTS song_muslist
                        (songid INTEGER NOT NULL, muslistid INTEGER NOT NULL, num INTEGER NOT NULL,
                        PRIMARY KEY (songid, muslistid),
                        FOREIGN KEY (songid) REFERENCES song(id),
                        FOREIGN KEY (muslistid) REFERENCES muslist(id)
                        )''')
        cursor.close()
        self.__conn.commit()
          

    def executeSelect(self, clause):
        cursor = self.__conn.cursor()
        rows = None
        cursor.execute(clause)
        rows = cursor.fetchall()
        self.__conn.commit()
        cursor.close()
        return rows  
    
    def executeInsertUpdateDelete(self, clause):
        cursor = self.__conn.cursor()
        cursor.execute(clause)
        self.__conn.commit()
        cursor.close()

    def closeConnection(self):
        self.__conn.close()


#x = DB()
#x.create()
#x.executeInsertUpdateDelete('DELETE FROM song')
#x.executeInsertUpdateDelete('UPDATE song SET filepath = ? where id = ?', [newfilepath,id])
#x.executeInsertUpdateDelete('INSERT INTO song(filepath) '
#                            'SELECT "D:\Músicas\Bixiga70\\01 100% 13.mp3"'
#                            'WHERE NOT EXISTS(SELECT 1 FROM song WHERE filepath = '
#                            '"D:\Músicas\Bixiga70\\01 100% 13.mp3");')
#x.executeInsertUpdateDelete('INSERT INTO song(filepath) '
#                            'SELECT "D:\Músicas\Bixiga70\\01 100% 13.mp3"'
#                            'WHERE NOT EXISTS(SELECT 1 FROM song WHERE filepath = '
#                            '"D:\Músicas\Bixiga70\\01 100% 13.mp3");')
#x.executeInsertUpdateDelete('INSERT OR IGNORE INTO song(filepath) VALUES ("D:\Músicas\Bixiga70\\01 100% 13.mp3")')
#x.executeInsertUpdateDelete('INSERT OR IGNORE INTO song(filepath) VALUES ("D:\Músicas\Bixiga70\\01 100% 13.mp3")')
#y = x.executeSelect('SELECT * FROM song')
#print(y)
