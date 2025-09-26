#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
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

# ================================
# 🔹 API pública (Ghibli Films)
# ================================
def obtener_peliculas():
    try:
        url = "https://ghibliapi.vercel.app/films"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Mapear a nuestro formato
        peliculas = []
        for i, peli in enumerate(data[:4]):  # solo 4 primeras para la demo
            peliculas.append({
                "id": i + 1,
                "titulo": peli["title"],
                "descripcion": peli["description"],
                "poster": peli["image"]
            })
        return peliculas
    except Exception as e:
        print(f"⚠️ Error obteniendo películas: {e}")
        return []

peliculas = obtener_peliculas()

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
        self.root.title("Películas REST + Oracle")
        self.root.geometry("900x600")

        ttk.Label(root, text="Películas disponibles", font=("Arial", 16)).pack(pady=10)

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
                frame_peli.grid(row=i // 2, column=col, padx=10, pady=10, sticky="n")

                # Imagen desde API
                img_data = requests.get(pelicula["poster"], timeout=10).content
                img = Image.open(BytesIO(img_data)).resize((200, 300))
                photo = ImageTk.PhotoImage(img)

                lbl_img = ttk.Label(frame_peli, image=photo)
                lbl_img.image = photo
                lbl_img.pack()

                # Título y descripción
                ttk.Label(frame_peli, text=pelicula["titulo"], font=("Arial", 14, "bold")).pack(pady=5)
                ttk.Label(frame_peli, text=pelicula["descripcion"], wraplength=250).pack()

                # Guardar en Oracle
                self.guardar_en_oracle(pelicula)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar películas: {e}")

    def guardar_en_oracle(self, pelicula):
        try:
            connection = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
            cursor = connection.cursor()

            # Evitar duplicados
            cursor.execute("SELECT COUNT(*) FROM peliculas WHERE id = :1", (pelicula["id"],))
            existe = cursor.fetchone()[0]

            if existe == 0:
                cursor.execute("""
                    INSERT INTO peliculas (id, titulo, descripcion, poster)
                    VALUES (:1, :2, :3, :4)
                """, (pelicula["id"], pelicula["titulo"], pelicula["descripcion"], pelicula["poster"]))
                connection.commit()

            cursor.close()
            connection.close()
        except Exception as e:
            print(f"⚠️ Error guardando en Oracle: {e}")

# ================================
# 🔹 Main
# ================================
if __name__ == "__main__":
    threading.Thread(target=run_api, daemon=True).start()
    root = tk.Tk()
    app_gui = PeliculasGUI(root)
    root.mainloop()
