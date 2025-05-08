"""
Streamlit dashboard az Iris modellhez.
Lehetővé teszi predikciók készítését és az EvidentlyAI drift report megjelenítését.
"""

import streamlit as st
import requests
import pandas as pd
import os

st.title('Iris ML Model Streamlit Dashboard')
st.write('Adja meg a virág jellemzőit, és a modell megmondja a fajt!')

# Bemeneti mezők
sepal_length = st.number_input('Sepal length (cm)', min_value=0.0, max_value=10.0, value=5.1)
sepal_width = st.number_input('Sepal width (cm)', min_value=0.0, max_value=10.0, value=3.5)
petal_length = st.number_input('Petal length (cm)', min_value=0.0, max_value=10.0, value=1.4)
petal_width = st.number_input('Petal width (cm)', min_value=0.0, max_value=10.0, value=0.2)

if st.button('Predikció'):
    # REST API hívás
    data = {
        'sepal_length': sepal_length,
        'sepal_width': sepal_width,
        'petal_length': petal_length,
        'petal_width': petal_width
    }
    try:
        response = requests.post('http://localhost:8000/predict', json=data)
        if response.status_code == 200:
            pred = response.json()['prediction']
            label = ['setosa', 'versicolor', 'virginica'][pred]
            st.success(f'A predikált faj: {label}')
        else:
            st.error('Hiba a predikció során!')
    except Exception as e:
        st.error(f'Hiba: {e}')






