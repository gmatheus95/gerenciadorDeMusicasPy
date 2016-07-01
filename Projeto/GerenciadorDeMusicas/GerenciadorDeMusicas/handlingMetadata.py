from mutagen.id3 import ID3


def retrieveFields(path):
    audio = ID3(path)

    track = (audio['TRCK'].text[0] if (audio.getall('TRCK') != []) else 'unknown')
    title = (audio['TIT2'].text[0] if (audio.getall('TIT2') != []) else 'unknown')
    album = (audio['TALB'].text[0] if (audio.getall('TALB') != []) else 'unknown')
    band = (audio['TPE1'].text[0] if (audio.getall('TPE1') != []) else 'unknown')

    fields = {'track': track, 'title': title, 'album': album, 'band': band}
    return fields

def changeFields(path, track, title, album, band):
    audio = ID3(path)
    audio['TRCK'].text[0] = track
    audio['TIT2'].text[0] = title
    audio['TALB'].text[0] = album
    audio['TPE1'].text[0] = band

    #to work properly in Windows
    audio.update_to_v23()
    audio.save(v2_version=3)

'''
audio = ID3('C:\\Users\\Guilherme\\Desktop\\Caro Emerald\\A Night Like This.mp3')
print(audio)
#audio['title'] = u'A Night Like This'
#audio['albumartist'] = u'Caro Emerald'
audio.update_to_v23()
audio.save(v2_version=3)

#def changeMetadata(track, title, )
'''