from flask import Flask, request, jsonify
from joblib import load
import numpy as np

app = Flask(__name__)
model = load('best_model.joblib')

def predict_match(person, potential_match):
    common_interests_count = len(set(person['groups']).intersection(set(potential_match['groups'])))
    common_personal_preferences_count = sum(
        1 for pref in person['personal'].values() if pref != "" and pref in potential_match['personal'].values()
    )
    occupation_similarity = person['occupation'] == potential_match['occupation']
    features = np.array([[common_interests_count, common_personal_preferences_count, occupation_similarity]])
    match_probability = model.predict_proba(features)[0][1]
    return match_probability > 0.5  # порог вероятности для совпадения

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    person = data['person']
    people_list = data['people_list']
    matches = [p['id'] for p in people_list if predict_match(person, p)]
    return jsonify(matches)

if __name__ == '__main__':
    app.run(debug=True)
