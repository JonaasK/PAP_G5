import time
import cv2
# import os
import urllib.request
from pdf2image import convert_from_path
import pytesseract
import os.path
from datetime import datetime

i = 0
p = 0
verificacao = 0

tempo = datetime.now()
year = int(tempo.strftime("%Y"))
month = int(tempo.strftime("%m"))
day = int(tempo.strftime("%d"))

day1 = day

for x in range(8):
    time.sleep(1)
    day1 = int(day1) + 1
    if day1 == 32:
        day1 = 1
        month = int(month) + 1
        if 0 < int(month) < 10:
            month = "0" + str(month)
        if month == 13:
            year += 1
            month = 1
    if 0 < int(day1) < 10:
        day1 = "0" + str(day1)

    try:
        url = f'https://www.valdorio.net/images/pdfs/Individual_Turmas_{year}_{month}_{day1}.pdf'
        req = urllib.request.urlopen(url)
        nome = "pdf_Horario.pdf"
        file = open(nome, "wb")
        file.write(req.read())
        file.close()
        verificacao = 1
    except:
        print(url)

url = f'https://www.valdorio.net/images/pdfs/Individual_Turmas_{year}_{month}_{day1}.pdf'
req = urllib.request.urlopen(url)
nome = "pdf_Horario.pdf"
file = open(nome, "wb")
file.write(req.read())
file.close()
verificacao = 1

if verificacao == 1:
    images = convert_from_path("pdf_Horario.pdf", poppler_path=r'C:\Program Files\poppler-0.68.0\bin')

    for p in range(len(images)):
        # Save pages as images in the pdf
        images[p].save('page' + str(p) + '.png', 'png')

    os.chdir(r"C:\Users\joaop\Desktop\Horarios_New")
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    while i <= p:
        image = cv2.imread("page" + str(i) + '.png', 0)
        thresh = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY_INV)[1]
        blur = cv2.GaussianBlur(thresh, (3, 3), 0)
        result = 255 - blur
        status = cv2.imwrite("ppt" + str(i) + '.png', result)
        cropped_image_turma = image[295:350, 95:350]
        text_turma = pytesseract.image_to_string(cropped_image_turma, config='--psm 6 -c preserve_interword_spaces=1')
        print(text_turma)
        text_turma = text_turma.replace('\n', '')
        text_turma = text_turma.replace(' ', '')

        file_exists = os.path.exists(text_turma + "_" + year + "_" + month + "_" + day1 + ".png")
        if file_exists == 1:
            os.remove(text_turma + "_" + year + "_" + month + "_" + day1 + ".png")

        os.rename("page" + str(i) + ".png", text_turma + "_" + year + "_" + month + "_" + day1 + ".png")
        i += 1
