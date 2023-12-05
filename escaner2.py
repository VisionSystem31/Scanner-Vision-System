import cv2 
import pytesseract 

# Directorio de pytesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract' 

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if ret == True:
        #Convertir en escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Filtro
        umbral = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 25)

        #Configuracion OCR
        config = "--psm 1" #Opcion numero 1

        texto_detectado = pytesseract.image_to_string(umbral, config=config)


        print(texto_detectado)
    
    cv2.imshow("Camara", umbral) 
    if cv2.waitKey(1) == 27: 
        cap.release()
        cv2.destroyAllWindows()
        break
