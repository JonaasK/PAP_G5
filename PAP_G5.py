"""
*---------------------------------------------------------------------------------------------------------------------*
|                                                                                                                     |
|                                                                                                                     |
|                                               PAP Grupo 5 - 2022/2023                                               |
|                                                     Feito por:                                                      |
|                                                    João Ventosa                                                     |
|                                                    Miguel Lemos                                                     |
|                                                                                                                     |
|                                                                                                                     |
*---------------------------------------------------------------------------------------------------------------------*
"""

import json
import cv2
import os
import urllib.request
from pdf2image import convert_from_path
import pytesseract
import os.path
from skimage import io
from datetime import datetime, timedelta
import numpy as np
import re


def recolha_de_horario():
    y = 0
    tempo_agora = datetime.now()

    for x in range(5):
        tempo = tempo_agora + timedelta(days=y)
        tempo = tempo.strftime('%Y_%m_%d')
        # tempo = '2023_01_03'

        try:
            url = f"https://www.valdorio.net/images/pdfs/Individual_Turmas_{tempo}.pdf"
            urllib.request.urlretrieve(url, "pdf_Horario.pdf")
            verificacao = 1
        except:
            print(url)
            y += 1
            verificacao = 0

    return verificacao, tempo


def dividir_pdf(verificacao, tempo):
    imagens = 0
    paginas = 0
    if verificacao == 1:
        images = convert_from_path("pdf_Horario.pdf", poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
        diretorio_existe = os.path.exists(f"C:\\Users\\joaop\\Desktop\\Horarios_New\\{tempo}")
        if diretorio_existe == 1:
            os.chdir(f"C:\\Users\\joaop\\Desktop\\Horarios_New\\{tempo}")
        else:
            os.mkdir(f"C:\\Users\\joaop\\Desktop\\Horarios_New\\{tempo}")
            os.chdir(f"C:\\Users\\joaop\\Desktop\\Horarios_New\\{tempo}")
        for paginas in range(len(images)):
            # Save pages as images in the pdf
            images[paginas].save('page' + str(paginas) + '.jpeg', 'jpeg')
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

        while imagens <= paginas:
            imagem = io.imread('page' + str(imagens) + '.jpeg')
            img_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            binario = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)[1]
            resultado = cv2.GaussianBlur(binario, (3, 3), 0)
            cv2.imwrite("Img_Processada_" + str(imagens) + ".jpeg", resultado)
            ficheiro_existe = os.path.exists(Turmas(imagens) + "_" + tempo + ".jpeg")
            if ficheiro_existe == 1:
                os.remove(Turmas(imagens) + "_" + tempo + ".jpeg")

            os.rename("page" + str(imagens) + ".jpeg", Turmas(imagens) + "_" + tempo + ".jpeg")
            imagens += 1
    return paginas


