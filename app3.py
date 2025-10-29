import streamlit as st
import pickle
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.parse

st.set_page_config(page_title="Movie Recommender", layout="wide")

# TMDB API Key

API_KEY = '138e6dbff59ea341484d5867d8879bf6'


# ✅ Cache data loading (runs only once)
@st.cache_data
def load_data():
    try:
        movies_dict = pickle.load(open('artificates/movie_list.pkl', 'rb'))
        movies = pd.DataFrame(movies_dict)
        similarity = pickle.load(open('artificates/similarity.pkl', 'rb'))
        return movies, similarity
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None


# ✅ Fetch movie data (poster + trailer)
def fetch_movie_data(movie_id):
    """Fetch both poster and trailer from TMDB API"""
    
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    videos_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}&language=en-US"
    
    poster = "https://placehold.co/500x750/222/FFF?text=No+Poster"
    trailer_url = None
    
    try:
        # Fetch poster
        movie_response = requests.get(movie_url, timeout=5)
        
        if movie_response.status_code == 200:
            movie_data = movie_response.json()
            poster_path = movie_data.get("poster_path")
            
            if poster_path:
                poster = "https://image.tmdb.org/t/p/w500" + poster_path
        
        # Fetch trailer
        videos_response = requests.get(videos_url, timeout=5)
        
        if videos_response.status_code == 200:
            videos_data = videos_response.json()
            videos = videos_data.get("results", [])
            
            # Priority: Official Trailer > Teaser > Any YouTube video
            for video in videos:
                if video.get("site") == "YouTube" and video.get("type") == "Trailer":
                    trailer_key = video.get("key")
                    trailer_url = f"https://www.youtube.com/watch?v={trailer_key}"
                    break
            
            # Fallback to teaser
            if not trailer_url:
                for video in videos:
                    if video.get("site") == "YouTube" and video.get("type") == "Teaser":
                        trailer_key = video.get("key")
                        trailer_url = f"https://www.youtube.com/watch?v={trailer_key}"
                        break
            
            # Fallback to any YouTube video
            if not trailer_url and videos:
                for video in videos:
                    if video.get("site") == "YouTube":
                        trailer_key = video.get("key")
                        trailer_url = f"https://www.youtube.com/watch?v={trailer_key}"
                        break
                    
    except Exception as e:
        print(f"Error fetching data for movie {movie_id}: {e}")
    
    return poster, trailer_url


# ✅ Parallel fetching for better performance
def fetch_movies_data_parallel(movie_ids):
    """Fetch posters and trailers for multiple movies in parallel"""
    results = {}
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_id = {executor.submit(fetch_movie_data, mid): mid for mid in movie_ids}
        
        for future in as_completed(future_to_id):
            movie_id = future_to_id[future]
            try:
                poster, trailer = future.result()
                results[movie_id] = {"poster": poster, "trailer": trailer}
            except Exception as e:
                print(f"Error processing movie {movie_id}: {e}")
                results[movie_id] = {
                    "poster": "https://placehold.co/500x750/222/FFF?text=No+Poster",
                    "trailer": None
                }
    
    return results


# ✅ Recommendation function
def recommend(movie, movies, similarity):
    """Generate movie recommendations based on similarity"""
    
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_titles = []
    recommended_ids = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_ids.append(movie_id)

    # Fetch all posters and trailers in parallel
    movies_data = fetch_movies_data_parallel(recommended_ids)
    
    recommended_posters = [movies_data[mid]["poster"] for mid in recommended_ids]
    recommended_trailers = [movies_data[mid]["trailer"] for mid in recommended_ids]

    return recommended_titles, recommended_posters, recommended_trailers


# ✅ Load cached data
movies, similarity = load_data()

if movies is None or similarity is None:
    st.stop()


# ========================================
# UI / Frontend
# ========================================

st.markdown(
    """
    <style>
    .stButton > button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #FF6B6B;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style='text-align:center; color:#FF4B4B;'>🍿 Movie Recommendation System 🎬</h1>
    <p style='text-align:center; color:#BBBBBB; font-size:18px;'>Select a movie and discover similar ones!</p>
    <br>
    """,
    unsafe_allow_html=True
)

# Movie selection
selected_movie = st.selectbox(
    "🔍 Search for a movie:",
    movies['title'].values,
    index=0
)

# Recommend button
if st.button("🎯 Get Recommendations"):
    
    with st.spinner("🎬 Finding perfect recommendations..."):
        recommended_titles, recommended_posters, recommended_trailers = recommend(
            selected_movie, movies, similarity
        )

    st.success("✨ Here are your recommendations!")
    st.markdown("---")
    
    # Display recommendations in 5 columns
    cols = st.columns(5)
    
    for idx, col in enumerate(cols):
        with col:
            # Movie poster
            st.image(recommended_posters[idx], use_container_width=True)
            
            # Movie title
            st.markdown(
                f"<h4 style='text-align:center; color:#FFFFFF;'>{recommended_titles[idx]}</h4>", 
                unsafe_allow_html=True
            )
            
            # Trailer button
            if recommended_trailers[idx]:
                st.link_button(
                    "▶️ Watch Trailer",
                    recommended_trailers[idx],
                    use_container_width=True
                )
            else:
                # Fallback to YouTube search
                query = urllib.parse.quote(f"{recommended_titles[idx]} official trailer")
                search_url = f"https://www.youtube.com/results?search_query={query}"
                st.link_button(
                    "🔍 Search Trailer",
                    search_url,
                    use_container_width=True
                )
            
            st.markdown("<br>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <p style='text-align:center; color:#888888; font-size:14px;'>
    Powered by TMDB API | Built with Streamlit ❤️
    </p>
    """,
    unsafe_allow_html=True
)