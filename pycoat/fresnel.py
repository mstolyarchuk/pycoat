# coding: utf-8

from __future__ import division

import numpy as np


def _calculate_rta(M, n_s, n_a):
    (m_11, m_12), (m_21, m_22) = M.A

    # Reflectance and transmittance amplitude coefficients
    r = ((n_a*m_11 - n_s*m_22 + n_a*n_s*m_12 - m_21) /
        (n_a*m_11 + n_s*m_22 + n_a*n_s*m_12 + m_21))

    t = (2 * n_a / \
        (n_a*m_11 + n_s*m_22 + n_a*n_s*m_12 + m_21))

    # Energy coefficients
    R = abs(r)**2
    T = n_s / n_a * abs(t)**2
    A = 1.0 - R - T

    # FIXME
    return R, T.real, A.real


def _rta_wavelength(f, arange, reference, angle=0, pol=None):
    n_s, n_a = f.substrate, 1.0

    angle = np.deg2rad(angle)
    if angle != 0:
        # Normalize anonymous functions
        normalize = {
            'S': lambda x, y: x * y,
            'P': lambda x, y: x / y
        }

        # q_a
        cos = np.cos(angle)
        q_a = normalize[pol](n_a, cos)

        # q_s
        sin_s = n_a / n_s * np.sin(angle)
        cos_s = np.sqrt(1+0j - np.square(sin_s))
        q_s = normalize[pol](n_s, cos_s)
    else:
        q_a = n_a
        q_s = n_s

    records = []
    for wavelength in arange:
        ratio = reference / wavelength

        # Find the product of the characteristic matrices for each layer
        # M = Mm * Mm-1 * ... * M1, where m - number of the layers
        M = np.eye(2)
        for layer in list(reversed(f.layers)):
            phase = 2 * np.pi * layer.nt * ratio
            phase = np.complex(phase)

            n = layer.n
            if angle != 0:
                sin_n = n_a / n * np.sin(angle)
                cos_n = np.sqrt(1+0j - np.square(sin_n))
                q = normalize[pol](n, cos_n)
                phase = phase * cos_n
            else:
                q = n

            # Populate the charateristic matrix of the layerln = 'SHLHL'
            M_layer = np.matrix([[np.cos(phase), (-1/q * np.sin(phase)) * 1j],
                                 [(-q * np.sin(phase)) * 1j, np.cos(phase)]])
            M = M * M_layer

        records.append((wavelength,) + _calculate_rta(M, q_s, q_a))

    return np.rec.fromrecords(records, names='wavelength, R, T, A')


def rta_wavelength(f, arange, reference, angle=0, pol=None):
    """Determines wavelength dependence of reflectance, transmittance and
    absorptance of a coating.

    Parameters
    ----------
    f : Optical filter
    arange : array_like
        The measurement wavelength range.
    reference :
        The reference wavelength.
    angle : number, optional
        The angle of incidence.
    pol : 'S' or 'P', optional
        Specifies a polarization state (the default is None, which means
        do both calculations).
    """
    if angle == 0:
        return _rta_wavelength(f, arange, reference)
    else:
        if pol:
            return _rta_wavelength(f, arange, reference, angle=angle, pol=pol)
        else:
            rta_s = _rta_wavelength(f, arange, reference, angle=angle, pol="S")
            rta_p = _rta_wavelength(f, arange, reference, angle=angle, pol="P")

            rta = np.recarray((len(arange),),
                dtype=[('wavelength', float),
                       ('R', float), ('Rs', float), ('Rp', float),
                       ('T', float), ('Ts', float), ('Tp', float),
                       ('A', float), ('As', float), ('Ap', float)]
            )

            rta['wavelength'] = rta_s['wavelength']

            rta['Rs'], rta['Ts'], rta['As'] = rta_s['R'], rta_s['T'], rta_s['A']
            rta['Rp'], rta['Tp'], rta['Ap'] = rta_p['R'], rta_p['T'], rta_p['A']

            rta['R'] = (rta['Rs'] + rta['Rp']) / 2.0
            rta['T'] = (rta['Ts'] + rta['Tp']) / 2.0
            rta['A'] = 1 - rta['R'] - rta['T']

            return rta


def rta_angle(f, angles, reference, wavelength=None):
    wavelength = wavelength or reference
    result = {}

    get_rta = rta_wavelength(afilter, reference, [wavelength])

    for angle in angles:
        if angle == 90:
            angle = 89.9999

        rta = rta_wavelength(f, [wavelength], reference, angle)
        result[angle] = rta

    return result
