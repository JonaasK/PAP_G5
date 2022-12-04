import os
import cv2
import pytesseract
import re
u = 0
# intervalo y1 + 140 | y2 + 150
intervalo = 0
# sempre mais 120 para ir para a proxima hora
y1 = 460
# sempre mais 110 para ir para a proxima hora
y2 = 580
# sempre mais 227 para ir para o proximo dia
x1 = 300
# sempre mais 237 para ir para o proximo dia
x2 = 500
change = 0
os.chdir(r"C:\Users\joaop\Desktop\Horarios_New")
i = 0
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# Open image with PIL
# img = Image.open(path_to_image)
# Extract text from image

# while i < 11:
image = cv2.imread("page" + str(i) + '.png', 1)
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)[1]
blur = cv2.GaussianBlur(thresh, (1, 1), 0)
result = 255 - blur
status = cv2.imwrite("ppt" + str(i) + '.png', result)
while u < 5:
    for h in range(2):
        cropped_image_turma1 = result[y1:y2, 300:500]
        text_turma1 = pytesseract.image_to_string(cropped_image_turma1, config='--psm 4')
        text_turma1 = text_turma1.replace(' | ', ' ')
        text_turma1 = text_turma1.replace(' = ', ' ')
        text_turma1 = text_turma1.replace('\n', ' ')
        arr = text_turma1.split(' ')
        while ("" in arr):
            arr.remove("")
        y1 = y1 + 120
        y2 = y2 + 110
    y1 = y1 + 140
    y2 = y2 + 150
    u += 1
    print(arr)
    if '' in text_turma1 and len(re.findall("[a-zA-Z]", text_turma1)) == 0:
        print('Não tem aula')
    elif len(arr) == 3:
        print('Aula de 1 hora')
        print(text_turma1)
    else:
        print('Aula de 2 horas')
        print(text_turma1)
"""
    cropped_image_turma2 = result[y1:y2, 300:500]
    text_turma2 = pytesseract.image_to_string(cropped_image_turma2, config='--psm 4')
    text_turma2 = text_turma2.replace(' | ', ' ')
    text_turma2 = text_turma2.replace(' = ', ' ')

    y1 = y1 + 140
    y2 = y2 + 150
"""


"""
    elif ' ' in text_turma1:
        print('Tem Aula')
        print(text_turma1)
    else:
        print('tem aula de 2 horas')
        print(text_turma1)
    if ' ' in text_turma2:
        print('Tem aula')
        print(text_turma2)
"""

#    i += 1

cropped_image_turma = image[720:830, 300:500]
# imagetm = cv2.imread("page5.png", 0)
# cropped_imagetm = imagetm[290:350, 95:350]     cropped_image_turma = image[450:1800, 300:500]
down_width = 200
down_height = 500
down_points = (down_width, down_height)
resized_down1 = cv2.resize(cropped_image_turma, down_points, interpolation=cv2.INTER_LINEAR)
# resized_down2 = cv2.resize(cropped_image_turma2, down_points, interpolation=cv2.INTER_LINEAR)
cv2.imshow('teste1', resized_down1)
# cv2.imshow('teste2', resized_down2)
cv2.waitKey(0)
# Eliminar nomes dos profs. e s. é so arranjar uma maneira de detetar os espacos entre palavras e remover a linha int.
# cropped_image_turma = result[720:850, 300:500] 3 hora
