import tkinter as tk
from PIL import Image, ImageTk 
import tkinter.messagebox as messagebox
import imutils
from ultralytics import YOLO
from statistics import mode
from pyzbar.pyzbar import decode
import cv2 
import time 
from fileread import *

def visualizar():
    global inicio, model, cap, frame, button, camera_id, loading_id
    global fecha_exp, lot_number, part_number, lblVideo
    global Text_fecha_exp, Text_lot_number, Text_part_number
    global Stop_fecha_exp, Stop_lot_number, Stop_part_number
    global cant_pouches, box1, Titulo_fecha_exp, Titulo_lot_number, Titulo_part_number, title_change, flag

    if inicio == 1:
        Titulo_part_number  = pantalla.create_text(320, 193, text=f"Part: {Part_ingresado}", font=("Helvetica", 30, "bold"), fill="#FFFFFF", anchor=tk.NW)
        Titulo_fecha_exp = pantalla.create_text(779, 193, text=f"Exp: {Exp_ingresado}", font=("Helvetica", 30, "bold"), fill="#FFFFFF", anchor=tk.NW)
        Titulo_lot_number = pantalla.create_text(1245, 193, text=f"Lot: {Lot_ingresado}", font=("Helvetica", 30, "bold"), fill="#FFFFFF", anchor=tk.NW)
        Frame_fondo_id = pantalla.create_image(295, 295, anchor=tk.NW, image=Frame_fondo)
        lblVideo = tk.Label(pantalla)
        lblVideo.configure(borderwidth=0)
        lblVideo.place(x = 320, y = 320)
        camera_id = 0
        inicio = 0
        button = 13
        model = YOLO("labelsM1.pt")
        fecha_exp = []
        lot_number = []
        part_number = []
        cap = cv2.VideoCapture(camera_id)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        Stop_fecha_exp = True
        Stop_lot_number = True
        Stop_part_number = True 
        pantalla.delete(background_loading_id)
        pantalla.delete(Text_loading)
        cant_pouches = 0
        box1 = False
        title_change = True
        flag = True
    else:
        pantalla.delete(frame)
    
    if cap is not None:
        ret, frame = cap.read()

        if ret == True:
            results = model.predict(frame, verbose=False, agnostic_nms=True, conf=0.75, imgsz=640, device=0)
            
            if results is not None:
                for result in results:
                    if result.boxes:
                        for box in result.boxes:
                            class_id = int(box.cls[0].item())
                            cords = box.xyxy[0].tolist()
                            x1, y1, x2, y2 = map(int, cords)
                            frame2 = frame[y1:y2, x1:x2]
                            gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
                            # _, imagen_umbral = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                            #umbral = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 25)
                            if class_id == 0:
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 4)
                                # cv2.putText(frame, f"{info}",(x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,)

                            if class_id == 1:
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)
                                # cv2.putText(frame, f"{info}",(x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,)
                            
                            if class_id == 2:
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
                                # cv2.putText(frame, f"{info}",(x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,)

                            for codes in decode(gray):
                                info = codes.data.decode('utf-8')
                                if class_id == 0:
                                    if Stop_fecha_exp == True: fecha_exp.append(info)

                                if class_id == 1:
                                    if Stop_lot_number == True: lot_number.append(info)
                                
                                if class_id == 2:
                                    if Stop_part_number == True: part_number.append(info)
                    else:
                        fecha_exp = []
                        lot_number = []
                        part_number = []
                        Stop_fecha_exp = True
                        Stop_lot_number = True
                        Stop_part_number = True
            if cant_pouches <= 5:
                title_change = True
                if len(part_number) >= 4:
                    pantalla.delete(Text_part_number)
                    if str(mode(part_number)) == Part_ingresado: Text_part_number  = pantalla.create_text(1116, 345, text=f"Part: {mode(part_number)}", font=("Helvetica", 35, "bold"), fill="green", anchor=tk.NW)
                    else: Text_part_number  = pantalla.create_text(1116, 345, text=f"Part: {mode(part_number)}*", font=("Helvetica", 35, "bold"), fill="red", anchor=tk.NW)
                    Stop_part_number = False
                else:
                    try: pantalla.delete(Text_part_number)
                    except: pass
                    Text_part_number  = pantalla.create_text(1116, 345, text=f"Part:__________", font=("Helvetica", 30, "bold"), fill="white", anchor=tk.NW)

                if len(fecha_exp) >= 4:
                    pantalla.delete(Text_fecha_exp)
                    if str(mode(fecha_exp)) == Exp_ingresado: Text_fecha_exp = pantalla.create_text(1116, 521, text=f"Exp: {mode(fecha_exp)}", font=("Helvetica", 35, "bold"), fill="green", anchor=tk.NW)
                    else: Text_fecha_exp = pantalla.create_text(1116, 521, text=f"Exp: {mode(fecha_exp)}*", font=("Helvetica", 35, "bold"), fill="red", anchor=tk.NW)
                    Stop_fecha_exp = False
                else:
                    try: pantalla.delete(Text_fecha_exp)
                    except: pass
                    Text_fecha_exp = pantalla.create_text(1116, 521, text=f"Exp:__________ ", font=("Helvetica", 30, "bold"), fill="white", anchor=tk.NW)

                if len(lot_number) >= 4:
                    pantalla.delete(Text_lot_number)
                    if str(mode(lot_number)) == Lot_ingresado:
                        Text_lot_number = pantalla.create_text(1116, 697, text=f"Lot: {mode(lot_number)}", font=("Helvetica", 35, "bold"), fill="green", anchor=tk.NW)
                        if flag:
                            cant_pouches += 1
                            flag = False
                            print(cant_pouches)
                    else: 
                        Text_lot_number = pantalla.create_text(1116, 697, text=f"Lot: {mode(lot_number)}*", font=("Helvetica", 35, "bold"), fill="red", anchor=tk.NW)
                    Stop_lot_number = False
                else:
                    try: pantalla.delete(Text_lot_number)
                    except: pass
                    Text_lot_number = pantalla.create_text(1116, 697, text=f"Lot:__________ ", font=("Helvetica", 30, "bold"), fill="white", anchor=tk.NW)
                    flag = True
            else:
                if title_change == True:
                    pantalla.delete(Titulo_part_number)
                    pantalla.delete(Titulo_fecha_exp)
                    pantalla.delete(Titulo_lot_number)
                    Titulo_part_number  = pantalla.create_text(320, 193, text=f"Part: 470015", font=("Helvetica", 30, "bold"), fill="yellow", anchor=tk.NW)
                    Titulo_fecha_exp = pantalla.create_text(779, 193, text=f"Exp: 2025-11-30", font=("Helvetica", 30, "bold"), fill="yellow", anchor=tk.NW)
                    Titulo_lot_number = pantalla.create_text(1245, 193, text=f"Lot: DM04234604", font=("Helvetica", 30, "bold"), fill="yellow", anchor=tk.NW)
                    title_change = False

                if len(part_number) >= 4:
                    pantalla.delete(Text_part_number)
                    if str(mode(part_number)) == "470015": Text_part_number  = pantalla.create_text(1116, 345, text=f"Part: {mode(part_number)}", font=("Helvetica", 35, "bold"), fill="green", anchor=tk.NW)
                    else: Text_part_number  = pantalla.create_text(1116, 345, text=f"Part: {mode(part_number)}*", font=("Helvetica", 35, "bold"), fill="red", anchor=tk.NW)
                    Stop_part_number = False
                else:
                    try: pantalla.delete(Text_part_number)
                    except: pass
                    Text_part_number  = pantalla.create_text(1116, 345, text=f"Part:__________", font=("Helvetica", 30, "bold"), fill="white", anchor=tk.NW)

                if len(fecha_exp) >= 4:
                    pantalla.delete(Text_fecha_exp)
                    if str(mode(fecha_exp)) == "2025-11-30": Text_fecha_exp = pantalla.create_text(1116, 521, text=f"Exp: {mode(fecha_exp)}", font=("Helvetica", 35, "bold"), fill="green", anchor=tk.NW)
                    else: Text_fecha_exp = pantalla.create_text(1116, 521, text=f"Exp: {mode(fecha_exp)}*", font=("Helvetica", 35, "bold"), fill="red", anchor=tk.NW)
                    Stop_fecha_exp = False
                else:
                    try: pantalla.delete(Text_fecha_exp)
                    except: pass
                    Text_fecha_exp = pantalla.create_text(1116, 521, text=f"Exp:__________ ", font=("Helvetica", 30, "bold"), fill="white", anchor=tk.NW)

                if len(lot_number) >= 4:
                    pantalla.delete(Text_lot_number)
                    if str(mode(lot_number)) == "DM04234604":
                        Text_lot_number = pantalla.create_text(1116, 697, text=f"Lot: {mode(lot_number)}", font=("Helvetica", 35, "bold"), fill="green", anchor=tk.NW)
                        box1 = True
                    else: Text_lot_number = pantalla.create_text(1116, 697, text=f"Lot: {mode(lot_number)}*", font=("Helvetica", 35, "bold"), fill="red", anchor=tk.NW)
                    Stop_lot_number = False
                else:
                    try: pantalla.delete(Text_lot_number)
                    except: pass
                    Text_lot_number = pantalla.create_text(1116, 697, text=f"Lot:__________ ", font=("Helvetica", 30, "bold"), fill="white", anchor=tk.NW)
                    if box1 == True:
                        box1 = False
                        cant_pouches = 0
                        pantalla.delete(Titulo_part_number)
                        pantalla.delete(Titulo_fecha_exp)
                        pantalla.delete(Titulo_lot_number)
                        Titulo_part_number  = pantalla.create_text(320, 193, text=f"Part: {Part_ingresado}", font=("Helvetica", 30, "bold"), fill="#FFFFFF", anchor=tk.NW)
                        Titulo_fecha_exp = pantalla.create_text(779, 193, text=f"Exp: {Exp_ingresado}", font=("Helvetica", 30, "bold"), fill="#FFFFFF", anchor=tk.NW)
                        Titulo_lot_number = pantalla.create_text(1245, 193, text=f"Lot: {Lot_ingresado}", font=("Helvetica", 30, "bold"), fill="#FFFFFF", anchor=tk.NW)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = imutils.resize(frame, width=640, height=480)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            lblVideo.configure(image=img)
            lblVideo.image = img
            
            pantalla.after(10, visualizar)
        else:
            cap = cv2.VideoCapture(camera_id)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
            print("La camara id es: ",camera_id)
            camera_id +=1
            if camera_id >= 10:
                camera_id = 0
            pantalla.after(100, visualizar)

