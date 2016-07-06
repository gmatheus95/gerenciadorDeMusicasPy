import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock
from functools import partial
from random import shuffle
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
    volume = NumericProperty(1.0)

    currentSongDuration = NumericProperty(None)
    currentSongPosition = NumericProperty(None)
    progressBarPosition = NumericProperty(0)

    localSong = None
    localSongPos = 0
    currentSongTitle = StringProperty('-')

    kv_directory = 'gui'
    currentState = "allSongs"
    buttonStatus = StringProperty("Play")
    repeatButtonStatus = StringProperty("Repeat")

    onBuild = True

    playList = []
    auxPlaylist = []

    def copy_playlist(self, root, num, nothing=None):
        self.localSong = self.auxPlaylist[num]
        self.localSongPos = num
        self.playList = self.auxPlaylist
        self.load_song(root, self.localSong, num)

    def __load_playlist(self, root, all=True, artist="", band=""):
        self.auxPlaylist = controller.allSongs
        if all == False:  # load all songs!
            self.auxPlaylist = []
            if artist != "":
                ids = artist.getSongs()
            else:
                ids = band.getSongs()
            for songid in ids:
                self.auxPlaylist.append(controller.allSongs[controller.dictSongs[str(songid)]])

    def __append_playlist(self, song, nothing=None):
        self.playList.append(song)

    def __remove_playlist(self, root, index, nothing=None):
        del self.playList[index]
        if self.playList == []:
            self.localSong = None
            self.sound.stop()
            Clock.unschedule(self.update_progress)
            self.sound.unload()
            self.buttonStatus = "Play"
        else:
            if self.localSongPos == index:
                self.localSong = self.playList[index]
                self.sound.stop()
                Clock.unschedule(self.update_progress)
                self.load_song(root,self.localSong,index)
                self.buttonStatus = "Play"
        self.view_playlist(root)

    def clear_playlist(self, root):
        self.playList = []
        self.localSong = None
        try:
            self.sound.stop()
            Clock.unschedule(self.update_progress)
            self.sound.unload()
            self.buttonStatus = "Play"
            self.view_playlist(root)
        except:
            return

    def next_playlist(self, root):
        if self.localSongPos >= (len(self.playList) - 1):
            self.localSongPos = 0
        else:
            self.localSongPos += 1
        self.load_song(root, self.playList[self.localSongPos], self.localSongPos)

    def previous_playlist(self, root):
        if self.localSongPos == 0:
            self.localSongPos = len(self.playList) - 1
        else:
            self.localSongPos -= 1
        self.load_song(root, self.playList[self.localSongPos], self.localSongPos)

    def shuffle_playlist(self, root):
        self.playList[self.localSongPos], self.playList[0] = self.playList[0], self.playList[self.localSongPos]
        copy = []
        for i in range(1, len(self.playList)):
            copy.append(self.playList[i])
        shuffle(copy)
        copy.insert(0, self.playList[0])
        self.playList = copy
        self.localSongPos = 0
        self.view_playlist(root)

    def view_playlist(self, root):
        if root.ids["musicPanel"].children:
            root.ids["musicPanel"].clear_widgets()
        music_view = MusicViewer()
        root.ids["musicPanel"].add_widget(music_view)

        songButtonList = []
        playlistButtonList = []
        for song in self.playList:
            songButtonList.append(Button(text=song.title, size=(50, 30), size_hint=(0.8, None)))
            music_view.add_widget(songButtonList[len(songButtonList) - 1])
            playlistButtonList.append(Button(text="-", size=(50, 30), size_hint=(0.2, None)))
            music_view.add_widget(playlistButtonList[len(playlistButtonList) - 1])

        # If there is a song, load it and binding the buttons
        if len(songButtonList) > 0:
            for num in range(0, len(songButtonList)):
                button_import = partial(self.load_song, root, self.playList[num])
                songButtonList[num].bind(on_press=button_import)
                playlist_button_import = partial(self.__remove_playlist, root, num)
                playlistButtonList[num].bind(on_press=playlist_button_import)

        return root

    def load_song(self,  root, song, num, nothing='nothing'):
        wasPlaying = False
        # TODO: Separate selected song from playing song
        if self.sound:
            if self.sound.state != 'stop':
                wasPlaying = True
                self.sound.stop()
                Clock.unschedule(self.update_progress)
        self.localSong = song
        self.localSongPos = num
        self.currentSongTitle = self.localSong.title + "  --  " + self.localSong.album + "  --  " + self.localSong.band
        self.filename = song.path
        self.sound = SoundLoader.load(self.filename)
        self.currentSongPosition = 0
        if wasPlaying:
            self.__play_music()
        if self.currentState == "metadata":
            self.view_metadata(root)

    def __load_all_songs(self, root, all=True, artist="", band=""):
        if root.ids["musicPanel"].children:
            root.ids["musicPanel"].clear_widgets()
        music_view = MusicViewer()
        root.ids["musicPanel"].add_widget(music_view)

        self.__load_playlist(root, all, artist, band)

        songButtonList = []
        playlistButtonList = []
        for song in self.auxPlaylist:
            songButtonList.append(Button(text=song.title, size=(50, 30), size_hint=(0.8, None)))
            music_view.add_widget(songButtonList[len(songButtonList) - 1])
            playlistButtonList.append(Button(text="+", size=(50, 30), size_hint=(0.2, None)))
            music_view.add_widget(playlistButtonList[len(playlistButtonList) - 1])
            self.localSongPos = 0

        # If there is a song, load it and binding the buttons
        if len(songButtonList) > 0:
            print(self.auxPlaylist)
            if self.onBuild == True:
                self.playList = self.auxPlaylist
                self.load_song(root, self.playList[0], 0, None)
                self.onBuild = False

            for num in range(0, len(songButtonList)):
                button_import = partial(self.copy_playlist, root, num)
                songButtonList[num].bind(on_press=button_import)
                playlist_button_import = partial(self.__append_playlist, self.auxPlaylist[num])
                playlistButtonList[num].bind(on_press=playlist_button_import)

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
            buttonList.append(Button(text=nameToPrint, size_hint=(.3, None)))
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
            buttonList.append(Button(text=nameToPrint, size_hint=(.3, None)))
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
        if self.localSong is not None:
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
        try:
            self.__play_music()
        except:
            return
        if self.sound.status != 'stop':
            self.buttonStatus = 'Stop'
        else:
            self.buttonStatus = 'Play'

    def update_progress(self, dt):
        if self.sound.status == "stop":
            Clock.unschedule(self.update_progress)
            self.localSongPos += 1
            if self.localSongPos == len(self.playList):
                if self.repeatButtonStatus == "Stop rep.":
                    self.localSongPos = 0
                    self.load_song(None, self.playList[self.localSongPos], self.localSongPos)
                    self.__play_music()
                else:
                    self.localSongPos = 0
                    self.sound.stop()
                    self.buttonStatus = "Play"
                    self.load_song(None, self.playList[self.localSongPos], self.localSongPos)
            else:
                self.load_song(None, self.playList[self.localSongPos], self.localSongPos)
                self.__play_music()
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

    def change_repeat_status(self):
        if self.repeatButtonStatus == "Repeat":
            self.repeatButtonStatus = "Stop rep."
        else:
            self.repeatButtonStatus = "Repeat"

if __name__ == '__main__':
    MusicLibraryApp().run()
