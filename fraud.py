from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Fraud detection logic
def detect_fraud_rule_based(transactions_df):
    fraud_transactions = []
    
    for index, transaction in transactions_df.iterrows():
        # Rule 1: High transaction amount
        if transaction['amount'] > 500:
            fraud_transactions.append(transaction)
        
        # Rule 2: Transaction location change in short time
        user_transactions = transactions_df[transactions_df['user_id'] == transaction['user_id']]
        for _, other_transaction in user_transactions.iterrows():
            if transaction['transaction_id'] != other_transaction['transaction_id']:
                time_diff = abs(datetime.strptime(transaction['timestamp'], "%Y-%m-%d %H:%M:%S") -
                                datetime.strptime(other_transaction['timestamp'], "%Y-%m-%d %H:%M:%S")).seconds
                if time_diff < 3600 and transaction['location'] != other_transaction['location']:
                    fraud_transactions.append(transaction)
    
    return pd.DataFrame(fraud_transactions).drop_duplicates()

# Endpoint to process transactions
@app.route('/process-transactions', methods=['POST'])
def process_transactions():
    try:
        # Get JSON data from frontend
        data = request.json  # Expecting a list of transactions
        df = pd.DataFrame(data)

        # Run fraud detection
        fraud_detected = detect_fraud_rule_based(df)
        return jsonify({
            "status": "success",
            "fraudulent_transactions": fraud_detected.to_dict(orient="records")
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)

