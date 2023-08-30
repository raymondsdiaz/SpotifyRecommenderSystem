
import json
import os
import pandas as pd
import numpy as np
import spotipy
import spotipy.util as util
import streamlit as st
import time
import gspread
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA

def getToken(oauth, code):

    token = oauth.get_access_token(code, as_dict=False, check_cache=False)
    # remove cached token saved in directory
    os.remove(".cache")
    
    # return the token
    return token

def signIn(token):
    sp = spotipy.Spotify(auth=token)
    return sp

def authenticate(token):
    scopes = "user-read-recently-played user-read-private user-top-read"
    sp = spotipy.Spotify(auth=token)
    return sp

def gsheetAuth():
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file('credentials.json', scopes=scopes)
    gc = gspread.authorize(credentials)
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    gs = gc.open_by_key('12is7Slj-ye7uq7JQyjcNnjKHxjbXj_v1XvDaLB-8sZE')
    return gs

def getRecentlyPlayed(sp):
    """Gets user's most recently played songs

    Args:
    sp (authToken): user auth token to access api

    Returns:
    track_ids: List of the user's most recently played songs
    """
    rp = sp.current_user_recently_played()
    track_ids = []
    rp_json = json.loads(json.dumps(rp))
    for x in rp_json['items']:
        track_ids.append(x['track']['uri'])    
    return track_ids

def getAudioFeatures(sp, track_ids):  
    """Gets audio features of specific track ids and generates a dataframe

    Args:
    sp (authToken): user auth token to access api
    track_ids (list): List of the user's most recently played songs

    Returns:
    df (dataframe): Most recently played dataframe containing audio features for each track
    """
    audioFeatures = []   
    for id in track_ids:
        features = sp.audio_features(id)[0]
        if features:
            audioFeatures.append(features)
    
    audioFeatures = [x for x in audioFeatures if x != '']
    df = pd.DataFrame(audioFeatures)
    df = pd.get_dummies(df, columns = ['mode'])
    df = df.astype({'mode_0': 'int64', 'mode_1': 'int64'}) 
    return df

def getSongsAndCreatePlaylist(sp, most_recent, songs, numSongs):
    """Takes the user's most recently played songs and compares to a 
    600k+ song dataset and generates a playlist for the user by calculating
    the cosine similarity between the two datasets and selecting the top songs
    based on the similarity value

    Args:
    sp (authToken): user auth token to access api
    most_recent (dataframe): Most recently played dataframe with filtered down features
    songs (dataframe): Tracks dataframe with filtered down features
        (default is False)
    numSongs (integer): Decides how many songs that will be added to the playlist

    Returns:
    No explicit returns as this is a function that runs to create a playlist for the use
    """
    songs['similarity'] = cosine_similarity(songs.drop(['id'],axis=1).values,most_recent.drop(['id'],axis=1).values)[:,0]
    new_playlist = songs.sort_values('similarity',ascending = False).head(10)
    print(new_playlist)
    ids = [*set(new_playlist['id'].tolist())]
    return ids

def clusterSongs(most_recent, clusters):
    cluster_pipeline = Pipeline([('scaler', StandardScaler()), ('kmeans', KMeans(n_clusters=clusters))])
    X = most_recent.drop(['id','uri','track_href','analysis_url','type'],axis=1)
    cluster_pipeline.fit(X)
    most_recent['cluster'] = cluster_pipeline.predict(X)
    return most_recent

def submitForm(userNum, userData):
    def sub_function():
        st.session_state.likes

    with st.form("my_test_form", clear_on_submit = True):
        st.text_input('Enter how many songs out of the 10 that were recommended you liked:', key = 'likes')
        st.form_submit_button("Submit here!", on_click=sub_function)
        time.sleep(10)
        like = st.session_state.likes
        df = pd.DataFrame({'userId': userNum, 'likes': like, 'data': userData})
        row = df.values.tolist()
        return row