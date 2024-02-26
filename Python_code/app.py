from Flask import Flask, request, jsonify
import h5py, pickle

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    with h5py.File('model_Louis.pkl', 'r') as f:
        model_louis = pickle.load(f)
    prediction = model_louis.predict(data)
    return create_response(data, prediction)

def create_response(data, prediction):
    response = {
        'data': data,
        'prediction': prediction
    }
    return jsonify(response)