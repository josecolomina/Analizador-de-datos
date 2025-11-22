import os
import sys

def run_step(step_name, command):
    print(f"\n{'='*50}")
    print(f"Ejecutando: {step_name}")
    print(f"{'='*50}")
    ret = os.system(command)
    if ret != 0:
        print(f"Error en {step_name}. Abortando.")
        sys.exit(1)

def main():
    # 1. Generación (si no existen datos o se fuerza)
    # Para este demo, siempre generamos para tener datos frescos
    run_step("Generación de Datos", "python3 src/generator.py")
    
    # 2. Ingesta
    run_step("Ingesta a DuckDB", "python3 src/ingestion.py")
    
    # 3. Procesamiento
    run_step("Procesamiento y Features", "python3 src/processing.py")
    
    # 4. Modelado
    run_step("Entrenamiento y Predicción", "python3 src/model.py")
    
    print("\nPipeline completado exitosamente.")
    print("Para ver el dashboard, ejecuta: streamlit run src/dashboard.py")

if __name__ == "__main__":
    main()
