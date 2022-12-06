import pandas as pd
import numpy as np
import requests

df = pd.read_json('The Bae songs/endsong_0.json')
df1 = pd.read_json('The Bae songs/endsong_1.json')

frames = [df, df1]

df = pd.concat(frames)
new = df["spotify_track_uri"].str.split(":", expand = True)
df['track_uri'] = new[2]

track_uri_2 = df['track_uri'].to_list()

track_uris = []
for t in track_uri_2:
    if t not in track_uris and t != None:
        track_uris.append(t)

new = df["spotify_track_uri"].str.split(":", expand = True)
df['track_uri'] = new[2]
CLIENT_ID = '318db19301c943faa5e64953abbe4d2e'
CLIENT_SECRET = '4ae28a402ee4435e9a5ab9cf040782ce'

AUTH_URL = 'https://accounts.spotify.com/api/token'

auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

auth_response_data = auth_response.json()

access_token = auth_response_data['access_token']

headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

BASE_URL = 'https://api.spotify.com/v1/'

feature_dict = {}

for t_uri in track_uris:
    feature_dict[t_uri] = {
        'danceability': 0,
        'energy': 0,
        'key': 0,
        'loudness' : 0,
        'speechiness': 0,
        'acousticness': 0,
        'instrumentalness': 0,
        'valence' : 0,
        'tempo': 0
        }
    
    r = requests.get(BASE_URL + 'audio-features/' + t_uri, headers=headers)
    s = r.json()
    try:
        feature_dict[t_uri]['danceability'] = s['danceability']
    except:
        pass
    try:
        feature_dict[t_uri]['energy'] = s['energy']
    except:
        pass
    try:
        feature_dict[t_uri]['key'] = s['key']
    except:
        pass
    try:
        feature_dict[t_uri]['loudness'] = s['loudness']
    except:
        pass
    try:
        feature_dict[t_uri]['speechiness'] = s['speechiness']
    except:
        pass
    try:
        feature_dict[t_uri]['acousticness'] = s['acousticness']
    except:
        pass
    try:
        feature_dict[t_uri]['valence'] = s['valence']
    except:
        pass
    try:
        feature_dict[t_uri]['tempo'] = s['tempo']
    except:
        pass
    try:
        feature_dict[t_uri]['instrumentalness'] = s['instrumentalness']
    except:
        pass

df_features = pd.DataFrame.from_dict(feature_dict, orient='index')
df_features.insert(0, 'track_uri', df_features.index)
df_features.reset_index(inplace=True, drop=True)


df_features.to_csv('AudioFeaturesTheBae.csv')