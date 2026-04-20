import os
import sys
import pandas as pd
from google.cloud import storage

from config.paths_config import *
from utils.common_functions import read_yaml

from src.logger import logging
from src.exception import CustomException

class DataIngestion:
    def __init__(self, config):
        self.config = read_yaml(config)
        self.data_ingestion_config = self.config["data_ingestion"]
        self.bucket_name = self.data_ingestion_config["bucket_name"]
        self.file_name = self.data_ingestion_config["bucket_file_name"]

        os.makedirs(RAW_DATA_DIR, exist_ok=True)

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)

            blob.download_to_filename(RAW_DATA_FILE_PATH)

            logging.info(f"Raw file is succesfully downloaded to the file location: {RAW_DATA_FILE_PATH}")

        except Exception as e:
            logging.error("Error while downloading the csv file")
            CustomException(e, sys)


if __name__ == "__main__":
    data_ingestion = DataIngestion(config=CONFIG_PATH)
    data_ingestion.download_csv_from_gcp()
