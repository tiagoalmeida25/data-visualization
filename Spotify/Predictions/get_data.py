import pandas as pd
import torch

def get_features():
    df_features = pd.read_csv('AudioFeaturesTable2.csv')
    return df_features

def get_data():
    df0 = pd.read_json('../my_spotify_data/endsong_0.json')
    df1 = pd.read_json('../my_spotify_data/endsong_1.json')
    df2 = pd.read_json('../my_spotify_data/endsong_2.json')
    df3 = pd.read_json('../my_spotify_data/endsong_3.json')

    merge = [df0, df1, df2, df3]

    df = pd.concat(merge)
    df.drop(['username','ip_addr_decrypted', 'platform', 'conn_country', 'user_agent_decrypted', 'spotify_track_uri', 'spotify_episode_uri', 'shuffle','skipped','offline_timestamp','offline','incognito_mode', 'reason_start'], axis=1, inplace=True)
    df.columns = ['Date', 'Duration','Track', 'Artist','Album', 'Episode','Podcast', 'Reason to End']

    df['Time'] = df['Date'].str.split('T', expand=True)[1].str[:-1]
    df['Date'] = df['Date'].str.split('T', expand=True)[0]

    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df['Time'] = pd.to_datetime(df['Time']).dt.time

    df['Duration'] = pd.to_numeric(df['Duration']) / 1000

    df.sort_values(by='Date',inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df

def get_podcasts():
    df = get_data()

    df_podcasts = df[df['Episode'].notna()].copy()
    df_podcasts.drop(['Track','Artist','Album'], axis=1, inplace=True)
    df_podcasts.reset_index(drop=True, inplace=True)

    return df_podcasts

def get_songs():
    df = get_data()

    df_tracks = df[df['Track'].notna()].copy()
    df_tracks.drop(['Episode','Podcast'], axis=1, inplace=True)
    df_tracks.reset_index(drop=True, inplace=True)

    return df_tracks


def get_labels():
    df_songs = get_songs()

    unique_quant = df_songs['Track'].value_counts()


    ranking = []
    for quant in unique_quant:
        if quant > 50:
            ranking.append(1)
        else:
            ranking.append(-1)

    ranking = torch.tensor(ranking)

    return ranking