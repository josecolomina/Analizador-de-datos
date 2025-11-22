# Pipeline de Predicción de Ventas E-commerce

> [!NOTE]
> 🇺🇸 **[Read in English](README_en.md)**

## Descripción General
Este proyecto implementa un pipeline de datos "end-to-end" para la predicción de ventas en comercio electrónico. Genera datos transaccionales sintéticos, los procesa en formato de series temporales, entrena un modelo de Machine Learning (Random Forest) y visualiza los resultados en un dashboard interactivo.

El objetivo es demostrar un flujo de trabajo moderno y ligero de ingeniería de datos y ciencia de datos utilizando Python.

## Arquitectura
El pipeline consta de cuatro etapas principales:

1.  **Generación de Datos**: Crea datos sintéticos realistas para productos, clientes y transacciones de ventas utilizando `Faker`.
2.  **Ingesta**: Carga datos CSV crudos en una base de datos analítica **DuckDB**.
3.  **Procesamiento**: Agrega datos transaccionales en cifras de ventas diarias y realiza ingeniería de características (lags, medias móviles).
4.  **Modelado**: Entrena un **RandomForestRegressor** (Scikit-learn) para predecir ventas futuras y genera un pronóstico de 30 días.
5.  **Visualización**: Presenta datos históricos y pronósticos a través de un dashboard de **Streamlit**.

## Stack Tecnológico
-   **Lenguaje**: Python 3.10+
-   **Base de Datos**: DuckDB (Base de datos SQL OLAP en proceso)
-   **Procesamiento de Datos**: Pandas, NumPy
-   **Machine Learning**: Scikit-learn
-   **Dashboard**: Streamlit
-   **Visualización**: Matplotlib

## Estructura del Proyecto
```
├── data/               # Almacenamiento de datos (CSVs crudos y base de datos DuckDB)
├── src/
│   ├── generator.py    # Generador de datos sintéticos
│   ├── ingestion.py    # Carga de datos y creación de esquema
│   ├── processing.py   # Ingeniería de características y agregación
│   ├── model.py        # Entrenamiento e inferencia del modelo ML
│   └── dashboard.py    # Aplicación Streamlit
├── main.py             # Orquestador del pipeline
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación del proyecto
```

## Configuración y Uso

### 1. Instalación
Clona el repositorio e instala las dependencias requeridas:

```bash
git clone <url-del-repositorio>
cd data_pipeline_project
pip install -r requirements.txt
```

### 2. Ejecutar el Pipeline
Ejecuta el pipeline de datos completo (generación -> ingesta -> procesamiento -> modelado):

```bash
python3 main.py
```

### 3. Lanzar el Dashboard
Inicia el dashboard interactivo para ver los resultados:

```bash
streamlit run src/dashboard.py
```

## Créditos
Desarrollado por **Jose Colomina Alvarez**.
