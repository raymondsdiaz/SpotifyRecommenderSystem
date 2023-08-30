import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd
import json
import spotipy.util as util
from spotify_rs_func import authenticate, gsheetAuth, getRecentlyPlayed, getAudioFeatures, getSongsAndCreatePlaylist, clusterSongs, submitForm

st.title("Most Recently Played Recommender System")
st.write("This is a program that will recommend 10 songs to you based off of your most recently played 50 songs.")
st.markdown("""
In order for you to run this program, you first will need to go to [link](https://developer.spotify.com/dashboard/create). Once you are here, follow the instructions below:
- App name: Song Recommendation
- App description: Retrieve 10 new songs based off my most recently played
- Redirect URI: http://localhost:7777/callback
""")
st.write("Once you are finished entering those values, check the understand and agree Spotify's ToS and Design Guidelines and click save and then head to settings to get your Client ID and Client Secret")
st.write("Please listen to the ten songs that are recommended below and input at the bottom of the page how many songs out of the 10 that you like and would save to a playlist")
st.write("No information below will be saved except for how many songs you like from the 10 songs that are recommended")
st.write("After you hit the submit button, ten songs will be recommended. After you listen to the ten songs, please input how many songs you liked at the bottom of the page and hit submit")

clientId = st.text_input("Enter Client ID here")
clientSecret = st.text_input("Enter Client Secret here")
username = st.text_input("Enter your username here")
button = st.button('Submit to get your recommendations')
scope = "user-read-recently-played user-read-private user-top-read"
redirectUri = 'http://localhost:7777/callback'

userData = []

if button:
	token = util.prompt_for_user_token(username, scope, client_id=clientId, client_secret=clientSecret, redirect_uri=redirectUri)
	if token: 
		gs = gsheetAuth()
		userNum = random.randint(1,1000)
		embed = 'https://open.spotify.com/embed/track/'
		sp = authenticate(token)
		tracks = pd.read_parquet('data/tracks.parquet', engine='pyarrow')
		track_ids = getRecentlyPlayed(sp)
		df = getAudioFeatures(sp,track_ids)
		df_clustered = clusterSongs(df,4).drop([ 'uri', 'track_href', 'analysis_url', 'duration_ms','type'],axis=1)
		print(df_clustered)
		most_recent = getSongsAndCreatePlaylist(sp, df_clustered, tracks, 10)
		for ids in most_recent:
			try:
				components.iframe(str(embed + ids), width=700, height=300)
			except ValueError:
				continue
		userData.append('ml_recommended')
		row = submitForm(userNum,userData)
		gs.values_append('Data', {'valueInputOption': 'RAW'}, {'values': row})
exit()