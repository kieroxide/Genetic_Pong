import numpy as np

class NeuralNet:
    def __init__(self, input_size, hidden_size, output_size):
        self.w1 = np.random.randn(hidden_size, input_size)
        self.w2 = np.random.randn(output_size, hidden_size)

        self.b1 = np.random.randn(hidden_size)    
        self.b2 = np.random.randn(output_size)    

        self.fitness = 0
        self.MUTATION_RATE = 0.2

    def forward(self, inputs):
        z1 = np.dot(self.w1, inputs) + self.b1        # Input to hidden
        a1 = np.tanh(z1)                      # Hidden activation
        z2 = np.dot(self.w2, a1) + self.b2           # Hidden to output
        output = 1 / (1 + np.exp(-z2))       # Sigmoid activation
        return output
    
    def crossover(self, other):
        child = NeuralNet(self.w1.shape[1], self.w1.shape[0], self.w2.shape[0])
        child.w1 = (self.w1 + other.w1) / 2
        child.b1 = (self.b1 + other.b1) / 2
        child.w2 = (self.w2 + other.w2) / 2
        child.b2 = (self.b2 + other.b2) / 2
        return child

    def mutate(self):
        self.w1 += np.random.randn(*self.w1.shape) * self.MUTATION_RATE
        self.b1 += np.random.randn(*self.b1.shape) * self.MUTATION_RATE
        self.w2 += np.random.randn(*self.w2.shape) * self.MUTATION_RATE
        self.b2 += np.random.randn(*self.b2.shape) * self.MUTATION_RATE
