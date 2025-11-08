import streamlit as st
import pandas as pd

# -----------------------------------------------------------
# 🎬 Netflix Dashboard (Minimal & Elegant)
# -----------------------------------------------------------

# Page setup
st.set_page_config(
    page_title="Netflix Dashboard",
    layout="wide",
    page_icon="🎬"
)

# Custom minimalist style
st.markdown("""
    <style>
        .main {
            background-color: #fafafa;
        }
        h1, h2, h3 {
            color: #E50914;  /* Netflix red */
        }
        .stMetric label, .stMarkdown, .stDataFrame {
            color: #333333;
        }
        footer {visibility: hidden;}
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
st.caption("A clean, minimal, and interactive EDA dashboard")

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
st.markdown("Built with ❤️ using Streamlit | © 2025 Reshav Pradhan")
