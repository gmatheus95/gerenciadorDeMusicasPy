import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock
from functools import partial
from backend.managerController import *

kivy.require('1.0.8')

controller = ManagerControllerSingleton()


class AudioBackground(BoxLayout):
    pass


class MetadataEditor(BoxLayout):
    pass

class MusicViewer(GridLayout):
    pass

class AlbumViewer(GridLayout):
    pass

class ArtistViewer(GridLayout):
    pass


class MusicLibraryApp(App):
    filename = StringProperty(None)
    sound = ObjectProperty(None, allownone=True)
    localSong = None
    localSongPos = 0
    volume = NumericProperty(1.0)
    currentSongDuration = NumericProperty(None)
    currentSongPosition = NumericProperty(None)
    progressBarPosition = NumericProperty(0)
    kv_directory = 'gui'
    currentState = "allSongs"
    onBuild = True
    playList = []
    buttonStatus = "Play"


    def load_song(self,  root, song, nothing='nothing'):
        wasPlaying = False
        # TODO: Separate selected song from playing song
        if self.sound:
            if self.sound.state != 'stop':
                wasPlaying = True
                self.sound.stop()
                Clock.unschedule(self.update_progress)
        self.localSong = song
        self.filename = song.path
        root.ids['lblSongName'].text = self.localSong.title
        self.sound = SoundLoader.load(self.filename)
        self.currentSongPosition = 0
        if wasPlaying:
            self.__play_music()
        if (self.currentState == "metadata"):
            self.view_metadata(root)


    def __load_all_songs(self, root, all = True, artist="", band=""):
        if root.ids["musicPanel"].children:
            root.ids["musicPanel"].clear_widgets()
        music_view = MusicViewer()
        root.ids["musicPanel"].add_widget(music_view)

        self.playList = controller.allSongs
        if (all == False): #load all songs!
            self.playList = []
            if (artist != ""):
                ids = artist.getSongs()
            else:
                ids = band.getSongs()
            for songid in ids:
                self.playList.append(controller.allSongs[controller.dictSongs[str(songid)]])

        songList = []
        for song in self.playList:
            songList.append(Button(text=song.title, size=(50, 30), size_hint=(1, None)))
            music_view.add_widget(songList[len(songList) - 1])
            self.localSongPos = 0

        # If there is a song, load it and binding the buttons
        if len(songList) > 0:
            if (self.onBuild == True):
                self.load_song(root, self.playList[0], None)
                self.onBuild = False
            for num in range(0, len(songList)):
                # Using a partial to pass args
                button_import = partial(self.load_song, root, self.playList[num])
                songList[num].bind(on_press=button_import)

        return root

    def build(self):
        root = AudioBackground(spacing=5)

        # Initializing components
        controller.initialize_components()



        # Listing all musics on db
        self.__load_all_songs(root)

        return root

    def view_all_songs(self,root):
        self.__load_all_songs(root)

    def import_songs(self, root):
        controller.import_song()
        if (self.currentState == "allSongs"):
            self.view_all_songs(root)
            return
        if (self.currentState == "albums"):
            self.view_albums(root)
            return
        if (self.currentState == "artists"):
            self.view_albums(root)
            return
        if (self.currentState == "metadata"):
            self.view_metadata(root)
            return


    def view_albums(self, root):
        self.currentState = "albums"
        if root.ids["miscPanel"].children:
            root.ids["miscPanel"].clear_widgets()
        album_view = AlbumViewer()
        root.ids["miscPanel"].add_widget(album_view)

        buttonList = []
        for album in controller.allAlbums:
            nameToPrint = album.getName()
            tam = len(album.getName())
            #formatting album name
            while tam > 20:
                nameToPrint = nameToPrint[0:20]
                nameToPrint += '\n'
                nameToPrint += album.getName()[20:]
                tam -= 20
            buttonList.append(Button(text=nameToPrint, size=(200, 200), size_hint=(None, None)))
            album_view.add_widget(buttonList[len(buttonList)-1])
            album_press = partial(self.album_press, controller.allAlbums[len(buttonList) - 1], root)
            buttonList[len(buttonList) - 1].bind(on_press=album_press)


    def view_artists(self, root):
        self.currentState="artists"
        if root.ids["miscPanel"].children:
            root.ids["miscPanel"].clear_widgets()
        artist_view = ArtistViewer()
        root.ids["miscPanel"].add_widget(artist_view)

        buttonList = []
        for artist in controller.allArtists:
            nameToPrint = artist.getName()
            tam = len(artist.getName())
            # formatting album name
            while tam > 20:
                nameToPrint = nameToPrint[0:20]
                nameToPrint += '\n'
                nameToPrint += artist.getName()[20:]
                tam -= 20
            buttonList.append(Button(text=nameToPrint,
                                     size=(200, 200), size_hint=(None, None)))
            artist_view.add_widget(buttonList[len(buttonList) - 1])
            artist_press = partial(self.artist_press, controller.allArtists[len(buttonList) - 1], root)
            buttonList[len(buttonList) - 1].bind(on_press=artist_press)

    def artist_press(self, artistObj, root, nothing):
        # Listing all musics on db
        self.__load_all_songs(root, artist=artistObj, all=False)

    def album_press(self, albumObj, root, nothing):
        self.__load_all_songs(root, all=False, band=albumObj)

    def view_metadata(self, root):
        self.currentState = "metadata"
        if root.ids["miscPanel"].children:
            root.ids["miscPanel"].clear_widgets()
        metadata_view = MetadataEditor()
        root.ids["miscPanel"].add_widget(metadata_view)

    def __play_music(self):
        self.currentSongDuration = self.sound.length

        # stop the sound if it's currently playing
        if self.sound.status != 'stop':
            self.sound.stop()
            Clock.unschedule(self.update_progress)
        else:
            self.sound.volume = self.volume
            self.sound.play()
            self.sound.seek(self.currentSongPosition)
            Clock.schedule_interval(self.update_progress, 0.5)


    def play_music(self, widget):
        self.__play_music()
        if self.sound.status != 'stop':
            self.buttonStatus = 'Stop'
        else:
            self.buttonStatus = 'Play'
        widget.text = self.buttonStatus

    def update_progress(self, dt):
        if self.sound.status == "stop":
            Clock.unschedule(self.update_progress)
            self.localSongPos += 1
            if self.localSongPos == len(self.playList):
                # se shuffle, foda-se
                # se repeat:
                self.localSongPos = 0
                # se nada: da um stop e localsongpos = 0
            self.load_song(None, self.playList[self.localSongPos])
            self.__play_music()
            # goes to the next song
            # change button play stop if there's not a next song
        self.currentSongPosition = self.sound.get_pos()
        self.progressBarPosition = (self.currentSongPosition * 100.0)/self.currentSongDuration

    def set_volume(self, value):
        self.volume = value
        if self.sound:
            self.sound.volume = value

    def change_track(self, widget):
        self.localSong.track = widget.text

    def change_title(self, widget):
        self.localSong.title = widget.text

    def change_album(self, widget):
        self.localSong.album = widget.text

    def change_artist(self, widget):
        self.localSong.band = widget.text

    def save_metadata(self):
        changeFields(self.localSong.path,
                     self.localSong.track,
                     self.localSong.title,
                     self.localSong.album,
                     self.localSong.band)

if __name__ == '__main__':
    MusicLibraryApp().run()
