import streamlit as st
import pandas as pd

# Set up page configuration
st.set_page_config(page_title="Mood-Based Music Recommender", page_icon="🎧", layout="wide")

# Inject custom CSS for black background and styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Montserrat', sans-serif;
            background-color: #0f0f0f;
            color: white;
        }

        .main {
            background-color: #0f0f0f;
            padding: 2rem;
            border-radius: 12px;
        }

        /* Clean and modern button */
        .stButton>button {
            background-color: #1DB954;
            color: white !important;
            font-size: 18px;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            padding: 0.6em 1.2em;
            transition: 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #17a84b;
            transform: scale(1.03);
        }

        .stSelectbox label, .stRadio label {
            font-size: 18px;
            color: white;
        }

        h1, h2, h3 {
            font-weight: 600;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.7);
        }

        .track-card {
            background-color: #1e1e1e;
            padding: 1em;
            border-radius: 12px;
            margin-bottom: 1em;
            display: flex;
            gap: 1em;
            align-items: center;
        }

        .track-card img {
            width: 80px;
            height: 80px;
            border-radius: 8px;
        }

        .track-info {
            flex: 1;
        }

        .track-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 0.3em;
        }

        .track-artist {
            font-size: 14px;
            color: #ccc;
        }
    </style>
""", unsafe_allow_html=True)

# Load dataset
df = pd.read_csv("dataset.csv")

# Mood detection logic
def get_mood(valence, energy):
    if valence >= 0.7 and energy >= 0.7:
        return 'Energetic'
    elif valence >= 0.7 and energy < 0.7:
        return 'Upbeat'
    elif valence >= 0.5 and energy < 0.5:
        return 'Relaxed'
    elif valence >= 0.5 and energy >= 0.5:
        return 'Romantic'
    elif valence < 0.5 and energy >= 0.7:
        return 'Motivational'
    elif valence < 0.5 and energy < 0.3:
        return 'Sad'
    elif valence < 0.5 and energy >= 0.3:
        return 'Melancholic'
    elif valence >= 0.5 and energy < 0.4:
        return 'Calm'
    elif valence >= 0.4 and energy >= 0.6:
        return 'Chill'
    else:
        return 'Neutral'

# Add mood column if not present
if 'mood' not in df.columns:
    df['mood'] = df.apply(lambda row: get_mood(row['valence'], row['energy']), axis=1)

# Main content
with st.container():
    st.title("🎧 Mood-Based Music Recommender")
    st.write("Select your current mood and get personalized song suggestions. Discover music that fits your vibe 🎶")

    moods = ['Energetic', 'Upbeat', 'Relaxed', 'Romantic', 'Motivational', 'Sad']
    selected_mood = st.selectbox("Choose a mood 🎯", moods)

    if st.button("Recommend Songs"):
        recommended = df[df['mood'] == selected_mood][['track_name', 'artists']]
        if not recommended.empty:
            st.subheader(f"🎶 Top Songs for {selected_mood} Mood:")
            for _, row in recommended.head(10).iterrows():
                st.markdown(f"""
                    <div class="track-card">
                        <div class="track-info">
                            <div class="track-title">{row['track_name']}</div>
                            <div class="track-artist">{row['artists']}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Oops! No songs found for this mood.")
