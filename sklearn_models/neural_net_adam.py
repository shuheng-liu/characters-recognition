from sklearn.neural_network import MLPClassifier
from .neural_net_config import sizes, random_seed as seed

model = MLPClassifier()
parameter_distribution = {
    "hidden_layer_sizes": sizes,
    "activation": ["logistic", "tanh", "relu"],
    "solver": ["adam"],
    "alpha": [0, 1e-4, 1e-3, 1e-2],
    "learning_rate_init": [1e-4, 1e-3, 1e-2],
    "random_state": [seed],
    "max_iter": [100, 200, 500],
    "beta_1": [0.5, 0.8, 0.9, 0.999],
    "beta_2": [0.9, 0.999, 0.99999],
}
