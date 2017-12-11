def infer():
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
