import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Price Predictor")


try:
    with open('df.pkl', 'rb') as file:
        df = pickle.load(file)

    with open('pipeline.pkl', 'rb') as file:
        pipeline = pickle.load(file)

   
    try:
        preprocessor = pipeline.named_steps['preprocessor']

        if not hasattr(preprocessor, '_name_to_fitted_passthrough'):
            preprocessor._name_to_fitted_passthrough = {}
    except:
        pass


except FileNotFoundError:
    st.error("Model files not found. Please ensure df.pkl and pipeline.pkl are in the root directory.")
    st.stop()

st.header('Enter Property Details')

col1, col2 = st.columns(2)

with col1:
    property_type = st.selectbox('Property Type', ['flat', 'house'])
    sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))
    bedrooms = float(st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist())))
    bathroom = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))
    balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))
    property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

with col2:
    built_up_area = float(st.number_input('Built Up Area (Sq.Ft)'))
    servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))
    store_room = float(st.selectbox('Store Room', [0.0, 1.0]))
    furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
    luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
    floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

if st.button('Predict Price'):

    columns = [
        'property_type',
        'sector',
        'bedRoom',
        'bathroom',
        'balcony',
        'agePossession',
        'built_up_area',
        'servant room',
        'store room',
        'furnishing_type',
        'luxury_category',
        'floor_category'
    ]

    data = [[
        property_type,
        sector,
        bedrooms,
        bathroom,
        balcony,
        property_age,
        built_up_area,
        servant_room,
        store_room,
        furnishing_type,
        luxury_category,
        floor_category
    ]]

    one_df = pd.DataFrame(data, columns=columns)

    prediction = pipeline.predict(one_df)

    base_price = np.expm1(prediction)[0]

    low = base_price - 0.22
    high = base_price + 0.22

    st.success(f"Estimated Price: ₹{round(low, 2)} Cr - ₹{round(high, 2)} Cr")