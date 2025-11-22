# E-commerce Sales Forecasting Pipeline

> [!NOTE]
> 🇪🇸 **[Leer en Español](README.md)**

## Overview
This project implements an end-to-end data pipeline for e-commerce sales forecasting. It generates synthetic transactional data, processes it into a time-series format, trains a Machine Learning model (Random Forest), and visualizes the results in an interactive dashboard.

The goal is to demonstrate a modern, lightweight data engineering and data science workflow using Python.

## Architecture
The pipeline consists of four main stages:

1.  **Data Generation**: Creates realistic synthetic data for products, customers, and sales transactions using `Faker`.
2.  **Ingestion**: Loads raw CSV data into a **DuckDB** analytical database.
3.  **Processing**: Aggregates transactional data into daily sales figures and performs feature engineering (lags, rolling means).
4.  **Modeling**: Trains a **RandomForestRegressor** (Scikit-learn) to predict future sales and generates a 30-day forecast.
5.  **Visualization**: Presents historical data and forecasts via a **Streamlit** dashboard.

## Tech Stack
-   **Language**: Python 3.10+
-   **Database**: DuckDB (In-process SQL OLAP database)
-   **Data Processing**: Pandas, NumPy
-   **Machine Learning**: Scikit-learn
-   **Dashboard**: Streamlit
-   **Visualization**: Matplotlib

## Project Structure
```
├── data/               # Data storage (raw CSVs and DuckDB database)
├── src/
│   ├── generator.py    # Synthetic data generator
│   ├── ingestion.py    # Data loading and schema creation
│   ├── processing.py   # Feature engineering and aggregation
│   ├── model.py        # ML model training and inference
│   └── dashboard.py    # Streamlit application
├── main.py             # Pipeline orchestrator
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## Setup and Usage

### 1. Installation
Clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd data_pipeline_project
pip install -r requirements.txt
```

### 2. Run the Pipeline
Execute the full data pipeline (generation -> ingestion -> processing -> modeling):

```bash
python3 main.py
```

### 3. Launch Dashboard
Start the interactive dashboard to view the results:

```bash
streamlit run src/dashboard.py
```

## Credits
Developed by **Jose Colomina Alvarez**.
