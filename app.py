from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
from config.paths_config import MODEL_FILE_PATH, LABEL_ENCODER_FILE_PATH
import logging
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FIELD_INFO = {
    'Location': {'type': 'select', 'label': 'Location', 'options': ['Albury', 'Alice Springs', 'Brisbane', 'Cairns', 'Canberra', 'Cobar', 'Coffs Harbour', 'Darwin', 'Hobart', 'Katherine', 'Launceston', 'Melbourne', 'Mildura', 'Moree', 'Perth', 'Portland', 'Sydney', 'Townsville', 'Walgett', 'Wollongong', 'Yulara']},
    'MinTemp': {'type': 'float', 'label': 'Minimum Temperature (°C)', 'min': -10, 'max': 50, 'step': 0.1},
    'MaxTemp': {'type': 'float', 'label': 'Maximum Temperature (°C)', 'min': -10, 'max': 50, 'step': 0.1},
    'Rainfall': {'type': 'float', 'label': 'Rainfall (mm)', 'min': 0, 'max': 500, 'step': 0.1},
    'Evaporation': {'type': 'float', 'label': 'Evaporation (mm)', 'min': 0, 'max': 100, 'step': 0.1},
    'Sunshine': {'type': 'float', 'label': 'Sunshine (hours)', 'min': 0, 'max': 24, 'step': 0.1},
    'WindGustSpeed': {'type': 'float', 'label': 'Wind Gust Speed (km/h)', 'min': 0, 'max': 200, 'step': 0.1},
    'WindSpeed9am': {'type': 'float', 'label': 'Wind Speed 9am (km/h)', 'min': 0, 'max': 150, 'step': 0.1},
    'WindSpeed3pm': {'type': 'float', 'label': 'Wind Speed 3pm (km/h)', 'min': 0, 'max': 150, 'step': 0.1},
    'Humidity9am': {'type': 'float', 'label': 'Humidity 9am (%)', 'min': 0, 'max': 100, 'step': 1},
    'Humidity3pm': {'type': 'float', 'label': 'Humidity 3pm (%)', 'min': 0, 'max': 100, 'step': 1},
    'Pressure9am': {'type': 'float', 'label': 'Pressure 9am (hPa)', 'min': 980, 'max': 1050, 'step': 0.1},
    'Pressure3pm': {'type': 'float', 'label': 'Pressure 3pm (hPa)', 'min': 980, 'max': 1050, 'step': 0.1},
    'Cloud9am': {'type': 'float', 'label': 'Cloud Coverage 9am (oktas)', 'min': 0, 'max': 8, 'step': 1},
    'Cloud3pm': {'type': 'float', 'label': 'Cloud Coverage 3pm (oktas)', 'min': 0, 'max': 8, 'step': 1},
    'Temp9am': {'type': 'float', 'label': 'Temperature 9am (°C)', 'min': -10, 'max': 50, 'step': 0.1},
    'Temp3pm': {'type': 'float', 'label': 'Temperature 3pm (°C)', 'min': -10, 'max': 50, 'step': 0.1},
    'WindGustDir': {'type': 'select', 'label': 'Wind Gust Direction', 'options': ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']},
    'WindDir9am': {'type': 'select', 'label': 'Wind Direction 9am', 'options': ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']},
    'WindDir3pm': {'type': 'select', 'label': 'Wind Direction 3pm', 'options': ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']},
    'RainToday': {'type': 'select', 'label': 'Rain Today', 'options': ['Yes', 'No']}
}

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', fields=FIELD_INFO)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        logger.info(f"Received data: {data}")

        model = joblib.load(MODEL_FILE_PATH)
        label_encoders = joblib.load(LABEL_ENCODER_FILE_PATH)

        logger.info(f"Label encoder keys: {list(label_encoders.keys())}")

        feature_order = [
            'Location', 'MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine',
            'WindGustDir', 'WindGustSpeed', 'WindDir9am', 'WindDir3pm',
            'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm',
            'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm',
            'Temp9am', 'Temp3pm', 'RainToday', 'Year', 'Month', 'Day'
        ]

        input_features = []

        now = datetime.now()
        current_year = now.year
        current_month = now.month
        current_day = now.day

        for col in feature_order:
            logger.info(f"Processing {col}")

            if col == 'Year':
                input_features.append(float(current_year))
                logger.info(f"Year: {current_year}")
                continue
            elif col == 'Month':
                input_features.append(float(current_month))
                logger.info(f"Month: {current_month}")
                continue
            elif col == 'Day':
                input_features.append(float(current_day))
                logger.info(f"Day: {current_day}")
                continue

            value = data.get(col)

            if value is None or value == '':
                logger.warning(f"Missing value for {col}")
                return jsonify({
                    'success': False,
                    'error': f'Please provide a value for {col}'
                }), 400

            try:
                if col in label_encoders:
                    le = label_encoders[col]

                    if hasattr(le, 'classes_'):
                        str_value = str(value).strip()

                        if str_value not in le.classes_:
                            logger.error(f"Value '{str_value}' not in encoder classes for {col}: {le.classes_}")
                            return jsonify({
                                'success': False,
                                'error': f'Invalid value "{str_value}" for {col}. Valid options: {", ".join(le.classes_)}'
                            }), 400

                        encoded_value = le.transform([str_value])[0]
                        input_features.append(float(encoded_value))
                        logger.info(f"{col} encoded: {str_value} -> {encoded_value}")
                    else:
                        numeric_value = float(value)
                        input_features.append(numeric_value)
                        logger.info(f"{col} numeric: {numeric_value}")
                else:
                    numeric_value = float(value)
                    input_features.append(numeric_value)
                    logger.info(f"{col} numeric (not in encoders): {numeric_value}")

            except Exception as e:
                logger.error(f"Error processing {col}: {str(e)}")
                return jsonify({
                    'success': False,
                    'error': f'Invalid value for {col}: {str(e)}'
                }), 400

        input_array = np.array(input_features).reshape(1, -1)
        logger.info(f"Input array shape: {input_array.shape}")
        logger.info(f"Input array values: {input_array}")
        logger.info(f"Number of features: {len(input_features)}")

        prediction = model.predict(input_array)[0]
        probability = model.predict_proba(input_array)[0] if hasattr(model, 'predict_proba') else None

        result = "Yes" if prediction == 1 else "No"
        confidence = float(max(probability)) * 100 if probability is not None else 0

        logger.info(f"Prediction: {result}, Confidence: {confidence}")

        return jsonify({
            'success': True,
            'prediction': result,
            'confidence': round(confidence, 2)
        })

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Prediction error: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
