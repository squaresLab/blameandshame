import git
from typing import Callable, List


def infer(evidence: git.Commit,
          f: Callable[int, float]) -> Callable[float, float]:
    """
    Infers the probability distribution `P(modified | G)` from supplied
    evidence and a given factor.
    """
    # infer P(modified) by observation of the provided evidence
    p_modified = None

    # compute the probability distribution over the domain of the factor
    # using the supplied evidence
    p_factor = None

    # compute P(modified | G=x)
    p_modified_given_factor = None


def divergence(observed: Localization, expected: Localization) -> float:
    """
    Measures the Kullback-Leibler divergence between an observed probability
    distribution, produced by a candidate model, and an expected probability,
    used to represent the ideal probability distribution that could be produced
    by a model, where each line that was modified is assigned a probability
    of 1.
    """
    raise NotImplementedError
