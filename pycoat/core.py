# coding: utf-8

import numpy as np
import quantities as pq

class Layer(object):
    """A single layer of a certain thickness.

    Parameters
    ----------
    n : float or complex
        A refractive index.
    nt : float
        An optical thickness.
    """
    def __init__(self, n, nt):
        self.n = n
        self.nt = nt


class Filter(object):
    """A single-layer or multilayer coating/substrate system.

    Parameters
    ----------
    substrate : float
        The medium refractive index that a thin film is coated on.
    layers : list
        List of :class:`Layer` instance.
    """
    def __init__(self, substrate, layers):
        self.substrate = substrate
        self.layers = layers

    def optical_thickness(self, reference, units='nm'):
        nt = [x.nt for x in self.layers]
        total = pq.Quantity(np.sum(nt) * reference / 4, units='nm')
        return total.rescale(units=units).item()

    def physical_thickness(self, reference, units='nm'):
        t = [ x.nt / x.n for x in self.layers]
        total = pq.Quantity(np.sum(t) * reference / 4, units='nm')
        return total.rescale(units=units).item()
