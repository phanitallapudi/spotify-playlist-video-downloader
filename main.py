from pytube import YouTube
from spotipy.oauth2 import SpotifyOAuth
from youtubesearchpython import VideosSearch
import re
import spotipy
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def extract_playlist_id(playlist_url):
    # Define a regular expression pattern to match the playlist ID
    pattern = r'/playlist/([a-zA-Z0-9]+)'

    # Use re.search to find the playlist ID in the URL
    match = re.search(pattern, playlist_url)

    # Check if a match was found
    if match:
        playlist_id = match.group(1)
        return playlist_id
    else:
        return None

def download_youtube_video(video_url, save_path):
    try:
        # Creating a YouTube object for the given video URL
        yt = YouTube(video_url)

        #video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video_stream = yt.streams.get_highest_resolution()

        # Download the video to the specified save path
        video_stream.download(output_path=save_path)
        #print("Video downloaded successfully!")

    except Exception as e:
        print(f"Error: {e}")

def videosSearch(string):
    #returns the top most link of the search results
    videosSearch = VideosSearch(string, limit = 1)
    return videosSearch.result()['result'][-1]['link']

def get_playlist_tracks(playlist_id):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='CLIENT_ID_OF_YOUR_SPOTIFY_DEVELOPERS_API_HERE',
                                                   client_secret='CLIENT_SECRET_OF_YOUR_SPOTIFY_DEVELOPERS_API_HERE',
                                                   redirect_uri='REDIRECT_URL_HERE_OF_YOUR_SPOTIFY_DEVELOPERS_API',
                                                   scope='playlist-read-private'))

    song_names = []
    results = sp.playlist_tracks(playlist_id)

    while results:
        for item in results['items']:
            track = item['track']
            song_names.append(track['name'])
            #adding the song name to the list

        results = sp.next(results)

    return song_names

if __name__ == "__main__":

    modules = ["pytube", "spotipy", "youtube-search-python"]
    for module in modules:
        if module not in sys.modules:
            install(module)

    playlist_link = input("Enter the url of the playlist you want to: ") #playlist your goes here
    playlist_id = extract_playlist_id(playlist_link) #extracting the playlist id from the url

    songs = get_playlist_tracks(playlist_id)

    if songs:
        for index, song in enumerate(songs, 1):
            video_url = videosSearch(song)
            save_path = "./videos/"  # Replace this with the path where you want to save the downloaded video
            download_youtube_video(video_url, save_path)
            print(f'{index}. "{song}" with url : "{video_url}" downloaded successfully')
    else:
        print("Failed to fetch playlist data.")
