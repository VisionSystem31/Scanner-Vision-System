import tkinter as tk
from PIL import Image, ImageTk 
import cv2
import imutils
from ultralytics import YOLO
from statistics import mode
from pyzbar.pyzbar import decode

Part_ingresado = "470015-07"
Exp_ingresado = "2025-11-30"
Lot_ingresado = "DM3202819"

def visualizar():
    global inicio, model, cap, frame, button, camera_id
    global fecha_exp, lot_number, part_number, lblVideo
    global Text_fecha_exp, Text_lot_number, Text_part_number
    global Stop_fecha_exp, Stop_lot_number, Stop_part_number

    if inicio == 1:

        Titulo_part_number  = pantalla.create_text(361, 279, text=f"Part: {Part_ingresado}", font=("Helvetica", 30, "bold"), fill="#EBFF03", anchor=tk.NW)
        Titulo_fecha_exp = pantalla.create_text(780, 279, text=f"Exp: {Exp_ingresado}", font=("Helvetica", 30, "bold"), fill="#EBFF03", anchor=tk.NW)
        Titulo_lot_number = pantalla.create_text(1197, 279, text=f"Lot: {Lot_ingresado}", font=("Helvetica", 30, "bold"), fill="#EBFF03", anchor=tk.NW)
    
        lblVideo = tk.Label(pantalla)
        lblVideo.configure(borderwidth=0)
        lblVideo.place(x = 370, y = 400)
        
        camera_id = 0
        inicio = 0
        button = 13
        model = YOLO("labels2.pt")
        fecha_exp = []
        lot_number = []
        part_number = []
        cap = cv2.VideoCapture(camera_id)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        Stop_fecha_exp = True
        Stop_lot_number = True
        Stop_part_number = True
    else:
        pantalla.delete(frame)
    
    if cap is not None:
        ret, frame = cap.read()

        if ret == True:
            results = model.predict(frame, verbose=True, agnostic_nms=True, conf=0.15, imgsz=640, device=0)
            
            if results is not None:
                for result in results:
                    if result.boxes:
                        for box in result.boxes:
                            class_id = int(box.cls[0].item())
                            cords = box.xyxy[0].tolist()
                            x1, y1, x2, y2 = map(int, cords)
                            frame2 = frame[y1:y2, x1:x2]
                            gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
                            umbral = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 25)
                            #_, imagen_umbral = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                            for codes in decode(umbral):
                                info = codes.data.decode('utf-8')
                                
                                if class_id == 0:
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 4)
                                    cv2.putText(frame, f"{info}",(x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,)
                                    if Stop_fecha_exp == True: fecha_exp.append(info)

                                if class_id == 1:
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)
                                    cv2.putText(frame, f"{info}",(x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,)
                                    if Stop_lot_number == True: lot_number.append(info)
                                
                                if class_id == 2:
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
                                    cv2.putText(frame, f"{info}",(x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,)
                                    if Stop_part_number == True: part_number.append(info)
            
            if len(part_number) >= 5:
                pantalla.delete(Text_part_number)
                if str(mode(part_number)) == Part_ingresado: Text_part_number  = pantalla.create_text(1083, 481, text=f"Part: {mode(part_number)}", font=("Helvetica", 35, "bold"), fill="white", anchor=tk.NW)
                else: Text_part_number  = pantalla.create_text(1083, 481, text=f"Part: {mode(part_number)}*", font=("Helvetica", 35, "bold"), fill="red", anchor=tk.NW)
                Stop_part_number = False
            else:
                try: pantalla.delete(Text_part_number)
                except: pass
                Text_part_number  = pantalla.create_text(1083, 481, text=f"Part: ________", font=("Helvetica", 35, "bold"), fill="white", anchor=tk.NW)
            

            if len(fecha_exp) >= 5:
                pantalla.delete(Text_fecha_exp)
                if str(mode(fecha_exp)) == Exp_ingresado: Text_fecha_exp = pantalla.create_text(1083, 616, text=f"Exp: {mode(fecha_exp)}", font=("Helvetica", 35, "bold"), fill="white", anchor=tk.NW)
                else: Text_fecha_exp = pantalla.create_text(1083, 616, text=f"Exp: {mode(fecha_exp)}*", font=("Helvetica", 35, "bold"), fill="red", anchor=tk.NW)
                Stop_fecha_exp = False
            else:
                try: pantalla.delete(Text_fecha_exp)
                except: pass
                Text_fecha_exp = pantalla.create_text(1083, 616, text=f"Exp: ________", font=("Helvetica", 35, "bold"), fill="white", anchor=tk.NW)

           
            if len(lot_number) >= 5:
                pantalla.delete(Text_lot_number)
                if str(mode(lot_number)) == Lot_ingresado: Text_lot_number = pantalla.create_text(1083, 745, text=f"Lot: {mode(lot_number)}", font=("Helvetica", 35, "bold"), fill="white", anchor=tk.NW)
                else: Text_lot_number = pantalla.create_text(1083, 745, text=f"Lot: {mode(lot_number)}*", font=("Helvetica", 35, "bold"), fill="red", anchor=tk.NW)
                Stop_lot_number = False
            else:
                try: pantalla.delete(Text_lot_number)
                except: pass
                Text_lot_number = pantalla.create_text(1083, 745, text=f"Lot: ________", font=("Helvetica", 35, "bold"), fill="white", anchor=tk.NW)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = imutils.resize(frame, width=640, height=480)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            lblVideo.configure(image=img)
            lblVideo.image = img
            
            pantalla.after(10, visualizar)
        else:
            cap = cv2.VideoCapture(camera_id)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
            print("La camara id es: ",camera_id)
            camera_id +=1
            if camera_id >= 10:
                camera_id = 0
            pantalla.after(100, visualizar)

def turn_off_action():
    root.destroy()

root = tk.Tk()
root.title("DAS Label Verification prototype")

root.attributes('-fullscreen', True)

pantalla = tk.Canvas(root, width=1920, height=1080, bg="#FFFFFF")
pantalla.pack()

Titulo = pantalla.create_text(157, 110, text="DAS Label Verification prototype", font=("Helvetica", 40, "bold"), fill="black", anchor=tk.NW)

#Boton de cerrado
Close = tk.PhotoImage(file="IMG/shutdown.png")
Close_Button = tk.Button(pantalla, image=Close, bg="#FFFFFF", command=turn_off_action, borderwidth=0, relief="flat")
Close_Button.place(x = 1794, y = 55)

inicio = 1

visualizar()

root.mainloop()