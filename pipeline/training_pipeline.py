import os
import sys

from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessing
from src.model_training import ModelTrainer

from config.paths_config import *
from src.logger import logging
from src.exception import CustomException

if __name__ == "__main__":
    try:
        logging.info("Starting the training pipeline")

        # Step 1: Data Ingestion
        data_ingestion = DataIngestion(config=CONFIG_PATH)
        data_ingestion.download_csv_from_gcp()

        # Step 2: Data Processing
        data_processor = DataProcessing(input_file=RAW_DATA_FILE_PATH, output_path=TRANSFORMED_DATA_DIR)
        data_processor.save_data()

        # Step 3: Model Training
        model_trainer = ModelTrainer(input_path=TRANSFORMED_DATA_DIR, output_path=MODEL_DIR)
        model_trainer.save_model()

        logging.info("Training pipeline completed successfully")

    except Exception as e:
        logging.error(f"Error in training pipeline: {e}")
        raise CustomException(e, sys)
