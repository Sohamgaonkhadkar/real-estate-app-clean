import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Recommend Apartments")

# Load datasets from the datasets folder
try:
    location_df = pickle.load(open('datasets/location_distance.pkl', 'rb'))
    cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
    cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
    cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl', 'rb'))
except FileNotFoundError as e:
    st.error(f"Error loading datasets: {e}")
    st.stop()

def recommend_properties_with_scores(property_name, top_n=5):
    # Weighted similarity matrix
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1.0 * cosine_sim3
    
    # Get index of the selected property
    try:
        idx = location_df.index.get_loc(property_name)
    except KeyError:
        return pd.DataFrame(columns=['PropertyName', 'SimilarityScore'])

    # Get similarity scores and sort
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get top_n (excluding the property itself)
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    
    return pd.DataFrame({
        'PropertyName': location_df.index[top_indices].tolist(),
        'SimilarityScore': top_scores
    })

# --- UI SECTION ---

# Search by Radius
st.title('Find Properties Nearby')
selected_location = st.selectbox('Select Center Location', sorted(location_df.columns.to_list()))
radius = st.number_input('Radius in Kms', min_value=1.0, step=1.0)

if st.button('Search Area'):
    # Filtering distance (stored in meters in location_df)
    result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()
    
    if result_ser.empty:
        st.info("No properties found within this radius.")
    else:
        for name, dist in result_ser.items():
            st.text(f"{name}: {round(dist/1000, 2)} kms away")

st.divider()

# Content-Based Recommendation
st.title('Recommend Similar Apartments')
selected_appartment = st.selectbox('Select an Apartment to find similar ones', sorted(location_df.index.to_list()))

if st.button('Recommend'):
    recommendation_df = recommend_properties_with_scores(selected_appartment)
    if not recommendation_df.empty:
        st.dataframe(recommendation_df, use_container_width=True)
    else:
        st.error("Could not find recommendations for this selection.")

