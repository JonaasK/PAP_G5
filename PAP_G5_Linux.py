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
import time
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
import requests

global objecto_principal

objecto_principal = {
    "turma": "",
    "versao": "",
    "horario": [
        {
            "dia": "segunda",
            "info": [

            ]
        },
        {
            "dia": "terca",
            "info": [
            ]
        },
        {
            "dia": "quarta",
            "info": [
            ]
        },
        {
            "dia": "quinta",
            "info": [
            ]
        },
        {
            "dia": "sexta",
            "info": [
            ]
        }
    ]
}


def limparObjecto():  # Limpar o objecto
    objecto_principal = {
        "turma": "",
        "versao": "",
        "horario": [
            {
                "dia": "segunda",
                "info": [

                ]
            },
            {
                "dia": "terca",
                "info": [
                ]
            },
            {
                "dia": "quarta",
                "info": [
                ]
            },
            {
                "dia": "quinta",
                "info": [
                ]
            },
            {
                "dia": "sexta",
                "info": [
                ]
            }
        ]
    }
    return objecto_principal


def recolha_de_horario():
    url_pdf = 0
    verificacao = 0
    tempo = 0
    y = 0
    tempo_agora = datetime.now()

    for x in range(5):
        tempo = tempo_agora + timedelta(days=y)  # somar dias ao horario do sistema
        tempo = tempo.strftime('%Y_%m_%d')  # definir formato da data
        # tempo = '2023_01_09'

        try:
            url_pdf = f"https://www.valdorio.net/images/pdfs/Individual_Turmas_{tempo}.pdf"  # defenir o url para retirar pdf
            urllib.request.urlretrieve(url_pdf,
                                       "pdf_Horario.pdf")  # retirar horario e salvar com o nome de "pdf_Horario.pdf")
            verificacao = 1
        except:
            print(url_pdf)  # mostrar url que não funcionou
            y += 1
            verificacao = 0

    return verificacao, tempo


def dividir_pdf(verificacao, tempo):
    imagens = 0
    paginas = 0
    if verificacao == 1:
        images = convert_from_path("pdf_Horario.pdf")  # ler o pdf
        diretorio_existe = os.path.exists(
            f"/root/PAP_G5/{tempo}")  # verificar se o diretorio existe
        if diretorio_existe == 1:
            os.chdir(f"/root/PAP_G5/{tempo}")  # mudar diretorio
        else:
            os.mkdir(f"/root/PAP_G5/{tempo}")  # criar diretorio
            os.chdir(f"/root/PAP_G5/{tempo}")  # mudar diretorio
        for paginas in range(len(images)):
            images[paginas].save('page' + str(paginas) + '.jpeg', 'jpeg')  # salvar imagens
        while imagens <= paginas:
            imagem = io.imread('page' + str(imagens) + '.jpeg')  # ler imagem
            img_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)  # imagem normal para escala de cinza
            binario = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)[
                1]  # aplica um limiar a imagem com escala cinza
            resultado = cv2.GaussianBlur(binario, (3, 3), 0)  # aplica uma suavização na imagem
            cv2.imwrite("Img_Processada_" + str(imagens) + ".jpeg", resultado)  # salva a imagem processada
            os.rename("page" + str(imagens) + ".jpeg", Turmas(imagens) + "_" + tempo + ".jpeg")  # renomear a imagem
            imagens += 1
    return paginas


def horario(y1, y2, x1, x2, i):
    status = io.imread("Img_Processada_" + str(i) + '.jpeg')  # ler imagem
    # cv2.imshow("Original", imagem_cortada)  # mostrar imagem
    # cv2.waitKey(0)  # espera de um input do teclado para avançar
    imagem_cortada = status[y1:y2, x1:x2]  # corta a imagem com as cordenadas dadas
    margem = cv2.Canny(imagem_cortada, 50, 150)  # detectar as margens da imagem
    linhas = cv2.HoughLinesP(margem, 1, np.pi / 180, 100, minLineLength=100,
                             maxLineGap=10)  # detectar as linhas da imagem
    string_turma = pytesseract.image_to_string(imagem_cortada, config='--psm 6 --oem 3 -c tessedit_create_tsv=1')  # retirar os dados da imagem
    # retirar caracteres desnecessários
    string_turma = string_turma.replace('_—', ' ')
    string_turma = string_turma.replace('=', '')
    string_turma = string_turma.replace('__', '')
    string_turma = string_turma.replace('_', '')
    string_turma = string_turma.replace('—', '')
    string_turma = string_turma.replace('  ', ' ')
    string_turma = string_turma.replace('', '')
    string_turma = string_turma.replace('\n', ' ')
    arr = string_turma.split(' ')  # dividir a string
    while "" in arr:
        arr.remove("")  # remover os elementos vazios da string
    if '' in string_turma and len(re.findall("[a-zA-Z]", string_turma)) == 0:
        horas = 0  # defenir hora = 0
        # print('Não tem aula')
    else:
        if linhas is not None:
            if string_turma.count(' ') > 4:
                horas = 1
            else:
                horas = 1
        else:
            horas = 2
    return string_turma, horas



