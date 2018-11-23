import random
from time import time
import inspyred
import evolutionary_problem as problem
import constants

from inspyred import ec


def main(prng=None, display=False):
    if prng is None:
        prng = random.Random()
        prng.seed(time())

    ea = inspyred.ec.GA(prng)

    ea.selector = inspyred.ec.selectors.tournament_selection

    ea.variator = [problem.mutate,
                   problem.crossover]

    # ea.replacer = inspyred.ec.replacers.steady_state_replacement
    ea.replacer = inspyred.ec.replacers.plus_replacement

    ea.terminator = inspyred.ec.terminators.generation_termination

    ea.observer = problem.observer

    final_pop = ea.evolve(generator=problem.generator,
                          evaluator=problem.evaluator,
                          pop_size=constants.POPULATION_SIZE,
                          bounder=problem.bounder,
                          maximize=problem.maximize,
                          tournament_size=2,
                          max_generations=1000,
                          mutation_rate=1.0)  # we need to control mutation manually with m_probs in constants

    if display:
        best = max(final_pop)
        print('Best Solution: \n{0}'.format(str(best)))
    return ea


if __name__ == '__main__':
    main(display=True)