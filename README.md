# Spotify Recommender System
![image](https://github.com/raymondsdiaz/SpotifyRecommenderSystem/assets/88802773/27b70dbf-f514-4619-a069-3406cf9bd3e3)

# Problem statement
One thing that I noticed in Spotify's "Discover Weekly" playlist was that it was limited to 30 song and that it was only curated once a week and contained only 30 songs. I saw this as an opportunity to create a recommender system based on a user's most recently played songs and that could be ran whenever a user wanted to find new songs.

# Dataset
There are two datasets that I used for my recommender system.

The first [dataset](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks?select=tracks.csv) is a dataset gathered from Kaggle which contains ~600k tracks that I will be utilizing as the dataset where we will be pulling songs to recommend to the user.

The second dataset is data pulled from Spotify's API and looking at a user's most recently played songs and creating a dataframe containing the tracks and their song features.

# Exploratory Data Analysis

Below are the features that I would be working with for my recommender system.

|     feature    |                                description                                |
|:--------------:|:-------------------------------------------------------------------------:|
|  acousticness  |              A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.             |
|     danceability     |                      Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.                    |
|      energy      |                            Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.                          |
| instrumentalness |                         Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.                       |
|    key    |                         The key the track is in. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1.                      |
| liveness |                Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.               |
|  loudness |                The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db.              |
| mode |                Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.                |
| speechiness |                Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.               |
|     tempo    |           The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.           |
| time_signature | An estimated time signature. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure). The time signature ranges from 3 to 7 indicating time signatures of "3/4", to "7/4". |
| valence | A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry). |

There was no data wrangling that needed to be done or imputing of values on the most recently played dataset because all the track features pulled from Spotify's API would return a value. Additionally, the data that was sourced also had all the track features pre-populated which got rid of the need to do any rigorous cleansing.

# Modeling

# Limitations

The biggest limitation that I faced when creating this recommender system was that Spotify's API offered limited amounts of data for what I wanted to accomplish. What I mean by this is that when you pull a user's most recently played songs, you are limited to only 50 songs. To create a recommender system that is much more precise and accurate for this specific use case, we should be using at least a months worth of listening history in order to capture a user's true music taste. And unfortunately, that just simply is not possible with Spotify's API.

The second biggest limitation that I faced when creating this recommender system was Spotipy's functionality with Streamlit. I had an idea to host my app on Streamlit so that users could test the app and see if it provided new song recommendations that were in line with their musical tastes. Unfortunately, the problem that I faced is that Spotipy's authentication flow was not compatible with Streamlit and there was no work around to trying to get it work. If the app was run internally on one's computer, the authentication flow would flow seamlessly.

# Final Thoughts
