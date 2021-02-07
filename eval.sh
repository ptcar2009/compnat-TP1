# python main.py \
#     --mutation_prob 0.3 \
#     --crossover_prob 0.6 \
#     --train_file "data/breast_cancer_coimbra_train.csv" \
#     --test_file "data/breast_cancer_coimbra_test.csv" \
#     --target_column "Classification" \
#     --n_classes 2 \
#     --checkpoint_prefix cancer_k7 \
#     --generations 100 \
#     --population_size 100 \
#     --elitism 1 \
#     --max_levels 5 \
#     --min_levels 2 \
#     -k 7

# python main.py \
#     --mutation_prob 0.3 \
#     --crossover_prob 0.6 \
#     --train_file "data/breast_cancer_coimbra_train.csv" \
#     --test_file "data/breast_cancer_coimbra_test.csv" \
#     --target_column "Classification" \
#     --n_classes 2 \
#     --checkpoint_prefix cancer_k3 \
#     --generations 100 \
#     --population_size 100 \
#     --elitism 1 \
#     --max_levels 5 \
#     --min_levels 2 \
#     -k 3 &
python main.py \
    --mutation_prob 0.05 \
    --crossover_prob 0.9 \
    --train_file "data/glass_train.csv" \
    --test_file "data/glass_test.csv" \
    --target_column "glass_type" \
    --n_classes 7 \
    --checkpoint_prefix glass_low_mutation \
    --generations 100 \
    --population_size 50 \
    --max_levels 5 \
    --min_levels 2 \
    -k 3 &

python main.py \
    --mutation_prob 0.3 \
    --crossover_prob 0.6 \
    --train_file "data/glass_train.csv" \
    --test_file "data/glass_test.csv" \
    --target_column "glass_type" \
    --n_classes 7 \
    --checkpoint_prefix glass_low_crossover \
    --generations 100 \
    --population_size 50 \
    --max_levels 5 \
    --min_levels 2 \
    -k 3 &

python main.py \
    --mutation_prob 0.3 \
    --crossover_prob 0.6 \
    --train_file "data/glass_train.csv" \
    --test_file "data/glass_test.csv" \
    --target_column "glass_type" \
    --n_classes 7 \
    --checkpoint_prefix glass_k7 \
    --generations 100 \
    --population_size 100 \
    --elitism 1 \
    --max_levels 5 \
    --min_levels 2 \
    -k 7 &

python main.py \
    --mutation_prob 0.3 \
    --crossover_prob 0.6 \
    --train_file "data/glass_train.csv" \
    --test_file "data/glass_test.csv" \
    --target_column "glass_type" \
    --n_classes 7 \
    --checkpoint_prefix glass_k3 \
    --generations 100 \
    --population_size 100 \
    --elitism 1 \
    --max_levels 5 \
    --min_levels 2 \
    -k 3 &

python main.py \
    --mutation_prob 0.3 \
    --crossover_prob 0.6 \
    --train_file "data/glass_train.csv" \
    --test_file "data/glass_test.csv" \
    --target_column "glass_type" \
    --n_classes 7 \
    --checkpoint_prefix glass_pop_30 \
    --generations 100 \
    --population_size 30 \
    --elitism 1 \
    --max_levels 5 \
    --min_levels 2 \
    -k 3 &

python main.py \
    --mutation_prob 0.3 \
    --crossover_prob 0.6 \
    --train_file "data/glass_train.csv" \
    --test_file "data/glass_test.csv" \
    --target_column "glass_type" \
    --n_classes 7 \
    --checkpoint_prefix glass_pop_50 \
    --generations 100 \
    --population_size 50 \
    --elitism 1 \
    --max_levels 5 \
    --min_levels 2 \
    -k 3 &

python main.py \
    --mutation_prob 0.3 \
    --crossover_prob 0.6 \
    --train_file "data/glass_train.csv" \
    --test_file "data/glass_test.csv" \
    --target_column "glass_type" \
    --n_classes 7 \
    --checkpoint_prefix glass_pop_100 \
    --generations 100 \
    --population_size 100 \
    --elitism 1 \
    --max_levels 5 \
    --min_levels 2 \
    -k 3 &

python main.py \
    --mutation_prob 0.3 \
    --crossover_prob 0.6 \
    --train_file "data/glass_train.csv" \
    --test_file "data/glass_test.csv" \
    --target_column "glass_type" \
    --n_classes 7 \
    --checkpoint_prefix glass_pop_500 \
    --generations 100 \
    --population_size 500 \
    --elitism 1 \
    --max_levels 5 \
    --min_levels 2 \
    -k 3 &

python main.py \
    --mutation_prob 0.3 \
    --crossover_prob 0.6 \
    --train_file "data/glass_train.csv" \
    --test_file "data/glass_test.csv" \
    --target_column "glass_type" \
    --n_classes 7 \
    --checkpoint_prefix glass_gen_30 \
    --generations 30 \
    --population_size 100 \
    --elitism 1 \
    --max_levels 5 \
    --min_levels 2 \
    -k 3 &

python main.py \
    --mutation_prob 0.3 \
    --crossover_prob 0.6 \
    --train_file "data/glass_train.csv" \
    --test_file "data/glass_test.csv" \
    --target_column "glass_type" \
    --n_classes 7 \
    --checkpoint_prefix glass_gen_50 \
    --generations 50 \
    --population_size 100 \
    --elitism 1 \
    --max_levels 5 \
    --min_levels 2 \
    -k 3 &

python main.py \
    --mutation_prob 0.3 \
    --crossover_prob 0.6 \
    --train_file "data/glass_train.csv" \
    --test_file "data/glass_test.csv" \
    --target_column "glass_type" \
    --n_classes 7 \
    --checkpoint_prefix glass_gen_100 \
    --generations 100 \
    --population_size 100 \
    --elitism 1 \
    --max_levels 5 \
    --min_levels 2 \
    -k 3 &

python main.py \
    --mutation_prob 0.3 \
    --crossover_prob 0.6 \
    --train_file "data/glass_train.csv" \
    --test_file "data/glass_test.csv" \
    --target_column "glass_type" \
    --n_classes 7 \
    --checkpoint_prefix glass_gen_500 \
    --generations 500 \
    --population_size 100 \
    --elitism 1 \
    --max_levels 5 \
    --min_levels 2 \
    -k 3 &