def loading_system():
    global Text_loading, background_loading_id
    background_loading_id = pantalla.create_image(0, 0, anchor=tk.NW, image=background_loading)
    Text_loading = pantalla.create_text(960, 520, text=f"Loading the system...", font=("Helvetica", 50, "bold"), fill="white")
    pantalla.after(100, visualizar)

def obtener_info():
    global Part_ingresado, Exp_ingresado, Lot_ingresado
    # Part_ingresado = Part.get()
    # Exp_ingresado = Exp.get()
    # Lot_ingresado = Lot.get()
    fileurl = '/home/jetson/Documents/temp/label_data.txt'
    variabledata = ReadData(fileurl)

    Part_ingresado = variabledata.get('PartNumber', '')
    Exp_ingresado = variabledata.get('ExpDate', '')
    Lot_ingresado = variabledata.get('LotNumber', '')
    if Part_ingresado == "" or Exp_ingresado == "" or Lot_ingresado == "":
        messagebox.showerror("Error", "Por favor, llenar todos los campos")
        return
    
    print("Número de Parte: ", Part_ingresado)
    print("Fecha de Expiración: ", Part_ingresado)
    print("Número de Lote: ", Part_ingresado)

    # confirmar = messagebox.askquestion("Confirmación", "¿Está seguro de que todos los campos están llenados correctamente?", icon='info')
    # if confirmar == 'yes':
    clear_id.destroy()
    Next_id.destroy()
    Part.destroy()
    Exp.destroy()
    Lot.destroy()
    pantalla.delete(Titulo_fecha_exp)
    pantalla.delete(Titulo_lot_number)
    pantalla.delete(Titulo_part_number)
    loading_system()
    # else:
    #     return

