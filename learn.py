"""
Training module for NEAT model of Mancala.
Pits genomes against each other, winners are more fit.

Author: Jack Stettner
Date: 13 November 2018
"""

import gym
import neat
import os
import numpy as np
import random
import mancala

BRAWLS_PER_GENERATION = 10
SHOW = False
epsilon = 0

def eval_genomes(genomes, config):
    """
    WELCOME TO THE THUNDERDOME

    Here we brawl pairs of genomes and adjust their fitness after each duel.
    """
    # global epsilon
    # print(genomes)
    board = mancala.Board(False)

    for genome_id, genome in genomes:
        genome.fitness = 0
        pit(genome, genomes[random.randint(0,len(genomes)-1)][1], config, board)

    # for _ in range(BRAWLS_PER_GENERATION):
        # random.shuffle(genomes)

        # i = 0
        # print(len(genomes))
        # while i+1 < len(genomes):
        #     pit(genomes[i][1], genomes[i+1][1], config)
        #     i += 2

    # brings all fitness values between 0 and 1
    # for genome_id, genome in genomes:
    #     genome.fitness /= BRAWLS_PER_GENERATION

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
            # input()
            ran = random.random()
            if turn == mancala.Turn.P1:
                obs = board.P1View()
                # print('p1',obs)
                action = net1.activate(obs)
                # if ran > epsilon:
                action = np.argmax(action)
                # else:
                #     print('random')
                #     action = random.randint(0,5)
                # print('action',action)
                board.P1Move(int(action))
            else:
                obs = board.P2View()
                # print('p2',obs)
                action = net2.activate(obs)
                # if ran > epsilon:
                action = np.argmax(action)
                # else:
                #     print('random')
                #     action = random.randint(0,5)
                # print('action',action)
                board.P2Move(int(action))
        else:
            break

                # print('p1 genome test')
                # print('[0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]', net1.activate([0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]))

    genome1_pts, genome2_pts = board.getScore()
    # print(str(genome1) + ' vs. ' + str(genome2) + ': ' + str(genome1_pts) + ' to ' + str(genome2_pts))

    print(board.P1View())
    # print('genome1_pts:',genome1_pts)
    genome1.fitness += (genome1_pts/48)
    # print('genome2_pts:',genome2_pts)
    # genome2.fitness += (genome1_pts/48)

def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    winner = p.run(eval_genomes, 300)
    print('\nBest genome:\n{!s}'.format(winner))
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    print(winner_net)



if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-ff')
    run(config_path)
