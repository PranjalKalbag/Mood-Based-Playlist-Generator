import pandas as pd
import time 
import requests
import json
client_id = 'f37b591fa695467594288574b1b6a68e'
client_secret = 'f7c71f73e3de4973aaad05d190f60053'

AUTH_URL = 'https://accounts.spotify.com/api/token'
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
})
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}
url = 'https://api.spotify.com/v1/search'

score = 1
mood = ['depressed', 'sad', 'neutral', 'joyful','ecstatic']
q = mood[score]
r = requests.get(url, params={ 'q': q, 'type': 'playlist' },  headers=headers)
r= r.json()
playlist = r['playlists']

items = playlist['items']
uri = []
for item in items:
    uri.append(item['uri'])
play_url = 'https://api.spotify.com/v1/me/player/queue'

for i in range(len(uri)):
    temp = uri[i]
    uri[i] = temp[17:]
songsuri = []
songname = []
for i in uri:
    get_track = 'https://api.spotify.com/v1/playlists/'+i+'/tracks'
    
    track = requests.get(get_track, params={'limit' : 1},headers=headers)
    track = track.json()
    var = track['items']
    var = var[0]
    var = var['track']
    var = var['uri']
    var = var[14:]
    if(':' in var):
        continue
    
    songsuri.append(var)

create_playlist = 'https://api.spotify.com/v1/users/agjfzhaxke0fhmytgakdu6ra1/playlists'
playlist_name = q + " score"
playlist_param = json.dumps({'name' : playlist_name})
playlist_create = requests.post(url = create_playlist, data=playlist_param,headers={"Content-Type":"application/json", 
                        "Authorization":access_token})

user_id = 'agjfzhaxke0fhmytgakdu6ra1'
# endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
endpoint_url = "https://api.spotify.com/v1/users/agjfzhaxke0fhmytgakdu6ra1/playlists"
spotifyToken = 'BQCVhrPioqelsBNgXqwwJXy-AaiOT6QEBf6yptOd1U8xdscVpAVkTzwpIo-yIyRBl0MNU0S2oM7NBiWigbArZ10WjgVDRN0ivaP4uqYZtcHbVzwAN1UOITdsDhL7IR10nEIZc92x3V2zHNSm1lFoodgYqUMz8ub8AuOfzrNCM940iVdjoTy4duymMzu10Xp235hFqSE2Oa_yEsuVFpoFCDKvAYJOkaJyMftEcSQOQ7W6hT_mmQua2xX7qjZVYORw5G17-aselmcZXSzlwKO83qrj570NIx1KytoyCKQ'
reqHeader = {'Authorization': 'Bearer {}'.format(spotifyToken), 'Content-Type': 'application/json'}
request_body = json.dumps({
          "name": q + " mood",
          "description": "Here is a playlist to suit your mood",
          "public": True # let's keep it between us - for now
        })
response = requests.post(url = endpoint_url, data = request_body, headers=reqHeader)
response = response.json()
new_playlist_id = response['id']
reqBody = {'uris': list(map((lambda songId: 'spotify:track:' + songId), songsuri))}
r = requests.post('https://api.spotify.com/v1/users/{}/playlists/{}/tracks'.format(user_id, new_playlist_id), 
            headers=reqHeader, json=reqBody)
