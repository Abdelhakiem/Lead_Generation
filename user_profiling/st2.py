import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import base64
import json

# Custom CSS for styling
import os

# Custom CSS for styling


# Custom CSS for styling
def local_css(file_name):
    # Resolve relative to this file
    base_dir = os.path.dirname(__file__)
    css_path = os.path.join(base_dir, file_name)
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file not found: {css_path}")

# Background image function
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{{"png"}};base64,{encoded_string.decode()});
        background-size: cover;
        background-attachment: fixed;
        background-opacity: 0.1;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

def user_profiling(user):
    local_css("style.css")  # Optional styling

    st.markdown(
        """
        <style>
        .header {
            font-size: 50px;
            font-weight: 700;
            background: linear-gradient(135deg, #6e8efb, #a777e3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 20px 0;
            text-align: center;
            margin-bottom: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f'<h1 class="header">User Profile Dashboard: {user["first_name"]} {user["last_name"]}</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(
            f"""
            <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center;">
                <div style="width: 120px; height: 120px; margin: 0 auto 15px; border-radius: 50%; background: linear-gradient(135deg, #6e8efb, #a777e3); display: flex; align-items: center; justify-content: center; color: white; font-size: 40px; font-weight: bold;">
                    {user["first_name"][0]}{user["last_name"][0]}
                </div>
                <h3 style="margin: 0; color: #333;">{user["first_name"]} {user["last_name"]}</h3>
                <p style="color: #666; margin: 5px 0;">{user["job"]}</p>
                <p style="color: #666; margin: 5px 0;">{user["location"]}, {user["education"]}</p>
                <hr style="border: 0.5px solid #eee; margin: 15px 0;">
                <div style="display: flex; justify-content: space-between;">
                    <div><p style="font-weight: bold; margin: 0; color: #333;">Age</p><p style="margin: 0; color: #666;">{user["age"]}</p></div>
                    <div><p style="font-weight: bold; margin: 0; color: #333;">Gender</p><p style="margin: 0; color: #666;">{user["gender"]}</p></div>
                    <div><p style="font-weight: bold; margin: 0; color: #333;">Status</p><p style="margin: 0; color: #666;">{user["marital_status"]}</p></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.metric("Total Posts", user["total_posts"])
        st.metric("Travel", user["travel_indicators"])
        st.metric("Top Hobby", user["top_hobby"])

        st.subheader("Top Habits")
        for habit in user["top_habits"]:
            st.markdown(f"- {habit}")

    with col2:
        st.subheader("Personality Summary")
        st.write(user["personality_summary"])

        tab1, tab2, tab3, tab4 = st.tabs(["📊 Interests", "📅 Activities", "💡 Life Indicators", "💰 Spending"])

        with tab1:
            st.subheader("Top Interests")
            interests_df = pd.DataFrame(user["top_interests"])
            fig = px.pie(interests_df, values='percentage', names='interest', hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("Key Activities")
            for i, activity in enumerate(user["key_activities"]):
                st.markdown(f"{i+1}. {activity}")

        with tab3:
            st.subheader("Life Indicators")
            for li in user["life_indicators"]:
                st.markdown(f"- {li}")

        with tab4:
            st.subheader("Spending Indicators")
            for sp in user["spending_indicators"]:
                st.markdown(f"- {sp}")

import os
import sqlite3
@st.cache_data
def load_user_profiles():
    # Compute absolute path to the DB
    base_dir = os.path.dirname(os.path.dirname(__file__))  # one level up from campaign_targeting/
    db_path = os.path.join(base_dir, 'dataset', 'databases', 'test_profiles.db')

    if not os.path.exists(db_path):
        st.error(f"Database not found at {db_path}")
        return pd.DataFrame()

    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query("SELECT * FROM user_profiles", conn)
    except Exception as e:
        st.error(f"Error reading user_profiles table: {e}")
        df = pd.DataFrame()
    finally:
        conn.close()
    return df


def user_directory_page():
    st.title("User Directory")
    df = load_user_profiles()
    if df.empty:
        st.error("No user profiles available.")
        return

    # Build display names
    df['display_name'] = df['first_name'] + ' ' + df['last_name']
    sel = st.selectbox("Select User", df['display_name'].tolist())
    if not sel:
        return

    user_row = df[df['display_name'] == sel].iloc[0]
    # Helper to parse JSON-like string columns
    def parse_list(col_name):
        val = user_row.get(col_name, None)
        if pd.isna(val):
            return []
        if isinstance(val, str):
            try:
                return json.loads(val)
            except Exception:
                try:
                    return eval(val)
                except Exception:
                    return []
        return val

    # Construct user dict matching required shape
    user = {
        'first_name': user_row['first_name'],
        'last_name': user_row['last_name'],
        'age': user_row['age'],
        'gender': user_row['gender'],
        'marital_status': user_row['marital_status'],
        'education': user_row['education'],
        'job': user_row['job'],
        'location': user_row['location'],
        'top_interests': [
            {'interest': user_row['first_interest'], 'percentage': user_row['first_interest_percentage']},
            {'interest': user_row['second_interest'], 'percentage': user_row['second_interest_percentage']},
            {'interest': user_row['third_interest'], 'percentage': user_row['third_interest_percentage']}
        ],
        'personality_summary': user_row['personality_summary'],
        'key_activities': parse_list('key_activities'),
        'total_posts': user_row['total_posts'],
        'top_habits': parse_list('top_habits'),
        'top_hobby': user_row['top_hobby'],
        'travel_indicators': user_row['travel_indicators'],
        'life_indicators': parse_list('life_indicators'),
        'spending_indicators': parse_list('spending_indicators')
    }
    user_profiling(user)




sample_user = {
    "first_name": "Alaa",
    "last_name": "Osama",
    "age": 24,
    "gender": "Female",
    "marital_status": "Single",
    "education": "BA Marketing",
    "job": "Marketing Specialist",
    "location": "Zagazig",
    "top_interests": [
        {"interest": "football", "percentage": 40},
        {"interest": "programming", "percentage": 30},
        {"interest": "fsdalkj", "percentage": 30}
    ],
    "personality_summary": "A driven and enthusiastic marketing specialist passionate about fashion and pop music, with a modern, vibrant personality and active social life.",
    "key_activities": [
        "Launched a new marketing campaign.",
        "Attended a fashion show in Cairo.",
        "Planning a trip to Sharm El-Sheikh."
    ],
    "total_posts": 10,
    "top_habits": [
        "listening to music while working",
        "attending social events"
    ],
    "top_hobby": "fashion",
    "travel_indicators": "rare",
    "life_indicators": [
        "Evening relaxation activities",
        "Dedicated work engagement",
        "Active social interactions"
    ],
    "spending_indicators": [
        "Spends on leisure activities",
        "Secondary travel expenditures"
    ]
}

def main():
    st.title("Test User Profile")
    user_profiling(sample_user)

if __name__ == "__main__":
    main()
