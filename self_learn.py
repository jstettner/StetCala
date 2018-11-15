"""
Training module for NEAT model of Mancala.
Pits genomes against each other, winners are more fit.

Author: Jack Stettner
Date: 13 November 2018
"""

import neat
import os
import numpy as np
import random
import mancala
import pickle

BRAWLS_PER_GENERATION = 10
SHOW = False
epsilon = .25

def eval_genomes(genomes, config):
    """
    WELCOME TO THE THUNDERDOME

    Here we brawl pairs of genomes and adjust their fitness after each duel.
    """
    global SHOW
    # global epsilon
    
    board = mancala.Board(SHOW)

    for _ in range(BRAWLS_PER_GENERATION):
        for genome_id, genome in genomes:
            genome.fitness = 0
            pit(genome, genomes[random.randint(0,len(genomes)-1)][1], config, board)

    # epsilon *= 0.9

def pit(genome1, genome2, config, board):
    """
    A single battle between two genomes.
    THIS FUNCTION ADJUSTS THEIR FITNESS
    """
    global epsilon

    # Creates a net for each genome
    net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

    board.reset()

    for _ in range(1000):
        if board.checkEmpty() == False:
            turn = board.getTurn()
            ran = random.random()
            if turn == mancala.Turn.P1:
                obs = board.P1View()
                action = net1.activate(obs)
                action = np.argmax(action)
                board.P1Move(int(action))
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

    genome1.fitness += (genome1_pts/48)

def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # p = neat.Population(config) # fresh population
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-171')

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(100))

    winner = p.run(eval_genomes, 300)
    print('\nBest genome:\n{!s}'.format(winner))
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    print(winner_net)

    with open('model.pkl', 'wb') as output:
        pickle.dump(winner_net, output)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-ff')
    run(config_path)
