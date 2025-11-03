import streamlit as st
import streamlit.components.v1 as components
import streamlit as st
from pathlib import Path
import os

st.set_page_config(page_title="Star Wars Intro", page_icon="static/droide.png", layout="centered", initial_sidebar_state="collapsed",)


col1, col2 = st.columns([1, 4]) 
#with col1:
    #st.image("static/droide.png",  width=50)

with col2:
    st.markdown(
        """
        <h1 style="margin-top: 5px;">Star Wars Dashboard</h1>
        """,
        unsafe_allow_html=True
    )
    #st.header("Star Wars Dashboard")


# ----- Cargar estilos CSS -----
css_file = Path("components/style.css")
if css_file.exists():
    st.markdown(f"<style>{css_file.read_text()}</style>",
                unsafe_allow_html=True)
else:
    st.error("No se encontró el archivo CSS.")

# ----- Cargar estilos CSS -----
css_file = Path("components/style.css")
if css_file.exists():
    st.markdown(f"<style>{css_file.read_text()}</style>",
                unsafe_allow_html=True)
else:
    st.error("No se encontró el archivo CSS.")

# --- FUNCIÓN PARA CARGAR ARCHIVOS ---
def leer_archivo(ruta):
    """Lee el contenido de un archivo y lo devuelve como una cadena."""
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Error: No se encontró el archivo en la ruta: {ruta}")
        return ""
    except Exception as e:
        st.error(f"Error al leer el archivo {ruta}: {e}")
        return ""

# --- RUTAS A TUS ARCHIVOS ---
# Asegúrate de que estos archivos estén en la misma carpeta que app.py
ruta_html = "components/index.html"
ruta_css = "components/style.css"


# --- LECTURA DEL CONTENIDO DE LOS ARCHIVOS ---
html_content = leer_archivo(ruta_html)
css_content = leer_archivo(ruta_css)


# --- VERIFICACIÓN DE CONTENIDO ---
if not all([html_content, css_content]):
    st.warning("No se pudieron cargar todos los archivos necesarios (HTML, CSS). La aplicación podría no funcionar como se espera.")
    st.stop()


# --- Botón manual para activar música ---
#if st.button("🎵 Reproducir música épica"):
    #st.audio("https://s.cdpn.io/1202/Star_Wars_original_opening_crawl_1977.mp3", format="audio/mp3")
st.audio("static/Star_Wars_original_opening_crawl_1977.mp3", format="audio/mp3",loop=True, autoplay=True) 
       
# --- HTML + CSS embebidos ---
html_code = f"""
<!DOCTYPE html>
<html lang="es">
  <head>
   <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Dashboard</title>
    <link rel="stylesheet" href="inicio/style.css" />
    <link rel="preconnect" href="https://fonts.gstatic.com" />
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400&display=swap" rel="stylesheet" />
    <style>
        {css_content}
    </style>
  </head>
  <body>
    {html_content}    
  </body>
</html>
"""

st.components.v1.html(html_code, height=900, scrolling=False)

col1, col2, col3 = st.columns([2, 2, 2])  # proporciones: izquierda, centro, derecha

with col2:
    if st.button("INGRESO DASHBOARD", key="acceso", use_container_width=True):
        st.switch_page("pages/app.py")