import cv2
import easyocr

def main():
    reader = easyocr.Reader(['en'], gpu=True)  # Puedes elegir los idiomas que necesites
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()

        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resultados_easyocr = reader.readtext(gray)

        for resultado in resultados_easyocr:
            text = resultado[1]
            print(text)
            print("---------------------------------------")
        
        cv2.imshow("frame", frame)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            cv2.destroyAllWindows()
            break

    cap.release()

if __name__=="__main__":
    main()
