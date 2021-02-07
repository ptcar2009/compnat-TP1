from graph_generation import generate_graphs
from argparse import ArgumentParser

parser = ArgumentParser("sge")

parser.add_argument("--population_size", "-p", default=500,
                    dest="population_size", type=int)
parser.add_argument("--mutation_prob", "-m", default=0.3,
                    dest="mutation_prob", type=float)
parser.add_argument("--elitism", "-e", default=10,
                    dest="elitism", type=int)
parser.add_argument("--max_levels", default=4,
                    dest="max_levels", type=int)
parser.add_argument("--min_levels", default=2,
                    dest="min_levels", type=int)
parser.add_argument("--crossover_prob", "-c", default=0.6,
                    dest="crossover_prob", type=float)
parser.add_argument("--tourney_size", "-k", default=3,
                    dest="k", type=int)
parser.add_argument("--generations", "-g", default=100,
                    dest="generations", type=int)
parser.add_argument("--checkpoint_every", default=5,
                    dest="checkpoint", type=int)
parser.add_argument("--checkpoint_prefix", default="",
                    dest="checkpoint_prefix", type=str)
parser.add_argument("--train_file", required=True,
                    dest="train_file", type=str)
parser.add_argument("--test_file", required=True,
                    dest="test_file", type=str)
parser.add_argument("--target_column", required=True, dest="target_column", type=str)
parser.add_argument("--n_classes", required=True, dest="n_classes", type=int)
parser.add_argument("--n_iter", "-n", dest="n_iter", default=10, type=int)

if __name__ == "__main__":
    args = parser.parse_args()
    params = {
        "population_size": args.population_size,
        "mutation_prob": args.mutation_prob,
        "elitism": args.elitism,
        "max_levels": args.max_levels,
        "min_levels": args.min_levels,
        "crossover_prob": args.crossover_prob,
        "k": args.k,
        "generations": args.generations,
        "checkpoint": args.checkpoint,
        "checkpoint_prefix": args.checkpoint_prefix,
    }

    generate_graphs(args.train_file,
                    args.test_file, args.target_column, args.n_classes, params)
