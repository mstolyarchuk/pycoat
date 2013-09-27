# coding: utf-8

from __future__ import division

import numpy as np
from colormath.color_objects import SpectralColor


def construct_filter(hln, indicies, thickness):
    from .core import Filter, Layer

    sub = indicies['S']
    layers = []
    for abbr, nt in zip(hln[1:], thickness):
        l = Layer(indicies[abbr], nt)
        layers.append(l)

    return Filter(sub, layers)


wavelength_conv = {
    'angstrom': 1e-10,
    'nm': 1e-9,
    'micron': 1e-6
}

def rescale(x, to_units, from_units='nm'):
    try:
        scale = wavelength_conv[from_units] / wavelength_conv[to_units]
    except KeyError:
        raise ValueError('Unknown units')

    return x * scale


def _prepare_rta(rta, prop):
    indices = np.arange(rta.size)
    mask = []
    for (w, idx) in zip(rta.wavelength, indices):
        if w % 10 == 0:
            mask.append(idx)

    filtered = rta.take(mask)
    return {
        'spec_%dnm' % w: x for (w, x) in (zip(filtered.wavelength, filtered[prop]))
    }

def rta_to_xyz(rta, prop, observer=2, illuminant='d65'):
    spectrum_dict = _prepare_rta(rta, prop)
    spc = SpectralColor(observer=observer, illuminant=illuminant, **spectrum_dict)
    return spc.convert_to('xyz')
