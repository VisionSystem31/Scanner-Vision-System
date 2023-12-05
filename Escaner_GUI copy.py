import tkinter as tk
from PIL import Image, ImageTk 
import cv2
import imutils
from ultralytics import YOLO
from statistics import mode
from pyzbar.pyzbar import decode

Valor_1 = "0086216118135"
Valor_2 = "0086216118135"
Valor_3 = "0086216118135"

def visualizar():
    global inicio, model, cap, frame, button, camera_id
    global Variable_1, Variable_2, Variable_3
    global Text_Variable_1, Text_Variable_2, Text_Variable_3
    global Stop_Variable_1, Stop_Variable_2, Stop_Variable_3
    if inicio == 1:
        camera_id = 0
        inicio = 0
        button = 13
        model = YOLO("labels4.pt")
        Variable_1 = []
        Variable_2 = []
        Variable_3 = []
        cap = cv2.VideoCapture(1)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
        Stop_Variable_1 = True
        Stop_Variable_2 = True
        Stop_Variable_3 = True
    else:
        pantalla.delete(frame)
    
    if cap is not None:
        ret, frame = cap.read()

        if ret == True:
            results = model.predict(frame, verbose=False, agnostic_nms=True, conf=0.25, imgsz=640, device=0)
            
            if results is not None:
                for result in results:
                    if result.boxes:
                        for box in result.boxes:
                            class_id = int(box.cls[0].item())
                            cords = box.xyxy[0].tolist()
                            x1, y1, x2, y2 = map(int, cords)
                            frame2 = frame[y1:y2, x1:x2]
                            gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
                            #_, imagen_umbral = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                            for codes in decode(gray):
                                info = codes.data.decode('utf-8')
                                
                                if class_id == 0 and Stop_Variable_1 == True: 
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 4)
                                    cv2.putText(frame, f"{info}",(x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,)
                                    Variable_1.append(info)

                                if class_id == 1 and Stop_Variable_2 == True: 
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)
                                    cv2.putText(frame, f"{info}",(x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,)
                                    Variable_2.append(info)
                                
                                if class_id == 2  and Stop_Variable_3 == True: 
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
                                    cv2.putText(frame, f"{info}",(x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,)
                                    Variable_3.append(info)
                    
            if len(Variable_1) == 5:
                # pantalla.delete(Text_Variable_1)
                if str(mode(Variable_1)) == Valor_1: Text_Variable_1 = pantalla.create_text(1248, 371, text=f"Part: {mode(Variable_1)}", font=("Helvetica", 30, "bold"), fill="green", anchor=tk.NW)
                else: Text_Variable_1 = pantalla.create_text(1248, 371, text=f"Part: {mode(Variable_1)}", font=("Helvetica", 30, "bold"), fill="red", anchor=tk.NW)
                Stop_Variable_1 = False
                Variable_1 = []

            if len(Variable_2) == 5:
                # pantalla.delete(Text_Variable_2)
                if str(mode(Variable_2)) == Valor_2: Text_Variable_2 = pantalla.create_text(1248, 515, text=f"Exp: {mode(Variable_2)}=", font=("Helvetica", 30, "bold"), fill="green", anchor=tk.NW)
                else: Text_Variable_2 = pantalla.create_text(1248, 515, text=f"Exp: {mode(Variable_2)}=", font=("Helvetica", 30, "bold"), fill="red", anchor=tk.NW)
                Stop_Variable_2 = False
                Variable_2 = []

            if len(Variable_3) == 5:
                # pantalla.delete(Text_Variable_3)
                if str(mode(Variable_3)) == Valor_3: Text_Variable_3  = pantalla.create_text(1248, 661, text=f"Lot: {mode(Variable_3)}", font=("Helvetica", 30, "bold"), fill="green", anchor=tk.NW)
                else: Text_Variable_3  = pantalla.create_text(1248, 661, text=f"Lot: {mode(Variable_3)}=", font=("Helvetica", 30, "bold"), fill="red", anchor=tk.NW)
                Stop_Variable_3 = False
                Variable_3 = []
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = imutils.resize(frame, width=1000, height=562)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            lblVideo.configure(image=img)
            lblVideo.image = img
            
            pantalla.after(10, visualizar)
        else:
            cap = cv2.VideoCapture(camera_id)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
            # print("La camara id es: ",camera_id)
            camera_id +=1
            if camera_id >= 10:
                camera_id = 0
            pantalla.after(100, visualizar)

def turn_off_action():
    root.destroy()

root = tk.Tk()
root.title("Escaner Vision System")

root.attributes('-fullscreen', True)

pantalla = tk.Canvas(root, width=1920, height=1080, bg="#FFFFFF")
pantalla.pack()

Titulo = pantalla.create_text(157, 110, text="Escaner Vision System", font=("Helvetica", 40, "bold"), fill="black", anchor=tk.NW)

#Boton de cerrado
Close = tk.PhotoImage(file="IMG/shutdown.png")
Close_Button = tk.Button(pantalla, image=Close, bg="#FFFFFF", command=turn_off_action, borderwidth=0, relief="flat")
Close_Button.place(x = 1794, y = 55)

lblVideo = tk.Label(pantalla)
lblVideo.configure(borderwidth=0)
lblVideo.place(x = 157, y = 259)
inicio = 1

Titulo_Variable_1 = pantalla.create_text(1248, 300, text=f"Part: {Valor_1}", font=("Helvetica", 30, "bold"), fill="blue", anchor=tk.NW)
Titulo_Variable_2 = pantalla.create_text(1248, 443, text=f"Exp: {Valor_2}", font=("Helvetica", 30, "bold"), fill="blue", anchor=tk.NW)
Titulo_Variable_3  = pantalla.create_text(1248, 589, text=f"Lot: {Valor_3}", font=("Helvetica", 30, "bold"), fill="blue", anchor=tk.NW)

visualizar()

root.mainloop()