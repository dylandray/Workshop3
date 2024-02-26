from flask import Flask, request, jsonify
import 

app = Flask(__name__)

# Charger le modèle
model = pickle.load(open('nom_du_modele.pkl', 'rb'))

@app.route('/prediction', methods=['POST'])
def predict():
    # Obtenir les caractéristiques du jeu à partir de la requête POST
    features = request.json['features']

    # Effectuer la prédiction en utilisant le modèle chargé
    prediction = model.predict([features])

    # Renvoyer la prédiction sous forme de réponse JSON
    response = {'prediction': prediction[0]}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
