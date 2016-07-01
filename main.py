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


class MusicLibraryApp(App):
    filename = StringProperty(None)
    sound = ObjectProperty(None, allownone=True)
    volume = NumericProperty(1.0)
    currentSongDuration = NumericProperty(None)
    currentSongPosition = NumericProperty(None)
    progressBarPosition = NumericProperty(100)

    kv_directory = 'gui'

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

        # Setting clock for progress bar
        Clock.schedule_interval(self.update_progress, 0.5)

        return root

    def update_progress(self, dt):
        pass

    def view_albums(self, root):
        if root.ids["miscPanel"].children:
            root.ids["miscPanel"].clear_widgets()
        album_view = AlbumViewer()
        root.ids["miscPanel"].add_widget(album_view)

        button = Button(text=controller.allAlbums[0].getName(), size=(200,200), size_hint=(None,None))
        album_view.add_widget(button)

    def view_metadata(self, root):
        if root.ids["miscPanel"].children:
            root.ids["miscPanel"].clear_widgets()
        metadata_view = MetadataEditor()
        root.ids["miscPanel"].add_widget(metadata_view)

    def play_music(self):
        self.filename = 'gui\c.mp3'
        if self.sound is None:
            self.sound = SoundLoader.load(self.filename)

        self.currentSongDuration = self.sound.length
        print(self.sound.get_pos())

        # stop the sound if it's currently playing
        if self.sound.status != 'stop':
            self.sound.stop()
        else:
            self.sound.volume = self.volume
            self.sound.play()

    def set_volume(self, value):
        self.volume = value
        if self.sound:
            self.sound.volume = value

if __name__ == '__main__':
    MusicLibraryApp().run()
