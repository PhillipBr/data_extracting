import requests
from bs4 import BeautifulSoup
import json
import os


def get_top_tracks(urls):
    unique_tracks = set()
    all_tracks = []

    song_id = 700000

    for url in urls:
        response = requests.get(url)
        if response.encoding is None or response.encoding == 'ISO-8859-1':
            response.encoding = 'utf-8'
        web_page = response.text

        soup = BeautifulSoup(web_page, "html.parser")
        rows = soup.select("table tbody tr")

        for row in rows:
            columns = row.find_all('td')
            if len(columns) > 0:
                links = columns[0].find_all('a')
                if len(links) >= 2:
                    artist = links[0].text.strip()
                    title = links[1].text.strip()
                    if (title, artist) not in unique_tracks:
                        unique_tracks.add((title, artist))
                        all_tracks.append({
                            "SongID": str(song_id),
                            "Title": title,
                            "Artist": artist
                        })
                        song_id += 1

    return all_tracks


def save_to_json(data, filename):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    urls = [
        "https://kworb.net/spotify/country/global_daily_totals.html",
        "https://kworb.net/spotify/country/us_daily_totals.html",
        "https://kworb.net/spotify/country/gb_daily_totals.html",
        "https://kworb.net/spotify/country/ad_daily_totals.html",
        "https://kworb.net/spotify/country/ar_daily_totals.html",
        "https://kworb.net/spotify/country/au_daily_totals.html",
        "https://kworb.net/spotify/country/at_daily_totals.html",
        "https://kworb.net/spotify/country/by_daily_totals.html",
        "https://kworb.net/spotify/country/be_daily_totals.html",
        "https://kworb.net/spotify/country/bo_daily_totals.html",
        "https://kworb.net/spotify/country/br_daily_totals.html",
        "https://kworb.net/spotify/country/bg_daily_totals.html",
        "https://kworb.net/spotify/country/ca_daily_totals.html",
        "https://kworb.net/spotify/country/cl_daily_totals.html",
        "https://kworb.net/spotify/country/co_daily_totals.html",
        "https://kworb.net/spotify/country/cr_daily_totals.html",
        "https://kworb.net/spotify/country/cy_daily_totals.html",
        "https://kworb.net/spotify/country/cz_daily_totals.html",
        "https://kworb.net/spotify/country/dk_daily_totals.html",
        "https://kworb.net/spotify/country/do_daily_totals.html",
        "https://kworb.net/spotify/country/ec_daily_totals.html",
        "https://kworb.net/spotify/country/eg_daily_totals.html",
        "https://kworb.net/spotify/country/sv_daily_totals.html",
        "https://kworb.net/spotify/country/ee_daily_totals.html",
        "https://kworb.net/spotify/country/fi_daily_totals.html",
        "https://kworb.net/spotify/country/fr_daily_totals.html",
        "https://kworb.net/spotify/country/de_daily_totals.html",
        "https://kworb.net/spotify/country/gr_daily_totals.html",
        "https://kworb.net/spotify/country/gt_daily_totals.html",
        "https://kworb.net/spotify/country/hn_daily_totals.html",
        "https://kworb.net/spotify/country/hk_daily_totals.html",
        "https://kworb.net/spotify/country/hu_daily_totals.html",
        "https://kworb.net/spotify/country/is_daily_totals.html",
        "https://kworb.net/spotify/country/in_daily_totals.html",
        "https://kworb.net/spotify/country/id_daily_totals.html",
        "https://kworb.net/spotify/country/ie_daily_totals.html",
        "https://kworb.net/spotify/country/il_daily_totals.html",
        "https://kworb.net/spotify/country/it_daily_totals.html",
        "https://kworb.net/spotify/country/jp_daily_totals.html",
        "https://kworb.net/spotify/country/kz_daily_totals.html",
        "https://kworb.net/spotify/country/lv_daily_totals.html",
        "https://kworb.net/spotify/country/lt_daily_totals.html",
        "https://kworb.net/spotify/country/lu_daily_totals.html",
        "https://kworb.net/spotify/country/my_daily_totals.html",
        "https://kworb.net/spotify/country/mt_daily_totals.html",
        "https://kworb.net/spotify/country/mx_daily_totals.html",
        "https://kworb.net/spotify/country/ma_daily_totals.html",
        "https://kworb.net/spotify/country/nl_daily_totals.html",
        "https://kworb.net/spotify/country/nz_daily_totals.html",
        "https://kworb.net/spotify/country/ni_daily_totals.html",
        "https://kworb.net/spotify/country/ng_daily_totals.html",
        "https://kworb.net/spotify/country/no_daily_totals.html",
        "https://kworb.net/spotify/country/pk_daily_totals.html",
        "https://kworb.net/spotify/country/pa_daily_totals.html",
        "https://kworb.net/spotify/country/py_daily_totals.html",
        "https://kworb.net/spotify/country/pe_daily_totals.html",
        "https://kworb.net/spotify/country/ph_daily_totals.html",
        "https://kworb.net/spotify/country/pl_daily_totals.html",
        "https://kworb.net/spotify/country/pt_daily_totals.html",
        "https://kworb.net/spotify/country/ro_daily_totals.html",
        "https://kworb.net/spotify/country/ru_daily_totals.html",
        "https://kworb.net/spotify/country/sa_daily_totals.html",
        "https://kworb.net/spotify/country/sg_daily_totals.html",
        "https://kworb.net/spotify/country/sk_daily_totals.html",
        "https://kworb.net/spotify/country/za_daily_totals.html",
        "https://kworb.net/spotify/country/kr_daily_totals.html",
        "https://kworb.net/spotify/country/es_daily_totals.html",
        "https://kworb.net/spotify/country/se_daily_totals.html",
        "https://kworb.net/spotify/country/ch_daily_totals.html",
        "https://kworb.net/spotify/country/tw_daily_totals.html",
        "https://kworb.net/spotify/country/th_daily_totals.html",
        "https://kworb.net/spotify/country/tr_daily_totals.html",
        "https://kworb.net/spotify/country/ua_daily_totals.html",
        "https://kworb.net/spotify/country/ae_daily_totals.html",
        "https://kworb.net/spotify/country/uy_daily_totals.html",
        "https://kworb.net/spotify/country/ve_daily_totals.html",
        "https://kworb.net/spotify/country/vn_daily_totals.html"

    ]
    top_tracks = get_top_tracks(urls)

    # Relative path to save the JSON file in the specified folder
    json_file_path = os.path.join(os.path.dirname(__file__), "../DATA/SAVED/kworb_tracks.json")
    save_to_json(top_tracks, json_file_path)

    for track in top_tracks:
        print(f"{track['SongID']}. {track['Title']} - {track['Artist']}")