def horario(y1, y2, x1, x2, i):
    status = io.imread("Img_Processada_" + str(i) + '.jpeg')
    imagem_cortada = status[y1:y2, x1:x2]
    cv2.imshow("Original", imagem_cortada)
    # cv2.waitKey(0)
    margem = cv2.Canny(imagem_cortada, 50, 150)
    linhas = cv2.HoughLinesP(margem, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
    string_turma = pytesseract.image_to_string(imagem_cortada, config='--psm 6 --oem 3 -c tessedit_create_tsv=1')
    string_turma = string_turma.replace('_—', ' ')
    string_turma = string_turma.replace('__', '')
    string_turma = string_turma.replace('_', '')
    string_turma = string_turma.replace('—', '')
    string_turma = string_turma.replace('\n', ' ')
    arr = string_turma.split(' ')
    while "" in arr:
        arr.remove("")
    if '' in string_turma and len(re.findall("[a-zA-Z]", string_turma)) == 0:
        horas = 0
        print('Não tem aula')
    else:
        if linhas is not None:
            if string_turma.count(' ') > 4:
                horas = 1
                pos = -1
                count = 0
                while count < 3:
                    pos = string_turma.find(' ', pos + 1)
                    count += 1
                pos = pos + 1
                parte1 = string_turma[:pos]
                parte2 = string_turma[pos:]
                print(parte1)
                print(parte2)
            else:
                print(string_turma)
                horas = 1
        else:
            print(string_turma)
            print(string_turma)
            horas = 2
    return string_turma, horas


def JSON_Turma(i):
    dados = {
        'turma': Turmas(i),
    }
    dados_json = json.dumps(dados)
    return dados_json


def JSON_Blocos(string_turma, horas):
    dados_json2 = 0
    if horas == 2:
        string_dividida = string_turma.split()
        dados = {
            'disciplina': string_dividida[0],
            'professor': string_dividida[1],
            'sala': string_dividida[2]
        }
        dados_json = json.dumps(dados)
        dados_json2 = json.dumps(dados)
    else:
        if horas == 0:
            dados = {
                'disciplina': '',
                'professor': '',
                'sala': ''
            }
            dados_json = json.dumps(dados)
        else:
            if string_turma.count(' ') > 4:
                pos = -1
                count = 0
                while count < 3:
                    pos = string_turma.find(' ', pos + 1)
                    count += 1
                pos = pos + 1
                parte1 = string_turma[:pos]
                parte2 = string_turma[pos:]
                print(parte1)
                string_dividida = parte1.split()
                dados1 = {
                    'disciplina': string_dividida[0],
                    'professor': string_dividida[1],
                    'sala': string_dividida[2]
                }
                dados_json = json.dumps(dados1)
                print(parte2)
                string_dividida = parte2.split()
                dados2 = {
                    'disciplina': string_dividida[0],
                    'professor': string_dividida[1],
                    'sala': string_dividida[2]
                }
                dados_json2 = json.dumps(dados2)
            else:
                print(string_turma)
                string_dividida = string_turma.split()
                dados = {
                    'disciplina': string_dividida[0],
                    'professor': string_dividida[1],
                    'sala': string_dividida[2]
                }
                dados_json = json.dumps(dados)

    return dados_json, dados_json2


def JSON_Dia(d):
    dia = ['Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta']
    dados = {
        'dia': dia[d]
    }
    dados_json = json.dumps(dados)
    return dados_json


def Turmas(i):
    imagem = cv2.imread("Img_Processada_" + str(i) + '.jpeg')
    imagem_turma = imagem[295:350, 95:350]
    nome_turmas = pytesseract.image_to_string(imagem_turma, config='--psm 6 -c preserve_interword_spaces=1')
    nome_turmas = nome_turmas.replace('\n', '')
    nome_turmas = nome_turmas.replace(' ', '')
    print(nome_turmas)

    return nome_turmas


# --------------------------------------- MAIN --------------------------------------- #


img = 0
D_semana = ['Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta']
blocos = 0
dias = 0
dimensao_y1 = 455
dimensao_y2 = 680
dimensao_x1 = 300
dimensao_x2 = 520

ver, t = recolha_de_horario()
if ver != 1:
    print("Não existe horario nos ultimos 5 dias.")

else:
    pags = dividir_pdf(ver, t)
    while img <= pags:
        while blocos < 5:
            if dias == 0:
                nome_turma = Turmas(img)
                print(nome_turma)
            if blocos == 0:
                print(D_semana[dias])
            string, H = horario(dimensao_y1, dimensao_y2, dimensao_x1, dimensao_x2, img)
            dimensao_y1 += 270
            dimensao_y2 += 265
            blocos += 1
        if dias < 4:
            if blocos == 5:
                dimensao_y1 = 455
                dimensao_y2 = 680
                dimensao_x1 += 230
                dimensao_x2 += 230
                blocos = 0
                dias += 1
        else:
            if dias == 4:
                dimensao_y1 = 455
                dimensao_y2 = 680
                dimensao_x1 = 300
                dimensao_x2 = 520
                dias = 0
                img += 1
                blocos = 0
