from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model
try:
    model = joblib.load("fraud_detection_model.pkl")
except Exception as e:
    model = None
    print("Model loading failed:", e)


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    fraud_type = None
    

    if request.method == "POST":
        form_data = request.form
        if model is None:
            return "Model failed to load. Check console for error.", 500

        # Normalize and clean form data
        input_data = {
            "amount": float(request.form["amount"]),
            "currency": request.form["currency"].strip().lower(),
            "payment_method": request.form["payment_method"].strip().lower(),
            "email_domain": request.form["email_domain"].strip().lower(),
            "device_type": request.form["device_type"].strip().lower(),
            "ip_country": request.form["ip_country"].strip().upper(),  # country code usually uppercase
            "account_age_days": int(request.form["account_age_days"]),
            "hour": int(request.form["hour"]),
            "day_of_week": int(request.form["day_of_week"])
        }

        input_df = pd.DataFrame([input_data])

        # Debug prints to console
        print("Input dataframe for prediction:")
        print(input_df)

        try:
            result = model.predict(input_df)
            print("Model prediction output:", result)

            if result[0] == 1:
                prediction = "Fraudulent"
                # Dummy fraud type logic (replace with actual logic if available)
                if input_data["amount"] > 1000:
                    fraud_type = "High-Value Scam"
                elif input_data["device_type"] == "mobile":
                    fraud_type = "Mobile Spoofing"
                else:
                    fraud_type = "General Fraud"
            else:
                prediction = "Legitimate"
        except Exception as e:
            print("Prediction failed:", e)
            prediction = "Error occurred during prediction."

    return render_template("index.html", prediction=prediction, fraud_type=fraud_type)
    

if __name__ == "__main__":
    app.run(debug=True)
