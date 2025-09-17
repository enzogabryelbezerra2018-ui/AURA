import streamlit as st
from llama_cpp import Llama
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
    
    # Carregar o modelo de IA
    MODEL_PATH = "Meta-Llama-3-8B-Instruct-Q4_K_M.gguf"
    if not os.path.exists(MODEL_PATH):
        st.error(f"O arquivo do modelo '{MODEL_PATH}' não foi encontrado.")
        st.stop()
    
    if "llm" not in st.session_state:
        st.session_state.llm = Llama(
            model_path=MODEL_PATH,
            chat_format="llama-3"
        )

    # Inicializar histórico de conversa
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
                    stream = st.session_state.llm.create_chat_completion(
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.history],
                        stream=True,
                    )
                    
                    full_response = ""
                    for chunk in stream:
                        content = chunk['choices'][0]['delta'].get('content', '')
                        full_response += content
                        st.markdown(full_response + "▌", unsafe_allow_html=True)
                    
                    st.session_state.history.append({"role": "assistant", "content": full_response})
                    st.markdown(full_response)
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro: {e}")
                    st.session_state.history.append({"role": "assistant", "content": "Desculpe, algo deu errado. Por favor, tente novamente mais tarde."})

# Executa o aplicativo
if __name__ == "__main__":
    chat_app()

