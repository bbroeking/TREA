from flask import Flask, request, jsonify
from sklearn.externals import joblib
import pandas as pd

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    json_ = request.get_json()
    vals = list(json_.values())
    query_df = pd.DataFrame([vals], columns=model_columns)
    print(query_df)
    prediction = clf.predict(query_df)
    print(prediction)
    return jsonify({"prediction": prediction[0][0]})


if __name__ == "__main__":
    clf = joblib.load("model.pkl")
    model_columns = joblib.load("model_columns.pkl")
    app.run(port=8080, debug=True)

