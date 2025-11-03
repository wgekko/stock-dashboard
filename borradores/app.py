import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import ta

# ============================
# FUNCIÓN: Descargar datos
# ============================
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

        # Calcular fechas según período
        end_date = datetime.now()
        periods = {'5d': 5, '1mo': 30, '3mo': 90, '6mo': 180, '1y': 365}
        days = periods.get(period, 9000)  # "max" = 9000 días
        start_date = end_date - timedelta(days=days)
        data = data[data.index >= start_date]

        return data

    except Exception as e:
        st.error(f"Error al descargar datos para {ticker}: {e}")
        return pd.DataFrame()


# ============================
# FUNCIÓN: Procesar datos
# ============================
def process_data(data):
    if data.empty:
        return data
    data.index = pd.to_datetime(data.index).tz_localize('UTC').tz_convert('US/Eastern')
    data.reset_index(inplace=True)
    data.rename(columns={'Date': 'Datetime'}, inplace=True)
    return data


# ============================
# FUNCIÓN: Calcular métricas
# ============================
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


# ============================
# FUNCIÓN: Indicadores técnicos
# ============================
def add_technical_indicators(data):
    if data.empty:
        return data

    # SMA y EMA
    data['SMA_20'] = ta.trend.sma_indicator(data['Close'], window=20)
    data['EMA_20'] = ta.trend.ema_indicator(data['Close'], window=20)

    # RSI
    data['RSI_14'] = ta.momentum.rsi(data['Close'], window=14)

    # MACD
    macd = ta.trend.MACD(data['Close'])
    data['MACD'] = macd.macd()
    data['MACD_Signal'] = macd.macd_signal()
    data['MACD_Hist'] = macd.macd_diff()

    # Bollinger Bands
    boll = ta.volatility.BollingerBands(data['Close'], window=20, window_dev=2)
    data['BB_High'] = boll.bollinger_hband()
    data['BB_Low'] = boll.bollinger_lband()

    # Stochastic Oscillator
    stochastic = ta.momentum.StochasticOscillator(
        high=data['High'], 
        low=data['Low'], 
        close=data['Close'], 
        window=14, 
        smooth_window=3
    )
    data['Stoch_%K'] = stochastic.stoch()
    data['Stoch_%D'] = stochastic.stoch_signal()

    return data


# ============================
# LAYOUT PRINCIPAL STREAMLIT
# ============================
st.set_page_config(page_title="Stock Dashboard", page_icon=":material/finance_mode:"  , layout="wide")
st.title(':material/finance: Real Time Stock Dashboard')

# ====== TARJETAS DE COTIZACIONES ======
st.subheader("Cotizaciones rápidas del mercado")

stock_symbols = ['AAPL', 'GOOGL', 'JPM', 'NVDA']
cols = st.columns(4)

for i, symbol in enumerate(stock_symbols):
    symbol_stooq = symbol + '.US'
    real_time_data = fetch_stock_data(symbol_stooq, '5d')
    if not real_time_data.empty:
        real_time_data = process_data(real_time_data)
        last_price = round(real_time_data['Close'].iloc[-1], 2)
        change = round(last_price - real_time_data['Open'].iloc[0], 2)
        pct_change = round((change / real_time_data['Open'].iloc[0]) * 100, 2)
        color = "green" if change > 0 else "red" if change < 0 else "gray"

        with cols[i]:
                st.markdown(
                    f"""
                        <div style="background-color:#1E362F;
                            border:1px solid #555;
                            padding:10px 10px; /* menos padding */
                            border-radius:6px;
                            text-align:center;
                            width:100%;
                            max-width:250px; /* más angosta */
                            margin:auto;
                            box-shadow:0px 0px 3px rgba(0,0,0,0.2);">
                            <h4 style="margin-bottom:2px; font-size:14px;">{symbol}</h4>
                            <h3 style="margin:0; font-size:16px;">${last_price}</h3>
                            <p style="color:{color}; font-weight:600; margin-top:2px; font-size:12px;">
                            {change:+.2f} ({pct_change:+.2f}%)
                            </p>
                        </div>
                    """,
                    unsafe_allow_html=True
                )

            
# ====== INFO FINAL ======
#st.sidebar.subheader('ℹ️ Acerca de')
#st.sidebar.info(
#    'Dashboard financiero de acciones de EE.UU.\n\n'
#    'Datos obtenidos de Stooq (actualizados diariamente).'
#)
