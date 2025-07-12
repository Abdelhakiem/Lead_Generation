# Lead Generation System

A web-based lead generation platform that leverages social media scraping, Large Language Models (LLMs) for user profiling, and transformer-based similarity scoring to identify and rank potential customers for targeted marketing campaigns.

---

## 🚀 Project Overview

* **Social Media Scraping**: Collects user posts and profile information by entering social media URLs.
* **LLM Analysis**: Enriches raw scraped data with AI-generated summaries, psychographics, interests, habits, and lifestyle indicators.
* **Campaign Targeting**: Allows manual demographic filtering combined with a transformer-based cross-encoder (MS MARCO MiniLM) to score and rank users against campaign descriptions.
* **User Profiling**: Interactive dashboards to explore detailed profiles of individuals, including metrics, habits, interests, activities, and spending patterns.

---

## ⚙️ Core Functionalities

### 1. Campaign Targeting

* **Manual Filters**: Age, gender, marital status, location, education, job role.
* **Campaign Description**: Text input for product or campaign copy.
* **Scoring**: Uses `cross-encoder/ms-marco-MiniLM-L6-v2` to compute a relevance score between each user’s profile and the campaign.
* **Threshold & Top‑N**: Slider to set a minimum score and input for maximum number of users to display.
* **Profile Drill‑Down**: Click a user in the results to view their detailed profile.

### 2. User Directory & Profiling

* **Directory**: Dropdown list of all users from the database or JSON file.
* **Profile Dashboard**: Rich UI cards showing basic info, metrics, habits, interactive charts for interests, lists for activities, life indicators, and spending.
* **Styling**: Custom CSS and optional background imagery for a polished look.

---

## 🗂 File Structure

```plaintext
Lead_Generation/
├── campaign_targeting/
│   ├── app.py                 # Campaign targeting page module
│   ├── artifacts/
│   │   └── cross_encoder_ms_marco/  # Cached transformer model
│   └── ...                    # Helper notebooks, test DB
├── user_profiling/
│   ├── st2.py                 # User directory & profiling page module
│   ├── llm_user_profiles_analysis.json  # AI-enriched profiles
│   └── style.css              # Custom styling for profile dashboard
├── dataset/
│   └── databases/
│       └── test_profiles.db   # SQLite database of scraped profiles
├── root_app.py                # Main multipage Streamlit entrypoint
├── server.py                  # Alias to run root_app
├── requirements.txt           # Python dependencies
└── README.md                  # This documentation
```

---

## 💻 Installation & Run

1. **Clone the repository**

   ```bash
   git clone git@github.com:Abdelhakiem/Lead_Generation.git
   cd Lead_Generation
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**

   ```bash
   streamlit run server.py
   ```

4. **Open in your browser**
   
   * Local: `http://localhost:8501`
---

## 📂 Data Sources

* **SQLite DB** (`dataset/databases/test_profiles.db`): Contains `user_profiles` table with columns matching fields used in profiling and targeting.
* **JSON** (`user_profiling/llm_user_profiles_analysis.json`): LLM-enriched user analyses, used for detailed profiling.

