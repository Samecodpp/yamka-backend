import argparse
import os
import time
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from utils import TrainingVisualizer

class PotholeTrainer:
    def __init__(self, input_path: str, outdir: str):
        self.input_path = input_path
        self.outdir = outdir
        self.features = None
        self.target = None

    def _load_data(self):
        try:
            df = pd.read_csv(self.input_path)
        except FileNotFoundError:
            print(f"Error: File '{self.input_path}' not found.")
            return None
        return df

    def _select_columns(self, df: pd.DataFrame):
        feature_variants = [
            ['speed', 'accelerometerX', 'accelerometerY', 'accelerometerZ', 'gyroX', 'gyroY', 'gyroZ'],
            ['speed', 'acc_x', 'acc_y', 'acc_z', 'gyr_x', 'gyr_y', 'gyr_z'],
        ]
        for fv in feature_variants:
            if all(col in df.columns for col in fv):
                self.features = fv
                break
        if not self.features:
            print("Error: Dataset does not contain required feature columns.")
            return False

        target_candidates = ['pothole_label', 'label']
        self.target = next((t for t in target_candidates if t in df.columns), None)
        if not self.target:
            print("Error: Dataset does not contain target column ('pothole_label' or 'label').")
            return False
        return True

    def train(self):
        df = self._load_data()
        if df is None:
            return False
        if not self._select_columns(df):
            return False

        X = df[self.features].fillna(0.0)
        y = df[self.target].astype(int)
        if y.min() == 1:
            y = y - 1

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y if len(y.unique()) > 1 else None
        )

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        param_grid_svc = {'C': [1, 10, 100], 'gamma': ['scale', 0.1, 1], 'kernel': ['rbf']}
        svc_base = SVC(class_weight='balanced', random_state=42)
        grid_search_svc = GridSearchCV(
            estimator=svc_base,
            param_grid=param_grid_svc,
            scoring='f1_macro',
            cv=3,
            verbose=2,
            n_jobs=-1
        )

        print("Starting Grid Search for SVC (Support Vector Classifier)...")
        start_time = time.time()
        grid_search_svc.fit(X_train_scaled, y_train)
        end_time = time.time()
        print(f"Grid Search for SVC completed in {end_time - start_time:.2f} seconds.")
        best_model_svc = grid_search_svc.best_estimator_
        y_pred = best_model_svc.predict(X_test_scaled)

        print("\n" + "="*70)
        print("               SVC F1_MACRO TUNING RESULTS            ")
        print("="*70)
        print(f"Best hyperparameters: {grid_search_svc.best_params_}")
        print(f"Best Macro F1-Score on cross-validation: {grid_search_svc.best_score_:.4f}")

        print("\n--- Classification report on test set ---")
        print(classification_report(y_test, y_pred))

        os.makedirs(self.outdir, exist_ok=True)
        model_path = os.path.join(self.outdir, 'svc_pothole_model.pkl')
        scaler_path = os.path.join(self.outdir, 'scaler.pkl')
        joblib.dump(best_model_svc, model_path)
        joblib.dump(scaler, scaler_path)
        print(f"Model saved: {model_path}")
        print(f"Scaler saved: {scaler_path}")

        if TrainingVisualizer is not None:
            viz = TrainingVisualizer(outdir=self.outdir)
            viz.plot_confusion_matrix(y_test, y_pred, class_names=[str(i) for i in range(len(y.unique()))])
            viz.visualize_svc_decision_boundary(X_train_scaled, y_train, X_test_scaled, y_test, grid_search_svc.best_params_)
        else:
            print("TrainingVisualizer not found. Skipping plots.")

        return True


def main():
    parser = argparse.ArgumentParser(description="Train SVC pothole classifier")
    file_dir = os.path.dirname(__file__)
    default_input = os.path.join(file_dir, "..", "data", "pothole_dataset.csv")
    default_outdir = os.path.join(file_dir, "..", "model")
    parser.add_argument("--input", default=os.path.normpath(default_input), help="Path to input CSV dataset")
    parser.add_argument("--outdir", default=os.path.normpath(default_outdir), help="Directory to save trained model and scaler")
    args = parser.parse_args()

    trainer = PotholeTrainer(input_path=args.input, outdir=args.outdir)
    success = trainer.train()
    if not success:
        exit(1)


if __name__ == "__main__":
    main()
