# Genetic Pong

A genetic algorithm implementation that evolves neural networks to play Pong. Watch as AI paddles learn to play better over generations through natural selection, crossover, and mutation.

## 🎮 Demo

The program evolves a population of neural networks over multiple generations, then displays the best performer from each generation playing Pong in real-time.

## 🧬 How It Works

1. **Population**: 1000 neural networks with random weights
2. **Evaluation**: Each network plays Pong and receives a fitness score based on survival time and paddle hits
3. **Selection**: Top 10% become parents for the next generation
4. **Reproduction**: Parents create offspring through crossover (weight averaging)
5. **Mutation**: Random noise is added to prevent stagnation
6. **Evolution**: Process repeats for 20 generations

## 🏗️ Architecture

- **Neural Network**: 6 inputs → 16 hidden neurons → 1 output
- **Inputs**: Ball position, velocity, paddle position, relative distance
- **Output**: Paddle movement (up/down/stay)
- **Activation**: Tanh (hidden) + Sigmoid (output)

## 🚀 Quick Start

### Prerequisites
```bash
pip install pygame numpy
```

### Run
```bash
python main.py
```

The program will:
1. Train for 100 generations (takes a few minutes)
2. Display each generation's best performer playing Pong
3. Press ESC or close window to skip to next generation

## ⚙️ Configuration

Edit constants in `main.py`:
```python
MAX_GENERATIONS = 40    # Number of evolution cycles
POP_SIZE = 1000        # Population size
NEURON_SIZE = 16       # Hidden layer neurons
MAX_FRAMES = 500       # Max game length per evaluation
```

## 📁 Project Structure

```
Genetic_Pong/
├── main.py          # Main genetic algorithm loop
├── NeuralNet.py     # Neural network with GA operations
├── Pong.py          # Pong game simulation
├── ai_controls.py   # AI paddle control logic
├── Canvas.py        # Pygame display management
└── README.md
```

## 🎯 Features

- **Multiprocessing**: Fast parallel fitness evaluation
- **Realistic Physics**: Angle-based ball bouncing
- **Visualization**: Watch the best AIs play
- **Clean Architecture**: Modular, well-documented code

## 📊 Expected Results

- **Early Generations**: Random, erratic movement
- **Middle Generations**: Basic ball tracking
- **Later Generations**: Strategic positioning and consistent hits

## 🛠️ Customization Ideas

- Adjust mutation rates for different evolution speeds
- Modify fitness function to reward specific behaviors
- Experiment with different network architectures
- Add save/load functionality for best networks

## 🔬 Technical Details

- **Genetic Algorithm**: Tournament selection with elitism
- **Crossover**: Uniform weight averaging between parents
- **Mutation**: Gaussian noise addition to all weights
- **Fitness**: `score × 10 + survival_frames`

Built with Python, NumPy, and Pygame.
