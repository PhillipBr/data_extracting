import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import json

def get_top_tracks(date, track_count):
    try:
        response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/", headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        web_page = response.text

        soup = BeautifulSoup(web_page, "html.parser")

        titles = soup.select("li ul h3")
        artistname = soup.select("li ul li span.c-label")

        tracks = []
        num_tracks = min(len(titles), len(artistname) // 7)

        for i in range(num_tracks):
            title = titles[i].text.strip()
            artist_name = artistname[i * 7].text.strip().split("\n")[0]
            song_id = f"B{date[:4]}{str(track_count + i + 1).zfill(4)}"
            tracks.append({"SongID": song_id, "Title": title, "Artist": artist_name})

        return tracks
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data for {date}: {e}")
        return []

def get_tracks_for_years(start_year, end_year):
    start_date = datetime.strptime(f"{start_year}-01-01", "%Y-%m-%d")
    end_date = datetime.strptime(f"{end_year}-12-31", "%Y-%m-%d")
    unique_tracks = {}
    track_count = 0

    while start_date <= end_date:
        date_str = start_date.strftime("%Y-%m-%d")
        top_tracks = get_top_tracks(date_str, track_count)
        for track in top_tracks:
            key = (track['Title'], track['Artist'])
            if key not in unique_tracks:
                unique_tracks[key] = track
                print(f"Title: {track['Title']}, Artist: {track['Artist']}")
                track_count += 1
        print(f"Fetched top tracks for {date_str}")
        start_date += timedelta(weeks=1)
        time.sleep(1)

    output_file_path = f"Billboard_Trends_{start_year}_to_{end_year}.json"
    with open(output_file_path, "w") as f:
        json.dump(list(unique_tracks.values()), f, indent=4)

    print(f"Unique tracks from {start_year} to {end_year} saved to {output_file_path}")

if __name__ == "__main__":
    start_year = 1990
    end_year = 1999
    get_tracks_for_years(start_year, end_year)
