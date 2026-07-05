import streamlit as st
import google.generativeai as genai
import os

# Konfigurasi Halaman Utama Streamlit (Tampilan Premium)
st.set_page_config(
    page_title="Chatbot Pustaka Cendekia SMAN 5 Tegal",
    page_icon="📚",
    layout="centered"
)

# Gaya CSS Khusus untuk memberikan estetika profesional yang serasi dengan Logo Perpus.png (Oranye & Emas)
st.markdown("""
    <style>
    /* Styling Header Sekolah */
    .school-header-container {
        display: flex;
        align-items: center;
        gap: 25px;
        background: linear-gradient(135deg, #fffcf6 0%, #fff3e0 100%);
        padding: 20px;
        border-radius: 16px;
        border-left: 5px solid #f57c00;
        box-shadow: 0 4px 15px rgba(245, 124, 0, 0.05);
        margin-bottom: 25px;
    }
    .title-container h1 {
        font-size: 26px;
        font-weight: 800;
        margin: 0;
        color: #e65100;
        line-height: 1.2;
    }
    .title-container .subtitle {
        font-size: 16px;
        font-weight: 700;
        margin: 4px 0 0 0;
        color: #fb8c00;
        letter-spacing: 0.5px;
    }
    .title-container .desc {
        font-size: 13px;
        margin: 3px 0 0 0;
        color: #5c5c5c;
    }
    
    /* Styling Chat Bubbles & Alerts */
    .stAlert {
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Sistem Keamanan Kunci: Membaca GOOGLE_API_KEY dari Streamlit Secrets secara otomatis (Permanen)
api_key_valid = False
google_api_key = ""

if "GOOGLE_API_KEY" in st.secrets:
    google_api_key = st.secrets["GOOGLE_API_KEY"]
    if google_api_key and not google_api_key.startswith("Isi_Dengan_"):
        api_key_valid = True

# Jika Secrets belum dikonfigurasi, sediakan input manual di sidebar sebagai cadangan darurat
if not api_key_valid:
    with st.sidebar:
        st.warning("⚠️ API Key permanen belum terdeteksi di Secrets.")
        manual_key = st.text_input("Masukkan Google API Key secara manual:", type="password")
        if manual_key:
            google_api_key = manual_key
            api_key_valid = True
else:
    # Jika sudah aman menggunakan Secrets, tampilkan status hijau bersih di sidebar tanpa tombol input pengganggu
    with st.sidebar:
        st.success("🔒 Google API Key terhubung otomatis & aman.")
        st.info("Aplikasi Resmi Perpustakaan Pustaka Cendekia - SMA Negeri 5 Tegal.")

# Logika Penampilan Logo Sekolah (Membaca file lokal Logo Perpus.png)
LOGO_FILE = "Logo Perpus.png"

# Membuat Layout Header Responsif
col1, col2 = st.columns([1, 4])

with col1:
    # Mengecek apakah file Logo Perpus.png sudah diunggah ke GitHub
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, use_container_width=True)
    else:
        # Tampilan cadangan jika logo belum diunggah ke repositori GitHub
        st.markdown(
            "<div style='font-size: 55px; text-align: center; margin-top: 10px;'>📚</div>", 
            unsafe_allow_html=True
        )
        with st.sidebar:
            st.warning(
                f"💡 Tips: Unggah file gambar logo Anda dengan nama **'{LOGO_FILE}'** "
                "ke repositori GitHub Anda agar logo sekolah tampil otomatis di atas judul."
            )

with col2:
    st.markdown(f"""
        <div class="title-container">
            <h1>Chatbot Pustaka Cendekia</h1>
            <p class="subtitle">SMA Negeri 5 Tegal</p>
            <p class="desc">Asisten Pintar Layanan Perpustakaan Sekolah & Pusat Literasi Siswa</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin: 15px 0 25px 0; border: 0; border-top: 1px solid #e0e0e0;'>", unsafe_allow_html=True)

# Konfigurasi Model AI Gemini Generasi Terbaru (Gemini 2.5 Flash)
if api_key_valid:
    try:
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error(f"Gagal melakukan konfigurasi sistem AI: {e}")
        st.stop()
else:
    st.info("Silakan konfigurasikan Google API Key Anda di menu Secrets Streamlit Cloud untuk mengaktifkan asisten pintar ini.")
    st.stop()

# Inisialisasi Memori Percakapan Chatbot
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Halo! Selamat datang di layanan perpustakaan **Pustaka Cendekia SMA Negeri 5 Tegal**. "
                "Saya adalah asisten virtual resmi Anda di sini. Ada yang bisa saya bantu hari ini seputar "
                "rekomendasi buku, informasi literasi, atau tugas-tugas belajar Anda?"
            )
        }
    ]

# Tampilkan seluruh riwayat pesan dengan format bawaan Streamlit yang bersih
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input Pertanyaan Pengguna
if user_input := st.chat_input("Tanyakan sesuatu seputar perpustakaan atau pelajaran..."):
    # Tampilkan pesan pengguna di layar dan simpan ke riwayat
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Kirim ke AI dengan Instruksi Sistem yang Ramah dan Mendidik
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown("*Sedang meramu jawaban terbaik...*")
        
        try:
            # Memformat seluruh riwayat pesan agar AI memahami alur percakapan sebelumnya
            formatted_history = []
            for msg in st.session_state.messages[:-1]:
                formatted_history.append({
                    "role": "user" if msg["role"] == "user" else "model",
                    "parts": [msg["content"]]
                })
            
            # Instruksi Kepribadian AI (Sopan, Ramah, Akademis, Bertema SMA Negeri 5 Tegal)
            system_instruction = (
                "Anda adalah asisten kecerdasan buatan resmi bernama 'Pustaka Cendekia', "
                "yang bertugas melayani perpustakaan di sekolah SMA Negeri 5 Tegal. "
                "Berikan jawaban yang sangat ramah, mendidik, sopan, dan mendukung "
                "kegiatan literasi para siswa dan guru. Sapa mereka dengan hangat. "
                "Jika ditanya mengenai sekolah atau perpustakaan, jawablah dengan penuh rasa bangga "
                "sebagai bagian dari keluarga besar SMA Negeri 5 Tegal."
            )
            
            # Gabungkan instruksi sistem dengan input dari pengguna saat ini
            full_prompt = f"{system_instruction}\n\nPertanyaan Pengguna: {user_input}"
            
            # Memanggil API Gemini 2.5 Flash
            response = model.generate_content(full_prompt)
            ai_response = response.text
            
            # Menampilkan hasil respons di layar dan menyimpannya ke riwayat
            response_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            response_placeholder.empty()
            st.error(f"Sistem mengalami gangguan teknis: {e}")
