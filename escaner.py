import cv2
from ultralytics import YOLO
import pytesseract 
import numpy as np 

def main():
    model = YOLO("best.pt")

    # config = "--psm 1"
    # config = "--psm 11"   
    config = "--psm 7 -l eng --oem 1 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
    cap = cv2.VideoCapture("demo.mp4")
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()

        if not ret:
            continue

        results = model.predict(frame, verbose=False, agnostic_nms=True, conf=0.50, imgsz=640, device=0)
        if results is not None:
            for result in results:
                if result.boxes:
                    for box in result.boxes:
                        class_id = int(box.cls[0].item())
                        cords = box.xyxy[0].tolist()
                        x1, y1, x2, y2 = map(int, cords)
                        frame2 = frame[y1:y2, x1:x2]
                        gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
                        
                        # Aplica algún procesamiento previo (puedes utilizar alguno de los métodos mencionados anteriormente)
                        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                        _, threshold = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                        
                        # Encuentra los contornos en la imagen binarizada
                        contours, _ = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        
                        # Encuentra el contorno más grande (asumiendo que es la placa)
                        largest_contour = max(contours, key=cv2.contourArea)
                        
                        # Crea una máscara para la placa
                        mask = np.zeros(gray.shape, dtype=np.uint8)
                        cv2.drawContours(mask, [largest_contour], -1, 255, -1)
                        
                        # Aplica la máscara a la imagen original
                        masked_image = cv2.bitwise_and(gray, gray, mask=mask)
                        umbral = cv2.adaptiveThreshold(masked_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 25)

                        texto_detectado = pytesseract.image_to_string(umbral, config=config)


                        print(texto_detectado)
                        cv2.imshow("frame2", umbral)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
                        cv2.putText(frame, f"{texto_detectado}",(x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,)

        cv2.imshow("frame", frame)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            cv2.destroyAllWindows()
            break

if __name__=="__main__":
    main()

