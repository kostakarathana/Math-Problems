import numpy as np
import pandas as pd

df = pd.read_csv("house_data.csv") # load our data

feature_cols = ["square_feet", "rooms", "bathrooms", "age",
                "distance_from_city", "floors", "carspaces"]

target_col = "price"

X = df[feature_cols].values
y = df[target_col].values

# --- Manual normalization (Min-Max scaling) ---
X_min = X.min(axis=0)
X_max = X.max(axis=0)
X_norm = (X - X_min) / (X_max - X_min)

def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

def knn_predict_single(X_train, y_train, x_query, k=5):
    dists = [euclidean_distance(x_query, x_train) for x_train in X_train]
    idx_sorted = np.argsort(dists)
    k_idx = idx_sorted[:k]
    return np.mean(y_train[k_idx])

# --- Predict for a new house ---
new_house = np.array([[2200, 4, 2.5, 15, 8.0, 2, 2]])

# Normalize using the same min-max as training data
new_house_norm = (new_house - X_min) / (X_max - X_min)

prediction = knn_predict_single(X_norm, y, new_house_norm[0], k=5)
print(f"Predicted price: ${prediction:,.0f}")