import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def get_albums(artist):
    results = sp.search(q=artist, limit=1, type='artist')
    if not results['artists']['items']:
        return None
    artist_id = results['artists']['items'][0]['id']

    albums = []
    results = sp.artist_albums(artist_id=artist_id, album_type='album', limit=50)
    albums.extend(results['items'])

    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])

    album_titles = [album['name'] for album in albums]
    return album_titles


def album(titles):
    random_index = random.randint(0, len(titles) - 1)
    return titles[random_index]


def clear(title):
    words = title.split()
    long_word = words[0]
    for word in words:
        if len(word) > len(long_word):
            long_word = word
    secret_word = '_' * len(long_word)
    secret_title = title.replace(long_word, secret_word, 1)
    return secret_title, long_word


def main():
    artist_name = input("Add meg az előadó nevét: ")

    albums = get_albums(artist_name)
    if not albums:
        print("Nem található ilyen előadó.")
        return

    random_album = album(albums)

    secret_title, long_word = clear(random_album)
    print(f"Album: {secret_title}")

    guess = input("Találd ki az album címéből hiányzó szót: ")
    if guess.lower() == long_word.lower():
        print("Helyes!")
    else:
        print("Nem. A helyes szó:", long_word)


main()
