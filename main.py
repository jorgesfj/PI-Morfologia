import numpy as np
import cv2
import json
from matplotlib import pyplot as plt


def binarizar_a_imagem(imagem):
    img = cv2.imread(imagem, 0)

    converter_preto = np.where((img <= 127), img, 255)
    converter_branco = np.where((converter_preto > 127), converter_preto, 0)

    return converter_branco


def erosao(imagem,elemento_estruturante):
    img = imagem
    forma_img = img.shape
    tamanho_elemento = len(elemento_estruturante)
    tamanho_imagem = np.pad(array=img, pad_width=tamanho_elemento, mode='constant')
    forma_elemento = tamanho_imagem.shape
    altura, largura = (forma_elemento[0] - forma_img[0]), (forma_elemento[1] - forma_img[1])
    submatrizes = np.array([
        tamanho_imagem[i:(i + len(elemento_estruturante)), j:(j + len(elemento_estruturante))]
        for i in range(forma_elemento[0] - altura) for j in range(forma_elemento[1] - largura)
    ])

    
    erosao_img = np.array([255 if (i == elemento_estruturante).all() else 0 for i in submatrizes])
    erosao_img = erosao_img.reshape(forma_img)
    return erosao_img

def dilatacao(imagem, elemento_estruturante):
    
    img = imagem
    forma_img = img.shape
    tamanho_elemento = len(elemento_estruturante) - 2
    tamanho_imagem = np.pad(array=img, pad_width=tamanho_elemento, mode='constant')
    forma_elemento = tamanho_imagem.shape
    altura, largura = (forma_elemento[0] - forma_img[0]), (forma_elemento[1] - forma_img[1])
    submatrizes = np.array([
        tamanho_imagem[i:(i + len(elemento_estruturante)), j:(j + len(elemento_estruturante))]
        for i in range(forma_elemento[0] - altura) for j in range(forma_elemento[1] - largura)
    ])
    imagem_dilatada = np.array([255 if (i == elemento_estruturante).any() else 0 for i in submatrizes])
    imagem_dilatada = imagem_dilatada.reshape(forma_img)
    return imagem_dilatada

def abertura(imagem, elemento_estruturante):
    imagem_erosao = erosao(imagem= imagem, elemento_estruturante=elemento_estruturante)
    imagem_dilatada = dilatacao(imagem= imagem_erosao, elemento_estruturante=elemento_estruturante)
    return imagem_dilatada

def fechamento(imagem, elemento_estruturante):
    imagem_dilatada = dilatacao(imagem= imagem, elemento_estruturante=elemento_estruturante)
    imagem_erosao = erosao(imagem=imagem_dilatada, elemento_estruturante=elemento_estruturante)
    return imagem_erosao
    

img = binarizar_a_imagem(imagem='image.png')
elemento_estruturante = [[255,255,255,255,255],[255,255,255,255,255],[255,255,255,255,255],[255,255,255,255,255],[255,255,255,255,255]]

imagem_erosao = erosao(imagem=img, elemento_estruturante=elemento_estruturante)
plt.imshow(imagem_erosao,'gray')
plt.show()

imagem_dilatada = dilatacao(imagem=img, elemento_estruturante=elemento_estruturante)
plt.imshow(imagem_dilatada,'gray')
plt.show()

img = binarizar_a_imagem(imagem='abertura.png')
imagem_abertura = abertura(imagem=img, elemento_estruturante=elemento_estruturante)
plt.imshow(imagem_abertura,'gray')
plt.show()

img = binarizar_a_imagem(imagem='fechamento.png')
imagem_fechamento = fechamento(imagem=img, elemento_estruturante=elemento_estruturante)
plt.imshow(imagem_fechamento,'gray')
plt.show()
