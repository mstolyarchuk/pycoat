# coding: utf-8

from __future__ import division


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
