import json
import time
import glob
import spotipy
from spotipy.exceptions import SpotifyException
import index

token_info = index.sp_oauth.get_cached_token()
token = token_info["access_token"] if token_info else None

if not token:
    raise ValueError("Token not found. Please run index.py to obtain the token.")

sp = spotipy.Spotify(auth=token)

# Corrected path for Songs_Index_REPAIR_2.json
song_index_repair_files = glob.glob("../DATA/Songs_Index_REPAIR_1.json")

repair_song_ids = set()
for file in song_index_repair_files:
    with open(file, "r", encoding="utf-8") as f:  # Specify UTF-8 encoding here
        song_index_data = json.load(f)
        repair_song_ids.update(str(song['SongID']) for song in song_index_data)

def find_songs_by_artist(song_id, artist, title):
    try:
        results = sp.search(q=f'artist:"{artist}" track:"{title}"', type='track', limit=1)

        if not results['tracks']['items']:
            primary_artist = artist.split(" Featuring")[0].split(" &")[0]
            results = sp.search(q=f'artist:"{primary_artist}" track:"{title}"', type='track', limit=1)

            if not results['tracks']['items']:
                results = sp.search(q=f'{primary_artist} {title}', type='track', limit=1)

                if not results['tracks']['items']:
                    print(f"Could not find track {title} by {artist}.")
                    return

        track = results['tracks']['items'][0]
        artist_id = track['artists'][0]['id']

        artist_info = sp.artist(artist_id)
        genres = ", ".join(artist_info['genres'])

        duration = (track['duration_ms'] / 60000 % 60)
        duration = f"{int(duration):02d}:{int(duration * 60) % 60:02d}"

        cover_image_url = "No Cover Image Available"
        if 'images' in track['album'] and len(track['album']['images']) > 0:
            cover_image_url = track['album']['images'][0]['url']

        song_info = {
            "SongID": song_id,
            "Album": track['album']['name'],
            "Duration": duration,
            "CoverImage": cover_image_url,
            "Popularity": track['popularity'],
            "ReleaseDate": track['album']['release_date'],
            "Genre": genres
        }

        print(f"{song_id} - '{title}' by '{artist}' is added to Song_Index_Test.json")

        tracks_songs_dict[song_id] = song_info

    except SpotifyException as e:
        print(f"Spotify exception: {e}")

# Corrected path for Tracks_Songs_tester.json
tracks_songs_file_path = "../DATA/Tracks_Songs_tester.json"

try:
    with open(tracks_songs_file_path, "r", encoding="utf-8") as f:  # Specify UTF-8 encoding here
        tracks_songs_dict = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    tracks_songs_dict = {}

for file in song_index_repair_files:
    with open(file, "r", encoding="utf-8") as f:  # Specify UTF-8 encoding here
        song_index_data = json.load(f)
        for song in song_index_data:
            song_id = str(song['SongID'])
            if song_id in tracks_songs_dict:
                print(f"Skipping SongID {song_id} as it is already present in Tracks_Songs_tester.json.")
                continue
            print(f"Searching for the track '{song['Title']}' by '{song['Artist']}'...")
            find_songs_by_artist(song_id, song['Artist'], song['Title'])
            time.sleep(1)  # To avoid rate limiting

            with open(tracks_songs_file_path, "w", encoding="utf-8") as f:  # Specify UTF-8 encoding here
                json.dump(list(tracks_songs_dict.values()), f, indent=4)
