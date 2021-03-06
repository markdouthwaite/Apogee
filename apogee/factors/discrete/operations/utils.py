"""
The MIT License

Copyright (c) 2017-2020 Mark Douthwaite
"""

import numpy as np


def assignment_to_index(assignment, card):
    return np.ravel_multi_index(assignment, card)


def index_to_assignment(index, card):
    return np.asarray(np.unravel_index(index, card), dtype=np.int64)


def get_cardinality(graph, *identifiers):
    """
    Get the cardinality of all nodes in given FactorGraph of DiscreteFactors.

    """

    cards = []
    for node in graph:
        if node.phi.variable in identifiers:
            cards.append(node.phi.cardinality(node.phi.variable))

    return cards


def ones_like_card(card):
    """
    Generate an array of ones of a length specified by the product of an array (card).

    """

    return np.ones(np.product(card))


def zeros_like_card(card):
    """
    Generate an array of zeros of a length specified by the product of an array (card).

    """

    return np.ones(np.product(card))


def format_discrete_marginals(*marginals, **kwargs):
    """
    Prettify some discrete marginal distributions
    
    Parameters
    ----------
    marginals: tuple
        A tuple of marginalised DiscreteFactors.
    kwargs: 
        dp, int, the precision to format the output to. Default: 4. 
        labels, dict, {k: v} where k: variable id, v: variable label.
        states, dict, {k: v} where k: variable id, v: list of strings, where strings are state labels.
        squeeze, bool, if True, the function will drop the variable label if only one marginal distribution is passed.
        unpack,  
        
    Returns
    -------
    out: dict

    TODO: Break up this function.
    
    """

    dp = kwargs.get("dp", 4)
    labels = kwargs.get(
        "labels", None
    )  # this is overridden if 'states' keyword is passed.
    states = kwargs.get("states", None)
    squeeze = kwargs.get("squeeze", False)
    space = kwargs.get("space", "p")  # 'prob' probability space, else 'log', log space
    unpack = kwargs.get("unpack", True)
    normed = kwargs.get("normed", True)

    if normed:
        marginals = [x.normalise() for x in marginals]

    if squeeze:
        unpack = False

    if unpack or states is not None:
        data = {
            mgnl.scope[0]: {
                j: round(p if space == "p" else np.log(p), dp)
                for j, p in enumerate(mgnl.parameters)
            }
            for mgnl in marginals
        }

        if states is not None:
            for k, v in data.items():
                for j, p in data[k].items():
                    if k in states.keys():
                        data[k][states[k][j]] = data[k][j]
                        del data[k][j]
    else:
        data = {mgnl.scope[0]: np.around(mgnl.parameters, dp) for mgnl in marginals}

    if labels is not None:
        for k, v in data.items():
            if k in labels.keys():
                data[labels[k]] = data[k]
                del data[k]

    if squeeze:
        if len(data.keys()) == 1:
            data = list(data.values())[0]

    return data
