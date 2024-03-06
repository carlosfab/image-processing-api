from io import BytesIO
from PIL import Image
import numpy as np
import requests
import cv2

def deskew_image_api(img: np.ndarray) -> np.ndarray:
    """
    Envia uma imagem para uma API que realiza a operação de deskew (correção de inclinação)
    e retorna a imagem corrigida.

    Args:
        img (np.ndarray): Imagem original em formato de array da NumPy.

    Returns:
        np.ndarray: Imagem após correção de inclinação.
    """
    API_ENDPOINT = "https://0gd0qxmt28.execute-api.us-east-2.amazonaws.com/desenvolvimento"

    # Codifica a imagem para formato PNG em bytes
    is_success, im_buf_arr = cv2.imencode(".png", img)
    byte_im = im_buf_arr.tobytes()

    # Envia a imagem codificada para a API e recebe a resposta
    response = requests.post(url=API_ENDPOINT, data=byte_im)

    # Converte a resposta (imagem corrigida) para um array da NumPy
    img_corrected = Image.open(BytesIO(response.content))

    return np.asarray(img_corrected)


def read_and_deskew_image(img_path: str, output_path: str = './deskewed_image.png') -> None:
    """
    Lê uma imagem do disco, aplica a correção de inclinação através de uma API e salva o resultado.

    Args:
        img_path (str): Caminho da imagem original.
        output_path (str): Caminho para salvar a imagem corrigida.
    """
    # Lê a imagem do caminho especificado
    img = cv2.imread(img_path)

    # Aplica a correção de inclinação utilizando a API
    img_deskewed = deskew_image_api(img)

    # Salva a imagem corrigida no caminho de saída especificado
    cv2.imwrite(output_path, img_deskewed)


if __name__ == "__main__":
    # Caminho da imagem a ser processada
    img_path = './test_img.png'

    # Executa a leitura e correção de inclinação da imagem
    read_and_deskew_image(img_path)
