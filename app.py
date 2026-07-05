import streamlit as st
import google.generativeai as genai

# ==============================================================================
# 1. KONFIGURASI HALAMAN & TAMPILAN (AESTHETIC)
# ==============================================================================
st.set_page_config(
    page_title="Pustaka Cendekia SMAN 5 Tegal",
    page_icon="📚",
    layout="centered"
)

# Gaya CSS Khusus untuk mempercantik tampilan chatbot dan logo
st.markdown("""
    <style>
    .school-header {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 2px solid #f0f2f6;
    }
    .school-logo {
        width: 80px;
        height: 80px;
        object-fit: contain;
    }
    .title-container h1 {
        font-size: 32px;
        margin: 0;
        color: #1e293b;
    }
    .title-container p {
        font-size: 16px;
        margin: 5px 0 0 0;
        color: #64748b;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. PENGATURAN API KEY (OTOMATIS & BACKUP)
# ==============================================================================
# Sistem akan mencoba membaca API Key secara otomatis dari Streamlit Secrets terlebih dahulu
api_key_valid = False
google_api_key = ""

if "GOOGLE_API_KEY" in st.secrets:
    google_api_key = st.secrets["GOOGLE_API_KEY"]
    if google_api_key and not google_api_key.startswith("Isi_Dengan_"):
        api_key_valid = True

# Jika Secrets belum diatur atau kosong, tampilkan kolom input manual di sidebar sebagai backup
if not api_key_valid:
    with st.sidebar:
        st.warning("⚠️ API Key permanen belum terdeteksi di Secrets.")
        manual_key = st.text_input("Masukkan Google API Key secara manual:", type="password")
        if manual_key:
            google_api_key = manual_key
            api_key_valid = True
else:
    # Jika sudah berhasil menggunakan Secrets, beri tanda hijau kecil di sidebar
    with st.sidebar:
        st.success("🔒 Google API Key terhubung otomatis & aman.")
        st.info("Aplikasi ini resmi dikelola oleh Perpustakaan SMA Negeri 5 Tegal.")

# ==============================================================================
# 3. KEPALA HALAMAN (LOGO DAN JUDUL RESMI SEKOLAH)
# ==============================================================================
# Catatan: Silakan ganti URL di bawah ini dengan URL logo resmi sekolah jika sudah ada di web/GitHub.
# Menggunakan logo buku default yang aesthetic jika URL belum diganti.
LOGO_URL = "https://www.sman5tegal.sch.id/upload/image/logo-sekolah.png" # Contoh URL resmi web sekolah

col1, col2 = st.columns([1, 5])
with col1:
    # Menampilkan logo sekolah
    st.image(LOGO_URL, width=80, output_format="PNG")
with col2:
    st.markdown("""
        <div class="title-container">
            <h1 style='margin-bottom: 0px; padding-bottom: 0px;'>Chatbot Pustaka Cendekia</h1>
            <p style='margin-top: 2px; font-weight: bold; color: #0d9488;'>SMA Negeri 5 Tegal</p>
            <p style='margin-top: 0px; font-size: 14px; color: #64748b;'>Asisten Pintar Layanan Perpustakaan Sekolah</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==============================================================================
# 4. INISIALISASI GEMINI AI (MODEL TERBARU)
# ==============================================================================
if api_key_valid:
    try:
        genai.configure(api_key=google_api_key)
        # Menggunakan model cerdas terbaru dari Google Gemini
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error(f"Gagal melakukan konfigurasi AI: {e}")
else:
    st.info("Silakan masukkan Google API Key Anda di menu Secrets Streamlit Cloud untuk mengaktifkan asisten pintar ini secara permanen.")
    st.stop()

# ==============================================================================
# 5. SISTEM CHATBOT (MEMORI DAN INTERAKSI)
# ==============================================================================
# Inisialisasi memori percakapan
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Halo! Saya asisten pintar Pustaka Cendekia SMA Negeri 5 Tegal. Ada yang bisa saya bantu seputar informasi buku, layanan perpustakaan, atau tugas sekolah Anda hari ini?"
        }
    ]

# Tampilkan seluruh riwayat pesan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Kolom Input Pengguna
if user_input := st.chat_input("Tanyakan sesuatu ke Pustaka Cendekia..."):
    # Tampilkan pesan pengguna
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Kirim ke Gemini AI dan dapatkan respon
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown("*Sedang berpikir...*")
        
        try:
            # Mengirim seluruh riwayat chat agar AI memiliki konteks percakapan sebelumnya
            formatted_history = []
            for msg in st.session_state.messages[:-1]:
                formatted_history.append({
                    "role": "user" if msg["role"] == "user" else "model",
                    "parts": [msg["content"]]
                })
            
            # Tambahkan instruksi sistem agar asisten bertingkah laku sopan dan ramah khas perpustakaan sekolah
            system_instruction = (
                "Anda adalah asisten AI pintar bernama 'Pustaka Cendekia', yang melayani perpustakaan "
                "di SMA Negeri 5 Tegal. Jawablah setiap pertanyaan dengan sangat ramah, sopan, mendidik, "
                "dan bantu para siswa serta guru dengan informasi yang akurat seputar literasi, buku, "
                "dan administrasi perpustakaan sekolah."
            )
            
            # Gabungkan instruksi dengan pertanyaan terakhir
            full_prompt = f"{system_instruction}\n\nPertanyaan Pengguna: {user_input}"
            
            response = model.generate_content(full_prompt)
            ai_response = response.text
            
            # Tampilkan respon di layar
            response_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            response_placeholder.empty()
            st.error(f"Terjadi kesalahan: {e}")
