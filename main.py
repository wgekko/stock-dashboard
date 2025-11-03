import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
#import os

hide_sidebar_style = """
    <style>
        /* Oculta la barra lateral completa */
        [data-testid="stSidebar"] {
            display: none;
        }
        /* Ajusta el área principal para usar todo el ancho */
        [data-testid="stAppViewContainer"] {
            margin-left: 0px;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

st.set_page_config(page_title="Star Wars Dashboard", page_icon="static/droide.png", layout="wide")

#st.header("Star Wars Intro Animada ::")
#st.image("static/droide.png", width="content", output_format="auto")

col1, col2 = st.columns([1, 4]) 
with col1:
    st.image("static/droide.png",  width=40)

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

# --- Botón manual para activar música ---
#if st.button("🎵 Reproducir música épica"):
    #st.audio("https://s.cdpn.io/1202/Star_Wars_original_opening_crawl_1977.mp3", format="audio/mp3")
st.audio("static/Star_Wars_original_opening_crawl_1977.mp3", format="audio/mp3",loop=True, autoplay=True) 
       
# --- HTML + CSS embebidos ---
html_code = """
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <style>
      :root {
        --main: #ffb13a;
        --font: 'Roboto', 'Oxygen', sans-serif;
      }

      html { font-size: 10px; }

      body {
        overflow: hidden;
        background-color: black;
        background-image: url(http://untroubled.org/backgrounds/space/stars.gif);
        font-family: var(--font);
        margin: 0;
        color: white;
      }

      h2 {
        text-align: center;
        margin: 0 0 60px 0;
        font-size: 5rem;
      }

      p {
        font-size: 3rem;
        line-height: 6rem;
        margin-bottom: 20px;
      }

      .star-wars {
        padding: 40px 80px; /* más ancho horizontalmente */
        text-align: justify;
        margin: 0 auto;
        letter-spacing: 1.5px;
        max-width: 1600px; /* pantalla más ancha */
        height: 900px;
        transform: perspective(250px) rotateX(18deg);
        animation: intro 90s linear infinite; /* animación en bucle */
      }

      .star-wars :is(h2, p) {
        color: var(--main);
      }

      @keyframes intro {
        0% {
          transform: perspective(250px) rotateX(18deg) translateY(900px);
          opacity: 1;
        }
        90% {
          opacity: 1;
        }
        100% {
          transform: perspective(250px) rotateX(25deg) translateY(-3000px);
          opacity: 0;
        }
      }
    </style>
  </head>
  <body>
    <main class="star-wars">
      <h2>Hace mucho tiempo,</h2>  
      <h2>en un mercado no tan lejano...</h2>
      <h2>EPISODIO I</h2>  
      <h2>EL DESPERTAR DE LOS MERCADOS</h2>
      <p>
        El universo financiero se encuentra en constante movimiento.  
        Las fuerzas del cambio, impulsadas por la tecnología y la información,  
        marcan el destino de cada acción que brilla en el firmamento bursátil.    
      </p>
      <p>
        Desde las profundidades del código, surge una nueva herramienta:  
        el <b>Real Time Stock Dashboard</b>, un sistema capaz de rastrear y revelar  
        la evolución de las acciones más poderosas de la galaxia económica.  
      </p>
      <p>
        Utilizando la sabiduría de los antiguos maestros del análisis técnico,  
        el dashboard observa tendencias, mide la fuerza del mercado  
        y calcula el equilibrio entre la esperanza y el miedo:  
        los indicadores RSI, MACD y las misteriosas Bandas de Bollinger. 
      </p>   
      <p>
        Hoy, nuevas señales emergen en los gráficos estelares...  
        Las acciones del universo financiero estadounidense se agitan,  
        marcando rutas de crecimiento, corrección y oportunidad.  
      </p>   
      <p>
        Desde los titanes tecnológicos hasta las fuerzas ocultas de Wall Street,  
        cada movimiento deja su huella en los registros del tiempo,  
        revelando el pulso vivo del mercado en constante expansión.  
      </p>
      <p>
        Solo el análisis, la paciencia y la Fuerza de los Datos  
        podrán revelar el destino final del mercado...
      </p>
    </main>
  </body>
</html>
"""

st.components.v1.html(html_code, height=600, scrolling=False)

col1, col2, col3 = st.columns([2, 2, 2])  # proporciones: izquierda, centro, derecha

with col2:
    if st.button("INGRESO  AL  DASHBOARD", key="acceso", use_container_width=True):
        st.switch_page("pages/app.py")