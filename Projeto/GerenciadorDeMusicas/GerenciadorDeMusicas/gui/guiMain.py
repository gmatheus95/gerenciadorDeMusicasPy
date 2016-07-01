import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.selectableview import SelectableView
from kivy.uix.listview import ListView, ListItemButton
from kivy.lang import Builder
from kivy.factory import Factory

from fixtures import integers_dict

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

class AudioButton(Button):
    filename = StringProperty(None)
    sound = ObjectProperty(None, allownone=True)
    volume = NumericProperty(1.0)

    def on_press(self):
        if self.sound is None:
            self.sound = SoundLoader.load(self.filename)
        # stop the sound if it's currently playing
        if self.sound.status != 'stop':
            self.sound.stop()
        self.sound.volume = self.volume
        self.sound.play()

    def release_audio(self):
        if self.sound:
            self.sound.stop()
            self.sound.unload()
            self.sound = None

    def set_volume(self, volume):
        self.volume = volume
        if self.sound:
            self.sound.volume = volume


class AudioBackground(BoxLayout):
    pass


class MusicLibraryApp(App):
    def build(self):
        root = AudioBackground(spacing=5)

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
        return root

    def release_audio(self):
        for audiobutton in self.root.ids.sl.children:
            audiobutton.release_audio()

    def set_volume(self, value):
        for audiobutton in self.root.ids.sl.children:
            audiobutton.set_volume(value)

if __name__ == '__main__':
    MusicLibraryApp().run()
