import streamlit as st
import requests
import base64
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Komik Nusantara AI", layout="wide")

# CSS Sederhana untuk Gaya Komik
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: white; }
    .caption-box {
        background-color: #fffeb3;
        color: black;
        padding: 15px;
        border: 3px solid black;
        border-radius: 8px;
        font-weight: bold;
        margin-bottom: 20px;
        box-shadow: 6px 6px 0px #e11d48;
    }
    </style>
    """, unsafe_allow_html=True)

# Mengambil API Key dari Secrets (PENTING!)
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

st.title("🎨 Portal Komik Nusantara AI")

# Database Cerita
cerita = {
    "Malin Kundang": [
        {"id": 1, "cap": "Malin berpamitan pada ibunya untuk merantau.", "prompt": "Indonesian folklore comic: young man saying goodbye to mother, wooden dock, digital art"},
        {"id": 2, "cap": "Malin Kundang dikutuk menjadi batu di tepi pantai.", "prompt": "Indonesian folklore comic: man turning into stone on a beach, stormy sea, lightning"}
    ],
    "Perang Banjar": [
        {"id": 1, "cap": "Kapal Belanda memasuki Sungai Barito.", "prompt": "Historical comic: Dutch steamships on Barito River, thick smoke, 19th century"},
        {"id": 2, "cap": "Pangeran Antasari memimpin rakyat bergerilya di hutan.", "prompt": "Heroic comic: Prince Antasari leading warriors in Kalimantan jungle, dramatic"}
    ]
}

pilih = st.selectbox("Pilih Cerita Rakyat:", list(cerita.keys()))

def get_img(p):
    if not API_KEY:
        st.error("⚠️ API Key belum dipasang di Secrets!")
        return None
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={API_KEY}"
    
    try:
        res = requests.post(url, json={"instances": {"prompt": p}, "parameters": {"sampleCount": 1}}, timeout=40)
        if res.status_code == 200:
            return res.json()['predictions'][0]['bytesBase64Encoded']
        else:
            st.error(f"Eror AI: {res.status_code}")
            return None
    except Exception as e:
        st.error(f"Koneksi Gagal: {e}")
        return None

st.divider()
for p in cerita[pilih]:
    st.write(f"### Panel {p['id']}")
    
    if st.button(f"🎨 Gambar Panel {p['id']}", key=f"btn_{p['id']}"):
        with st.spinner("AI sedang melukis..."):
            data = get_img(p['prompt'])
            if data:
                st.image(base64.b64decode(data), use_container_width=True)
    
    st.markdown(f'<div class="caption-box">{p["cap"]}</div>', unsafe_allow_html=True)
