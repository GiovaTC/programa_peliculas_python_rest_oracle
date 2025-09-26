# programa_peliculas_python_rest_oracle .

<img width="203" height="193" alt="image" src="https://github.com/user-attachments/assets/acd0ce8a-579d-497b-a76e-797430d0bb13" />  

# 🎬 Programa en Python: Películas REST + Oracle :
Este proyecto en **Python** implementa :

- **Frontend (Interfaz gráfica con Tkinter):** muestra dos películas (imagen, título, descripción) .  
- **Backend REST (Flask):** expone las películas en endpoints HTTP .  
- **Base de datos Oracle:** guarda la información de las películas (usando `oracledb`) .  

## 🔹 Flujo
1. El frontend consume el **API REST** vía `requests` .  
2. Los datos obtenidos se almacenan en **Oracle** .  

---

## 📌 Script principal: `app.py`
```python
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
DB_USER = "user"
DB_PASS = "password"
DB_DSN = "localhost:1521/XEPDB1"

# ================================
# 🔹 Datos simulados de películas
# ================================
peliculas = [
    {
        "id": 1,
        "titulo": "Inception",
        "descripcion": "Un ladrón roba secretos del subconsciente.",
        "poster": "https://m.media-amazon.com/images/I/51s+o2aD4nL._AC_.jpg"
    },
    {
        "id": 2,
        "titulo": "The Matrix",
        "descripcion": "Un hacker descubre la verdad sobre su realidad.",
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
        self.root.title("Películas REST + Oracle")
        self.root.geometry("700x500")

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
                frame_peli.grid(row=0, column=col, padx=10, pady=10, sticky="n")

                # Imagen
                img_data = requests.get(pelicula["poster"]).content
                img = Image.open(BytesIO(img_data)).resize((200, 300))
                photo = ImageTk.PhotoImage(img)

                lbl_img = ttk.Label(frame_peli, image=photo)
                lbl_img.image = photo
                lbl_img.pack()

                # Título y descripción
                ttk.Label(frame_peli, text=pelicula["titulo"], font=("Arial", 14, "bold")).pack(pady=5)
                ttk.Label(frame_peli, text=pelicula["descripcion"], wraplength=200).pack()

                # Guardar en Oracle
                self.guardar_en_oracle(pelicula)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar películas: {e}")

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
            print(f"⚠️ Error guardando en Oracle: {e}")

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

🔹 Script DDL Oracle :
Ejecuta en Oracle :

CREATE TABLE peliculas (
    id NUMBER PRIMARY KEY,
    titulo VARCHAR2(100),
    descripcion VARCHAR2(500),
    poster VARCHAR2(300)
);

🔹 requirements.txt :
Flask==3.0.3
requests==2.32.3
oracledb==3.3.0
Pillow==10.2.0

🚀 Ejecución :
Crea y activa tu entorno virtual .

Instala dependencias :
bash
pip install -r requirements.txt

Ejecuta el programa :
bash
python app.py

Se abre la ventana con las dos películas, traídas vía REST y almacenadas en Oracle .
