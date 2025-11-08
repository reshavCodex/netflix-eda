import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt

# -----------------------------------------------------------
# 🎬 Netflix Dashboard (Cinematic & Minimal)
# -----------------------------------------------------------

# Page setup
st.set_page_config(
    page_title="Netflix Dashboard",
    layout="wide",
    page_icon="🎬"
)

# -----------------------------------------------------------
# 🌈 Custom Styling
# -----------------------------------------------------------

theme_base = st.get_option("theme.base")
is_dark = theme_base == "dark"

# Dynamic colors
bg_color = "#000000" if is_dark else "#FFFFFF"
text_color = "#FFFFFF" if is_dark else "#1A1A1A"
highlight_color = "#E50914"
metric_value_color = "#FAFAFA" if is_dark else "#000000"

# Custom CSS for layout & animations
st.markdown(f"""
    <style>
        /* Background gradient */
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(180deg, #000000 0%, #141414 50%, #000000 100%);
        }}

        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: #141414;
            color: {text_color};
        }}

        /* Netflix red glowing title */
        h1 {{
            font-weight: 900 !important;
            color: {highlight_color} !important;
            text-shadow: 0px 0px 15px rgba(229, 9, 20, 0.7),
                         0px 0px 25px rgba(229, 9, 20, 0.5);
            animation: fadeIn 2s ease-in-out;
            text-align: center;
        }}

        @keyframes fadeIn {{
            from {{opacity: 0; transform: translateY(-10px);}}
            to {{opacity: 1; transform: translateY(0);}}
        }}

        h2, h3 {{
            color: {highlight_color};
        }}

        /* Metric & label text */
        [data-testid="stMetricLabel"] {{
            color: {text_color} !important;
        }}

        [data-testid="stMetricValue"] {{
            color: {metric_value_color} !important;
            font-weight: 700 !important;
        }}

        footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# Load dataset
# -----------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['country'].fillna('Unknown', inplace=True)
    df['rating'].fillna('Not Rated', inplace=True)
    return df

df = load_data()

# -----------------------------------------------------------
# Header
# -----------------------------------------------------------
st.title("🎬 Netflix Movies & TV Shows Dashboard")
st.caption("A cinematic, minimal, and interactive EDA dashboard")

# -----------------------------------------------------------
# Sidebar Filters
# -----------------------------------------------------------
st.sidebar.header("🎛️ Filters")
type_filter = st.sidebar.multiselect(
    "Select Type",
    options=df['type'].unique(),
    default=df['type'].unique()
)

country_filter = st.sidebar.selectbox(
    "Select Country",
    options=['All'] + list(df['country'].value_counts().head(15).index)
)

filtered_df = df[df['type'].isin(type_filter)]
if country_filter != 'All':
    filtered_df = filtered_df[filtered_df['country'] == country_filter]

# -----------------------------------------------------------
# Overview Cards
# -----------------------------------------------------------
st.markdown("## 📊 Overview")

col1, col2, col3 = st.columns(3)
col1.markdown(f"""
<div style="background-color:#141414; padding:20px; border-radius:10px; text-align:center;">
<h3 style='color:#E50914;'>🎬 Total Titles</h3>
<h2 style='color:white;'>{len(filtered_df):,}</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div style="background-color:#141414; padding:20px; border-radius:10px; text-align:center;">
<h3 style='color:#E50914;'>🎞️ Movies</h3>
<h2 style='color:white;'>{len(filtered_df[filtered_df['type']=="Movie"]):,}</h2>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div style="background-color:#141414; padding:20px; border-radius:10px; text-align:center;">
<h3 style='color:#E50914;'>📺 TV Shows</h3>
<h2 style='color:white;'>{len(filtered_df[filtered_df['type']=="TV Show"]):,}</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------------------------------
# Movies vs TV Shows
# -----------------------------------------------------------
st.markdown("## 🍿 Movies vs TV Shows")
type_counts = filtered_df['type'].value_counts()

if not type_counts.empty:
    sns.set_palette(["#E50914", "#B81D24"])
    st.bar_chart(type_counts, use_container_width=True)
else:
    st.info("No data available for this selection.")

st.markdown("---")

# -----------------------------------------------------------
# Titles Added Over the Years
# -----------------------------------------------------------
st.markdown("## 📅 Titles Added Per Year")
yearly = filtered_df['year_added'].value_counts().sort_index()
if not yearly.empty:
    st.line_chart(yearly, use_container_width=True)
else:
    st.info("No yearly data found for selected filters.")

st.markdown("---")

# -----------------------------------------------------------
# Top 10 Countries
# -----------------------------------------------------------
st.markdown("## 🌍 Top 10 Content-Producing Countries")
top_countries = filtered_df['country'].value_counts().head(10)
if not top_countries.empty:
    st.bar_chart(top_countries, use_container_width=True)
else:
    st.info("No country data available.")

st.markdown("---")

# -----------------------------------------------------------
# Top 10 Genres
# -----------------------------------------------------------
st.markdown("## 🎭 Top 10 Genres on Netflix")
genres = filtered_df['listed_in'].dropna().str.split(', ').explode()
top_genres = genres.value_counts().head(10)
if not top_genres.empty:
    st.bar_chart(top_genres, use_container_width=True)
else:
    st.info("No genre data available.")

st.markdown("---")

# -----------------------------------------------------------
# Ratings Distribution
# -----------------------------------------------------------
st.markdown("## ⭐ Ratings Distribution")
rating_counts = filtered_df['rating'].value_counts().head(10)
if not rating_counts.empty:
    st.bar_chart(rating_counts, use_container_width=True)
else:
    st.info("No rating data available.")

st.markdown("---")

# -----------------------------------------------------------
# Search Bar
# -----------------------------------------------------------
st.subheader("🔎 Search Titles")
search_term = st.text_input("Type a title or keyword:")
if search_term:
    results = filtered_df[filtered_df['title'].str.contains(search_term, case=False, na=False)]
    if not results.empty:
        st.dataframe(results)
    else:
        st.warning("No matches found.")

# -----------------------------------------------------------
# Footer
# -----------------------------------------------------------
st.markdown("---")
st.caption(f"🕓 Last updated on {dt.datetime.now().strftime('%B %d, %Y %I:%M %p')} | Built with ❤️ by Reshav Pradhan")
