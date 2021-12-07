import copy
import random
import time

from bitarray import bitarray, util
from deap import base, creator, tools, algorithms
from deap.tools import HallOfFame

import puzzle_operations as puzzle


# This is needed to make bitarray deepcopy correctly with the genetic algorithm library.
# I didn't write this, I just copied to code they did for python's array.array.
class _bitarray(bitarray):
    @staticmethod
    def __new__(cls, seq=()):
        return super(_bitarray, cls).__new__(cls, seq)

    def __deepcopy__(self, memo):
        """Overrides the deepcopy from bitarray that does not copy
        the object's attributes and class type.
        """
        cls = self.__class__
        copy_ = cls.__new__(cls, self)
        memo[id(self)] = copy_
        copy_.__dict__.update(copy.deepcopy(self.__dict__, memo))
        return copy_

    def __reduce__(self):
        return self.__class__, (list(self),), self.__dict__


# Again, need a function for zero initialization for the genetic algorithm library.
def zero():
    return 0


def convert_bits_to_rotations(individual: bitarray):
    rotations = []
    for i in range(0, len(individual), 2):
        # 4 rotations (0, 1, 2, 3), so each rotation takes 2 bits
        rotations.append(util.ba2int(individual[i: i + 2]))
    return rotations


# Input: The axis each block attaches through
# Output: The count of adjacent blocks (without double counting) and collisions.
def count_adjacent_and_collisions(axis):
    point = (0, 0, 0)
    points = {point}
    adjacent = 0
    collisions = 0
    for a in axis:
        point = puzzle.add_tuple(point, a)
        adjacent_points = puzzle.get_adjacent(point)
        intersection = len(adjacent_points.intersection(points))
        if point in points:
            collisions += 1
        else:
            adjacent += intersection
            points.add(point)
    return adjacent, collisions


# Components of score: adjacent blocks, collisions, and non-zero rotations
def evaluate_adjacent(individual):
    rotations = convert_bits_to_rotations(individual)  # convert bitarray to list of rotations (0, 90, 180, 270 degrees)
    new_axis = puzzle.update_all_puzzle_axis(individual.axis, rotations)
    adj, col = count_adjacent_and_collisions(new_axis)
    non_zero = sum(1 for r in rotations if r != 0)
    return adj, col, non_zero


# Components of score: bounding box volume, collisions, and non-zero rotations
def evaluate_volume(individual):
    rotations = convert_bits_to_rotations(individual)  # convert bitarray to list of rotations (0, 90, 180, 270 degrees)
    new_axis = puzzle.update_all_puzzle_axis(individual.axis, rotations)
    points = puzzle.calculate_points(new_axis)
    volume = puzzle.volume(points)
    collisions = len(points) - len(set(points))
    non_zero = sum(1 for r in rotations if r != 0)
    return volume, collisions, non_zero


def main():
    # 'adjacent' or 'volume'
    # adjacent works a lot better
    fitness = 'adjacent'

    if fitness == 'adjacent':
        # weights needed to maximize adjacent squares, minimize collisions, minimize total rotations
        creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0, -0.05))

    if fitness == 'volume':
        # weights needed to minimize volume, minimize collisions, minimize total rotations
        creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1000.0, -0.05))

    # an "Individual" is our list of rotations (0, 90, 180, 270)
    creator.class_replacers[bitarray] = _bitarray
    creator.create("Individual", bitarray, fitness=creator.FitnessMulti, axis=puzzle.real_puzzle_axis)

    IND_SIZE = len(puzzle.real_puzzle_axis) * 2
    toolbox = base.Toolbox()
    toolbox.register("attr_bit", random.choice, [0, 1])
    toolbox.register("individual_random", tools.initRepeat, creator.Individual, toolbox.attr_bit, n=IND_SIZE)
    toolbox.register("individual_zero", tools.initRepeat, creator.Individual, zero, n=IND_SIZE)
    toolbox.register("population", tools.initCycle, list, (toolbox.individual_zero,))

    # evolution operators
    toolbox.register("mate", tools.cxTwoPoint)  # or cxTwoPoint, cxUniform(indpb=float)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)  # many selection options
    if fitness == 'adjacent':
        toolbox.register("evaluate", evaluate_adjacent)
    if fitness == 'volume':
        toolbox.register("evaluate", evaluate_volume)

    start = time.time()
    fame = HallOfFame(maxsize=10)
    pop, logbook = algorithms.eaSimple(population=toolbox.population(n=1000), toolbox=toolbox, cxpb=0.3, mutpb=0.3,
                                       ngen=5000, halloffame=fame)
    end = time.time()

    best_rotations = fame[0]
    best_rotations = convert_bits_to_rotations(best_rotations)
    axis = puzzle.update_all_puzzle_axis(fame[0].axis, best_rotations)
    points = puzzle.calculate_points(axis)
    cube = set()
    for x in range(3):
        for y in range(3):
            for z in range(3):
                cube.add((x, y, z))
    print(f'best rotation sequence {fitness}, collisions, total rotations: {fame[0].fitness.values}')
    print(f'sequence of rotations: {best_rotations}')
    print(f'points of the cube: {points}')
    print(f'set difference: {set(points) - cube}')
    print(f'{end - start} seconds')


if __name__ == '__main__':
    main()
