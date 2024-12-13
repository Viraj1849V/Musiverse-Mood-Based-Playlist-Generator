import random
import json
from textblob import TextBlob
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Define predefined playlists
mood_playlists = {
    "Happy": [
        "Happy - Pharrell Williams",
        "Walking on Sunshine - Katrina and The Waves",
        "Can’t Stop the Feeling! - Justin Timberlake",
        "Don’t Worry, Be Happy - Bobby McFerrin",
        "Don’t Stop Me Now - Queen",
        "Dancing Queen - ABBA",
        "Shake It Off - Taylor Swift",
        "Uptown Funk - Mark Ronson ft. Bruno Mars",
        "Sucker - Jonas Brothers",
        "HandClap - Fitz and The Tantrums",
    ],
    "Sad": [
        "Someone Like You - Adele",
        "Someone You Loved - Lewis Capaldi",
        "Stay With Me - Sam Smith",
        "When the Party's Over - Billie Eilish",
        "Fix You - Coldplay",
        "The Blower's Daughter - Damien Rice",
        "Hallelujah - Jeff Buckley",
        "Let Her Go - Passenger",
        "Let It Go - James Bay",
        "Skinny Love - Bon Iver",
    ],
    "Energetic": [
        "Survivor - Eye of the Tiger",
        "Imagine Dragons - Believer",
        "Eminem - Lose Yourself",
        "The White Stripes - Seven Nation Army",
        "Kanye West - Stronger",
        "Prodigy - Firestarter",
        "AC/DC - Thunderstruck",
        "Beastie Boys - Sabotage",
        "Calvin Harris - Summer",
        "Martin Garrix - Animals",
    ],
    "Relaxed": [
        "Norah Jones - Don’t Know Why",
        "Jack Johnson - Better Together",
        "John Mayer - Gravity",
        "Coldplay - Yellow",
        "Ed Sheeran - Thinking Out Loud",
        "Jason Mraz - I’m Yours",
        "Louis Armstrong - What a Wonderful World",
        "Otis Redding - Sittin’ On The Dock of the Bay",
        "Fleetwood Mac - Dreams",
        "Enya - Only Time",
    ],
    "Romantic": [
        "Ed Sheeran - Perfect",
        "Bruno Mars - Just the Way You Are",
        "John Legend - All of Me",
        "Elvis Presley - Can’t Help Falling in Love",
        "Taylor Swift - Lover",
        "Frank Sinatra - Fly Me to the Moon",
        "Jason Derulo - Marry Me",
        "Etta James - At Last",
        "Christina Perri - A Thousand Years",
        "Michael Bublé - Everything",
    ],
    "Motivational": [
        "Rachel Platten - Fight Song",
        "Katy Perry - Roar",
        "Eminem - Not Afraid",
        "Queen - We Are the Champions",
        "Bon Jovi - It’s My Life",
        "Journey - Don’t Stop Believin’",
        "Imagine Dragons - Thunder",
        "Beyoncé - Run the World (Girls)",
        "Kelly Clarkson - Stronger (What Doesn’t Kill You)",
        "Sia - Chandelier",
    ],
}

# Text-based mood detection
def detect_mood_from_text(text):
    """Detect mood from text input."""
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > 0.5:
        return "Happy"
    elif sentiment < -0.5:
        return "Sad"
    else:
        return "Relaxed"

# Generate playlist
def generate_playlist(mood):
    """Generate a playlist based on the detected mood."""
    if mood in mood_playlists:
        return random.sample(mood_playlists[mood], min(5, len(mood_playlists[mood])))
    else:
        return []

# Spotify API Integration
def fetch_songs_from_spotify(mood):
    """Fetch songs from Spotify based on mood."""
    CLIENT_ID = "6b4d48d1ff6a48f89c6a1b2756933665"  # Replace with your Spotify API Client ID
    CLIENT_SECRET = "9b558f79409943329b8fa9c87f11136c"  # Replace with your Spotify API Client Secret

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    )
    results = sp.search(q=mood, type='track', limit=10)
    tracks = [f"{track['name']} by {track['artists'][0]['name']}" for track in results['tracks']['items']]
    return tracks

# Save custom playlists
def save_playlist(mood, playlist):
    """Save the playlist to a JSON file."""
    try:
        with open("custom_playlists.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data[mood] = playlist
    with open("custom_playlists.json", "w") as file:
        json.dump(data, file, indent=4)
    print(f"Playlist for mood '{mood}' saved successfully!")

# Load saved playlists
def load_playlists():
    """Load playlists from a JSON file."""
    try:
        with open("custom_playlists.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Main Program
print("Welcome to MUSIVERSE, a mood based playlist generator!")
print("You can describe your mood or choose from predefined moods (Happy, Sad, Energetic, Relaxed, Romantic, Motivational).")

# User input for mood
user_input = input("How are you feeling today? Describe in a sentence or enter a mood: ").capitalize()
detected_mood = detect_mood_from_text(user_input) if " " in user_input else user_input

# Display mood
print(f"Detected Mood: {detected_mood}")

# Fetch playlist
source = input("Do you want songs from (1) Predefined Playlist or (2) Spotify? Enter 1 or 2: ")
if source == "1":
    playlist = generate_playlist(detected_mood)
elif source == "2":
    playlist = fetch_songs_from_spotify(detected_mood)
else:
    playlist = []

# Display playlist
if playlist:
    print(f"\nHere is your {detected_mood} playlist:")
    for i, song in enumerate(playlist, 1):
        print(f"{i}. {song}")

    # Save playlist
    save_option = input("Do you want to save this playlist? (yes/no): ").lower()
    if save_option == "yes":
        save_playlist(detected_mood, playlist)
else:
    print("Sorry, no songs available for this mood.")

# Option to load saved playlists
load_option = input("Do you want to see saved playlists? (yes/no): ").lower()
if load_option == "yes":
    saved_playlists = load_playlists()
    if saved_playlists:
        print("\nSaved Playlists:")
        for mood, songs in saved_playlists.items():
            print(f"\n{mood.capitalize()} Playlist:")
            for song in songs:
                print(f"- {song}")
    else:
        print("No saved playlists found.")