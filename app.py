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
