import streamlit as st

st.set_page_config(
     page_title="Gurgaon Real Estate Analytics App",
     page_icon="🏢" 
)

st.write("# Welcome to the Gurgaon Real Estate Analytics App!")
st.sidebar.success("Select a tool from the sidebar above.")
st.markdown("""
### How to use this app:
1. **Price Predictor**: Estimate the price of a property based on features.
2. **Analysis App**: Visualize trends and price heatmaps.
3. **Recommender**: Find similar apartments or properties within a radius.
""")