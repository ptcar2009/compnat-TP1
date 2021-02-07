from matplotlib import pyplot as plt


def plot_checkpoint(history, file_name, title, ):
    x = list(range(len(history["max_fitness"])))
    plt.plot(x, history["max_fitness"], label="Max Fitness")
    plt.plot(x, history["min_fitness"], label="Min Fitness")
    plt.plot(x, history["avg_fitness"], label="Average Fitness")
    plt.plot(x, history["test_fitness"], label="Test Fitness")
    plt.legend()
    plt.title(title)
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.savefig(file_name)
