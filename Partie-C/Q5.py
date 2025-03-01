import sys
import os
import random
import url_parser
import matplotlib.pyplot as plt
from num2words import num2words

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Partie-A')))
from random_fuzzer import RandomFuzzer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Partie-B')))
from mutation_fuzzer import MutationFuzzer


class Coverage:
    def __init__(self):
        self.covered_lines = set()

    def trace(self, frame, event, arg):
        if event == "line":
            code = frame.f_code
            filename = code.co_filename
            lineno = frame.f_lineno
            self.covered_lines.add((filename, lineno))
        return self.trace

    def start(self):
        sys.settrace(self.trace)

    def stop(self):
        sys.settrace(None)

    def coverage(self):
        return self.covered_lines


def calculate_cumulative_coverage(input_population, function):
    cumulative_coverage = []
    all_coverage = set()

    for inp in input_population:
        coverage = Coverage()
        coverage.start()
        try:
            function(inp)
        except Exception:
            pass
        coverage.stop()
        all_coverage |= coverage.coverage()
        cumulative_coverage.append(len(all_coverage))
    return cumulative_coverage


def plot(cumulative_coverage):
    plt.plot(cumulative_coverage)
    plt.title('Coverage')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered')
    plt.show()

# Exemple de couverture avec MutationFuzzer à modifier pour les tâches de la Partie-C
class MyFuzzer:
    def __init__(self, trials=500):
        self.trials = trials

    def fuzz(self):
        return str(random.randint(-1000000, 1000000))

random.seed(2125787)
trials = 500

random_fuzzer = RandomFuzzer()
random_inputs = [random_fuzzer.fuzz() for _ in range(trials)]
random_coverage = calculate_cumulative_coverage(random_inputs, num2words)

mutation_fuzzer = MutationFuzzer(seeds=["3452020"])
mutation_inputs = [mutation_fuzzer.fuzz() for _ in range(trials)]
mutation_coverage = calculate_cumulative_coverage(mutation_inputs, num2words)

my_fuzzer = MyFuzzer()
my_inputs = [my_fuzzer.fuzz() for _ in range(trials)]
my_coverage = calculate_cumulative_coverage(my_inputs, num2words)

plot([random_coverage, mutation_coverage, my_coverage])

