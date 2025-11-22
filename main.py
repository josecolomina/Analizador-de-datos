import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def run_step(step_name: str, command: list):
    """
    Executes a pipeline step as a subprocess.
    
    Args:
        step_name (str): Name of the step for logging.
        command (list): Command to execute as a list of strings.
    """
    logger.info(f"{'='*50}")
    logger.info(f"Starting Step: {step_name}")
    logger.info(f"{'='*50}")
    
    try:
        subprocess.run(command, check=True)
        logger.info(f"Step '{step_name}' completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing {step_name}: {e}")
        sys.exit(1)

def main():
    """
    Main pipeline execution controller.
    Orchestrates the data generation, ingestion, processing, and modeling steps.
    """
    steps = [
        ("Data Generation", ["python3", "src/generator.py"]),
        ("Data Ingestion", ["python3", "src/ingestion.py"]),
        ("Feature Engineering", ["python3", "src/processing.py"]),
        ("Model Training & Forecasting", ["python3", "src/model.py"])
    ]

    for step_name, command in steps:
        run_step(step_name, command)

    logger.info("\nPipeline execution finished successfully.")
    print("\nTo launch the dashboard, run: streamlit run src/dashboard.py")

if __name__ == "__main__":
    main()
