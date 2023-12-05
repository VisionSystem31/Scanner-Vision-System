import numpy as np
import cv2
from pylibdmtx import pylibdmtx
from ultralytics import YOLO

def main():
    model = YOLO("Barcode.pt")
    cap = cv2.VideoCapture(0)
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
                        # umbral = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 25)
                        _, imagen_umbral = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                        
                        msg = pylibdmtx.decode(gray)
                        print(msg)  

                        # for codes in decode(imagen_umbral):
                        #     info = codes.data.decode('utf-8')
                        #     print(info)
                        
                        cv2.imshow("frame2", gray)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
                        # cv2.putText(frame,(x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,)

        cv2.imshow("frame", frame)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            cv2.destroyAllWindows()
            break

if __name__=="__main__":
    main()