import cv2
import os
import urllib.request
from pdf2image import convert_from_path
import pytesseract
import os.path
from datetime import datetime, timedelta


def recolha_de_horario():
    y = 0
    tempo_agora = datetime.now()

    for x in range(5):
        tempo = tempo_agora + timedelta(days=y)
        tempo = tempo.strftime('%Y_%m_%d')

        try:
            url = f"https://www.valdorio.net/images/pdfs/Individual_Turmas_{tempo}.pdf"
            urllib.request.urlretrieve(url, "pdf_Horario.pdf")
        except:
            print(url)
            y += 1
        verificacao = 1
    return verificacao, tempo


def dividir_pdf(verificacao, tempo):
    imagens = 0
    paginas = 0
    if verificacao == 1:
        images = convert_from_path("pdf_Horario.pdf", poppler_path=r'C:\Program Files\poppler-0.68.0\bin')

        for paginas in range(len(images)):
            # Save pages as images in the pdf
            images[paginas].save('page' + str(paginas) + '.jpeg', 'jpeg')

        os.chdir(r"C:\\Users\\joaop\\Desktop\\Horarios_New")
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

        while imagens <= paginas:
            imagem = cv2.imread("page" + str(imagens) + '.jpeg', 1)
            binario = cv2.threshold(imagem, 127, 255, cv2.THRESH_BINARY)[1]
            # suavizacao = cv2.GaussianBlur(binario, (3, 3), 0)
            resultado = 255 - binario
            cv2.imwrite("Img_Processada_" + str(imagens) + '.jpeg', resultado)
            imagem_turma = resultado[295:350, 95:350]
            texto_turma = pytesseract.image_to_string(imagem_turma, config='--psm 6 -c preserve_interword_spaces=1')
            print(texto_turma)
            texto_turma = texto_turma.replace('\n', '')
            texto_turma = texto_turma.replace(' ', '')

            ficheiro_existe = os.path.exists(texto_turma + "_" + tempo + ".jpeg")
            if ficheiro_existe == 1:
                os.remove(texto_turma + "_" + tempo + ".jpeg")

            os.rename("page" + str(imagens) + ".jpeg", texto_turma + "_" + tempo + ".jpeg")
            imagens += 1


ver, t = recolha_de_horario()
dividir_pdf(ver, t)
