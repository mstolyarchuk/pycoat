# coding: utf-8

import numpy as np

from .. import fresnel, core
from .utils import rta_to_xyz


def spectral(thickness, hln, indicies, targets, reference, prop='R'):
    N = len(targets)
    k = 2

    f = construct_filter(hln, indicies, thickness)
    wavelengths = [t[0] for t in targets]
    rta = fresnel.rta_wavelength(f, wavelengths, reference)

    result = 0
    for i, target in enumerate(targets):
        result = result + target[2] * np.power(target[1] - rta[i][prop], k)

    return np.power(result / N, 1/k)


def xy(thickness, hln, indicies, targets, reference):
    N = len(targets)

    f = construct_filter(hln, indicies, thickness)
    visible = range(380, 771, 10)

    xy_list = []
    for angle, _ in targets:
        rta = fresnel.rta_wavelength(f, visible, reference, angle=angle)
        xyz = rta_to_xyz(rta, 'R', illuminant='D65')
        xyy = xyz.convert_to('xyY')
        xy_list.append((xyy.xyy_x, xyy.xyy_y))

    result = 0
    for xy, t in zip(xy_list, targets):
        result = result + (xy[0] - t[1][0])**2 + (xy[1] - t[1][1])**2

    return result
