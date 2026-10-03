from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

API_URL = "http://localhost:8000"  # FastAPI backend address

st.set_page_config(page_title="BioLens", page_icon="💙", layout="wide")
st.markdown(
    "<style>#MainMenu,footer,header{visibility:hidden}"
    ".block-container{padding:0!important;max-width:100%!important}</style>",
    unsafe_allow_html=True,
)

base = Path(__file__).parent / "frontend"
html = (base / "index.html").read_text(encoding="utf-8")
css = (base / "style.css").read_text(encoding="utf-8")
js = (base / "script.js").read_text(encoding="utf-8")

html = html.replace('<link rel="stylesheet" href="style.css">', f"<style>{css}</style>")
html = html.replace(
    '<script src="script.js"></script>',
    f'<script>window.API_URL="{API_URL}";{js}</script>',
)

components.html(html, height=1500, scrolling=True)
