import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Analytics Demo", layout="wide")

st.title('Gurgaon Real Estate Analytics')

# ---------------- LOAD DATA ----------------
new_df = pd.read_csv('datasets/data_viz1.csv')

feature_text = pickle.load(open('datasets/feature_text.pkl', 'rb'))

# ---------------- MAP DATA ----------------
group_df = new_df.groupby('sector', as_index=False).agg({
    'price': 'mean',
    'price_per_sqft': 'mean',
    'built_up_area': 'mean',
    'latitude': 'mean',
    'longitude': 'mean'
})

# Ensure latitude and longitude are numeric
group_df['latitude'] = pd.to_numeric(group_df['latitude'], errors='coerce')
group_df['longitude'] = pd.to_numeric(group_df['longitude'], errors='coerce')

# Remove rows with missing coordinates
group_df.dropna(subset=['latitude', 'longitude'], inplace=True)

# ---------------- MAP ----------------
st.header('Sector Price per Sqft Map')

fig = px.scatter_mapbox(
    group_df,
    lat="latitude",
    lon="longitude",
    color="price_per_sqft",
    size='built_up_area',
    color_continuous_scale=px.colors.cyclical.IceFire,
    zoom=10,
    mapbox_style="open-street-map",
    width=1200,
    height=700,
    hover_name='sector'
)

fig.update_layout(
    margin={"r":0, "t":0, "l":0, "b":0}
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- WORD CLOUD ----------------
st.header('Common Features Wordcloud')

wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='black',
    stopwords=set(['s']),
    min_font_size=10
).generate(feature_text)

fig_wc, ax_wc = plt.subplots(figsize=(10, 5))

ax_wc.imshow(wordcloud, interpolation='bilinear')
ax_wc.axis("off")

st.pyplot(fig_wc)

# ---------------- AREA VS PRICE ----------------
st.header('Area Vs Price Analysis')

property_selection = st.selectbox(
    'Select Property Type',
    ['flat', 'house']
)

filt_df = new_df[new_df['property_type'] == property_selection]

fig_scatter = px.scatter(
    filt_df,
    x="built_up_area",
    y="price",
    color="bedRoom",
    title=f"{property_selection.capitalize()} Area vs Price"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# ---------------- PRICE DISTRIBUTION ----------------
st.header('Price Distribution by Property Type')

fig_dist, ax_dist = plt.subplots(figsize=(10, 4))

sns.kdeplot(
    new_df[new_df['property_type'] == 'house']['price'],
    label='House',
    fill=True,
    ax=ax_dist
)

sns.kdeplot(
    new_df[new_df['property_type'] == 'flat']['price'],
    label='Flat',
    fill=True,
    ax=ax_dist
)

ax_dist.legend()

st.pyplot(fig_dist)