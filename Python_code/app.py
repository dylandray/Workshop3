from Flask import Flask, request, jsonify
from louis_model import GenerateModel

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    model, mse, r2 = GenerateModel(evaluate=True)
    prediction = model.predict(data)
    return create_response(data, mse, r2, prediction)

def create_response(data, mse, r2, prediction):
    response = {
        'data': data,
        'mse': mse,
        'r2 score': r2,
        'prediction': prediction
    }
    return jsonify(response)