import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pprint

# Note, it is expected that you have at least 1 song in your liked playlist and at least 1 album saved.
def remove_duplicates():
    username = 'bs40404'
    scope = 'user-modify-playback-state user-read-playback-state user-library-modify user-library-read'
    client_id = 'e004309d630544a5958730c3057677b3'
    client_secret = '39b2462f03f74330ad65ca09ee3eeadd'
    redirect_uri = 'https://localhost:8080'

    token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
    if token:
        sp = spotipy.Spotify(auth=token)
        # Gather Data from spotify API
        liked_songs = set()
        liked_album_songs = set()

        # Gather all the tracks from liked albums.
        offset = 0
        while True:
            album_data = sp.current_user_saved_albums(limit=50, offset=offset)
            
            for item in album_data['items']:
                album = item['album']
                tracks = album['tracks']['items']
                for track in tracks:
                    track_name = track['name']
                    track_artist = track['artists'][0]['name']
                    track_id = track['id']
                    liked_album_songs.add(Track(track_name, track_artist, track_id))

            # Check to see if we should keep making calls to get more albums.
            more_data = album_data['next']
            if not more_data:
                break
            else:
                offset += 50
        
        # Gather all the tracks from liked songs.
        offset = 0
        while True:
            liked_song_data = sp.current_user_saved_tracks(limit=50, offset=offset)
            
            for item in liked_song_data['items']:
                 track = item['track']
                 track_name = track['name']
                 track_artist = track['artists'][0]['name']
                 track_id = track['id']
                 liked_songs.add(Track(track_name, track_artist, track_id))

            # Check to see if we should keep making calls to get more liked songs.
            more_data = liked_song_data['next']
            if not more_data:
                break
            else:
                offset += 50

        # Find intersection of sets
        duplicates = liked_album_songs & liked_songs        

        # Unlike duplicates
        track_ids = []
        for song in duplicates:
            track_ids.append(song.id)
        if len(track_ids) > 0:
            sp.current_user_saved_tracks_delete(track_ids)
            print(f'Removed {duplicates} from liked songs.')
        else:
            print('No duplicates found.')

    else:
        print(f'Cant get token for {username}')

class Track:
    def __init__(self, name, artist, id):
        self.name = name
        self.artist = artist
        self.id = id

    def __repr__(self):
        return self.name + ' ' + self.artist

    def __str__(self):
        return self.name + ' ' + self.artist

    def __eq__(self, other):
        return other.name == self.name and other.artist == self.artist
    def __hash__(self):
        return hash(self.name + ' ' + self.artist)
