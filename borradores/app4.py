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
st.set_page_config(page_title="Stock Dashboard", layout="wide")
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

            
            #st.markdown(
            #    f"""
            #"""    <div style="background-color:#1E362F;border:1px solid #DDD;padding:15px;
            #                border-radius:10px;text-align:center;box-shadow:1px 1px 4px rgba(0,0,0,0.1);">
            #        <h5 style="margin-bottom:5px;">{symbol}</h5>
            #        <h4 style="margin:0;">${last_price}</h4>
            #        <p style="color:{color};font-weight:bold;margin-top:5px;">
            #            {change:+.2f} ({pct_change:+.2f}%)
            #        </p>
            #    </div>
            #    """,
            #    unsafe_allow_html=True
            #    )
            

st.divider()
# ====== CONTROLES EN EL CUERPO PRINCIPAL ======
st.subheader(":material/settings_applications: Parámetros del gráfico")

with st.container(border=True):
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        ticker_input = st.text_input('Ticker', 'AMD').upper()
        ticker = ticker_input + '.US' if not ticker_input.endswith('.US') else ticker_input

    with col2:
        time_period = st.selectbox(
            'Período de tiempo',
            ['5d', '1mo', '3mo', '6mo', '1y', 'max']
        )

    with col3:
        chart_type = st.selectbox(
            'Tipo de gráfico',
            ['Candlestick', 'Line']
        )

    col1, col2 = st.columns([3, 1])
    with col1:
        indicators = st.multiselect(
            'Indicadores técnicos',
            ['SMA 20', 'EMA 20', 'RSI 14', 'MACD', 'Bollinger Bands', 'Stochastic Oscillator']
        )

    with col2:
        st.write("")  
        st.write("") 
        actualizar = st.button('Actualizar', use_container_width=True)

