import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = 'data/ecommerce.db'

st.set_page_config(page_title="E-commerce Sales Forecast", layout="wide")

@st.cache_data
def load_data() -> pd.DataFrame:
    """
    Loads forecast data from DuckDB.
    
    Returns:
        pd.DataFrame: DataFrame containing historical and forecasted sales.
    """
    try:
        con = duckdb.connect(DB_PATH, read_only=True)
        df = con.execute("SELECT * FROM forecasts ORDER BY ds").fetchdf()
        con.close()
        return df
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        st.error("Error loading data from database.")
        return pd.DataFrame()

def main():
    """
    Main function to render the Streamlit dashboard.
    """
    st.title("📊 Dashboard de Predicción de Ventas by Jose Colomina Alvarez")
    st.markdown("Visualización de ventas históricas y predicción a 30 días usando Machine Learning.")
    
    df = load_data()
    
    if df.empty:
        return
    
    # KPI Calculation
    history = df[df['type'] == 'history']
    forecast = df[df['type'] == 'forecast']
    
    last_30_days_sales = history.iloc[-30:]['y_pred'].sum()
    predicted_30_days_sales = forecast['y_pred'].sum()
    growth = ((predicted_30_days_sales - last_30_days_sales) / last_30_days_sales) * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Ventas Últimos 30 Días", f"€{last_30_days_sales:,.2f}")
    col2.metric("Predicción Próximos 30 Días", f"€{predicted_30_days_sales:,.2f}", f"{growth:.1f}%")
    col3.metric("Días Predichos", len(forecast))
    
    # Visualization
    st.subheader("Tendencia de Ventas y Predicción")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot history
    ax.plot(history['ds'], history['y_pred'], label='Histórico', color='#1f77b4', alpha=0.7)
    
    # Plot forecast
    ax.plot(forecast['ds'], forecast['y_pred'], label='Predicción', color='#ff7f0e', linestyle='--', linewidth=2)
    
    # Formatting
    ax.set_title('Ventas Diarias: Histórico vs Predicción')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Ventas (€)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Date formatting
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)
    
    st.pyplot(fig)
    
    # Recent Data Table
    st.subheader("Datos Recientes y Predicciones")
    st.dataframe(df.tail(60).sort_values('ds', ascending=False))

if __name__ == "__main__":
    main()
