import sqlite3
import tkinter as tk
from tkinter import ttk

def cargar_inscripciones():
    conn = sqlite3.connect("../db/sicue.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, estudiante_id, plan_id, fecha_inscripcion, estado FROM inscripciones")
    inscripciones = cursor.fetchall()
    conn.close()
    return inscripciones

def actualizar_estado(id_inscripcion, nuevo_estado):
    conn = sqlite3.connect("../db/sicue.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE inscripciones SET estado = ? WHERE id = ?", (nuevo_estado, id_inscripcion))
    conn.commit()
    conn.close()
    lbl_status.config(text=f"Inscripción {id_inscripcion} actualizada a {nuevo_estado}")

def mostrar_estado_actual(event):
    seleccionado = tree.selection()
    if seleccionado:
        item = tree.item(seleccionado)
        estado_actual = item['values'][4]
        lbl_estado_actual.config(text=f"Estado actual: {estado_actual}")

def crear_interfaz():
    root = tk.Tk()
    root.title("Gestión de Inscripciones")
    root.geometry("600x400")
    
    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    global tree
    tree = ttk.Treeview(frame, columns=("ID", "Estudiante", "Plan", "Fecha", "Estado"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Estudiante", text="Estudiante ID")
    tree.heading("Plan", text="Plan ID")
    tree.heading("Fecha", text="Fecha Inscripción")
    tree.heading("Estado", text="Estado")
    tree.pack(fill=tk.BOTH, expand=True)
    
    tree.bind("<<TreeviewSelect>>", mostrar_estado_actual)
    
    inscripciones = cargar_inscripciones()
    for inscripcion in inscripciones:
        tree.insert("", tk.END, values=inscripcion)
    
    def cambiar_estado(nuevo_estado):
        seleccionado = tree.selection()
        if seleccionado:
            item = tree.item(seleccionado)
            id_inscripcion = item['values'][0]
            actualizar_estado(id_inscripcion, nuevo_estado)
            tree.set(seleccionado, column="Estado", value=nuevo_estado)
            lbl_estado_actual.config(text=f"Estado actual: {nuevo_estado}")
    
    frame_botones = ttk.Frame(root)
    frame_botones.pack(pady=10)
    
    btn_aprobar = ttk.Button(frame_botones, text="Aprobar", command=lambda: cambiar_estado("Aprobado"))
    btn_aprobar.grid(row=0, column=0, padx=5)
    
    btn_denegar = ttk.Button(frame_botones, text="Denegar", command=lambda: cambiar_estado("Denegado"))
    btn_denegar.grid(row=0, column=1, padx=5)
    
    global lbl_status
    lbl_status = ttk.Label(root, text="")
    lbl_status.pack()
    
    global lbl_estado_actual
    lbl_estado_actual = ttk.Label(root, text="Estado actual: ")
    lbl_estado_actual.pack()
    
    root.mainloop()

if __name__ == "__main__":
    crear_interfaz()
