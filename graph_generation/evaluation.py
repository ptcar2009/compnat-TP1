from pandas import read_csv
from copy import deepcopy
from sge import StructuredGrammarEvolution
import numpy as np

def train(params, X, Y, X_test, Y_test):
    model = StructuredGrammarEvolution(array_len=len(X[0]), **params)
    history = model.fit(X, Y, X_test, Y_test)
    return {"model": model, "history":history}

def evaluate(train_file, test_file, target_column, orig_params, n_iter):
    with open(train_file) as file:
        df_train = read_csv(file)
    X_train = df_train.drop([target_column], axis=1).values
    Y_train = df_train[target_column]

    with open(test_file) as file:
        df_test = read_csv(file)
    X_test = df_test.drop([target_column], axis=1).values
    Y_test = df_test[target_column]

    max_fitness = 0
    avg_fitness = 0
    total_fitness = 0
    fitnesses = []
    best_history = None
    avg_history = np.zeros(orig_params["generations"])
    max_history = np.zeros(orig_params["generations"])
    min_history = np.zeros(orig_params["generations"])
    test_history = np.zeros(orig_params["generations"])
    for it in range(n_iter):
        params = deepcopy(orig_params)
        params["checkpoint_prefix"] = params["checkpoint_prefix"] + f"_it_{it}_"
        train_result = train(params, X_train, Y_train, X_test, Y_test)
        fitness = train_result["model"](X_test, Y_test)
        total_fitness += fitness
        fitnesses += [fitness]
        avg_history += np.array(train_result["history"]["history"]["avg_fitness"])
        max_history += np.array(train_result["history"]["history"]["max_fitness"])
        min_history += np.array(train_result["history"]["history"]["min_fitness"])
        test_history += np.array(train_result["history"]["history"]["test_fitness"])
        if fitness >= max_fitness:
            best_history = train_result["history"]["history"]
        max_fitness = max(fitness, max_fitness)
        avg_fitness = total_fitness / (it + 1)
    fitnesses = np.array(fitnesses)

    return {
        "max": max_fitness,
        "avg": avg_fitness,
        "std": fitnesses.std(),
        "history": {
            "avg_fitness": avg_history/n_iter,
            "max_fitness": max_history/n_iter,
            "min_fitness": min_history/n_iter,
            "test_fitness": test_history/n_iter,
        },
        "best_history": best_history
    }