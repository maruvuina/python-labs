import random
import numpy as np

NUMBER_OF_WALKS = 5000
NUMBER_OF_STEPS = 500
TRANSIT_TIME = 30

def generator_type_rand(number_of_walks, number_of_steps): 
    steps = []
    for _ in range(number_of_walks):
        tempStep = []
        for _ in range(number_of_steps + 1):
            step = 1 if random.randint(0, 1) else -1
            tempStep.append(step)
        steps.append(tempStep)
    return np.array(steps)

def generator_type_randint(number_of_walks, number_of_steps): 
    steps = np.random.randint(0, 2, size=(number_of_walks, number_of_steps + 1), dtype='int')
    steps = np.where(steps > 0, 1, -1)
    return steps

def many_random_walk(number_of_walks, number_of_steps, generator_type):
    steps = []
    if generator_type == 'randint':
        steps = generator_type_randint(number_of_walks, number_of_steps)
    else:
        steps = generator_type_rand(number_of_walks, number_of_steps)
    steps[:, 0] = 0
    walks = np.cumsum(steps, axis = 1)
    return walks

def find_minimum_transition_time(walks, transit_time):
    transition_times = np.full(shape = (walks.shape[0]), fill_value = np.nan)
    for index, walker in enumerate(walks):
        iterator = np.nditer(walker, flags=['c_index'])
        while not iterator.finished:
            positive_iterator_value = abs(iterator[0])
            if positive_iterator_value >= transit_time:
                transition_times[index] = iterator.index
                break
            iterator.iternext()
        pass
    transition_times_without_nan = transition_times[np.logical_not(np.isnan(transition_times))]
    if transition_times_without_nan.size == 0:
        return 'transition time not reached'
    return transition_times_without_nan.min()

def main():
    generator_type = 'rand'
    walks = many_random_walk(NUMBER_OF_WALKS, NUMBER_OF_STEPS, generator_type)
    print('Min value:', walks.min())
    print('Max value:', walks.max())
    print('Minimum transition time is', find_minimum_transition_time(walks, TRANSIT_TIME), 'through', TRANSIT_TIME)

main()
