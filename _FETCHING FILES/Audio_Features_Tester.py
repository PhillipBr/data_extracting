import json
import time
import glob
import spotipy
from spotipy.exceptions import SpotifyException
import index

key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

token_info = index.sp_oauth.get_cached_token()
token = token_info["access_token"] if token_info else None

if not token:
    raise ValueError("Token not found. Please run index.py to obtain the token.")

sp = spotipy.Spotify(auth=token)

audio_features_dict = {}
audio_features_file_path = "../DATA/Audio_Features_Tester.json"

try:
    with open(audio_features_file_path, "r") as f:
        audio_features_dict = json.load(f)
except FileNotFoundError:
    print("Audio_Features_Tester.json not found. Starting with an empty dictionary.")


def get_audio_features(song_id, track_id):
    audio_features = sp.audio_features([track_id])[0]
    if audio_features is None:
        print(f"No audio features found for SongID {song_id} with TrackID {track_id}")
        return

    key = key_names[audio_features['key']]
    if audio_features['mode'] == 0:
        key = key + "m"
    audio_data = {
        "SongID": song_id,
        "Key": key,
        "Energy": audio_features['energy'],
        "Danceability": audio_features['danceability'],
        "Loudness": audio_features['loudness'],
        "Speechiness": audio_features['speechiness'],
        "Acousticness": audio_features['acousticness'],
        "Instrumentalness": audio_features['instrumentalness'],
        "Liveness": audio_features['liveness'],
        "Valence": audio_features['valence'],
        "Tempo": audio_features['tempo'],
        "TimeSignature": audio_features['time_signature']
    }
    print(f"{song_id} is added to Audio_Features_Tester.json")
    audio_features_dict[song_id] = audio_data


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
        get_audio_features(song_id, track['id'])
    except SpotifyException as e:
        print(f"Spotify exception: {e}")

song_index_repair_files = glob.glob("../DATA/Songs_Index_REPAIR_*.json")
for file in song_index_repair_files:
    with open(file, "r", encoding="utf-8") as f:
        song_index_data = json.load(f)
        for song in song_index_data:
            song_id = str(song['SongID'])
            if song_id in audio_features_dict:
                print(f"Skipping SongID {song_id} as it is already present in Audio_Features_Tester.json.")
                continue
            print(f"Searching for the track '{song['Title']}' by '{song['Artist']}'...")
            find_songs_by_artist(song_id, song['Artist'], song['Title'])
            time.sleep(1)

            with open(audio_features_file_path, "w", encoding="utf-8") as f:
                json.dump(list(audio_features_dict.values()), f, indent=4)