def Dados_Blocos(string_turma, horas, dia):
    string_turma = string_turma.replace('  ', ' ')  # remover caracteres desnecessários
    if horas == 2:
        string_dividida = string_turma.split()  # dividir string
        try:
            # adicionar os dados retirados
            dados = {
                'disciplina': string_dividida[0],
                'professor': string_dividida[1],
                'sala': string_dividida[2]
            }
        except:
            # adicionar os dados retirados se a função acima der erro
            dados = {
                'disciplina': string_dividida[0],
                'professor': '',
                'sala': ''
            }
        objecto_principal["horario"][dias]["info"].append(dados)  # adicionar dados ao objecto_principal
        objecto_principal["horario"][dias]["info"].append(dados)  # adicionar dados ao objecto_principal
    else:
        if horas == 0:
            print("Não tem aula")
        else:
            if string_turma.count(' ') > 4:
                pos = -1
                count = 0
                string_turma.replace('  ', ' ') # remover caracteres desnecessários
                while count < 3:
                    pos = string_turma.find(' ', pos + 1)  # encontrar o terceiro espaço
                    count += 1
                pos = pos + 1
                parte1 = string_turma[:pos]  # dividir a string para a primeira parte
                parte2 = string_turma[pos:]  # dividir a string para a segunda parte
                parte2 = parte2.strip()
                print(parte1)
                string_dividida = parte1.split()  # remove os espaços iniciais e finais da string
                try:
                    # adicionar os dados retirados
                    dados1 = {
                        'disciplina': string_dividida[0],
                        'professor': string_dividida[1],
                        'sala': string_dividida[2]
                    }
                except:
                    # adicionar os dados retirados se a função acima der erro
                    dados1 = {
                        'disciplina': string_dividida[0],
                        'professor': '',
                        'sala': ''
                    }
                objecto_principal["horario"][dias]["info"].append(dados1)  # adicionar dados ao objecto_principal
                print(parte2)
                try:
                    # adicionar os dados retirados
                    dados2 = {
                        'disciplina': string_dividida[0],
                        'professor': string_dividida[1],
                        'sala': string_dividida[2]
                    }
                except:
                    # adicionar os dados retirados se a função acima der erro
                    dados2 = {
                        'disciplina': string_dividida[0],
                        'professor': '',
                        'sala': ''
                    }
                objecto_principal["horario"][dias]["info"].append(dados2)  # adicionar dados ao objecto_principal
            else:
                print(string_turma)
                string_dividida = string_turma.split()  # dividir string
                try:
                    # adicionar os dados retirados
                    dados = {
                        'disciplina': string_dividida[0],
                        'professor': string_dividida[1],
                        'sala': string_dividida[2]
                    }
                except:
                    # adicionar os dados retirados se a função acima der erro
                    dados = {
                        'disciplina': string_dividida[0],
                        'professor': '',
                        'sala': ''
                    }
                objecto_principal["horario"][dia]["info"].append(dados)  # adicionar dados ao objecto_principal


def Turmas(i):
    imagem = cv2.imread("Img_Processada_" + str(i) + '.jpeg')  # ler imagem
    imagem_turma = imagem[295:350, 95:350]  # recortar imagem
    nome_turmas = pytesseract.image_to_string(imagem_turma, config='--psm 6 -c preserve_interword_spaces=1')  # retirar os dados da imagem recortada
    # retirar caracteres desnecessários
    nome_turmas = nome_turmas.replace('\n', '')
    nome_turmas = nome_turmas.replace('', '')
    nome_turmas = nome_turmas.replace(' ', '')

    return nome_turmas


def connectar_API(tempo, i, dados):
    i = i - 1
    imagem_t = f"/root/PAP_G5/{tempo}/" + Turmas(i) + "_" + tempo + ".jpeg"  # caminho para a imagem
    url = 'https://apphorarios.pt/api/auth'  # url para aceder a autenticação da API
    r = requests.get(url, data={'apiKey': 'D)QN#)e+Cud`9,3uL.Rh7&pJD#qvFu)N'})  # request para ter o token de acesso a API
    json_r = r.json()
    token = json_r['token']  # retirar token
    print(token)
    url = 'https://apphorarios.pt/horario/' + objecto_principal['turma'] + '/insert/image?token=' + token  # url para enviar dados para a API
    requests.post(url, files={'horario': open(imagem_t, 'rb')})  # enviar dados para a API
    url = 'https://apphorarios.pt/horario/' + objecto_principal['turma'] + '/insert/json?token=' + token
    requests.post(url, json=dados)


# --------------------------------------- MAIN --------------------------------------- #

# defenir variaveis a 0
fim = 0
img = 0
D_semana = [0, 1, 2, 3, 4]
blocos = 0
dias = 0
dimensao_y1 = 455
dimensao_y2 = 680
dimensao_x1 = 300
dimensao_x2 = 520

ver, t = recolha_de_horario()  # função para retirar o ficheiro pdf
if ver != 1:
    print("Não existe horario nos ultimos 5 dias.")

else:
    pags = dividir_pdf(ver, t) # função para dividir pdf em imagens
    pags += 1
    while img <= pags:
        while blocos < 5:
            if dias == 0:
                if blocos == 0:
                    if img >= 1:
                        Dados_Json = json.dumps(objecto_principal)  # função para transformar dados da string objecto_principal em JSON
                        stringObj = json.loads(Dados_Json)
                        # connectar_API(t, img, stringObj)  # função para connectar a API e envia os dados
                        print(Dados_Json)
                        objecto_principal = limparObjecto()  # função para limpar a string objecto_principal
                    if img >= pags:
                        fim = 1
                        break
                    nome_turma = Turmas(img)  # função para retirar o nome das turmas
                    objecto_principal["turma"] = nome_turma  # adiciona o nome da turma no objecto_principal
            string, H = horario(dimensao_y1, dimensao_y2, dimensao_x1, dimensao_x2, img)  # função para retirar os dados do horario
            Dados_Blocos(string, H, D_semana[dias])  # função para inserir os dados no objecto_principal
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
        if fim == 1:
            break
