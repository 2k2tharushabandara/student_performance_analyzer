
from flask import Flask, request, jsonify
import joblib, pandas as pd

app = Flask(__name__)

clf_model = joblib.load("model_classification.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    df = pd.DataFrame([data])

    grade = clf_model.predict(df)[0]
    probs = clf_model.predict_proba(df)[0]
    classes = clf_model.named_steps['model'].classes_

    return jsonify({
        "predicted_grade": grade,
        "grade_probabilities": {c: float(p) for c, p in zip(classes, probs)}
    })

if __name__ == "__main__":
    app.run(debug=True)