def clear_fields():
    Part.delete(0, tk.END)
    Exp.delete(0, tk.END)
    Lot.delete(0, tk.END)

def turn_off_action():
    root.destroy()

root = tk.Tk()
root.title("Label Verification Prototype")

root.attributes('-fullscreen', True)
# root.geometry("1920x1080")

pantalla = tk.Canvas(root, width=1920, height=1080, bg="#0E131F", highlightthickness=0)
pantalla.pack()

Titulo = pantalla.create_text(210, 52, text="Label Verification Prototype", font=("Helvetica", 40, "bold"), fill="white", anchor=tk.NW)

#Boton de cerrado
Close = tk.PhotoImage(file="IMG/x-circle.png")
Close_Button = tk.Button(pantalla, image=Close, bg="#0E131F", command=turn_off_action, borderwidth=0, relief="flat", highlightthickness=0)
Close_Button.place(x = 1794, y = 55)

#Fondo
background = tk.PhotoImage(file="IMG/background.png")
background_id = pantalla.create_image(221, 156, anchor=tk.NW, image=background)

#Frame_fondo
Frame_fondo = tk.PhotoImage(file="IMG/Frame_fondo.png")
background_loading = tk.PhotoImage(file="IMG/background_loading.png")

#Boton de Clear
clear = tk.PhotoImage(file="IMG/clear.png")
clear_id = tk.Button(pantalla, image=clear, bg="#0B3954", command=clear_fields, borderwidth=0, relief="flat", highlightthickness=0)
clear_id.place(x = 640, y = 787)

