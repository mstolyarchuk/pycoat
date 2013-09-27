# coding: utf-8

import re
from functools import reduce


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
