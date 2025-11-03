# stock-dashboard
analisis de precios en tiempo real

IMPORTANTE 
se tiene que crear una carpeta  .Streamlit
y dentro de ella crear un archivo 
------------------------------------------------------------------------------------------------------------------------------------------------
config.toml
y dentro 
[server]
enableStaticServing = true

[[theme.fontFaces]]
family = "Inter"
url = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap"

[theme]
primaryColor = "#FF8C00"
backgroundColor = "#0D1B2A"
secondaryBackgroundColor = "#1B263B"
textColor = "#FFA500"
linkColor = "#FFA500"
borderColor = "#CCCCCC"
showWidgetBorder = true
baseRadius = "0.5rem"
buttonRadius = "0.5rem"
font = "Inter"
headingFontWeights = [600, 500]
headingFontSizes = ["2.5rem", "1.8rem"]
codeFont = "Courier New"
codeFontSize = "0.75rem"
codeBackgroundColor = "#112B3C"
showSidebarBorder = false
chartCategoricalColors = [
  "#FF8C00",  # Orange oscuro
  "#FFA500",  # Naranja clásico
  "#FFD700",  # Mostaza / dorado
  "#E1C16E",  # Mostaza claro
  "#C8E25D",  # Lima suave
  "#A8D08D",  # Verde pastel
  "#7AC36A",  # Verde hoja
  "#4CAF50",  # Verde medio
  "#40C4FF",  # Celeste vibrante
  "#00B0F0",  # Celeste profesional
  "#3399FF",  # Celeste más oscuro
  "#1E88E5",  # Azul Francia
  "#1976D2",  # Azul fuerte
  "#1565C0",  # Azul oscuro
  "#0D47A1"   # Azul muy profundo
]

chartCategoricalColors1 = [
  "#FF8C00",
  "#FFA500",
  "#FFB347",
  "#FFD580",
  "#FFA07A",
  "#FF7F50",
  "#FF6F00",
  "#CC7000",
  "#FFC107",
  "#FFDD57",
  "#E67E22",
  "#D35400",
  "#F39C12",
  "#E67E22",
  "#F4A261"
]

[theme.sidebar]
backgroundColor = "#1E3A5F"
secondaryBackgroundColor = "#1B263B"
headingFontSizes = ["1.6rem", "1.4rem", "1.2rem"]
dataframeHeaderBackgroundColor = "#1A2A40"

---------------------------------------------------------------------------------------------------------------------------------------------

Real Time Stock Dashboard

Este proyecto es un dashboard interactivo de acciones en tiempo real construido con Streamlit y Plotly, que permite consultar cotizaciones de acciones, visualizar gráficos históricos, calcular métricas financieras y mostrar indicadores técnicos como SMA, EMA, RSI, MACD, Bollinger Bands y Stochastic Oscillator.

El dashboard se conecta a Stooq.com para obtener los datos históricos de acciones y proporciona una interfaz visual intuitiva para el análisis técnico.

Características

Consultas de cotizaciones rápidas para varios símbolos de acciones.

Gráficos interactivos en candlestick o línea.

Cálculo y visualización de indicadores técnicos:

SMA 20

EMA 20

RSI 14

MACD

Bollinger Bands

Stochastic Oscillator

Métricas clave de las acciones:

Último precio

Cambio absoluto y porcentual

Máximo y mínimo

Volumen

Tablas interactivas de datos históricos y métricas técnicas.

Oculta la barra lateral para maximizar el área del dashboard.

Tecnologías utilizadas

Python 3.10+

Streamlit
 – Para la interfaz web.

Plotly
 – Para gráficos interactivos.

Pandas
 – Para manipulación de datos.

TA-Lib / ta
 – Para indicadores técnicos.

Datetime
 – Manejo de fechas y períodos.

git clone [https://github.com/wgekko/stock-dashboard.git]
cd stock-dashboard

video demo 

https://github.com/user-attachments/assets/65404060-5a68-4915-a672-aaaf188a919e