#Boton de Next
Next = tk.PhotoImage(file="IMG/next.png")
Next_id = tk.Button(pantalla, image=Next, bg="#0B3954", command=loading_system, borderwidth=0, relief="flat", highlightthickness=0)
Next_id.place(x = 1100, y = 787)

# Campo de texto para ingresar Número de Parte 
Part = tk.Entry(pantalla, bg="white", font=("Helvetica", 30), borderwidth=0, relief="flat", highlightthickness=0)
Part.config(width=25) 
Part.place(x=950, y=295)

# Campo de texto para ingresar Fecha de Expiración
Exp = tk.Entry(pantalla, bg="white", font=("Helvetica", 30), borderwidth=0, relief="flat", highlightthickness=0)
Exp.config(width=25) 
Exp.place(x=950, y=450)

# Campo de texto para ingresar Fecha de Expiración
Lot = tk.Entry(pantalla, bg="white", font=("Helvetica", 30), borderwidth=0, relief="flat", highlightthickness=0)
Lot.config(width=25) 
Lot.place(x=950, y=604)
inicio = 1

Titulo_fecha_exp = pantalla.create_text(393, 295, text=f"Número de Parte: ", font=("Helvetica", 35, "bold"), fill="white", anchor=tk.NW)
Titulo_lot_number = pantalla.create_text(393, 450, text=f"Fecha de Expiración: ", font=("Helvetica", 35, "bold"), fill="white", anchor=tk.NW)
Titulo_part_number  = pantalla.create_text(393, 605, text=f"Número de Lote: ", font=("Helvetica", 35, "bold"), fill="white", anchor=tk.NW)

root.mainloop()