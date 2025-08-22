import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(
    page_title="Movie Survey",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .question-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #FF6B6B;
    }
    .submit-btn {
        background-color: #4ECDC4;
        color: white;
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 25px;
        font-size: 1.1rem;
        cursor: pointer;
    }
    .submit-btn:hover {
        background-color: #45B7AA;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'survey_submitted' not in st.session_state:
    st.session_state.survey_submitted = False

def save_survey_data(data):
    """Save survey data to a JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"survey_responses_{timestamp}.json"
    
    # Create data directory if it doesn't exist
    os.makedirs("survey_data", exist_ok=True)
    
    filepath = os.path.join("survey_data", filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    return filepath

def main():
    # Header
    st.markdown('<h1 class="main-header">🎬 Movie Survey</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    if not st.session_state.survey_submitted:
        # Survey Form
        with st.form("movie_survey"):
            st.markdown("### 📝 Please fill out this movie survey to help us understand your preferences!")
            
            # Personal Information
            st.markdown('<div class="question-container">', unsafe_allow_html=True)
            st.subheader("👤 Personal Information")
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name", placeholder="Enter your full name")
                age = st.number_input("Age", min_value=13, max_value=100, value=25)
            
            with col2:
                email = st.text_input("Email (optional)", placeholder="Enter your email")
                occupation = st.selectbox(
                    "Occupation",
                    ["Student", "Professional", "Retired", "Other"]
                )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Movie Preferences
            st.markdown('<div class="question-container">', unsafe_allow_html=True)
            st.subheader("🎭 Movie Preferences")
            
            favorite_genre = st.multiselect(
                "What are your favorite movie genres? (Select all that apply)",
                ["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", 
                 "Thriller", "Documentary", "Animation", "Fantasy", "Mystery", "Western"]
            )
            
            watch_frequency = st.radio(
                "How often do you watch movies?",
                ["Daily", "Weekly", "Monthly", "Rarely", "Never"]
            )
            
            preferred_platform = st.selectbox(
                "What's your preferred way to watch movies?",
                ["Streaming Services (Netflix, Prime, etc.)", "Movie Theaters", 
                 "DVD/Blu-ray", "TV Channels", "Other"]
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Movie Ratings
            st.markdown('<div class="question-container">', unsafe_allow_html=True)
            st.subheader("⭐ Movie Ratings")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("Rate the following aspects (1-10):")
                story_rating = st.slider("Story Quality", 1, 10, 5)
                acting_rating = st.slider("Acting Performance", 1, 10, 5)
                visual_rating = st.slider("Visual Effects", 1, 10, 5)
            
            with col2:
                st.write("&nbsp;")  # Spacer
                st.write("&nbsp;")  # Spacer
                st.write("&nbsp;")  # Spacer
                music_rating = st.slider("Music/Soundtrack", 1, 10, 5)
                overall_rating = st.slider("Overall Experience", 1, 10, 5)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Recent Movies
            st.markdown('<div class="question-container">', unsafe_allow_html=True)
            st.subheader("🎥 Recent Movies")
            
            recent_movies = st.text_area(
                "What movies have you watched recently? (List them separated by commas)",
                placeholder="e.g., Inception, The Dark Knight, La La Land"
            )
            
            best_movie = st.text_input(
                "What's the best movie you've ever watched?",
                placeholder="Enter movie title"
            )
            
            worst_movie = st.text_input(
                "What's the worst movie you've ever watched?",
                placeholder="Enter movie title"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Movie Industry Opinions
            st.markdown('<div class="question-container">', unsafe_allow_html=True)
            st.subheader("💭 Industry Opinions")
            
            remake_opinion = st.radio(
                "What's your opinion on movie remakes?",
                ["Love them - they often improve on the original",
                 "Like them - some are good, some are bad",
                 "Neutral - depends on the movie",
                 "Dislike them - originals are usually better",
                 "Hate them - they're unnecessary"]
            )
            
            streaming_impact = st.multiselect(
                "How has streaming changed your movie-watching habits? (Select all that apply)",
                ["Watch more movies overall", "Watch fewer movies in theaters",
                 "Discover more indie/foreign films", "Binge-watch series instead",
                 "No significant change", "Watch movies on mobile devices"]
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Additional Comments
            st.markdown('<div class="question-container">', unsafe_allow_html=True)
            st.subheader("💬 Additional Comments")
            
            additional_comments = st.text_area(
                "Any additional comments or suggestions about movies?",
                placeholder="Share your thoughts, recommendations, or any other feedback..."
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Submit Button
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button(
                "📊 Submit Survey",
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                # Validate required fields
                if not name:
                    st.error("Please enter your name to continue.")
                    return
                
                if not favorite_genre:
                    st.error("Please select at least one favorite genre.")
                    return
                
                # Collect all survey data
                survey_data = {
                    "timestamp": datetime.now().isoformat(),
                    "personal_info": {
                        "name": name,
                        "age": age,
                        "email": email,
                        "occupation": occupation
                    },
                    "preferences": {
                        "favorite_genres": favorite_genre,
                        "watch_frequency": watch_frequency,
                        "preferred_platform": preferred_platform
                    },
                    "ratings": {
                        "story_quality": story_rating,
                        "acting_performance": acting_rating,
                        "visual_effects": visual_rating,
                        "music_soundtrack": music_rating,
                        "overall_experience": overall_rating
                    },
                    "movies": {
                        "recent_movies": recent_movies,
                        "best_movie": best_movie,
                        "worst_movie": worst_movie
                    },
                    "opinions": {
                        "remake_opinion": remake_opinion,
                        "streaming_impact": streaming_impact
                    },
                    "additional_comments": additional_comments
                }
                
                # Save survey data
                filepath = save_survey_data(survey_data)
                
                # Update session state
                st.session_state.survey_submitted = True
                st.session_state.survey_data = survey_data
                st.session_state.filepath = filepath
                
                st.success("✅ Survey submitted successfully!")
                st.balloons()
    
    # Show results after submission
    if st.session_state.survey_submitted:
        st.markdown("## 📊 Survey Results Summary")
        
        data = st.session_state.survey_data
        
        # Personal Information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 👤 Personal Information")
            st.write(f"**Name:** {data['personal_info']['name']}")
            st.write(f"**Age:** {data['personal_info']['age']}")
            st.write(f"**Occupation:** {data['personal_info']['occupation']}")
            if data['personal_info']['email']:
                st.write(f"**Email:** {data['personal_info']['email']}")
        
        with col2:
            st.markdown("### 🎭 Preferences")
            st.write(f"**Favorite Genres:** {', '.join(data['preferences']['favorite_genres'])}")
            st.write(f"**Watch Frequency:** {data['preferences']['watch_frequency']}")
            st.write(f"**Preferred Platform:** {data['preferences']['preferred_platform']}")
        
        # Ratings Chart
        st.markdown("### ⭐ Ratings Breakdown")
        ratings_df = pd.DataFrame({
            'Aspect': list(data['ratings'].keys()),
            'Rating': list(data['ratings'].values())
        })
        
        # Create a bar chart
        st.bar_chart(ratings_df.set_index('Aspect'))
        
        # Additional Information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎥 Movie Information")
            if data['movies']['recent_movies']:
                st.write(f"**Recent Movies:** {data['movies']['recent_movies']}")
            if data['movies']['best_movie']:
                st.write(f"**Best Movie:** {data['movies']['best_movie']}")
            if data['movies']['worst_movie']:
                st.write(f"**Worst Movie:** {data['movies']['worst_movie']}")
        
        with col2:
            st.markdown("### 💭 Opinions")
            st.write(f"**Remake Opinion:** {data['opinions']['remake_opinion']}")
            st.write(f"**Streaming Impact:** {', '.join(data['opinions']['streaming_impact'])}")
        
        if data['additional_comments']:
            st.markdown("### 💬 Additional Comments")
            st.write(data['additional_comments'])
        
        st.markdown("---")
        st.info(f"📁 Survey data saved to: {st.session_state.filepath}")
        
        # Reset button
        if st.button("🔄 Take Another Survey"):
            st.session_state.survey_submitted = False
            st.rerun()

if __name__ == "__main__":
    main()
