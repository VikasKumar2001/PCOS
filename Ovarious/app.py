import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, url_for
import pickle

app = Flask(__name__, static_url_path='/static')

model = pickle.load(open('best_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict')
def predict_page():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form.to_dict()

        # Convert select fields to binary values (Y/N to 1/0)
        binary_fields = ['Skin_darkening', 'Hair_growth', 'Weight_gain', 'Hair_loss']
        for field in binary_fields:
            if field in data:
                data[field] = 1 if data[field].lower() == 'yes' else 0
        
        # Convert all other fields to floats
        features = [float(data[key]) if key not in binary_fields else data[key] for key in data]

        final_features = [np.array(features)]
        prediction = model.predict(final_features)
        output = round(prediction[0], 2)

        return render_template('prediction.html', prediction_text='Your predicted value is {}'.format(output))
    except ValueError:
        return render_template('index.html', prediction_text='Invalid input. Please enter valid numbers.')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    features = []
    binary_fields = ['Skin_darkening', 'Hair_growth', 'Weight_gain', 'Hair_loss']
    for key, value in data.items():
        if key in binary_fields:
            features.append(1 if value.lower() == 'yes' else 0)
        else:
            features.append(float(value))
    
    prediction = model.predict([np.array(features)])
    output = prediction[0]
    output=int(output)
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
