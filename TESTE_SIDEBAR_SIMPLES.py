import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

st.sidebar.title("SIDEBAR TESTE")
st.sidebar.write("Se você vê isso, sidebar funciona!")
st.sidebar.button("Botão teste")

st.title("Dashboard Teste")
st.write("Sidebar está visível?")



