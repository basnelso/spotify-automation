import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pprint
from duplicate_remover import remove_duplicates

def main():
    DEVICE_NAME = 'SNELSON-DESKTOP'
    username = 'bs40404'
    scope = 'user-modify-playback-state user-read-playback-state user-library-modify user-library-read'
    client_id = 'e004309d630544a5958730c3057677b3'
    client_secret = '39b2462f03f74330ad65ca09ee3eeadd'
    redirect_uri = 'https://localhost:8080'

    token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
    if token:
        sp = spotipy.Spotify(auth=token)
        device_id = None
        device_data = sp.devices()
        if device_data:
            devices = device_data['devices']
            for device in devices:
                if device['name'] == DEVICE_NAME:
                    device_id = device['id']
        
        if device_id:
            sp.transfer_playback(device_id)
            print(f'Playback transfered to {DEVICE_NAME}.')
        else:
            print(f'Could not find {DEVICE_NAME}.')
    else:
        print("Authorization failed.")

    remove_duplicates()


if __name__ == '__main__':
    main()