import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

class TrainingVisualizer:
    def __init__(self, outdir: str = "."):
        self.outdir = outdir
        os.makedirs(self.outdir, exist_ok=True)

    def visualize_svc_decision_boundary(self, X_train_scaled, y_train, X_test_scaled, y_test, best_params):
        pca = PCA(n_components=2)
        X_train_pca = pca.fit_transform(X_train_scaled)
        X_test_pca = pca.transform(X_test_scaled)

        svc_pca = SVC(**best_params, class_weight='balanced')
        svc_pca.fit(X_train_pca, y_train)

        plt.figure(figsize=(10, 6))
        x_min, x_max = X_train_pca[:, 0].min() - 1, X_train_pca[:, 0].max() + 1
        y_min, y_max = X_train_pca[:, 1].min() - 1, X_train_pca[:, 1].max() + 1
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 400), np.linspace(y_min, y_max, 400))

        Z = svc_pca.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        plt.contourf(xx, yy, Z, alpha=0.3, cmap="viridis")
        scatter = plt.scatter(X_test_pca[:, 0], X_test_pca[:, 1], c=y_test, s=40, cmap="viridis", edgecolor="k")

        plt.title("SVC in PCA-2D space")
        plt.xlabel("PCA 1")
        plt.ylabel("PCA 2")
        plt.colorbar(scatter, label="Class")
        plt.grid(True)
        out_path = os.path.join(self.outdir, "svc_decision_boundary.png")
        plt.savefig(out_path, format="png", dpi=300, bbox_inches="tight")
        plt.close()
        return out_path

    def plot_confusion_matrix(self, y_true, y_pred, class_names=None, title="SVC Confusion Matrix"):
        """Plot and save confusion matrix PNG.

        Saves: confusion_matrix_svc.png under outdir
        """
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=class_names if class_names else "auto",
                    yticklabels=class_names if class_names else "auto")
        plt.xlabel("Predicted class")
        plt.ylabel("True class")
        plt.title(title)
        out_path = os.path.join(self.outdir, "confusion_matrix_svc.png")
        plt.savefig(out_path, dpi=300, bbox_inches='tight')
        plt.close()
        return out_path
