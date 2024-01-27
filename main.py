import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random


def beker():
    return input('>>> ')


def main():
    # spotify osztály létrehozása
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    # előadó kiválasztása
    print('Ez egy olyan játék amely során meg kell adnod kedvenc előadódat, majd az egyik albumját. Ennek az albumnak '
          'véletlenszerűen kiválasztom egy egy dalát aminek ki kell találnod a leghosszabb szavát!')
    print('-----------------------------------------------------------------------------------------------------------')
    print('Tehát? Ki a kedvenc előadód?')
    eloado = beker()

    # előadó keresése
    result = sp.search(q=eloado, limit=10, type='artist')

    artists = result['artists']['items']
    szamlalo = 0

    limit = 10
    index = 1
    while result['artists']['next'] and index < limit:
        results = sp.next(result['artists'])
        artists.extend(results['artists']['items'])
        index += 1

    eloadok = []
    for item in artists:
        eloadok.append({'srsz': szamlalo, 'nev': item['name'], 'id': item['id'], 'popularity': item['popularity']})
        szamlalo += 1

    for elem in eloadok:
        print(elem['srsz'], ':', elem['nev'], ', popularity:', elem['popularity'])

    print('Ezeket az előadókat találtuk a megadott név alapján')
    print('a sorszám beírásával tudsz választani közülük')
    valasztas = int(beker())

    print('')
    print('---------------------------------------------------------------------------')

    resp2 = sp.artist_albums(eloadok[valasztas]['id'], album_type='album', limit=50)

    albumok = []
    szamlalo = 0
    for _ in resp2['items']:
        albumok.append({'id': _['id'], 'name': _['name'], 'srsz': szamlalo})
        szamlalo += 1

    for _ in albumok:
        print(_['srsz'], ':', _['name'])

    print('ezek a megadott előadó albumai')
    print('a sorszám beírásával tudsz választani közülük')
    valasztas = int(beker())

    resp3 = sp.album_tracks(albumok[valasztas]['id'])
    dalok = []
    for dal in resp3['items']:
        dalok.append(dal['name'])

    cim = dalok[random.randint(0, len(dalok)-1)]
    cim = cim.split(' ')
    leghosszabb = cim[0]
    for legh in cim:
        if len(legh) > len(leghosszabb):
            leghosszabb = legh

    leghosszabbak = []
    for _ in cim:
        if len(_) == len(leghosszabb):
            leghosszabbak.append(_)

    leghosszabb = leghosszabbak[random.randint(0, len(leghosszabbak)-1)]
    for szo in cim:
        if szo == leghosszabb:
            for unds in szo:
                print('_', end='')
            print(' ', end='')
        else:
            print(szo, end=' ')

    print('')

    print('találd ki a hiányzó szót! (Az aláhúzások száma megegyezik a betűk számával)')
    valasz = beker()
    if valasz.lower() == leghosszabb.lower():
        print('Eltaláltad!')
    else:
        print('sanjos nem találtad el! A helyes megfejtés:', leghosszabb)


main()