"""Main genetic algorithm implementation for evolving Pong-playing neural networks."""

from Pong import Pong
from NeuralNet import NeuralNet
import random
import multiprocessing

MUTATION_RATE = 0.1
NEURON_SIZE = 60
SCORE_WEIGHT = 10
MAX_FRAMES = 500

def main():
    """Run genetic algorithm and display best performers."""
    MAX_GENERATIONS = 100
    POP_SIZE = 1000
    PARENT_SIZE = round(POP_SIZE * 0.1)

    #Generates NeuralNets for to be each member of the population
    #NeuralNet(input_size, Hidden_Size, Output_Size)
    population = [NeuralNet(6, NEURON_SIZE, 1) for _ in range(POP_SIZE)]

    best_performers_per_gen = simulate_generations(MAX_GENERATIONS, POP_SIZE, PARENT_SIZE, population)
    
    #Display best performers games
    for performer, gen in best_performers_per_gen:
        pong = Pong(drawn=True, net=performer, maxFrames=float('inf'), gen=gen)
        pong.start()

def simulate_generations(MAX_GENERATIONS, POP_SIZE, PARENT_SIZE, population):
    """Evolve population over multiple generations."""
    best_performers_per_gen = []
    for gen in range(MAX_GENERATIONS):
        print(f"Generation: {gen}")
        #Simulates generation and returns top performers
        parents = rank_generation(population, PARENT_SIZE)
        best_performer = parents[0]
        best_performers_per_gen.append((best_performer, gen + 1))
        #Repopulates with parents, mutates to avoid homogenity
        children = repopulate(POP_SIZE, parents)
        #Joins them both to create the next generation
        population = parents + children
        #Best performer to watch after all generations done
    return best_performers_per_gen

def repopulate(POP_SIZE, parents):
    """Create new generation through crossover and mutation."""
    children = []
    while len(children) < POP_SIZE - len(parents):
        p1, p2 = random.sample(parents, 2)
        child = p1.crossover(p2)
        child.mutate()
        children.append(child)
    return children

def rank_generation(population, PARENT_SIZE):
    """Evaluate and rank population by fitness."""
    with multiprocessing.Pool() as pool:
        population = pool.map(evaluate_net, population)
    selectBest(population)
    parents = population[:PARENT_SIZE]
    return parents

def evaluate_net(net):
    """Evaluate neural network fitness by playing Pong."""
    pong = Pong(drawn=False, net=net, maxFrames=MAX_FRAMES)
    frames, score = pong.start()
    net.fitness = score*SCORE_WEIGHT + frames
    return net

def selectBest(population):
    """Sort population by fitness (highest first)."""
    population.sort(key=lambda net: net.fitness, reverse=True)

if __name__ == '__main__':
    main()