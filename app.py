import streamlit as st
import requests
import base64
import os

st.set_page_config(page_title="Komik Nusantara AI", layout="wide")

# CSS Sederhana
st.markdown("<style>.stApp { background-color: #0f172a; color: white; }</style>", unsafe_allow_html=True)

API_KEY = st.secrets.get("GEMINI_API_KEY", "")

st.title("🎨 Komik Nusantara AI")

cerita = {
    "Malin Kundang": [
        {"id": 1, "cap": "Malin berpamitan pada ibunya.", "prompt": "Indonesian folklore comic: young man saying goodbye to mother, dock, digital art"},
        {"id": 2, "cap": "Malin menjadi batu.", "prompt": "Indonesian folklore comic: man turning into stone on a beach, storm, lightning"}
    ]
}

pilih = st.selectbox("Pilih Cerita:", list(cerita.keys()))

def get_img(p):
    url = f"[https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key=](https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key=){API_KEY}"
    res = requests.post(url, json={"instances": {"prompt": p}, "parameters": {"sampleCount": 1}})
    if res.status_code == 200:
        return res.json()['predictions'][0]['bytesBase64Encoded']
    return None

for p in cerita[pilih]:
    st.write(f"### Panel {p['id']}")
    if st.button(f"Gambar Panel {p['id']}", key=p['id']):
        with st.spinner("AI sedang menggambar..."):
            data = get_img(p['prompt'])
            if data: st.image(base64.b64decode(data))
            else: st.error("Gagal! Cek API Key di Settings.")
    st.info(p['cap'])
