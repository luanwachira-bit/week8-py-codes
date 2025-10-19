"""Simple Streamlit app for exploring the CORD-19 metadata.csv
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re

st.set_page_config(layout="wide")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    if 'publish_time' in df.columns:
        df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
        df['year'] = df['publish_time'].dt.year
    else:
        df['year'] = pd.NA
    df['title'] = df.get('title', '').fillna('').astype(str)
    df['abstract'] = df.get('abstract', '').fillna('').astype(str)
    return df

@st.cache_data
def top_title_words(series: pd.Series, n=100):
    def tokenize(text):
        text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        return [t for t in text.split() if len(t) > 2]
    counter = Counter()
    for t in series.fillna(''):
        counter.update(tokenize(t))
    return counter.most_common(n)

st.title('CORD-19 Metadata Explorer')
st.write('A simple explorer for the CORD-19 metadata file')

st.sidebar.header('Controls')

data_path = st.sidebar.text_input('Path to metadata CSV', 'metadata.csv')

try:
    df = load_data(data_path)
    if df.empty:
        raise FileNotFoundError()
except Exception:
    st.warning("Could not load 'metadata.csv' from the provided path. Falling back to bundled sample 'metadata_sample.csv'.")
    df = load_data('metadata_sample.csv')

min_year = int(df['year'].min()) if pd.notna(df['year'].min()) else 2019
max_year = int(df['year'].max()) if pd.notna(df['year'].max()) else 2022

year_range = st.sidebar.slider('Year range', min_year, max_year, (min_year, max_year))

filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

st.subheader(f'Summary (rows: {len(filtered)})')
col1, col2 = st.columns(2)
with col1:
    st.write('Publications by year')
    year_counts = filtered['year'].value_counts().sort_index()
    fig, ax = plt.subplots()
    year_counts.plot(kind='bar', ax=ax)
    ax.set_xlabel('Year')
    ax.set_ylabel('Count')
    st.pyplot(fig)

with col2:
    st.write('Top journals')
    if 'journal' in filtered.columns:
        top_j = filtered['journal'].fillna('unknown').value_counts().head(10)
        st.bar_chart(top_j)

st.write('Top title words')
words = top_title_words(filtered['title'], n=100)
wc = WordCloud(width=800, height=300, background_color='white').generate_from_frequencies(dict(words))
fig, ax = plt.subplots(figsize=(12, 4))
ax.imshow(wc, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

st.subheader('Data sample')
st.dataframe(filtered.head(50))

st.write('Notes: In Colab, run Streamlit with a tunnelling service like ngrok.')
