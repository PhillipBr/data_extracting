import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

client_id = 'client_id'
client_secret = 'client_secret'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = {
    "global": "37i9dQZEVXbMDoHDwVN2tF",
    "united states": "37i9dQZEVXbLRQDuF5jeBp",
    "united kingdom": "37i9dQZEVXbLnolsZ8PSNw",
    "andorra": "37i9dQZEVXbMxjQJh4Um8T",
    "argentina": "37i9dQZEVXbMMy2roB9myp",
    "austria": "37i9dQZEVXbKNHh6NIXu36",
    "australia": "37i9dQZEVXbJPcfkRz0wJ0",
    "bulgaria": "37i9dQZEVXbNfM2w2mq1B8",
    "belgium": "37i9dQZEVXbLy5tBFyQvd4",
    "bolivia": "37i9dQZEVXbJqfMFK4d691",
    "brazil": "37i9dQZEVXbMXbN3EUUhlg",
    "canada": "37i9dQZEVXbKj23U1GF4IR",
    "switzerland": "37i9dQZEVXbJiyhoAPEfMK",
    "chile": "37i9dQZEVXbL0GavIqMTeb",
    "colombia": "37i9dQZEVXbOa2lmxNORXQ",
    "costa rica": "37i9dQZEVXbMZAjGMynsQX",
    "czech republic": "37i9dQZEVXbIP3c3fqVrJY",
    "germany": "37i9dQZEVXbJiZcmkrIHGU",
    "denmark": "37i9dQZEVXbL3J0k32lWnN",
    "dominican republic": "37i9dQZEVXbKAbrMR8uuf7",
    "ecuador": "37i9dQZEVXbJlM6nvL1nD1",
    "estonia": "37i9dQZEVXbLesry2Qw2xS",
    "spain": "37i9dQZEVXbNFJfN1Vw8d9",
    "finland": "37i9dQZEVXbMxcczTSoGwZ",
    "france": "37i9dQZEVXbIPWwFssbupI",
    "greece": "37i9dQZEVXbJqdarpmTJDL",
    "guatemala": "37i9dQZEVXbLy5tBFyQvd4",
    "hong kong": "37i9dQZEVXbLwpL8TjsxOG",
    "honduras": "37i9dQZEVXbJp9wcIM9Eo5",
    "hungary": "37i9dQZEVXbNHwMxAkvmF8",
    "indonesia": "37i9dQZEVXbObFQZ3JLcXt",
    "ireland": "37i9dQZEVXbKM896FDX8L1",
    "israel": "37i9dQZEVXbJ6IpvItkve3",
    "india": "37i9dQZEVXbLZ52XmnySJg",
    "iceland": "37i9dQZEVXbKMzVsSGQ49S",
    "italy": "37i9dQZEVXbIQnj7RRhdSX",
    "japan": "37i9dQZEVXbKXQ4mDTEBXq",
    "south korea": "37i9dQZEVXbNxXF4SkHj9F",
    "lithuania": "37i9dQZEVXbMx56Rdq5lwc",
    "luxembourg": "37i9dQZEVXbKGcyg6TFGx6",
    "latvia": "37i9dQZEVXbJWuzDrTxbKS",
    "mexico": "37i9dQZEVXbO3qyFxbkOE1",
    "malaysia": "37i9dQZEVXbJlfUljuZExa",
    "nicaragua": "37i9dQZEVXbISk8kxnzfCq",
    "netherlands": "37i9dQZEVXbKCF6dqVpDkS",
    "norway": "37i9dQZEVXbJvfa0Yxg7E7",
    "new zealand": "37i9dQZEVXbM8SIrkERIYl",
    "panama": "37i9dQZEVXbKypXHVwk1f0",
    "peru": "37i9dQZEVXbJfdy5b0KP7W",
    "philippines": "37i9dQZEVXbNBz9cRCSFkY",
    "poland": "37i9dQZEVXbN6itCcaL3Tt",
    "portugal": "37i9dQZEVXbKyJS56d1pgi",
    "paraguay": "37i9dQZEVXbNOUPGj7tW6T",
    "romania": "37i9dQZEVXbNZbJ6TZelCq",
    "sweden": "37i9dQZEVXbLoATJ81JYXz",
    "singapore": "37i9dQZEVXbK4gjvS1FjPY",
    "slovakia": "37i9dQZEVXbKIVTPX9a2Sb",
    "el salvador": "37i9dQZEVXbLxoIml4MYkT",
    "thailand": "37i9dQZEVXbMnz8KIWsvf9",
    "turkey": "37i9dQZEVXbIVYVBNw9D5K",
    "taiwan": "37i9dQZEVXbMnZEatlMSiu",
    "uruguay": "37i9dQZEVXbMJJi3wgRbAy",
    "vietnam": "37i9dQZEVXbLdGSmz6xilI",
    "south africa": "37i9dQZEVXbMH2jvi6jvjk"
}

with open('reg_spotify.json', 'w') as outfile:
    outfile.write('[')

    first = True
    song_id = 1000000

    for country, playlist_id in playlists.items():
        results = sp.playlist_tracks(playlist_id)
        while results:
            for item in results['items']:
                track = item['track']
                title = track['name']
                artist = track['artists'][0]['name']

                song_data = {

                    'SongID': song_id,
                    'Title': title,
                    'Artist': artist

                }
                print(f'"{title}" by "{artist}" is in the database')


                if not first:
                    outfile.write(',\n')
                json.dump(song_data, outfile)
                first = False

                song_id += 1
                print(f'"{title}" by "{artist}" saved correctly')

            if results['next']:
                results = sp.next(results)
            else:
                results = None

    outfile.write(']')

print('All data extracted and saved to reg_spotify.json.')
