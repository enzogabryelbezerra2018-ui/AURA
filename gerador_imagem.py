import streamlit as st
from diffusers import AutoPipelineForText2Image
import torch

# Define o modelo para imagens detalhadas
model_name = "stabilityai/stable-diffusion-xl-base-1.0"

# Define a plataforma de processamento (GPU, se disponível, é muito mais rápido)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Carrega o "motor" da IA de imagem.
pipeline = AutoPipelineForText2Image.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    use_safetensors=True
)
pipeline.to(device)

# Função para gerar a imagem
def generate_detailed_image(prompt):
    with st.spinner("Aura está criando a sua obra de arte..."):
        # A IA gera a imagem
        image = pipeline(prompt).images[0]
        st.image(image, caption=prompt)
        st.success("Imagem gerada com sucesso!")

# Exemplo de como você pode usar a função
st.title("Gerador de Imagens com a Aura")
st.markdown("Peça qualquer imagem detalhada que você quiser!")

user_prompt = st.text_input("Sua descrição da imagem:")

if st.button("Gerar Imagem"):
    if user_prompt:
        generate_detailed_image(user_prompt)
    else:
        st.error("Por favor, digite uma descrição para a imagem.")

