
import json
import cv2
import base64
import numpy as np

def encode_image_to_base64(
        img: np.ndarray
        ) -> str:
    """
    Codifica uma imagem (array da NumPy) diretamente para a representação em string Base64, 
    salvando temporariamente em um arquivo.

    Args:
        img (np.ndarray): A imagem como um array da NumPy para ser codificada.

    Returns:
        str: A representação da imagem codificada em Base64.
    """
    # Caminho temporário para salvar a imagem
    aux_path = '/tmp/tmp_image.png'
    # Salva a imagem no caminho temporário
    cv2.imwrite(aux_path, img)

    # Abre a imagem salva, codifica em Base64, e retorna a string decodificada
    with open(aux_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode("utf-8")

    return encoded_string


def decode_base64_to_image(
        encoded_string: str,
        img_path: str = "/tmp/decoded_img.png"  # Alterado para usar o diretório /tmp
        ) -> np.ndarray:
    """
    Decodifica uma string Base64 para uma imagem e salva como arquivo, então lê a imagem do arquivo e retorna como um array da NumPy.

    Args:
        encoded_string (str): String Base64 da imagem a ser decodificada.
        img_path (str): Caminho do arquivo onde a imagem decodificada será salva. Modificado para /tmp/decoded_img.png

    Returns:
        np.ndarray: A imagem decodificada como um array da NumPy.
    """

    img_data = base64.b64decode(encoded_string)
    with open(img_path, "wb") as image_file:
        image_file.write(img_data)

    image = cv2.imread(img_path)
    return image

    

def deskew_image(image):
    """
    Corrige a inclinação da imagem.

    Parâmetros:
        image (numpy.ndarray): Imagem para corrigir.

    Retorna:
        numpy.ndarray: Imagem corrigida.
    """
    # Converte para tons de cinza e inverte as cores
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    # Aplica threshold para binarizar e encontrar coordenadas dos pixels não-zero
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))

    # Calcula o ângulo de inclinação
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Computa a matriz de rotação e aplica a rotação
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    return rotated


def lambda_handler(event, context):
    # Exemplo de como obter a string base64 da imagem a partir do evento
    base64_string = event['body']

    # Decodifica a string base64 para uma imagem
    image = decode_base64_to_image(base64_string)

    # Aplica a correção de inclinação na imagem
    processed_image = deskew_image(image)

    # Codifica a imagem processada em Base64
    processed_image_base64 = encode_image_to_base64(processed_image)

    # Retorna a imagem processada codificada em Base64
    return {
        'statusCode': 200,
        'isBase64Encoded': True,
        'headers': {'Content-Type': 'image/png'},
        'body': processed_image_base64
    }
