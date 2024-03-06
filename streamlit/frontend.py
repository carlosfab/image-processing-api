import streamlit as st
import numpy as np
import requests
import cv2

st.set_page_config(page_title="Corretor de Inclinação de Imagens - Visão Computacional AWS", layout="wide")

def deskew_image_api(img: np.ndarray) -> np.ndarray:
    API_ENDPOINT = "https://0gd0qxmt28.execute-api.us-east-2.amazonaws.com/desenvolvimento"
    # Codifica a imagem para formato PNG em bytes
    is_success, im_buf_arr = cv2.imencode(".png", img)
    if not is_success:
        raise Exception("Não foi possível codificar a imagem para o formato PNG")
    byte_im = im_buf_arr.tobytes()

    # Envia a imagem codificada para a API e recebe a resposta
    response = requests.post(url=API_ENDPOINT, data=byte_im)
    if response.status_code != 200:
        raise Exception(f"Falha na requisição à API: {response.status_code}")

    # Lê a imagem diretamente da resposta como um array NumPy
    img_corrected = np.frombuffer(response.content, np.uint8)
    img_corrected = cv2.imdecode(img_corrected, cv2.IMREAD_COLOR)

    return img_corrected

def convert_uploaded_file_to_cv2_image(uploaded_file):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return img

def main():
    st.title("Aplicativo de Correção de Inclinação")
    
    # Texto descritivo abaixo do título
    st.write("""
    Este aplicativo demonstra o uso da AWS para aplicações de visão computacional, 
    abrangendo desde a configuração da conta AWS e AWS CLI, até a criação de uma função Lambda com Docker
    para processamento de imagens, e finalmente a exposição dessa funcionalidade via API Gateway.
    """)
    
    # Adiciona o informações na sidebar
    st.sidebar.image("logo.png")
    st.sidebar.write("Autor: Carlos Melo")
    st.sidebar.write("Repositório: [GitHub](http://github.com/carlosfab/image-processing-api)")
    st.sidebar.write("[Especialização em Visão Computacional](https://escola.sigmoidal.ai/especializacao-em-visao-computacional/)")

    
    uploaded_file = st.file_uploader("Escolha uma imagem para corrigir", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Convertendo a imagem carregada para um formato que a API pode processar
        img_original = convert_uploaded_file_to_cv2_image(uploaded_file)

        # Aplicando correção de inclinação
        try:
            img_deskewed = deskew_image_api(img_original)

            # Convertendo imagens de BGR para RGB para exibição
            img_original_rgb = cv2.cvtColor(img_original, cv2.COLOR_BGR2RGB)
            img_deskewed_rgb = cv2.cvtColor(img_deskewed, cv2.COLOR_BGR2RGB)

            # Exibindo imagens lado a lado
            col1, col2 = st.columns(2)
            with col1:
                st.image(img_original_rgb, caption="Imagem Original", use_column_width=True)
            with col2:
                st.image(img_deskewed_rgb, caption="Imagem Corrigida", use_column_width=True)
        except Exception as e:
            st.error(f"Erro ao processar a imagem: {e}")

if __name__ == "__main__":
    main()
