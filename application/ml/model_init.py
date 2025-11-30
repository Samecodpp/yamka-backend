import os
import joblib

def init_model():
    base_dir = os.path.dirname(__file__)
    dataset_path = os.path.join(base_dir, "data", "pothole_dataset.csv")
    model_path = os.path.join(base_dir, "model")
    model_file = os.path.join(model_path, "svc_pothole_model.pkl")
    scaler_file = os.path.join(model_path, "scaler.pkl")

    if os.path.exists(model_file) and os.path.exists(scaler_file):
        print(f"Loading existing model from {model_file}")
        model = joblib.load(model_file)
        scaler = joblib.load(scaler_file)
        return {"model": model, "scaler": scaler}

    print("Model not found. Training new model...")
    from training.train import PotholeTrainer
    trainer = PotholeTrainer(input_path=dataset_path, outdir=model_path)
    success = trainer.train()
    if not success:
        raise RuntimeError("Model training failed (dataset missing or invalid).")

    model = joblib.load(model_file)
    scaler = joblib.load(scaler_file)
    return {"model": model, "scaler": scaler}

def predict(model, features):
    """
    Predict pothole severity from sensor features

    Args:
        model: dict with 'model' and 'scaler' keys
        features: list or RepeatedScalarContainer from gRPC

    Returns:
        int: predicted pothole severity (1-5)
    """
    import pandas as pd

    # Convert gRPC RepeatedScalarContainer to list
    features_list = list(features)

    feature_names = ['speed', 'accelerometerX', 'accelerometerY', 'accelerometerZ',
                     'gyroX', 'gyroY', 'gyroZ']

    df = pd.DataFrame([features_list], columns=feature_names)
    X_scaled = model['scaler'].transform(df)
    prediction = model['model'].predict(X_scaled)[0] + 1
    return int(prediction)
