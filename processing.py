import enum
from json import detect_encoding
from re import M
from statistics import mean
import cv2
import numpy as np
import sys
from utils import show
from utils import imshow_hstack

def extract_mask(image, show_images=True):
    # suavizar a imagem removendo ruído
    img = cv2.medianBlur(image, 5)

    if show_images: imshow_hstack(image, img)

    # obter uma imagem binária
    _, img_thresh = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY_INV)
    if show_images: imshow_hstack(img, img_thresh)

    """
        utilizar um extrator de contornos para identificar elementos conexos
        estrutura do objeto hierarchy é
        ex: [1, -1, -1, -1]
    """

    regions, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    """
        Armazenar regiões para as quais não há filhos e nem pais
        Isso caracteriza regiões que sofrem reflexo nas imagens
    """
    k = 0
    intereseted_regions = []
    for region in regions:
        if hierarchy[0][k][2] == -1 and hierarchy[0][k][3] > -1:
            intereseted_regions.append(region)
        k = k + 1

        # completar as regiões de reflexo da imagem com pixels pretos

    cv2.drawContours(img_thresh, intereseted_regions, -1, (0,0,0), -1)
    if show_images: imshow_hstack(img, img_thresh)
    

    kernel = np.ones((5,5), np.uint8)
    img_thresh = cv2.dilate(img_thresh, kernel, iterations=5)
    img_thresh = cv2.erode(img_thresh, kernel, iterations=5)
    if show_images: imshow_hstack(img, img_thresh, "Apos erosao e dilatacao")

    edges = cv2.Canny(img_thresh, 100, 200)

    detected_circles = cv2.HoughCircles(edges, 3, 1, 40, param1=10, param2=15, minRadius=0, maxRadius=0)
    print(detected_circles)

    """
        desenhar círculos concêntricos sobre a imagem original
        e verificar a intensidade média dos pixels contidos nos círculos

        Deve ser produzida uma assinatura de intensidade destancando o
        raio onde termina a pupila e o raio onde termina a iris

        até 30 ainda é pupila
        entre 30 e 115 é íris
        acima de 115 é esclera

    """

    data_detected_circles = []
    for i in detected_circles[0]:
        pupilRadius = 0
        pupilMean = 0
        irisRadius = 0
        irisMean = 0
        pupil_x = int(i[0])
        pupil_y = int(i[1])
        r = int(1*i[2]) # raio

        while r < int(3*i[2]):
            array_circle = np.zeros(img.shape, dtype="uint8")
            cv2.circle(img, (pupil_x, pupil_y), int(i[2]), (0,0,0), -1)
            cv2.circle(array_circle, (pupil_x, pupil_y), r, (255,255,255), 1)

            sum = 0
            npixels = 0
            for w in range(img.shape[0]):
                for h in range(img.shape[1]):
                    if array_circle[w][h] == 255:
                        sum = sum + img[w][h]
                        npixels = npixels + 1
            
            mean = sum / npixels
            if mean <= 40:
                pupilRadius = r
                pupilMean = mean
            elif mean > 40 and mean <= 115:
                irisRadius = r
                irisMean = mean
            else:
                break

            # if show_images: imshow_hstack(img, array_circle, "circle")

            r = r + 2
            print(r)
            data_detected_circle = (pupil_x, pupil_y, pupilRadius, irisRadius)
            data_detected_circles.append(data_detected_circle)
    # aqui ele passou por todos os círculos detectados, com a transformada de Hough

    # descobrir o círculo com a maior intensidade média da íris
    i_max = -1
    value_max = -1
    for i, d in enumerate(data_detected_circles):
        if d[3] > value_max:
            i_max = i
            value_max = d[3]
    
    mask_values = data_detected_circles[i_max]
    mask = np.zeros(img.shape, dtype="uint8")

    cv2.circle(mask, (mask_values[0], mask_values[1]), mask_values[3], (255,255,255), -1)
    cv2.circle(mask, (mask_values[0], mask_values[1]), mask_values[2], (0,0,0), -1)
    
    if show_images: imshow_hstack(img, mask, "mask")


    img_mask = cv2.bitwise_and(img, mask, mask=mask)

    return img_mask, mask_values
    