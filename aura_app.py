import streamlit as st
from openai import OpenAI
import os

# Função para injetar CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Lógica da conversa e renderização da interface
def chat_app():
    # Configuração da página e injeção do CSS
    st.set_page_config(page_title="Aura - IA", page_icon="✨", layout="centered")
    local_css("style.css")

    # Título com o ícone de coração e subtítulo
    st.markdown('<h1 class="stTitle">💜 Aura - Sua Inteligência Artificial</h1>', unsafe_allow_html=True)
    st.markdown('### ✨ Olá! Eu sou a Aura, sua assistente pessoal. ✨')
    
    # Adicionar uma linha divisória para separar o cabeçalho
    st.markdown("---")

    # Inicializar cliente da API e histórico de conversa
    if "history" not in st.session_state:
        st.session_state.history = [
            {"role": "system", "content": "Você é Aura, uma IA amigável e útil."},
            {"role": "assistant", "content": "Olá! Como posso te ajudar hoje?"}
        ]
    
    # Exibir o histórico de conversa
    for msg in st.session_state.history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        elif msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(msg["content"])
    
    # Caixa de texto para o usuário
    user_input = st.chat_input("Digite sua mensagem...")
    
    if user_input:
        # Adicionar a mensagem do usuário ao histórico
        st.session_state.history.append({"role": "user", "content": user_input})
        
        # Exibir a mensagem do usuário
        with st.chat_message("user"):
            st.markdown(user_input)

        # Lógica para gerar a resposta da IA
        with st.chat_message("assistant"):
            with st.spinner("Aura está pensando..."):
                try:
                    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.history],
                        temperature=0.7,
                        max_tokens=500
                    )
                    aura_reply = response.choices[0].message.content
                    st.markdown(aura_reply)
                    st.session_state.history.append({"role": "assistant", "content": aura_reply})
                except Exception as e:
                    st.error(f"Ocorreu um erro: {e}")
                    st.session_state.history.append({"role": "assistant", "content": "Desculpe, algo deu errado. Por favor, tente novamente mais tarde."})

# Executa o aplicativo
if __name__ == "__main__":
    chat_app()
