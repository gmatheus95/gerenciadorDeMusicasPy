import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.selectableview import SelectableView
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.slider import Slider
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.clock import Clock

from backend.managerController import *
from gui.fixtures import integers_dict

kivy.require('1.0.8')

# Lists definitions
Factory.register('SelectableView', cls=SelectableView)
Factory.register('ListItemButton', cls=ListItemButton)
Builder.load_string('''
[CustomListItem@SelectableView+BoxLayout]:
    size_hint_y: ctx.size_hint_y
    height: ctx.height
    ListItemButton:
        text: ctx.text
        is_selected: ctx.is_selected
''')

controller = ManagerControllerSingleton()

# class AudioButton(Button):
#     filename = StringProperty(None)
#     sound = ObjectProperty(None, allownone=True)
#     volume = NumericProperty(1.0)
#
#     def on_press(self):
#         if self.sound is None:
#             self.sound = SoundLoader.load(self.filename)
#         # stop the sound if it's currently playing
#         if self.sound.status != 'stop':
#             self.sound.stop()
#         self.sound.volume = self.volume
#         self.sound.play()
#
#     def release_audio(self):
#         if self.sound:
#             self.sound.stop()
#             self.sound.unload()
#             self.sound = None
#
#     def set_volume(self, volume):
#         self.volume = volume
#         if self.sound:
#             self.sound.volume = volume


class AudioBackground(BoxLayout):
    pass


class MetadataEditor(BoxLayout):
    pass


class AlbumViewer(GridLayout):
    pass

class ArtistViewer(GridLayout):
    pass


class MusicLibraryApp(App):
    filename = StringProperty(None)
    sound = ObjectProperty(None, allownone=True)
    localSong = None
    volume = NumericProperty(1.0)
    currentSongDuration = NumericProperty(None)
    currentSongPosition = NumericProperty(None)
    progressBarPosition = NumericProperty(0)

    kv_directory = 'gui'

    def load_song(self, song):
        self.localSong = song
        self.filename = song.path
        self.sound = SoundLoader.load(self.filename)
        self.currentSongPosition = 0

    def build(self):
        root = AudioBackground(spacing=5)

        # Instantiating list of musics
        list_item_args_converter = \
            lambda row_index, rec: {'text': rec['text'],
                                    'is_selected': rec['is_selected'],
                                    'size_hint_y': None,
                                    'height': 25}

        # Here we create a dict adapter with 1..100 integer strings as
        # sorted_keys, and integers_dict from fixtures as data, passing our
        # CompositeListItem kv template for the list item view. Then we
        # create a list view using this adapter. args_converter above converts
        # dict attributes to ctx attributes.
        dict_adapter = DictAdapter(sorted_keys=[str(i) for i in range(100)],
                                   data=integers_dict,
                                   args_converter=list_item_args_converter,
                                   template='CustomListItem')

        list_view = ListView(adapter=dict_adapter)

        root.ids["musicPanel"].add_widget(list_view)

        # Initializing components
        controller.initialize_components()

        # TODO: REMOVER DEPOIS DO TESTE
        self.load_song(controller.allSongs[5])
        print(controller.allSongs[5].path)

        return root

    def import_songs(self, root):
        controller.import_song()

    def view_albums(self, root):
        if root.ids["miscPanel"].children:
            root.ids["miscPanel"].clear_widgets()
        album_view = AlbumViewer()
        root.ids["miscPanel"].add_widget(album_view)

        buttonList = []
        for album in controller.allAlbums:
            buttonList.append(Button(text=album.getName(), size=(200, 200), size_hint=(None, None)))
            album_view.add_widget(buttonList[len(buttonList)-1])

    def view_artists(self, root):
        if root.ids["miscPanel"].children:
            root.ids["miscPanel"].clear_widgets()
        artist_view = ArtistViewer()
        root.ids["miscPanel"].add_widget(artist_view)

        buttonList = []
        for artist in controller.allArtists:
            buttonList.append(Button(text=artist.getName(), size=(200, 200), size_hint=(None, None)))
            artist_view.add_widget(buttonList[len(buttonList) - 1])

    def view_metadata(self, root):
        if root.ids["miscPanel"].children:
            root.ids["miscPanel"].clear_widgets()
        metadata_view = MetadataEditor()
        root.ids["miscPanel"].add_widget(metadata_view)

    def play_music(self):
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

    def update_progress(self, dt):
        self.currentSongPosition = self.sound.get_pos()
        if self.currentSongPosition > 0:
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
