import clips
import tkinter as tk
from tkinter import messagebox

# Configurar el sistema experto con CLIPS
sistemaExperto = clips.Environment()

# Definir las reglas en CLIPS para clasificar tipos de televisores
reglas = [
    "(defrule tv_pequeno (tamaño ?t&:(<= ?t 32)) (uso dormitorio) (resolucion HD) => (assert (tipo tv_pequeno_dormitorio_HD)))",
    "(defrule tv_pequeno (tamaño ?t&:(<= ?t 32)) (uso dormitorio) (resolucion Full_HD) => (assert (tipo tv_pequeno_dormitorio_Full_HD)))",
    "(defrule tv_mediano (tamaño ?t&:(>= ?t 33) &:(<= ?t 55)) (uso sala) (resolucion 4K) => (assert (tipo tv_mediano_sala_4K)))",
    "(defrule tv_grande (tamaño ?t&:(>= ?t 56)) (uso sala) (resolucion 8K) => (assert (tipo tv_grande_sala_8K)))",
    "(defrule tv_grande (tamaño ?t&:(>= ?t 56)) (uso cine) (resolucion 4K) => (assert (tipo tv_grande_cine_4K)))",
    "(defrule tv_grande (tamaño ?t&:(>= ?t 56)) (uso cine) (resolucion 8K) => (assert (tipo tv_grande_cine_8K)))"
]

for regla in reglas:
    sistemaExperto.build(regla)

# Función que evalúa las reglas y selecciona el tipo de televisor
def clasificar_tv():
    # Limpiar las aserciones anteriores
    sistemaExperto.reset()

    # Insertar hechos en CLIPS según la selección del usuario
    sistemaExperto.assert_string(f"(tamaño {tamaño_var.get()})")
    sistemaExperto.assert_string(f"(uso {uso_var.get()})")
    sistemaExperto.assert_string(f"(resolucion {resolucion_var.get()})")

    # Ejecutar las reglas
    sistemaExperto.run()

    resultado = "No se encontró un tipo de televisor para esta combinación."

    # Revisar cada hecho en el sistema experto
    for fact in sistemaExperto.facts():
        fact_str = str(fact)
        if "(tipo " in fact_str:
            tipo_tv = fact_str.split("(tipo ")[1].split(")")[0].strip()
            resultado = f"Tipo de Televisor: {tipo_tv.replace('_', ' ')}"
            break

    # Mostrar el resultado
    messagebox.showinfo("Clasificación de Televisor", resultado)


# Crear la ventana principal
root = tk.Tk()
root.title("Sistema Experto de Clasificación de Televisores")

# Variables para almacenar las selecciones
tamaño_var = tk.StringVar()
uso_var = tk.StringVar(value="sala")
resolucion_var = tk.StringVar(value="HD")

# Etiquetas y menús desplegables para las opciones
tk.Label(root, text="Tamaño (pulgadas):").pack()
tk.Entry(root, textvariable=tamaño_var).pack()

tk.Label(root, text="Uso del Televisor:").pack()
tk.OptionMenu(root, uso_var, "dormitorio", "sala", "cine").pack()

tk.Label(root, text="Resolución:").pack()
tk.OptionMenu(root, resolucion_var, "HD", "Full_HD", "4K", "8K").pack()

# Botón para ejecutar la clasificación
tk.Button(root, text="Clasificar Televisor", command=clasificar_tv).pack()

# Iniciar la aplicación
root.mainloop()