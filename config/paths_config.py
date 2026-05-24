import os

###################################### DATA INGESTION RELATED PATHS ######################################
RAW_DATA_DIR = os.path.join("artifacts", "raw_data")
RAW_DATA_FILE_PATH = os.path.join(RAW_DATA_DIR, "data.csv")

CONFIG_PATH = os.path.join("config", "config.yaml")

###################################### DATA TRANSFORMATION RELATED PATHS ######################################
TRANSFORMED_DATA_DIR = os.path.join("artifacts", "transformed_data")

X_TRAIN_PATH = os.path.join(TRANSFORMED_DATA_DIR, "X_train.csv")
X_TEST_PATH = os.path.join(TRANSFORMED_DATA_DIR, "X_test.csv")
Y_TRAIN_PATH = os.path.join(TRANSFORMED_DATA_DIR, "y_train.csv")
Y_TEST_PATH = os.path.join(TRANSFORMED_DATA_DIR, "y_test.csv")

LABEL_ENCODER_FILE_PATH = os.path.join(TRANSFORMED_DATA_DIR, "label_encoder.pkl")
SCALER_FILE_PATH = os.path.join(TRANSFORMED_DATA_DIR, "scaler.pkl")


