import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import ta

# Descargar datos desde Stooq (CSV público)
def fetch_stock_data(ticker, period):
    try:
        url = f"https://stooq.com/q/d/l/?s={ticker.lower()}&i=d"
        data = pd.read_csv(url)

        if data.empty:
            st.warning(f"No se encontraron datos para {ticker} en Stooq.")
            return pd.DataFrame()

        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        data = data.sort_index()

        # Filtrar según el período seleccionado
        end_date = datetime.now()
        if period == '5d':
            start_date = end_date - timedelta(days=5)
        elif period == '1mo':
            start_date = end_date - timedelta(days=30)
        elif period == '3mo':
            start_date = end_date - timedelta(days=90)
        elif period == '6mo':
            start_date = end_date - timedelta(days=180)
        elif period == '1y':
            start_date = end_date - timedelta(days=365)
        else:
            start_date = datetime(2000, 1, 1)

        data = data[data.index >= start_date]

        return data

    except Exception as e:
        st.error(f"Error al descargar datos para {ticker}: {e}")
        return pd.DataFrame()


# Procesar datos y añadir zona horaria
def process_data(data):
    if data.empty:
        return data
    data.index = pd.to_datetime(data.index).tz_localize('UTC').tz_convert('US/Eastern')
    data.reset_index(inplace=True)
    data.rename(columns={'Date': 'Datetime'}, inplace=True)
    return data


# Calcular métricas básicas
def calculate_metrics(data):
    if data.empty:
        return 0, 0, 0, 0, 0, 0
    last_close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[0]
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100 if prev_close != 0 else 0
    high = data['High'].max()
    low = data['Low'].min()
    volume = data['Volume'].sum() if 'Volume' in data.columns else 0
    return last_close, change, pct_change, high, low, volume


# Añadir indicadores técnicos
def add_technical_indicators(data):
    if data.empty:
        return data
    data['SMA_20'] = ta.trend.sma_indicator(data['Close'], window=20)
    data['EMA_20'] = ta.trend.ema_indicator(data['Close'], window=20)

    # Reemplazar valores NaN por “—” para evitar que se muestren como None
    data['SMA_20'] = data['SMA_20'].fillna('—')
    data['EMA_20'] = data['EMA_20'].fillna('—')
    return data


###############################################
## PART 2: Layout principal de la aplicación ##
###############################################

st.set_page_config(layout="wide")
st.title('📈 Real Time Stock Dashboard (Fuente: Stooq)')

# ====== NUEVO BLOQUE: Tarjetas de cotizaciones rápidas ======
st.subheader("💹 Cotizaciones rápidas del mercado (Stooq)")

# Lista de símbolos predefinidos
stock_symbols = ['AAPL', 'GOOGL', 'MELI', 'NVDA']

# Mostrar las “cards” en 4 columnas
cols = st.columns(4)
for i, symbol in enumerate(stock_symbols):
    symbol_stooq = symbol + '.US'
    real_time_data = fetch_stock_data(symbol_stooq, '5d')
    if not real_time_data.empty:
        real_time_data = process_data(real_time_data)
        last_price = round(real_time_data['Close'].iloc[-1], 2)
        change = round(last_price - real_time_data['Open'].iloc[0], 2)
        pct_change = round((change / real_time_data['Open'].iloc[0]) * 100, 2)

        # Color según si sube o baja
        color = "green" if change > 0 else "red" if change < 0 else "gray"

        # Mostrar tarjeta estilizada
        with cols[i]:
            st.markdown(
                f"""
                <div style="background-color:#1E362F;border:1px solid #DDD;padding:15px;
                            border-radius:10px;text-align:center;box-shadow:1px 1px 4px rgba(0,0,0,0.1);">
                    <h4 style="margin-bottom:5px;">{symbol}</h4>
                    <h3 style="margin:0;">${last_price}</h3>
                    <p style="color:{color};font-weight:bold;margin-top:5px;">
                        {change:+.2f} ({pct_change:+.2f}%)
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

st.divider()  # Línea separadora

# ====== SIDEBAR ======
st.sidebar.header(':material/finance_mode:Parámetros del gráfico')

# Entrada del ticker y agregado automático de ".US"
ticker_input = st.sidebar.text_input('Ticker', 'ADBE').upper()
ticker = ticker_input + '.US' if not ticker_input.endswith('.US') else ticker_input

# Parámetros adicionales
time_period = st.sidebar.selectbox(
    'Período de tiempo',
    ['5d', '1mo', '3mo', '6mo', '1y', 'max']
)
chart_type = st.sidebar.selectbox('Tipo de gráfico', ['Candlestick', 'Line'])
indicators = st.sidebar.multiselect('Indicadores técnicos', ['SMA 20', 'EMA 20'])

# ====== BOTÓN PRINCIPAL ======
if st.sidebar.button('Actualizar'):
    data = fetch_stock_data(ticker, time_period)
    data = process_data(data)
    data = add_technical_indicators(data)

    if not data.empty:
        last_close, change, pct_change, high, low, volume = calculate_metrics(data)

        # Mostrar métricas principales
        st.metric(label=f"{ticker} Último Precio", value=f"{last_close:.2f} USD", delta=f"{change:.2f} ({pct_change:.2f}%)")

        col1, col2, col3 = st.columns(3)
        col1.metric("Máximo", f"{high:.2f} USD")
        col2.metric("Mínimo", f"{low:.2f} USD")
        col3.metric("Volumen", f"{volume:,.0f}")

        # Crear gráfico
        fig = go.Figure()
        if chart_type == 'Candlestick':
            fig.add_trace(go.Candlestick(
                x=data['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Precio'
            ))
        else:
            fig = px.line(data, x='Datetime', y='Close', title=f"{ticker} Price Chart")

        # Añadir indicadores técnicos
        for indicator in indicators:
            if indicator == 'SMA 20':
                fig.add_trace(go.Scatter(x=data['Datetime'], y=data['SMA_20'], name='SMA 20', line=dict(color='blue')))
            elif indicator == 'EMA 20':
                fig.add_trace(go.Scatter(x=data['Datetime'], y=data['EMA_20'], name='EMA 20', line=dict(color='orange')))

        # Formato del gráfico
        fig.update_layout(
            title=f'{ticker} ({time_period})',
            xaxis_title='Fecha',
            yaxis_title='Precio (USD)',
            height=600,
            xaxis_rangeslider_visible=False
        )

        # Mostrar gráfico con nuevo parámetro moderno
        st.plotly_chart(fig, width='stretch')

        # Mostrar tablas de datos
        st.subheader('📄 Datos Históricos')
        st.dataframe(data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']])

        st.subheader('📈 Indicadores Técnicos')
        st.dataframe(data[['Datetime', 'SMA_20', 'EMA_20']])

# ====== INFO FINAL ======
st.sidebar.subheader('Acerca de')
st.sidebar.info('Dashboard financiero de acciones de EE.UU.\n\nLos tickers están en tiempo real desde Stooq.')


