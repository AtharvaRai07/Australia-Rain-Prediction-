import os
import yaml
import sys
import pandas as pd

from src.logger import logging
from src.exception import CustomException

def read_yaml(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File is not in the give path")

        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            logging.info("Succesfully read the YAML file")
            return config

    except Exception as e:
        logging.error("Error while reading YAML file")
        raise CustomException(str(e), sys)


def read_csv(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File is not in the give path")

        df = pd.read_csv(file_path)
        logging.info("Succesfully read the CSV file")
        return df

    except Exception as e:
        logging.error("Error while reading CSV file")
        raise CustomException(str(e), sys)

def save_csv(df:pd.DataFrame, file_path:str):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        if isinstance(df, pd.DataFrame):
            out_df = df

        elif isinstance(df, pd.Series):
            out_df = df.to_frame()

        else:
            out_df = pd.DataFrame(df)

        out_df.to_csv(file_path, index=False)
        logging.info("Succesfully saved the CSV file")

    except Exception as e:
        logging.error("Error while saving CSV file")
        raise CustomException(str(e), sys)
    

