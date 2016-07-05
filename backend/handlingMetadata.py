from mutagen.mp3 import MP3
from mutagen import MutagenError
from mutagen.id3 import ID3, TIT2, TALB, TRCK, TPE1



def retrieveFields(path):

    try:
        audio = ID3(path)
    except MutagenError:
        return -1

    track = (audio['TRCK'].text[0] if (audio.getall('TRCK') != []) else 'unknown')
    title = (audio['TIT2'].text[0] if (audio.getall('TIT2') != []) else 'unknown')
    album = (audio['TALB'].text[0] if (audio.getall('TALB') != []) else 'unknown')
    band = (audio['TPE1'].text[0] if (audio.getall('TPE1') != []) else 'unknown')
    audio = MP3(path)
    duration = audio.info.length

    fields = {'track': track, 'title': title, 'album': album, 'band': band, 'duration': duration}
    return fields


def changeFields(path, track, title, album, band):
    audio = ID3(path)

    audio['TRCK'] = TRCK(encoding=3, text=track)
    audio['TIT2'] = TIT2(encoding=3, text=title)
    audio['TALB'] = TALB(encoding=3, text=album)
    audio['TPE1'] = TPE1(encoding=3, text=band)
    # To work properly in Windows
    audio.update_to_v23()
    audio.save(v2_version=3)
    print('Metadata saved successfully.')
