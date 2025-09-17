import streamlit as st
from openai import OpenAI
import os

# Inicializar cliente
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Aura - IA", page_icon="✨", layout="centered")
st.title("💜 Aura - Sua Inteligência Artificial")

# Histórico de conversa
if "history" not in st.session_state:
    st.session_state.history = [{"role": "system", "content": "Você é Aura, uma IA amigável e útil."}]

# Caixa de texto
user_input = st.chat_input("Digite sua mensagem...")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.history,
        temperature=0.7,
        max_tokens=500
    )

    aura_reply = response.choices[0].message.content
    st.session_state.history.append({"role": "assistant", "content": aura_reply})

# Mostrar histórico como balões de chat
for msg in st.session_state.history:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(msg["content"])
