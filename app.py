#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTK
import requests
import oracledb
from io import BytesIO
from flask import Flask, jsonify
import threading

# ================================
# 🔹 Configuración de Oracle
# ================================
DB_USER = "system"
DB_PASS = "Tapiero123"
DB_DSN = "localhost:1521/orcl"

peliculas = [
    {
        "id": 1,
        "titulo": "inception",
        "descripcion": "un ladron roba secretos del subconciente .",
        "poster": "https://m.media-amazon.com/images/I/51s+o2aD4nL._AC_.jpg"
    },
    {
        "id": 2,
        "titulo": "the matrix",
        "descripcion": "un hacker descubre la verdad sobre su realidad .",
        "poster": "https://m.media-amazon.com/images/I/51EG732BV3L._AC_SY445_.jpg"
    }
]

# ================================
# 🔹 API REST con Flask
# ================================
app = Flask(__name__)

@app.route("/peliculas", methods=["GET"])
def get_peliculas():
    return jsonify(peliculas)

def run_api():
    app.run(port=5000, debug=False, use_reloader=False)


# ================================
# 🔹 Interfaz gráfica con Tkinter
# ================================
class PeliculasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("peliculas REST + oracle .")
        self.root.geometry("700*500")

        ttk.Label(root, text="peliculas disponibles", font=("Arial", 16)).pack(pady=10)

        self.frame = ttk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        self.mostrar_peliculas()

    def mostrar_peliculas(self):
        try:
            response = requests.get("http://127.0.0.1:5000/peliculas")
            response.raise_for_status()
            data = response.json()

            for i, pelicula in enumerate(data):
                col = i % 2
                frame_peli = ttk.Frame(self.frame, padding=10, relief="ridge")
                frame_peli.grid(row=0, column=col, padx=10, pady=10, sticky="n")

            #imagen
            img_data = requests.get(pelicula["poster"]).content
            img = Image.open(BytesIO(img_data)).resize((200, 300))
            photo = ImageTK.PhotoImage(img)

            lbl_img = ttk.Label(frame_peli, image=photo)
            lbl_img.image = photo
            lbl_img.pack()

            #titulo y descripcion
            ttk.Label(frame_peli, text=pelicula["titulo"], font=("Arial", 14, "bold")).pack(pady=5)
            ttk.Label(frame_peli, text=pelicula["descripcion"], wraplength=200).pack()

            #guardar en oracle  
            self.guardar_en_oracle(pelicula)
        
        except Exception as e:
            messagebox.showerror("error", f"no se pudieron cargar peliculas: {e}")
    
    def guardar_en_oracle(self, pelicula):
        try:
            connection = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO peliculas (id, titulo, descripcion, poster)
                VALUES (:1, :2, :3, :4)
            """, (pelicula["id"], pelicula["titulo"], pelicula["descripcion"], pelicula["poster"]))

            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"⚠️ error guardando en oracle: {e}")

# ================================
# 🔹 Main
# ================================
if __name__ == "__main__":
    # Correr API en hilo aparte
    threading.Thread(target=run_api, daemon=True).start()

    # GUI
    root = tk.Tk()
    app_gui = PeliculasGUI(root)
    root.mainloop()

