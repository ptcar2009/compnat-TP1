from .evaluation import evaluate
from .history import plot_checkpoint


def generate_graphs(train_file, test_file, target_column, n_classes, params):
    params["classes"] = n_classes
    history = evaluate(train_file, test_file,
                       target_column, params, 10)["history"]
    plot_checkpoint(history, "graphs/" + params["checkpoint_prefix"],
                    str(params["checkpoint_prefix"]).replace("_", " ").capitalize()
                    )
