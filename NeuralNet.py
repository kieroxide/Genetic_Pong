import numpy as np

class NeuralNet:
    def __init__(self, input_size, hidden_size, output_size):
        self.w1 = np.random.randn(hidden_size, input_size)
        self.w2 = np.random.randn(output_size, hidden_size)

    def forward(self, inputs):
        z1 = np.dot(self.w1, inputs)         # Input to hidden
        a1 = np.tanh(z1)                      # Hidden activation
        z2 = np.dot(self.w2, a1)             # Hidden to output
        output = 1 / (1 + np.exp(-z2))       # Sigmoid activation
        return output