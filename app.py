import streamlit as st
import pandas as pd

# -----------------------------------------------------------
# 🎬 Netflix Dashboard (Minimal & Theme Adaptive)
# -----------------------------------------------------------

# Page setup
st.set_page_config(
    page_title="Netflix Dashboard",
    layout="wide",
    page_icon="🎬"
)

# -----------------------------------------------------------
# 🌈 Adaptive Styling (Improved for Dark Mode)
# -----------------------------------------------------------

theme_base = st.get_option("theme.base")
is_dark = theme_base == "dark"

# Set colors depending on theme
bg_color = "#0E1117" if is_dark else "#FFFFFF"
text_color = "#FAFAFA" if is_dark else "#262730"
highlight_color = "#E50914"  # Netflix red
metric_value_color = "#FFFFFF" if is_dark else "#000000"

st.markdown(f"""
    <style>
        /* Base background and text color */
        .main {{
            background-color: {bg_color};
            color: {text_color};
        }}

        h1, h2, h3 {{
            color: {highlight_color};
        }}

        /* --- Metric Styling --- */
        /* Metric label (small text) */
        [data-testid="stMetricLabel"] {{
            color: {text_color} !important;
        }}

        /* Metric value (numbers) */
        [data-testid="stMetricValue"] {{
            color: {metric_value_color} !important;
            font-weight: 700 !important;
        }}

        /* Sidebar text */
        [data-testid="stSidebar"] {{
            color: {text_color};
        }}

        /* Remove footer */
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
st.caption("A clean, minimal, and adaptive EDA dashboard")

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
# Overview Metrics
# -----------------------------------------------------------
st.subheader("📊 Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", len(filtered_df[filtered_df['type'] == 'Movie']))
col3.metric("TV Shows", len(filtered_df[filtered_df['type'] == 'TV Show']))

st.divider()

# -----------------------------------------------------------
# Content Type Distribution
# -----------------------------------------------------------
st.subheader("🎞️ Movies vs TV Shows")
type_counts = filtered_df['type'].value_counts()
if not type_counts.empty:
    st.bar_chart(type_counts, use_container_width=True)
else:
    st.info("No data available for this selection.")

# -----------------------------------------------------------
# Titles Added Over the Years
# -----------------------------------------------------------
st.subheader("📅 Titles Added Per Year")
yearly = filtered_df['year_added'].value_counts().sort_index()
if not yearly.empty:
    st.line_chart(yearly, use_container_width=True)
else:
    st.info("No yearly data found for selected filters.")

# -----------------------------------------------------------
# Top 10 Countries
# -----------------------------------------------------------
st.subheader("🌍 Top 10 Content-Producing Countries")
top_countries = filtered_df['country'].value_counts().head(10)
if not top_countries.empty:
    st.bar_chart(top_countries, use_container_width=True)
else:
    st.info("No country data available.")

# -----------------------------------------------------------
# Top 10 Genres
# -----------------------------------------------------------
st.subheader("🎭 Top 10 Genres on Netflix")
genres = filtered_df['listed_in'].dropna().str.split(', ').explode()
top_genres = genres.value_counts().head(10)
if not top_genres.empty:
    st.bar_chart(top_genres, use_container_width=True)
else:
    st.info("No genre data available.")

# -----------------------------------------------------------
# Ratings Distribution
# -----------------------------------------------------------
st.subheader("⭐ Ratings Distribution")
rating_counts = filtered_df['rating'].value_counts().head(10)
if not rating_counts.empty:
    st.bar_chart(rating_counts, use_container_width=True)
else:
    st.info("No rating data available.")

# -----------------------------------------------------------
# Show Raw Data
# -----------------------------------------------------------
with st.expander("🔍 View Raw Data"):
    st.dataframe(filtered_df)

# -----------------------------------------------------------
# Footer
# -----------------------------------------------------------
st.markdown("---")
st.markdown(
    f"<p style='text-align:center; color:{text_color};'>"
    f"Built with ❤️ using Streamlit | © 2025 Reshav Pradhan</p>",
    unsafe_allow_html=True
)
