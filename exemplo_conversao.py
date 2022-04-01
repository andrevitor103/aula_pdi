import cv2
#criar pasta imagem e colocar imagem
imagem = cv2.imread("imagens/watch.png")
imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
imagem_hsv = cv2.cvtColor(imagem, cv2.COLOR_HSV2BGR)

cv2.imshow("Imagem cinza", imagem_cinza)
cv2.waitKey(0)

cv2.imshow("Imagem hsv", imagem_hsv)
cv2.waitKey(0)
