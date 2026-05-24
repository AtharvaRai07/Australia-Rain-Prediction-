import os
import sys
import pandas as pd
import numpy as np
import joblib
from pyparsing import col
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from utils.common_functions import read_yaml
from config.paths_config import *
from src.logger import logging
from src.exception import CustomException

class DataProcessing:
    def __init__(self, input_file: str, output_path: str):

        self.input_file = input_file
        self.output_path = output_path

        self.config = read_yaml(CONFIG_PATH)
        self.test_size = self.config['data_preprocessing']['test_size']
        self.random_state = self.config['data_preprocessing']['random_state']
        self.target_column = self.config['data_preprocessing']['target_column']

        os.makedirs(self.output_path, exist_ok=True)

    def load_data(self):
        try:
            logging.info(f"Loading data from {self.input_file}")
            data = pd.read_csv(self.input_file)
            logging.info(f"Data loaded successfully with shape {data.shape}")
            return data
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise CustomException(e, sys)

    def preprocess_data(self, df: pd.DataFrame):
        try:
            logging.info("Preprocessing data")

            df['Date'] = pd.to_datetime(df['Date'])
            df['Year'] = df['Date'].dt.year
            df['Month'] = df['Date'].dt.month
            df['Day'] = df['Date'].dt.day

            df.drop('Date', axis=1, inplace=True)

            cat_cols = [col for col in df.columns if df[col].dtype == 'str']
            num_cols = [col for col in df.columns if col not in cat_cols]

            for col in num_cols:
                df[col] = df[col].fillna(df[col].mean())

            df.dropna(inplace=True)

            logging.info("Data preprocessing completed successfully")
            return df

        except Exception as e:
            logging.error(f"Error preprocessing data: {e}")
            raise CustomException(e, sys)

    def label_encode(self, df: pd.DataFrame):
        try:
            logging.info("Label encoding categorical columns")

            cat_cols = [col for col in df.columns if df[col].dtype == 'str']
            label_encoders = {}
            for col in cat_cols:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                label_encoders[col] = le
                label_mapping = dict(zip(le.classes_, le.transform(le.classes_)))

            logging.info(f"Label encoding mappings: {label_mapping}")

            logging.info("Label encoding completed successfully")
            return df, label_encoders

        except Exception as e:
            logging.error(f"Error in label encoding: {e}")
            raise CustomException(e, sys)


    def split_data(self, df: pd.DataFrame, target_col: str):
        try:
            logging.info("Splitting data into train and test sets")

            X = df.drop(target_col, axis=1)
            y = df[target_col]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size, random_state=self.random_state)

            logging.info(f"Data split completed successfully with train shape {X_train.shape} and test shape {X_test.shape}")
            return X_train, X_test, y_train, y_test

        except Exception as e:
            logging.error(f"Error splitting data: {e}")
            raise CustomException(e, sys)

    def save_data(self):
        try:
            logging.info("Saving preprocessed data")

            data = self.load_data()
            preprocessed_data = self.preprocess_data(data)
            encoded_data, label_encoders = self.label_encode(preprocessed_data)
            X_train, X_test, y_train, y_test = self.split_data(encoded_data, self.target_column)

            X_train.to_csv(X_TRAIN_PATH, index=False)
            X_test.to_csv(X_TEST_PATH, index=False)
            y_train.to_csv(Y_TRAIN_PATH, index=False)
            y_test.to_csv(Y_TEST_PATH, index=False)

            joblib.dump(label_encoders, LABEL_ENCODER_FILE_PATH)

        except Exception as e:
            logging.error(f"Error saving data: {e}")
            raise CustomException(e, sys)


if __name__ == "__main__":
    try:
        data_processor = DataProcessing(input_file=RAW_DATA_FILE_PATH, output_path=TRANSFORMED_DATA_DIR)
        data_processor.save_data()
    except Exception as e:
        logging.error(f"Error in data processing: {e}")
        raise CustomException(e, sys)
