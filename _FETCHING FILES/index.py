import os
from flask import Flask, request, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)


scopes = "ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing streaming app-remote-control user-read-email user-read-private playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private"

sp_oauth = SpotifyOAuth(
    client_id="client_id",
    client_secret="client_secret",
    redirect_uri="redirect_uri",
    scope=scopes,
    cache_path="your_cache_path_here"
)


@app.route("/")
def index():
    return redirect("/login")


@app.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route("/callback")
def callback():
    error = request.args.get("error")
    code = request.args.get("code")
    state = request.args.get("state")

    print(f"Received code: {code}")

    if error:
        print(f"Callback Error: {error}")
        return f"Callback Error: {error}"

    try:
        token_info = sp_oauth.get_access_token(code)
        access_token = token_info["access_token"]
        refresh_token = token_info["refresh_token"]
        expires_in = token_info["expires_in"]

        print(f"access_token: {access_token}")
        print(f"refresh_token: {refresh_token}")
        print(f"Successfully retrieved access token. Expires in {expires_in} s.")

        return "Success! You can now close the window."

    except Exception as e:
        print(f"Error getting Tokens: {e}, {str(e.args)}")
        return f"Error getting Tokens: {e}, {str(e.args)}"


if __name__ == "__main__":
    app.run(port=5000, debug=True)




