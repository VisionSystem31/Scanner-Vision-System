import cv2
from ultralytics import YOLO
from pyzbar.pyzbar import decode

def main():
    model = YOLO("labelsM1.pt")
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    part =" "
    exp = " "
    lot =" "
    counterA =0
    counterB=0
    counterC=0
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
                        _, umbral = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
                        for codes in decode(gray):
                            if class_id==2 and counterA <1:
                                counterA+=1
                                part=codes.data.decode('utf-8')
                                print(f"El numero de parte es:{part} ")
                                cv2.putText(frame,part, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,)

                            elif class_id==0 and counterB < 1:
                                counterB+=1 
                                exp= codes.data.decode('utf-8')
                                print(f"La fecha de exp es:{exp} ")
                                cv2.putText(frame, exp, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,)

                            elif class_id==1 and counterC < 1:
                                counterC+=1
                                lot=codes.data.decode('utf-8')
                                print(f"El numero de lote es:{lot} ")
                                cv2.putText(frame,lot, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,)                        
                        # for codes in decode(gray):
                        #     info = codes.data.decode('utf-8')
                        #     print(info)
                        
                        cv2.imshow("frame2", gray)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
        cv2.imshow("frame", frame)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            cv2.destroyAllWindows()
            break

if __name__=="__main__":
    main()

