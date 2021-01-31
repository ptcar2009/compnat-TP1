import json
from operator import itemgetter
from .tree import DistanceCreator
import random
from copy import deepcopy
import warnings
from sklearn.metrics.cluster import v_measure_score
import numpy
# Funções para clustering utilizando PyClustering
# Importante: para realização do TP é imprescindível que seu PyClustering esteja na versão 0.10.1 ou superior
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.utils.metric import distance_metric, type_metric


class StructuredGrammarEvolution:
    def __init__(self,
                 array_len,
                 population_size=100,
                 mutation_prob=0.3,
                 crossover_prob=0.1,
                 k=3,
                 elitism=3,
                 max_levels=2,
                 min_levels=2,
                 generations=100,
                 classes=2,
                 checkpoint=5,
                 checkpoint_prefix=""
                 ) -> None:
        warnings.filterwarnings("ignore")
        self.population_size = population_size
        self.crossover_prob = crossover_prob
        self.k = k
        self.mutation_prob = mutation_prob
        self.elitism = elitism
        self.distance_creator = DistanceCreator(
            array_len, max_levels, min_levels, mutation_prob=mutation_prob)
        self.generations = generations
        self.classes = classes
        self.checkpoint = checkpoint
        self.checkpoint_prefix = checkpoint_prefix

    def __call__(self, X, Y) -> float:
        return self._eval(self.best_indivitual, X, Y)

    def initializePopulation(self):
        self.population = [self.distance_creator.createIndivitual()
                           for _ in range(self.population_size)]

    def tourney(self):
        individuals = random.sample(self.population, self.k)
        individuals.sort(key=lambda i: i['fitness'], reverse=True)
        return deepcopy(individuals[0])

    def create_generation(self):
        self.population.sort(key=lambda x: x["fitness"], reverse=True)
        new_pop = self.population[:self.elitism]
        while len(new_pop) < self.population_size:
            new_t = self.tourney()
            if random.random() < self.mutation_prob:
                new_t["genome"] = self.distance_creator.mutate(new_t["genome"])
                new_t["fitness"] = new_t["fenotype"] = None

            if random.random() < self.crossover_prob:
                t1 = self.tourney()
                t2 = self.tourney()
                new_t = self.distance_creator.crossover(t1, t2)
                new_t["fitness"] = new_t["fenotype"] = None
            new_pop.append(new_t)
        self.population = new_pop

    def _eval(self, ind, X, Y):
        if ind["fenotype"] == None:
            self.distance_creator.expand(ind)
        manhattan_metric = distance_metric(
            type_metric.USER_DEFINED,
            func=ind["fenotype"])

        # define número de clusters
        k = self.classes
        # Inicializa centróides utilizando método K-Means++
        try:
            initial_centers = kmeans_plusplus_initializer(X, k).initialize()
        # cria instância do K-Means utilizando sua métrica de distância
            kmeans_instance = kmeans(
                X, initial_centers, metric=manhattan_metric)
        except ZeroDivisionError:
            return 0
        # treina o modelo
        kmeans_instance.process()
        # recupera os clusters gerados
        clusters = kmeans_instance.get_clusters()
        pred = numpy.zeros(len(X))
        for i in range(len(clusters)):
            pred[clusters[i]] = i+1

        return v_measure_score(Y, pred)

    def evaluate_individual(self, ind):
        try:
            score = self._eval(ind, self.X, self.Y)
        except ZeroDivisionError:
            score = 0
        ind["fitness"] = score

    def fit(self, X, Y):
        self.X = X
        self.Y = Y
        self.initializePopulation()
        avg_fitness = []
        max_fitness = []
        min_fitness = []
        for it in range(self.generations):
            print(f"Generation {it + 1} out of {self.generations}")
            total_fit = 0
            min_fit = 1
            max_fit = 0
            for i, d in enumerate(self.population):
                if d["fitness"] == None:
                    self.evaluate_individual(d)
                if d["fitness"] < min_fit:
                    min_fit = d["fitness"]
                if d["fitness"] > max_fit:
                    max_fit = d["fitness"]
                total_fit += d["fitness"]
                prog_size = 20
                prog = int((i + 1)/len(self.population) * prog_size)
                print("\r|{}{}| avg: {:.5f} - max: {:.5f} - min: {:.5f}".format(
                    prog * "█", (prog_size - prog) * " ", total_fit/(i + 1), max_fit, min_fit), end="")
            print()
            max_fitness += [max_fit]
            min_fitness += [min_fit]
            avg_fitness += [total_fit / len(self.population)]

            self.population.sort(reverse=True, key=itemgetter("fitness"))
            self.best_indivitual = self.population[0]
            if it % self.checkpoint == 0 and it != 0:
                print(
                    f"Saving checkpoint at checkpoints/checkpoint_{it//5}.json")
                with open(f"checkpoints/{self.checkpoint_prefix}checkpoint_{it//5}.json", "w") as f:
                    json.dump({
                        "max_fitness": max_fitness,
                        "min_fitness": min_fitness,
                        "avg_fitness": avg_fitness,
                        "best_individual": {
                            "fitness": self.best_indivitual["fitness"],
                            "genome": self.best_indivitual["genome"],
                        },
                    }, f)
            self.create_generation()

        for i, d in enumerate(self.population):
            if d["fitness"] == None:
                self.evaluate_individual(d)
        return {
            "history": {
                "max_fitness": max_fitness,
                "min_fitness": min_fitness,
                "avg_fitness": avg_fitness,
            },
            "best_individual": self.best_indivitual,
        }
