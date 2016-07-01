from mutagen.id3 import ID3

audio = ID3('C:\\Users\\Guilherme\\Desktop\\Caro Emerald\\A Night Like This.mp3')
print(audio)
#audio['title'] = u'A Night Like This'
#audio['albumartist'] = u'Caro Emerald'
audio.update_to_v23()
audio.save(v2_version=3)

