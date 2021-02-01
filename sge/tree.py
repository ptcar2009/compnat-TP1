import random
from copy import deepcopy
# Métrica v_measure_score
import numpy
from numpy.core.numeric import Inf
from operator import itemgetter

from sympy.parsing.sympy_parser import eval_expr
max_levels = 2


class DistanceCreator:

    def __init__(self,
                 point_size,
                 max_levels=6,
                 min_levels=3,
                 mutation_prob=0.1
                 ) -> None:
        self.upper = {}
        self.mutation_prob = mutation_prob
        vars1 = []
        vars2 = []
        for i in range(point_size):
            vars1 += [f"X1[{i}]"]
            
        for i in range(point_size):
            vars2 += [f"X2[{i}]"]


        self.grammar = {
            **{f"<expr_{i}>": [f"<expr_{i+1}> <op> <expr_{i+1}>", f"( <expr_{i+1}> <op> <expr_{i+1}> )"] for i in range(min_levels)},
            **{f"<expr_{min_levels + i}>": [f"<expr_{min_levels + i+1}> <op> <expr_{min_levels + i+1}>", f"( <expr_{min_levels + i+1}> <op> <expr_{min_levels + i+1}> )", "<term>"] for i in range(max_levels - min_levels)},
            f"<expr_{max_levels}>": ["<term> <op> <term>", "<term>"],
            "<term>": [
                "<var>",
                "( <pre-op> <var> )",
                "<func> ( <var> )",
            ],
            "<pre-op>": [
                "1/",
                "-",
                "+",
            ],
            "<func>": [
                "abs"
            ],
            "<op>": [
                "+",
                "*",
                "-",
                "/",
            ],
            "<var>":  ["<var_1>", "<var_2>"],
            "<var_1>": vars1,
            "<var_2>": vars2,
        }
        self.non_terminals = sorted(self.grammar.keys())
        rec_refs = self.countRecursiveReferences()
        self.ref_count = {key: self.findReferences(
            key, *rec_refs) for key in self.grammar.keys()}

    def createIndivitual(self):
        return {
            "genome": {
                key: [random.randrange(len(value)) for _ in range(self.ref_count[key])] for (
                    key, value) in self.grammar.items()
            },
            "fitness": None,
            "fenotype": None,
        }

    def countRecursiveReferences(self):
        countReferences = {}
        isReferencedBy = {}
        count = {}
        for nt in self.non_terminals:
            for production in self.grammar[nt]:
                for option in production.split():
                    visited = {}
                    if option in self.non_terminals:
                        if option in visited:
                            continue
                        isReferencedBy.setdefault(option, [])
                        isReferencedBy[option] += [nt]

                        count.setdefault(option, 0)
                        count[option] = count[option] + 1
                        visited[option] = True
            for key in count:
                count.setdefault(key, 0)
                countReferences.setdefault(key, {})
                countReferences[key].setdefault(nt, 0)
                countReferences[key][nt] = max(
                    countReferences[key][nt], count[key])

        return isReferencedBy, countReferences

    def findReferences(self, nt, isReferencedBy, countReferencesByProd):
        results = []
        if nt == "<expr_0>":
            return 1
        if nt in self.upper.keys():
            return self.upper[nt]
        references = max(countReferencesByProd[nt].values())
        for ref in isReferencedBy[nt]:
            results.append(self.findReferences(
                ref, isReferencedBy, countReferencesByProd))
        references = references * max(results)
        self.upper[nt] = references
        return references

    def expand(self,individual):
        genes = individual["genome"]

        pattern = ["<expr_0>"]
        current_index = {i: 0 for i in self.grammar.keys()}
        while True:
            over = True
            for i, e in enumerate(pattern):
                if e in self.grammar.keys():
                    out = self.grammar[e][genes[e][current_index[e]]]
                    out = str(out)
                    out = out.split(" ")
                    pattern = pattern[:i] + out + pattern[i + 1:]
                    current_index[e] += 1
                    over = False
                    break   

            if over:
                break
        individual["fenotype"] = eval("lambda X1, X2: " + " ".join(pattern))



    def mutate(self, genes):
        genes = deepcopy(genes)
        for key, value in genes.items():
            mutation_mask = [random.random() for _ in range(len(value))]
            for i in range(len(value)):
                if mutation_mask[i] < self.mutation_prob:
                    genes[key][i] = random.randrange(len(self.grammar[key]))
        return genes

    def crossover(self, tree1, tree2):
        tree1 = deepcopy(tree1)
        tree2 = deepcopy(tree2)
        mask = random.choices(list(self.grammar.keys()),
                              k=random.randrange(len(self.grammar)))
        for key in mask:
            tree1["genome"][key], tree2["genome"][key] = tree2["genome"][key], tree1["genome"][key]
        return tree1
