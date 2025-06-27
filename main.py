from Pong import Pong
from NeuralNet import NeuralNet
import numpy as np
import random
import multiprocessing

def main():
    MAX_GENERATIONS = 400
    POP_SIZE = 100
    PARENT_SIZE = round(POP_SIZE * 0.3)
    population = [NeuralNet(6, 16, 1) for _ in range(POP_SIZE)]
    best = population[0]
    for gen in range(MAX_GENERATIONS):
        print(f"Generation: {gen}")
        with multiprocessing.Pool() as pool:
            population = pool.map(evaluate_net, population)
        selectBest(population)
        parents = population[:PARENT_SIZE]
        children = []
        while len(children) < POP_SIZE - len(parents):
            p1, p2 = random.sample(parents, 2)
            child = crossover(p1, p2)
            mutate(child)
            children.append(child)

        population = parents + children
        best = population[0]
    pong = Pong(drawn=True, net=best, maxFrames=float('inf'))
    pong.start()

def evaluate_net(net):
    pong = Pong(drawn=True, net=net, maxFrames=500)
    frames, score = pong.start()
    net.fitness = score*20 + frames
    return net

def crossover(parent1, parent2):
    child = NeuralNet(parent1.w1.shape[1], parent1.w1.shape[0], parent1.w2.shape[0])

    # Average weights
    child.w1 = (parent1.w1 + parent2.w1) / 2
    child.w2 = (parent1.w2 + parent2.w2) / 2

    return child

def mutate(net, mutation_rate=0.1):
    net.w1 += np.random.randn(*net.w1.shape) * mutation_rate
    net.w2 += np.random.randn(*net.w2.shape) * mutation_rate

def selectBest(population):
    population.sort(key=lambda net: net.fitness, reverse=True)

if __name__ == '__main__':
    main()