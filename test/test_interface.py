import tkinter as tk
from tkinter import ttk

def boton_clicado():
    print("¡El botón ha sido clicado!")

ventana = tk.Tk()

# Establecer colores personalizados
color_rojo_suave = "#FF9999"  # Rojo suave
color_rojo_claro = "#FFCCCC"  # Rojo claro
color_azul_suave = "#99CCFF"  # Azul suave

# Crear estilos personalizados
style = ttk.Style()

style.configure('Estilo.RojoSuave.TButton', background=color_rojo_suave, foreground='black')
style.configure('Estilo.RojoClaro.TButton', background=color_rojo_claro, foreground='black')
style.configure('Estilo.AzulSuave.TButton', background=color_azul_suave, foreground='black')

# Crear botones con los estilos personalizados
boton_rojo_suave = ttk.Button(ventana, text="Botón Rojo Suave", command=boton_clicado,
                              background='Estilo.RojoSuave.TButton')
boton_rojo_suave.pack()

boton_rojo_claro = ttk.Button(ventana, text="Botón Rojo Claro", command=boton_clicado,
                              background='Estilo.RojoClaro.TButton')
boton_rojo_claro.pack()

boton_azul_suave = ttk.Button(ventana, text="Botón Azul Suave", command=boton_clicado,
                              background='Estilo.AzulSuave.TButton')
boton_azul_suave.pack()

ventana.mainloop()
