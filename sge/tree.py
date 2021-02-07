import random
from copy import deepcopy
from typing import Any, Dict, List, Tuple, Union, Callable

# Métrica v_measure_score
import numpy
from numpy.core.numeric import Inf
from sympy.parsing.sympy_parser import eval_expr

max_levels = 2


class DistanceCreator:
    """Creates individuals and operations between them to run a symbolic regression on
    a distance function between points in a cluster. The genome is generated from a
    structured grammar as seen in https://www.researchgate.net/profile/Nuno_Lourenco2/publication/293043815_Unveiling_the_properties_of_structured_grammatical_evolution/links/5ef31c4192851cba7a462b0f/Unveiling-the-properties-of-structured-grammatical-evolution.pdf
    """

    def __init__(self,
                 point_size: int,
                 max_levels=6,
                 min_levels=3,
                 mutation_prob=0.5
                 ) -> None:
        """Initializer for the distance creator.  Min levels define the minimum levels for any tree branch.

        Args:
            point_size (int): Size of each point in the set that is to be regressed.
            max_levels (int, optional): Maximum levels of any tree branch.. Defaults to 6.
            min_levels (int, optional): Minimum levels of any tree branch. Defaults to 3.
            mutation_prob (float, optional): Probability for a given gene to be mutated when the inidividual is mutated. Defaults to 0.1.
        """
        self.rec_refs = {}
        self.mutation_prob = mutation_prob

        vars1 = []
        vars2 = []
        for i in range(point_size):
            vars1 += [f"X1[{i}]"]

        for i in range(point_size):
            vars2 += [f"X2[{i}]"]

        self.grammar = {
            **{f"<expr_{i}>": [f"<expr_{i+1}> <op> <expr_{i+1}>", f"<func> ( <expr_{i+1}> <op> <expr_{i+1}> )"] for i in range(min_levels)},
            **{f"<expr_{min_levels + i}>": [f"<expr_{min_levels + i+1}> <op> <expr_{min_levels + i+1}>", f"<func> ( <expr_{min_levels + i + 1}> <op> <expr_{min_levels + i + 1}> )", "<term>"] for i in range(max_levels - min_levels)},
            f"<expr_{max_levels}>": ["<term_1> <op> <term_2>", "<term_2> <op> <term_1>"],
            "<term>": [
                "<term_1>", "<term_2>"
            ],
            "<term_1>": [
                "<var_1>",
                "<pre-op> ( <var_1> )",
            ],
            "<term_2>": [
                "<var_2>",
                "<pre-op> ( <var_2> )",
            ],
            "<pre-op>": [
                "1/",
                "-",
                "+",
                "abs",
                "numpy.math.sqrt"
            ],
            "<func>": [
                "abs",
                ""
            ],
            "<op>": [
                "+",
                "*",
                "-",
                "/",
            ],
            "<var_1>": vars1,
            "<var_2>": vars2,
        }

        self.non_terminals = sorted(self.grammar.keys())

        # these two lines are described in the pseudocode of the reference paper
        rec_refs = self.countRecursiveReferences()
        self.ref_count = {
            key: self.findReferences(key, *rec_refs) for key in self.grammar.keys()
        }

    def createIndivitual(self) -> Dict[str, Any]:
        """Creates a random individual from the grammar created on instantiation.

        Returns:
            Dict[str, Any]: The individual generated, with fitness and fenotypes set to None
        """
        ind = {
            "genome": {
                key: numpy.random.randint(0, len(value), size=self.ref_count[key]) for (
                    key, value) in self.grammar.items()
            },
            "fitness": None,
            "fenotype": None,
        }
        return ind

    def countRecursiveReferences(self) -> Tuple[Dict[str, List[str]], Dict[str, Dict[str, int]]]:
        """Counts the maximum number of references any given production in the grammar can have on the final tree.

        Returns:
            Tuple[Dict[str, List[str]], Dict[str, Dict[str, int]]]: A list of each item that references a given item and the maximum references any non terminal has for each item.
        """
        countReferences = {}
        isReferencedBy = {}
        for nt in self.non_terminals: # for each non-terminal in the grammar
            for production in self.grammar[nt]: # for each possible production on that non terminal
                count = {}
                for option in production.split(): # iterate over the production's terms
                    count.setdefault(option, 0)
                    if option in self.non_terminals: # if the term is a non terminal
                        count[option] += 1  # the number of times that option has been referenced increases
                        isReferencedBy.setdefault(option, set())
                        isReferencedBy[option].add(nt)
                
                for key in count:
                    count.setdefault(key, 0)
                    countReferences.setdefault(key, {})
                    countReferences[key].setdefault(nt, 0)

                    countReferences[key][nt] = max(
                        countReferences[key][nt], count[key])   # the number of references of the non terminal is for this
                                                                # term is the maximum between all productions in this non terminal

        return isReferencedBy, countReferences


    def findReferences(self, nt: str,
                       isReferencedBy: Dict[str, List[str]],
                       countReferencesByProd: Dict[str, Dict[str, int]]
                       ) -> Dict[str, int]:
        """Gets the maximum number of references a non terminal production has.

        Args:
            nt (str): Non terminal to be analyzed
            isReferencedBy (Dict[str, List[str]]): List of references for each item
            countReferencesByProd (Dict[str, Dict[str, int]]): number of references each production has to each other production

        Returns:
            Dict[str, int]: the maximum number of references each non terminal has.
        """
        results = []

        if nt == "<expr_0>": # if its the root term, the maximum number of references is one
            return 1
        if nt in self.rec_refs: # basic memoization
            return self.rec_refs[nt]

        references = sum(countReferencesByProd[nt].values()) # otherwise, initialize the reference count 
                                                             # as the sum of the direct references for the term
        for ref in isReferencedBy[nt]: 
            results.append(self.findReferences(
                ref, isReferencedBy, countReferencesByProd))

        references = references * max(results) # then multiply the referece count by the maximum number of references
                                               # in its referents

        self.rec_refs[nt] = references # memoization
        
        return references

    def expand(self, individual: Dict[str, Union[str, Dict[str, List[int]], Callable]]):
        """Expands an individual from its genotype fo create its fenotype. The fenotype is created as a lambda
        function between two arrays that returns the distance between these two points.

        Args:
            individual (Dict[str, Union[str, Dict[str, List[int], [Callable]]): Individual to be expanded.
        """
        genes = individual["genome"]

        pattern = ["<expr_0>"] # starts the pattern as the root symbol

        current_index = {i: 0 for i in self.grammar.keys()} # initializes the indexes for each gene respective
                                                            # to a non terminal in the grammar

        i = 0
        while i < len(pattern): # while we have not reached the end of the expansion
            key = pattern[i]

            if key in self.grammar.keys():
                current_option = genes[key][current_index[key]] # option set by the gene

                out = self.grammar[key][current_option] 
                out = out.split(" ")
                
                pattern = pattern[:i] + out + pattern[i + 1:] # inserts the expantion into the current pattern

                current_index[key] += 1 # sets the index to look for the next gene
                continue
            i += 1

        individual["fenotype"] = eval("lambda X1, X2: " + " ".join(pattern)) # generates the function as a lambda function
                                                                             # the idea is to speed up the evaluation process
                                                                             # while still having the flexibility of the
                                                                             # eval function in python

    def mutate(self, genes: Dict[str, List[int]]) -> Dict[str, List[int]]:
        """Mutates a set of genes based on the probability of mutation set on instantiation.
        The mutation is applied point by point, from each section to each possible reference.

        Args:
            genes (Dict[str, List[int]]): The original genes to be mutated

        Returns:
            Dict[str, List[int]]: The new genes generated from the mutation
        """
        
        genes = deepcopy(genes)
        for key in genes.keys():
            # the mutation gets a set number of genes from the length of the genome and changes them to
            # new random choices. This number is proportional to the mutation probability
            mutated_indexes = random.choices(range(self.ref_count[key]), k=int(self.mutation_prob * self.ref_count[key]))
            genes[key][mutated_indexes] = numpy.random.randint(0, len(self.grammar[key]))

        return genes

    def crossover(self,
                  ind1: Dict[str, Union[str, Dict[str, List[int]], Callable]],
                  ind2: Dict[str, Union[str, Dict[str, List[int]], Callable]]
                  ) -> Dict[str, Union[str, Dict[str, List[int]], Callable]]:
        """Performs crossover between two individuals without altering the original individual. The crossover
        is applied by section of the gene, not by each gene.

        Args:
            ind1 (Dict[str, Union[str, Dict[str, List[int], [Callable]]): The first individual
            ind2 (Dict[str, Union[str, Dict[str, List[int], [Callable]]): The second individual

        Returns:
            Dict[str, Union[str, Dict[str, List[int], [Callable]]: The crossover between both individuals.
        """
        ind1 = deepcopy(ind1)
        ind2 = deepcopy(ind2)

        mask = random.choices(list(self.grammar.keys()),
                              k=random.randrange(len(self.grammar) - 2))
        for key in mask:
            ind1["genome"][key], ind2["genome"][key] = ind2["genome"][key], ind1["genome"][key]
        return ind1
