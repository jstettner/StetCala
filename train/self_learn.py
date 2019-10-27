"""
Training module for NEAT model of Mancala.
Pits genomes against each other, fitness depends on match performance.

Author: Jack Stettner
Date: 16 November 2018
"""

import neat
import os
import numpy as np
import random
from Mancala import mancala
import pickle
import re
from tqdm import tqdm

# p-processing
# from joblib import Parallel, delayed
# import multiprocessing

BRAWLS_PER_GENERATION = 100
SHOW = False
epsilon = .05
EMPTY_PENALTY = 0.3
GENERATIONS = 100

def eval_genomes(genomes, config):
    """
    WELCOME TO THE THUNDERDOME

    Here we brawl pairs of genomes and adjust their fitness after each duel.
    """
    global SHOW
    # global epsilon

    board = mancala.Board(SHOW)
    for genome_id, genome in genomes:
        genome.fitness = 0

    for _ in tqdm(range(BRAWLS_PER_GENERATION)):
        for genome_id, genome in genomes:
            pit_against_empty_penalty(genome, genomes[random.randint(0,len(genomes)-1)][1], config, board)

        # num_cores = multiprocessing.cpu_count()
        # result = Parallel(n_jobs=num_cores)(delayed(pit_against_empty_penalty)(genome[1], genomes[random.randint(0,len(genomes)-1)][1], config, mancala.Board(SHOW)) for genome in genomes)

        # for i in range(len(genomes)):
        #     pit_against_random_empty_penalty(genomes[i][1], config, board)

    # epsilon *= 0.9

def pit_against_random_empty_penalty(genome1, config, board):
    """
    A single battle between two one genome and a random player.
    THIS FUNCTION ADJUSTS THEIR FITNESS
    """
    global EMPTY_PENALTY

    # Creates a net for each genome
    net1 = neat.nn.FeedForwardNetwork.create(genome1, config)

    board.reset()

    demerits = 0

    for _ in range(1000):
        if board.checkEmpty() == False:
            turn = board.getTurn()
            ran = random.random()
            if turn == mancala.Turn.P1:
                # this is the only player being evaluated in the current duel
                obs = board.P1View()
                action = net1.activate(obs)
                action = np.argmax(action)
                empty = board.P1Move(int(action))

                # adding demerits
                if empty:
                    demerits += EMPTY_PENALTY
            else:
                action = random.randint(0,5)
                board.P2Move(action)
        else:
            break

    genome1_pts, random_pts = board.getScore()

    genome1.fitness += (genome1_pts) - demerits

def pit_against_no_penalty(genome1, genome2, config, board):
    """
    A single battle between two genomes.
    THIS FUNCTION ADJUSTS THEIR FITNESS
    """
    global epsilon
    global EMPTY_PENALTY

    # Creates a net for each genome
    net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

    board.reset()

    for _ in range(1000):
        if board.checkEmpty() == False:
            turn = board.getTurn()
            ran = random.random()
            if turn == mancala.Turn.P1:
                # this is the only player being evaluated in the current duel
                obs = board.P1View()
                action = net1.activate(obs)
                action = np.argmax(action)
                empty = board.P1Move(int(action))
            else:
                obs = board.P2View()
                action = net2.activate(obs)
                if ran > epsilon:
                    action = np.argmax(action)
                else:
                    action = random.randint(0,5)
                board.P2Move(int(action))
        else:
            break

    genome1_pts, genome2_pts = board.getScore()

    genome1.fitness += (genome1_pts)

def pit_against_empty_penalty(genome1, genome2, config, board):
    """
    A single battle between two genomes.
    THIS FUNCTION ADJUSTS THEIR FITNESS
    """
    global epsilon
    global EMPTY_PENALTY

    # Creates a net for each genome
    net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

    board.reset()

    demerits = 0

    for _ in range(1000):
        if board.checkEmpty() == False:
            turn = board.getTurn()
            ran = random.random()
            if turn == mancala.Turn.P1:
                # this is the only player being evaluated in the current duel
                obs = board.P1View()
                action = net1.activate(obs)
                action = np.argmax(action)
                empty = board.P1Move(int(action))

                # adding demerits
                if empty:
                    demerits += EMPTY_PENALTY
            else:
                obs = board.P2View()
                action = net2.activate(obs)
                if ran > epsilon:
                    action = np.argmax(action)
                else:
                    action = random.randint(0,5)
                board.P2Move(int(action))
        else:
            break

    genome1_pts, genome2_pts = board.getScore()

    genome1.fitness += genome1_pts - demerits

def run():
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'config-ff')
    # config_file = con
    global GENERATIONS
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # p = neat.Population(config) # fresh population
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-242') # restored checkpoint
    p = get_latest_checkpoint(config) # combines the last two lines

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    winner = p.run(eval_genomes, GENERATIONS)
    print('\nBest genome:\n{!s}'.format(winner))
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    print(winner_net)

    with open('model.pkl', 'wb') as output:
        pickle.dump(winner_net, output)

def get_latest_checkpoint(config):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]

    print (files)

    regex = re.compile(r'^neat-checkpoint-\d*')
    checkpoint_files = list(filter(regex.search, files))

    if len(checkpoint_files) == 0:
        return neat.Population(config) # fresh population
    else:
        max = checkpoint_files[0]
        for file_name in checkpoint_files:
            if int(file_name[16:]) > int(max[16:]):
                max = file_name

        return neat.Checkpointer.restore_checkpoint(max)

# if __name__ == '__main__':
#     local_dir = os.path.dirname(__file__)
#     config_path = os.path.join(local_dir, 'config-ff')
    # run(config_path)
