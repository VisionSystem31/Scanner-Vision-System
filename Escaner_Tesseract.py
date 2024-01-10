import cv2 
import pytesseract 
import Jetson.GPIO as GPIO

button = 11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button, GPIO.IN)


# Directorio de pytesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract' 

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
cv2.namedWindow('Camara', cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()

    if ret == True:
        #Convertir en escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # _, binary_image = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        umbral = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 25)
        if not GPIO.input(button):

            #Filtro
            # umbral = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 25)

            #Configuracion OCR
            config = "--psm 1" #Opcion numero 1
            # config = "--psm 7 -l eng --oem 1 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"

            texto_detectado = pytesseract.image_to_string(umbral, config=config)


            print(texto_detectado)
            print("----------------------------------------------------------------")
        cv2.resizeWindow('Camara', 640,480)
        cv2.imshow("Camara", umbral) 
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        cap.release()
        cv2.destroyAllWindows()
        break
