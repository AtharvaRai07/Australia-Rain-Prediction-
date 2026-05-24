import os
import sys
import joblib
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, classification_report

from config.paths_config import *
from utils.common_functions import read_csv
from src.logger import logging
from src.exception import CustomException

class ModelTrainer:
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path

        os.makedirs(MODEL_DIR, exist_ok=True)

    def load_data(self):
        try:
            logging.info(f"Loading training and testing data from {self.input_path}")

            X_train = read_csv(X_TRAIN_PATH)
            y_train = read_csv(Y_TRAIN_PATH)
            X_test = read_csv(X_TEST_PATH)
            y_test = read_csv(Y_TEST_PATH)

            logging.info("Training data loaded successfully")
            return X_train, y_train, X_test, y_test

        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise CustomException(e, sys)

    def train_model(self, X_train, y_train):
        try:
            logging.info("Training the XGBoost model")

            xgb_clf = XGBClassifier(eval_metric='logloss')
            xgb_clf.fit(X_train, y_train)

            logging.info("Model training completed successfully")
            return xgb_clf

        except Exception as e:
            logging.error(f"Error training model: {e}")
            raise CustomException(e, sys)

    def evaluate_model(self, model, X_test, y_test):
        try:
            logging.info("Evaluating the model on test data")

            y_pred = model.predict(X_test)

            accuarcy = accuracy_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            report = classification_report(y_test, y_pred)

            logging.info(f"Model evaluation completed successfully with accuracy: {accuarcy}, recall: {recall}, precision: {precision}, f1-score: {f1}")
            return accuarcy, recall, precision, f1, report

        except Exception as e:
            logging.error(f"Error evaluating model: {e}")
            raise CustomException(e, sys)

    def save_model(self):
        try:
            logging.info(f"Saving the trained model to {MODEL_FILE_PATH}")

            X_train, y_train, X_test, y_test = self.load_data()
            model = self.train_model(X_train, y_train)
            accuarcy, recall, precision, f1, report = self.evaluate_model(model, X_test, y_test)

            joblib.dump(model, MODEL_FILE_PATH)

            with open(MODEL_TEST_RESULT, "w") as f:
                f.write(f"Accuracy: {accuarcy:.2f}\n")
                f.write(f"Recall: {recall:.2f}\n")
                f.write(f"Precision: {precision:.2f}\n")
                f.write(f"F1 Score: {f1:.2f}\n")
                f.write(f"Classification Report:\n{report}\n")

            logging.info(f"Model saved successfully at {MODEL_FILE_PATH} and evaluation results saved at {MODEL_TEST_RESULT}")

        except Exception as e:
            logging.error(f"Error saving model: {e}")
            raise CustomException(e, sys)


if __name__ == "__main__":
    try:
        model_trainer = ModelTrainer(input_path=TRANSFORMED_DATA_DIR, output_path=MODEL_DIR)
        model_trainer.save_model()

    except Exception as e:
        logging.error(f"Error in model training: {e}")
        raise CustomException(e, sys)


