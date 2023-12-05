import tkinter as tk
from escaner3 import *


def verificar_datos():
    numero_parte = entry_numero_parte.get()
    fecha_expiracion = entry_fecha_expiracion.get()
    numero_lote = entry_numero_lote.get()

    # Aquí podrías procesar o guardar los datos como desees
    print(f"Número de Parte: {numero_parte}")
    print(f"Fecha de Expiración: {fecha_expiracion}")
    print(f"Número de Lote: {numero_lote}")

    entry_numero_parte.config(state='disabled')
    entry_fecha_expiracion.config(state='disabled')
    entry_numero_lote.config(state='disabled')

root = tk.Tk()
root.title("Verificador de Barcodes DAS")

def nueva_verificacion():


    entry_numero_parte.config(state='normal')
    entry_fecha_expiracion.config(state='normal')
    entry_numero_lote.config(state='normal')

    entry_numero_parte.delete(0, tk.END)
    entry_fecha_expiracion.delete(0, tk.END)
    entry_numero_lote.delete(0, tk.END)

#BOTONES
# Función para guardar los datos ingresados
btn_guardar = tk.Button(root, text="Fijar", command=verificar_datos)
btn_guardar.pack()

btn_guardar = tk.Button(root, text="Nueva Verificacion", command=nueva_verificacion)
btn_guardar.pack()

# Etiqueta y campo de entrada para Número de Parte
label_numero_parte = tk.Label(root, text="Número de Parte:")
label_numero_parte.pack()
entry_numero_parte = tk.Entry(root)
entry_numero_parte.pack()

# Etiqueta y campo de entrada para Fecha de Expiración
label_fecha_expiracion = tk.Label(root, text="Fecha de Expiración:")
label_fecha_expiracion.pack()
entry_fecha_expiracion = tk.Entry(root)
entry_fecha_expiracion.pack()

# Etiqueta y campo de entrada para Número de Lote
label_numero_lote = tk.Label(root, text="Número de Lote:")
label_numero_lote.pack()
entry_numero_lote = tk.Entry(root)
entry_numero_lote.pack()

root.mainloop()
