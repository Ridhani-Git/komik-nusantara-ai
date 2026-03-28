import streamlit as st
import requests
import base64
import json
import os

# 1. Konfigurasi Halaman Dasar
st.set_page_config(
    page_title="Portal Komik Nusantara AI",
    page_icon="🎨",
    layout="wide"
)

# Gaya Visual (CSS) agar tampilan seperti Komik Profesional
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .caption-box {
        background-color: #fffeb3;
        color: black;
        padding: 15px;
        border: 3px solid black;
        border-radius: 8px;
        font-weight: bold;
        margin-bottom: 20px;
        box-shadow: 6px 6px 0px #e11d48;
        font-family: 'Courier New', Courier, monospace;
    }
    h1, h2, h3 { font-family: 'Arial Black', sans-serif; color: #e11d48; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Mengambil API Key dari Streamlit Secrets
# PENTING: Di Dashboard Streamlit Cloud > Settings > Secrets harus ada baris ini:
# GEMINI_API_KEY = "AIzaSy..."
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# Judul Utama
st.markdown("<h1 style='text-align: center;'>🎨 PORTAL KOMIK NUSANTARA AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Ubah Legenda Nusantara menjadi Visual Nyata dengan AI</p>", unsafe_allow_html=True)

# 3. Database Cerita Rakyat
cerita_rakyat = {
    "Malin Kundang": [
        {"id": 1, "caption": "Malin berpamitan pada ibunya di dermaga kecil untuk merantau mengejar nasib.", "prompt": "Indonesian folklore comic style: young man in traditional West Sumatra clothes saying goodbye to his old mother, wooden dock, 19th century village coast, digital illustration"},
        {"id": 2, "caption": "Malin Kundang dikutuk menjadi batu di tepi pantai setelah durhaka kepada ibunya.", "prompt": "Indonesian folklore comic style: man in merchant clothes turning into stone statue on a beach, stormy sea, lightning, dramatic shadows, cinematic"}
    ],
    "Perang Banjar": [
        {"id": 1, "caption": "Kapal Belanda memasuki Sungai Barito, mengincar kekayaan Kesultanan Banjar.", "prompt": "Historical comic: 19th century Dutch steamships on Barito River, thick smoke, jungle landscape, cinematic, oil painting style"},
        {"id": 2, "caption": "Pangeran Antasari memimpin rakyat bergerilya di belantara Kalimantan Selatan.", "prompt": "Heroic comic: Prince Antasari leading Indonesian warriors in the jungle, traditional weapons, determined expression, high contrast, dramatic"}
    ]
}

# Sidebar untuk memilih cerita
with st.sidebar:
    st.header("📖 Pilih Legenda")
    pilihan = st.selectbox("Daftar Cerita:", list(cerita_rakyat.keys()))
    st.divider()
    st.info("Klik tombol 'Gambar' untuk mulai membuat visual adegan.")

# 4. Fungsi Mengambil Gambar dari AI
def generate_image(prompt_text):
    if not API_KEY or API_KEY.strip() == "":
        st.error("⚠️ API Key belum dipasang di Secrets!")
        return None
        
    # Menggunakan model 'imagen-3.0-fast-001' yang lebih ramah bagi pengguna free tier
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-fast-001:predict?key={API_KEY}"
    
    # PERBAIKAN PAYLOAD: 'instances' harus berupa LIST of objects
    payload = {
        "instances": [
            {
                "prompt": prompt_text
            }
        ],
        "parameters": {
            "sampleCount": 1
        }
    }
    
    try:
        res = requests.post(url, json=payload, timeout=60)
        
        if res.status_code == 200:
            result = res.json()
            if 'predictions' in result and len(result['predictions']) > 0:
                return result['predictions'][0]['bytesBase64Encoded']
            else:
                st.error("AI tidak memberikan gambar. Coba lagi.")
                return None
        else:
            # Menampilkan detail eror untuk debugging
            st.error(f"Eror dari Server (Status {res.status_code})")
            with st.expander("Klik untuk Detail Eror"):
                try:
                    st.json(res.json())
                except:
                    st.write(res.text)
            return None
    except Exception as e:
        st.error(f"Kesalahan Koneksi: {e}")
        return None

# 5. Tampilan Panel Komik
st.subheader(f"Cerita: {pilihan}")
panels = cerita_rakyat[pilihan]
cols = st.columns(2)

for i, p in enumerate(panels):
    with cols[i % 2]:
        st.write(f"### Panel {p['id']}")
        
        # Session State agar gambar tetap ada saat klik tombol lain
        key_img = f"img_{pilihan}_{p['id']}"
        ph = st.empty()
        
        if key_img in st.session_state:
            ph.image(base64.b64decode(st.session_state[key_img]), use_container_width=True)
        else:
            ph.warning("Visual belum dibuat.")
            
        # Tombol Gambar
        if st.button(f"🎨 Gambar Panel {p['id']}", key=f"btn_{pilihan}_{p['id']}"):
            with st.spinner("AI sedang melukis adegan..."):
                data = generate_image(p['prompt'])
                if data:
                    st.session_state[key_img] = data
                    st.rerun()

        # Kotak Narasi Teks
        st.markdown(f'<div class="caption-box">{p["caption"]}</div>', unsafe_allow_html=True)

st.divider()
st.caption("Dibuat dengan Python, Streamlit, dan Google Gemini AI")
