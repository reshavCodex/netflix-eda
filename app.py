import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt

# -----------------------------------------------------------
# 🎬 Netflix Dashboard (Cinematic Adaptive Theme)
# -----------------------------------------------------------

# Page setup
st.set_page_config(
    page_title="Netflix Dashboard",
    layout="wide",
    page_icon="🎬"
)

# -----------------------------------------------------------
# 🌈 Detect Theme
# -----------------------------------------------------------

theme_base = st.get_option("theme.base")
is_dark = theme_base == "dark"

# Color palette for both themes
highlight_color = "#E50914"
if is_dark:
    bg_color = "#000000"
    section_bg = "#141414"
    text_color = "#FFFFFF"
    card_text = "#FAFAFA"
else:
    bg_color = "#FAF7F2"         # light beige background
    section_bg = "#FFFFFF"       # white cards
    text_color = "#111111"
    card_text = "#111111"

# -----------------------------------------------------------
# ✨ Styling & Animation
# -----------------------------------------------------------

st.markdown(f"""
<style>

/* Backgrounds */
[data-testid="stAppViewContainer"] {{
    background: linear-gradient(180deg, {bg_color} 0%, {section_bg} 50%, {bg_color} 100%);
}}
[data-testid="stSidebar"] {{
    background-color: {section_bg};
    color: {text_color};
}}

/* Header */
h1 {{
    font-weight: 900 !important;
    color: {highlight_color} !important;
    text-shadow: 0px 0px 15px rgba(229, 9, 20, 0.6),
                 0px 0px 25px rgba(229, 9, 20, 0.4);
    text-align: center;
    animation: fadeInSmooth 2s ease-in-out;
}}

h2, h3 {{
    color: {highlight_color};
}}

/* Metric Labels & Values */
[data-testid="stMetricLabel"] {{
    color: {text_color} !important;
}}
[data-testid="stMetricValue"] {{
    color: {card_text} !important;
    font-weight: 700 !important;
}}

/* Fade-in animations */
@keyframes fadeInSmooth {{
    0% {{ opacity: 0; transform: translateY(-10px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
}}

h1, h2, h3, .stMarkdown {{
    animation: fadeInSmooth 1.5s ease-in-out;
}}

/* Hover lift for cards */
div[data-testid="stMarkdownContainer"] div[style*="background-color:#141414"],
div[data-testid="stMarkdownContainer"] div[style*="background-color:#FFFFFF"] {{
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}
div[data-testid="stMarkdownContainer"] div[style*="background-color:#141414"]:hover,
div[data-testid="stMarkdownContainer"] div[style*="background-color:#FFFFFF"]:hover {{
    transform: translateY(-5px);
    box-shadow: 0 4px 15px rgba(229, 9, 20, 0.4);
}}

/* Chart fade-in */
[data-testid="stVegaLiteChart"], [data-testid="stBarChart"], [data-testid="stLineChart"] {{
    animation: fadeInSmooth 1.2s ease-in-out;
}}

footer {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# Load Dataset
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
st.caption("A cinematic, minimal, and adaptive EDA dashboard")

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
card_bg = section_bg

col1.markdown(f"""
<div style="background-color:{card_bg}; padding:20px; border-radius:10px; text-align:center;">
<h3 style='color:{highlight_color};'>🎬 Total Titles</h3>
<h2 style='color:{card_text};'>{len(filtered_df):,}</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div style="background-color:{card_bg}; padding:20px; border-radius:10px; text-align:center;">
<h3 style='color:{highlight_color};'>🎞️ Movies</h3>
<h2 style='color:{card_text};'>{len(filtered_df[filtered_df['type']=="Movie"]):,}</h2>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div style="background-color:{card_bg}; padding:20px; border-radius:10px; text-align:center;">
<h3 style='color:{highlight_color};'>📺 TV Shows</h3>
<h2 style='color:{card_text};'>{len(filtered_df[filtered_df['type']=="TV Show"]):,}</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------------------------------
# Charts
# -----------------------------------------------------------

st.markdown("## 🍿 Movies vs TV Shows")
type_counts = filtered_df['type'].value_counts()
if not type_counts.empty:
    sns.set_palette(["#E50914", "#B81D24"])
    st.bar_chart(type_counts, use_container_width=True)
else:
    st.info("No data available for this selection.")

st.markdown("---")

st.markdown("## 📅 Titles Added Per Year")
yearly = filtered_df['year_added'].value_counts().sort_index()
if not yearly.empty:
    st.line_chart(yearly, use_container_width=True)
else:
    st.info("No yearly data found for selected filters.")

st.markdown("---")

st.markdown("## 🌍 Top 10 Content-Producing Countries")
top_countries = filtered_df['country'].value_counts().head(10)
if not top_countries.empty:
    st.bar_chart(top_countries, use_container_width=True)
else:
    st.info("No country data available.")

st.markdown("---")

st.markdown("## 🎭 Top 10 Genres on Netflix")
genres = filtered_df['listed_in'].dropna().str.split(', ').explode()
top_genres = genres.value_counts().head(10)
if not top_genres.empty:
    st.bar_chart(top_genres, use_container_width=True)
else:
    st.info("No genre data available.")

st.markdown("---")

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