# ====== LÓGICA PRINCIPAL ======
if actualizar:
    data = fetch_stock_data(ticker, time_period)
    data = process_data(data)
    data = add_technical_indicators(data)

    if data.empty:
        st.warning("No hay datos para mostrar.")
        st.stop()

    # Columna con fecha formateada para mostrar
    data['Datetime_str'] = data['Datetime'].dt.strftime('%d/%m/%Y')

    last_close, change, pct_change, high, low, volume = calculate_metrics(data)

    # Mostrar métricas principales
    st.metric(
        label=f"{ticker} Último Precio",
        value=f"{last_close:.2f} USD",
        delta=f"{change:.2f} ({pct_change:.2f}%)"
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Máximo", f"{high:.2f} USD")
    col2.metric("Mínimo", f"{low:.2f} USD")
    col3.metric("Volumen", f"{volume:,.0f}")


# ====== SIDEBAR ======
#st.sidebar.header(':material/settings_applications: Parámetros del gráfico')

#ticker_input = st.sidebar.text_input('Ticker', 'AMD').upper()
#ticker = ticker_input + '.US' if not ticker_input.endswith('.US') else ticker_input

#time_period = st.sidebar.selectbox('Período de tiempo', ['5d', '1mo', '3mo', '6mo', '1y', 'max'])
#chart_type = st.sidebar.selectbox('Tipo de gráfico', ['Candlestick', 'Line'])

#indicators = st.sidebar.multiselect(
#    'Indicadores técnicos',
#    ['SMA 20', 'EMA 20', 'RSI 14', 'MACD', 'Bollinger Bands', 'Stochastic Oscillator']
#)

# ====== BOTÓN PRINCIPAL ======
#if st.sidebar.button('Actualizar'):
#    data = fetch_stock_data(ticker, time_period)
#    data = process_data(data)
#    data = add_technical_indicators(data)

#    if data.empty:
#        st.warning("No hay datos para mostrar.")
#        st.stop()

    # Columna con fecha formateada para mostrar
#    data['Datetime_str'] = data['Datetime'].dt.strftime('%d/%m/%Y')

#    last_close, change, pct_change, high, low, volume = calculate_metrics(data)

    # Mostrar métricas principales
#    st.metric(label=f"{ticker} Último Precio", value=f"{last_close:.2f} USD",
#              delta=f"{change:.2f} ({pct_change:.2f}%)")

#    col1, col2, col3 = st.columns(3)
#    col1.metric("Máximo", f"{high:.2f} USD")
#    col2.metric("Mínimo", f"{low:.2f} USD")
#    col3.metric("Volumen", f"{volume:,.0f}")

    # ====== GRÁFICO PRINCIPAL ======
#    fig = go.Figure()

#    if chart_type == 'Candlestick':
#        fig.add_trace(go.Candlestick(
#            x=data['Datetime'],
#            open=data['Open'],
#            high=data['High'],
#            low=data['Low'],
#            close=data['Close'],
#            name='Precio'
#        ))
#    else:
#        fig = px.line(data, x='Datetime', y='Close', title=f"{ticker} Price Chart")

    # Añadir indicadores técnicos
#    for indicator in indicators:
#        if indicator == 'SMA 20':
#            fig.add_trace(go.Scatter(x=data['Datetime'], y=data['SMA_20'], name='SMA 20', line=dict(color='blue')))
#        elif indicator == 'EMA 20':
#            fig.add_trace(go.Scatter(x=data['Datetime'], y=data['EMA_20'], name='EMA 20', line=dict(color='orange')))
#        elif indicator == 'Bollinger Bands':
#            fig.add_trace(go.Scatter(x=data['Datetime'], y=data['BB_High'], name='BB Superior', line=dict(color='gray', dash='dot')))
#            fig.add_trace(go.Scatter(x=data['Datetime'], y=data['BB_Low'], name='BB Inferior', line=dict(color='gray', dash='dot')))

#    fig.update_layout(
#        title=f'{ticker} ({time_period})',
#        xaxis_title='Fecha',
#        yaxis_title='Precio (USD)',
#        height=600,
#        xaxis_rangeslider_visible=False
#    )

#    st.plotly_chart(fig, config={"responsive": True})

    # ====== SUBGRÁFICOS RSI y MACD ======
    if 'RSI 14' in indicators:
        fig_rsi = px.line(data, x='Datetime', y='RSI_14', title='RSI (14)')
        fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
        fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
        st.plotly_chart(fig_rsi, config={"responsive": True})

    if 'MACD' in indicators:
        fig_macd = go.Figure()
        fig_macd.add_trace(go.Scatter(x=data['Datetime'], y=data['MACD'], name='MACD', line=dict(color='blue')))
        fig_macd.add_trace(go.Scatter(x=data['Datetime'], y=data['MACD_Signal'], name='Señal', line=dict(color='orange')))
        fig_macd.add_trace(go.Bar(x=data['Datetime'], y=data['MACD_Hist'], name='Histograma', marker_color='gray'))
        fig_macd.update_layout(title='MACD', height=300)
        st.plotly_chart(fig_macd, config={"responsive": True})

    # ====== SUBGRÁFICO STOCHASTIC OSCILLATOR ======
    if 'Stochastic Oscillator' in indicators:
        fig_stoch = go.Figure()
        fig_stoch.add_trace(go.Scatter(
            x=data['Datetime'], y=data['Stoch_%K'], name='%K', line=dict(color='blue')
        ))
        fig_stoch.add_trace(go.Scatter(
            x=data['Datetime'], y=data['Stoch_%D'], name='%D', line=dict(color='orange')
        ))
        fig_stoch.add_hline(y=80, line_dash="dash", line_color="red")
        fig_stoch.add_hline(y=20, line_dash="dash", line_color="green")
        fig_stoch.update_layout(title='Stochastic Oscillator', height=300)
        st.plotly_chart(fig_stoch, config={"responsive": True})

    # ====== TABLAS ORDENADAS (más reciente primero) ======
    data_sorted = data.sort_values(by='Datetime', ascending=False)

    st.subheader(':material/database_search: Datos Históricos')
    st.dataframe(
        data_sorted[['Datetime_str', 'Open', 'High', 'Low', 'Close', 'Volume']],
        width='stretch' #use_container_width=True
    )

    st.subheader(':material/analytics: Indicadores Técnicos')
    st.dataframe(
        data_sorted[['Datetime_str', 'SMA_20', 'EMA_20', 'RSI_14', 'MACD',
                     'MACD_Signal', 'BB_High', 'BB_Low', 'Stoch_%K', 'Stoch_%D']],
        width='stretch' #use_container_width=True
    )

# ====== INFO FINAL ======
#st.sidebar.subheader('ℹ️ Acerca de')
#st.sidebar.info(
#    'Dashboard financiero de acciones de EE.UU.\n\n'
#    'Datos obtenidos de Stooq (actualizados diariamente).'
#)
