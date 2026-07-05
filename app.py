import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv # Jika nanti menggunakan file .env lokal

# 1. Konfigurasi Halaman Streamlit (Mobile-Friendly)
st.set_page_config(
    page_title="Chatbot Pustaka Cendekia",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Chatbot Pustaka Cendekia")
st.caption("Asisten Pintar Layanan Perpustakaan Sekolah")

# 2. Ambil API Key Google GenAI
# Saat di-deploy online, API Key disarankan disimpan di Secrets Management
api_key = st.sidebar.text_input("Masukkan Google API Key:", type="password")

if api_key:
    # Konfigurasi Google GenAI
    genai.configure(api_key=api_key)
    
    # Menggunakan model Gemini terbaru yang stabil untuk teks
    model = genai.GenerativeModel("gemini-2.5-flash")

    # 3. Inisialisasi Riwayat Obrolan (Session State)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "Halo! Saya asisten pintar Pustaka Cendekia. Ada yang bisa saya bantu seputar perpustakaan hari ini?"
            }
        ]

    # Display riwayat chat dari session state
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # 4. Input pengguna
    if user_input := st.chat_input("Tanyakan sesuatu ke Pustaka Cendekia..."):
        # Tampilkan chat user
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Generate respon dari Gemini AI
        with st.chat_message("assistant"):
            with st.spinner("Berpikir..."):
                try:
                    # Anda bisa menambahkan instruksi khusus/konteks sekolah di dalam prompt ini nanti
                    system_instruction = "Anda adalah asisten ramah untuk perpustakaan sekolah bernama Pustaka Cendekia. "
                    full_prompt = f"{system_instruction}\n\nUser: {user_input}"
                    
                    response = model.generate_content(full_prompt)
                    st.write(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
else:
    st.info("Silakan masukkan Google API Key Anda di sidebar untuk mulai menggunakan chatbot.", icon="🔑")
