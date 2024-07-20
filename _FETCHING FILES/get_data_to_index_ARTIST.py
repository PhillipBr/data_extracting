import spotipy
import json
from spotipy.exceptions import SpotifyException
import index

token_info = index.sp_oauth.get_cached_token()
token = token_info["access_token"] if token_info else None

if not token:
    raise ValueError("Token not found. Please run index.py to obtain the token.")

sp = spotipy.Spotify(auth=token)

ARTISTS_LIST_A = ["BABYMETAL"]

JSON_PATH = r"SI_ADAPT0.json"


def read_existing_song_data(json_path):
    try:
        with open(json_path, "r") as f:
            content = f.read()
            if not content.strip():  # Check if the file is empty or contains only whitespace
                return []
            return json.loads(content)
    except FileNotFoundError:
        return []

def write_to_json(json_path, data):
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)

def collect_unique_songs(artist_name, start_id):
    existing_data = read_existing_song_data(JSON_PATH)
    next_song_id = start_id + len(existing_data) if existing_data else start_id

    unique_songs = set((entry['Artist'], entry['Title']) for entry in existing_data)

    offset = 0
    LIMIT = 50
    new_data = []

    while True:
        if offset >= 1000:
            break

        results = sp.search(q=f'artist:{artist_name}', type='track', limit=LIMIT, offset=offset)
        tracks = results['tracks']['items']

        if not tracks:
            break

        for track in tracks:
            artist = track['artists'][0]['name']
            title = track['name']

            if artist != artist_name:
                continue

            if (artist, title) in unique_songs:
                continue

            unique_songs.add((artist, title))

            new_data.append({
                "SongID": f"{next_song_id}",
                "Artist": artist,
                "Title": title
            })
            next_song_id += 1

        offset += LIMIT

    existing_data += new_data
    write_to_json(JSON_PATH, existing_data)

def collect_songs_for_artists(start_id=500000):
    for artist in ARTISTS_LIST_A:
        collect_unique_songs(artist, start_id)

collect_songs_for_artists()
