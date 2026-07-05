import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Pustaka Cendekia - Chatbot Perpustakaan", page_icon="📚", layout="centered")

st.title("📚 Chatbot Pustaka Cendekia")
st.subheader("Asisten Pintar Perpustakaan Sekolah")
st.write("Tanyakan ketersediaan buku, rekomendasi bacaan, atau prosedur administrasi perpustakaan.")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("Wajib: Silakan masukkan GEMINI_API_KEY di dalam file .streamlit/secrets.toml")
    st.stop()

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

SYSTEM_INSTRUCTION = """
Anda adalah asisten virtual bernama 'Pustaka Cendekia' untuk perpustakaan sekolah.
Tugas utama Anda adalah:
1. Membantu siswa, guru, dan staf mencari buku atau merekomendasikan bahan pustaka.
2. Menjawab alur administrasi perpustakaan (misal: batas pinjam 7 hari, denda keterlambatan Rp1.000/hari).
3. Selalu menjawab dengan sopan, ramah, dan edukatif menggunakan bahasa Indonesia yang baik.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ketik pertanyaan Anda di sini..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    contents_payload = []
    for msg in st.session_state.messages:
        role_type = "user" if msg["role"] == "user" else "model"
        contents_payload.append(types.Content(role=role_type, parts=[types.Part.from_text(text=msg["content"])]))
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents_payload,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION, temperature=0.4),
            )
            assistant_response = response.text
            message_placeholder.markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        except Exception as e:
            st.error(f"Terjadi kesalahan koneksi API: {e}")
