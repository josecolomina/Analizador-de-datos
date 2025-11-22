import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.set_page_config(page_title="E-commerce Sales Forecast", layout="wide")

DB_PATH = 'data/ecommerce.db'

@st.cache_data
def load_data():
    con = duckdb.connect(DB_PATH, read_only=True)
    df = con.execute("SELECT * FROM forecasts ORDER BY ds").fetchdf()
    con.close()
    return df

def main():
    st.title("📊 Dashboard de Predicción de Ventas by Jose Colomina Alvarez")
    st.markdown("Visualización de ventas históricas y predicción a 30 días usando Machine Learning.")
    

    df = load_data()
    
    # KPIs
    history = df[df['type'] == 'history']
    forecast = df[df['type'] == 'forecast']
    
    last_30_days_sales = history.iloc[-30:]['y_pred'].sum()
    predicted_30_days_sales = forecast['y_pred'].sum()
    growth = ((predicted_30_days_sales - last_30_days_sales) / last_30_days_sales) * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Ventas Últimos 30 Días", f"€{last_30_days_sales:,.2f}")
    col2.metric("Predicción Próximos 30 Días", f"€{predicted_30_days_sales:,.2f}", f"{growth:.1f}%")
    col3.metric("Días Predichos", len(forecast))
    
    # Gráfica con Matplotlib (Requerimiento del usuario)
    st.subheader("Tendencia de Ventas y Predicción")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot historia
    ax.plot(history['ds'], history['y_pred'], label='Histórico', color='#1f77b4', alpha=0.7)
    
    # Plot predicción
    ax.plot(forecast['ds'], forecast['y_pred'], label='Predicción', color='#ff7f0e', linestyle='--', linewidth=2)
    
    # Formato
    ax.set_title('Ventas Diarias: Histórico vs Predicción')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Ventas (€)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Formato de fechas
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)
    
    st.pyplot(fig)
    
    # Tabla de datos recientes
    st.subheader("Datos Recientes y Predicciones")
    st.dataframe(df.tail(60).sort_values('ds', ascending=False))

if __name__ == "__main__":
    main()
