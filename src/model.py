import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler


def load_data():
    data = pd.read_csv("../data/retail.csv", encoding="latin1")
    return data


def clean_data(data):
    data = data.dropna(subset=["CustomerID"])
    data = data[data["Quantity"] > 0]
    data = data[data["UnitPrice"] > 0]
    data["TotalPrice"] = data["Quantity"] * data["UnitPrice"]
    data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])
    return data


def create_customer_features(data):
    customer = data.groupby("CustomerID").agg({
        "TotalPrice": ["sum", "mean", "std"],
        "Quantity": ["sum", "mean"],
        "InvoiceNo": "count"
    })

    customer.columns = [
        "TotalSpend",
        "AvgSpend",
        "SpendStd",
        "TotalQuantity",
        "AvgQuantity",
        "TransactionCount"
    ]

    customer = customer.fillna(0)
    return customer


def train_model(customer):

    # Store features separately (important!)
    features = customer.copy()

    model = IsolationForest(contamination=0.02, random_state=42)

    # Train model
    model.fit(features)

    # Predict anomaly
    customer["anomaly"] = model.predict(features)

    # Get risk score
    customer["risk_score"] = model.decision_function(features)

    # Scale risk score 0-100
    scaler = MinMaxScaler()
    customer["risk_score"] = scaler.fit_transform(
        customer[["risk_score"]]
    ) * 100

    return customer

    return customer


if __name__ == "__main__":
    data = load_data()
    data = clean_data(data)
    customer = create_customer_features(data)
    customer = train_model(customer)

    customer.to_csv("../results/customer_risk.csv")
    print(customer.head())














