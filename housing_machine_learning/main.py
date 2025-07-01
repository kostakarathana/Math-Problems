import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

df: pd.DataFrame = pd.read_csv("housing_machine_learning/data.csv") # type: ignore

X: np.ndarray = df[['Size (sqft)', 'Age (years)', 'Rooms', 'Bathrooms', 'Garage Size (cars)']].values
y: np.ndarray = df['Price (USD)'].values.reshape(-1, 1) # type: ignore

# Feature Normalization
def normalize_features(X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mu: np.ndarray = np.mean(X, axis=0)
    sigma: np.ndarray = np.std(X, axis=0)
    X_norm: np.ndarray = (X - mu) / sigma
    return X_norm, mu, sigma

X_norm, mu, sigma = normalize_features(X)

m = len(y)
X_with_bias = np.concatenate([np.ones((m, 1)), X_norm], axis=1)


def compute_cost(X: np.ndarray, y: np.ndarray, theta: np.ndarray) -> float:
    m: int = len(y)
    predictions = X.dot(theta)
    cost = (1 / (2 * m)) * np.sum((predictions - y) ** 2)
    return cost

def gradient_descent(
    X: np.ndarray,
    y: np.ndarray,
    theta: np.ndarray,
    alpha: float,
    iterations: int
) -> tuple[np.ndarray, list[float]]:
    m = len(y)
    cost_history: list[float] = []

    for _ in range(iterations):
        predictions = X.dot(theta)
        error = predictions - y
        gradient = (1 / m) * X.T.dot(error)
        theta -= alpha * gradient
        cost_history.append(compute_cost(X, y, theta))

    return theta, cost_history


# Initialize theta to zeros
theta = np.zeros((X_with_bias.shape[1], 1))

# Set learning rate and number of iterations
alpha = 0.01
iterations = 500

# Run gradient descent
theta, cost_history = gradient_descent(X_with_bias, y, theta, alpha, iterations)

def predict(new_data: np.ndarray) -> np.ndarray:
    # Normalize using training mean and std
    new_data_norm = (new_data - mu) / sigma

    # Add bias (intercept term)
    new_data_with_bias = np.concatenate([np.ones((new_data_norm.shape[0], 1)), new_data_norm], axis=1)

    # Predict using learned theta
    return new_data_with_bias.dot(theta)

example_house = np.array([[2600, 3, 8, 4, 3]])  # Replace with any values
predicted_price = predict(example_house)

print(f"Predicted price: ${predicted_price[0][0]:,.2f}")

