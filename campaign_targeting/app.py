import os
import streamlit as st
import pandas as pd
import torch
# Try importing tokenizer/model; fallback for environments without AutoTokenizer
try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    tok_class = AutoTokenizer
    model_class = AutoModelForSequenceClassification
except ImportError:
    from transformers import BertTokenizerFast, BertForSequenceClassification
    tok_class = BertTokenizerFast
    model_class = BertForSequenceClassification

# --- Constants ---
ARTIFACT_DIR = "artifacts/cross_encoder_ms_marco"
MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L6-v2"

# --- Load model from artifacts ---import sqlite3
import sqlite3

@st.cache_data
def load_user_profiles():
    conn = sqlite3.connect("../test_profiles.db")
    df = pd.read_sql_query("SELECT * FROM user_profiles", conn)
    print(df.head())
    conn.close()
    return df

# Load profiles dataframe
user_df = load_user_profiles()


# --- Data Loading ---
@st.cache_data
def load_user_profiles():
    conn = sqlite3.connect("../test_profiles.db")
    df = pd.read_sql_query("SELECT * FROM user_profiles", conn)
    print(df.head())
    conn.close()
    return df

# Load profiles dataframe
user_df = load_user_profiles()

# --- Sidebar: Manual Filters ---
st.sidebar.header("Manual Filters")

age_min, age_max = st.sidebar.slider(
    "Age range", 
    int(user_df['age'].min()), 
    int(user_df['age'].max()), 
    (int(user_df['age'].min()), int(user_df['age'].max()))
)

selected_genders = st.sidebar.multiselect("Gender", user_df['gender'].unique().tolist(), default=user_df['gender'].unique().tolist())
selected_marital = st.sidebar.multiselect("Marital Status", user_df['marital_status'].unique().tolist(), default=user_df['marital_status'].unique().tolist())
selected_locations = st.sidebar.multiselect("Locations", user_df['location'].unique().tolist(), default=user_df['location'].unique().tolist())
selected_education = st.sidebar.multiselect("Education", user_df['education'].unique().tolist(), default=user_df['education'].unique().tolist())
selected_jobs = st.sidebar.multiselect("Job Roles", user_df['job'].unique().tolist(), default=user_df['job'].unique().tolist())

# --- Main Area ---
st.title("Campaign Targeting Dashboard")

campaign_desc = st.text_area(
    "Campaign Description", 
    placeholder="Enter product or campaign description here..."
)
def load_cross_encoder():
    tokenizer = tok_class.from_pretrained(ARTIFACT_DIR)
    model = model_class.from_pretrained(ARTIFACT_DIR)
    model.eval()
    return tokenizer, model

tokenizer, model = load_cross_encoder()

if st.button("Run Targeting"):
    # Apply manual filters
    df_filtered = user_df[
        (user_df['age'] >= age_min) &
        (user_df['age'] <= age_max) &
        (user_df['gender'].isin(selected_genders)) &
        (user_df['marital_status'].isin(selected_marital)) &
        (user_df['location'].isin(selected_locations)) &
        (user_df['education'].isin(selected_education)) &
        (user_df['job'].isin(selected_jobs))
    ].copy()

    # --- Similarity Computation ---
    
    def compute_similarity(row, campaign_description):
        interests = [
            f"{row['first_interest']} ({row['first_interest_percentage']}%)",
            f"{row['second_interest']} ({row['second_interest_percentage']}%)",
            f"{row['third_interest']} ({row['third_interest_percentage']}%)"
        ]
        user_text = (
            row['personality_summary'] + " \n" +
            'Interests: ' + ', '.join(interests) + " \n" +
            'Key Activities: ' + ', '.join(eval(row['key_activities'])) + " \n" +
            'Top Habits: ' + ', '.join(eval(row['top_habits'])) + " \n" +
            f"Top Hobby: {row['top_hobby']} \n" +
            f"Travel Indicator: {row['travel_indicators']} \n" +
            'Life Indicators: ' + ', '.join(eval(row['life_indicators'])) + " \n" +
            'Spending Indicators: ' + ', '.join(eval(row['spending_indicators']))
        )
        features = tokenizer(
            [user_text],
            [campaign_description],
            padding=True,
            truncation=True,
            return_tensors="pt"
        )
        with torch.no_grad():
            logits = model(**features).logits
        # Return raw logit as float
        return float(logits[0].item())

    # Compute and ensure float dtype
    df_filtered['score'] = df_filtered.apply(lambda r: compute_similarity(r, campaign_desc), axis=1).astype(float)

    # Threshold slider
    threshold = st.sidebar.slider(
        "Score Threshold", 
        float(df_filtered['score'].min()), 
        float(df_filtered['score'].max()), 
        float(df_filtered['score'].mean()), 
        0.01
    )

    # Dynamic default top_n
    default_top_n = min(50, len(df_filtered))
    top_n = st.sidebar.number_input(
        "Max Users to Display", 
        min_value=1, 
        max_value=len(df_filtered), 
        value=default_top_n
    )

    df_results = df_filtered[df_filtered['score'] >= threshold]
    # Now score is float, nlargest works
    df_results = df_results.nlargest(top_n, 'score')

    st.subheader(f"Matched Users: {len(df_results)}")
    # st.dataframe(df_results[['first_name', 'last_name', 'age', 'gender', 'location', 'score']])
    st.dataframe(df_results.drop(['score','created_at'], axis=1))
