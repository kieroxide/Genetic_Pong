from Pong import Pong
from NeuralNet import NeuralNet
import numpy as np
import random
import multiprocessing


MUTATION_RATE = 0.3
NEURON_SIZE = 8
SCORE_WEIGHT = 20
MAX_FRAMES = 500

def main():
    MAX_GENERATIONS = 10
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
    children = []
    while len(children) < POP_SIZE - len(parents):
        p1, p2 = random.sample(parents, 2)
        child = crossover(p1, p2)
        mutate(child)
        children.append(child)
    return children

def rank_generation(population, PARENT_SIZE):
    with multiprocessing.Pool() as pool:
        population = pool.map(evaluate_net, population)
    selectBest(population)
    parents = population[:PARENT_SIZE]
    return parents

def evaluate_net(net):
    pong = Pong(drawn=False, net=net, maxFrames=MAX_FRAMES)
    frames, score = pong.start()
    net.fitness = score*SCORE_WEIGHT + frames
    return net

def crossover(parent1, parent2):
    child = NeuralNet(parent1.w1.shape[1], parent1.w1.shape[0], parent1.w2.shape[0])

    # Average weights
    child.w1 = (parent1.w1 + parent2.w1) / 2
    child.w2 = (parent1.w2 + parent2.w2) / 2

    return child

def mutate(net, mutation_rate=MUTATION_RATE):
    net.w1 += np.random.randn(*net.w1.shape) * mutation_rate
    net.w2 += np.random.randn(*net.w2.shape) * mutation_rate

def selectBest(population):
    population.sort(key=lambda net: net.fitness, reverse=True)

if __name__ == '__main__':
    main()