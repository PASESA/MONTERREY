import tkinter as tk

# Crear una ventana principal
root = tk.Tk()
tipo_pago_ = ""

def cambiar_valor(contrario):
    try:
        contrario.set(False)
        if variable_tipo_pago_transferencia.get():
            tipo_pago_ = "Transferencia"

        if variable_tipo_pago_efectivo.get():
            tipo_pago_ = "Efectivo"

        print(tipo_pago_)
    except Exception as e:
        pass

def vaciar():
    variable_tipo_pago_transferencia.set(False)
    variable_tipo_pago_efectivo.set(False)



label_frame_tipo_pago = tk.LabelFrame(root, text="Tipo de pago")
label_frame_tipo_pago.grid(column=0, row=0, padx=10, pady=10, sticky=tk.NW)

# Crear una variable de control para el estado del checkbox
variable_tipo_pago_efectivo = tk.BooleanVar()
# Crear un checkbox y asociarlo a la variable de control
checkbox_efectivo = tk.Checkbutton(label_frame_tipo_pago, text="Efectivo", variable=variable_tipo_pago_efectivo, command=lambda:{cambiar_valor(variable_tipo_pago_transferencia)})

# Ubicar el checkbox en la ventana principal
checkbox_efectivo.grid(column=0, row=0, padx=0, pady=0, sticky=tk.NW)

variable_tipo_pago_transferencia = tk.BooleanVar()

checkbox_transferencia = tk.Checkbutton(label_frame_tipo_pago, text="Transferencia", variable=variable_tipo_pago_transferencia, command=lambda:{cambiar_valor(variable_tipo_pago_efectivo)})

# Ubicar el checkbox en la ventana principal
checkbox_transferencia.grid(column=0, row=1, padx=0, pady=0, sticky=tk.NW)

# Ejecutar el bucle principal de la aplicación
root.mainloop()

