# coding: utf-8

import re
from functools import reduce

from .core import Layer


def _flatten(desc, args=None):
    """Simplifies a HL-notation description.

    Examples
    --------
    Simplify a description:

    >>> flatten('S(HL)^2(2H)(LH)^2')
    'SHLHL2HLHLH'

    >>> flatten('S(HL)^2(0.97H)(LH)^2')
    'SHLHL0.97HLHLH'

    Simplify a description contains variables:

    >>> variables = {'k': 2, 'a': 0.97}
    >>> flatten('S(HL)^k(aH)(LH)^k', variables)
    'SHLHL0.97HLHLH'
    """

    # Replace variables by input values
    if args:
        output = reduce(lambda x, y: x.replace(y, str(args[y])), args, desc)
    else:
        output = desc

    exponent_re = re.compile('\(([A-Z]+)\)\^(\d+)')
    output = exponent_re.sub(lambda m: int(m.group(2)) * m.group(1), output)

    # Finally, remove extra brackets, e.g. '(0.97H)' -> '0.97H'
    return re.sub('[()]', '', output)

def load(desc, indices):
    """Deserialize input to a ``Filter`` instance.

    Parameters
    ----------
    desc : str
       A HLN formatted string that describes a filter structure aka filter
       description.
    indices : dict
        Dictionary of layer abbreviations and refractive indices.

    Returns
    -------
    out : Filter

    Examples
    --------
    f = load('SHL', {'S': 1.51, 'H': 2.0, 'L': 1.38})
    f
    """
    raise NotImplementedError

def dump(afilter):
    """
    Examples
    --------
    f = load('SHLHL', {'S': 1.51, 'H': 2.0, 'L': 1.38})
    f.dump()
    'S(HL)^2'
    """
    raise NotImplementedError
