# coding: utf-8

from __future__ import division

import unittest

from pycoat.core import Filter, Layer
from pycoat.hln import load
from pycoat import utils


class TestCore(unittest.TestCase):
    def test_filter_thickness(self):
        f = Filter(1.52, [Layer(1.35, 1), Layer(1.6, 1)])

        self.assertAlmostEqual(f.optical_thickness(500), 250)
        self.assertAlmostEqual(f.optical_thickness(500, 'micron'), 0.25)

        self.assertAlmostEqual(f.physical_thickness(500), 170.7175, 3)
        self.assertAlmostEqual(f.physical_thickness(500, 'micron'), 0.1707, 3)


class TestHln(unittest.TestCase):
    def test_load(self):
        f = load('SHL', {'S': 1.51, 'H': 2.0, 'L': 1.38})
        self.assertEqual(f.substrate, 1.51)
        self.assertEqual(f.layers[1].n, 1.38)
        self.assertEqual(f.layers[1].nt, 1)

    @unittest.skip('')
    def test_dump(self):
        f = load('SHLHL', {'S': 1.51, 'H': 2.0, 'L': 1.38})
        self.assertEqual(f.dump(), 'S(HL)^2')


class TestUtils(unittest.TestCase):
    def test_construct_filter(self):
        indices = {'S': 1.51, 'H': 2.0, 'L': 1.38}
        thickness = [0.625, 1.0, 0.5]
        f = utils.construct_filter('SHLH', indices, thickness)
        self.assertEqual(f.substrate, 1.51)
        self.assertEqual(f.layers[0].n, 2.0)
        self.assertEqual(f.layers[0].nt, 0.625)


    def test_units_conversion(self):
        nm = 500
        values = {
            'angstrom': nm * 10,
            'nm': nm,
            'micron': nm / 10**3,
        }
        for units in values.keys():
            self.assertEqual(utils.rescale(nm, units), values[units])

    def test_units_unknown(self):
        with self.assertRaises(ValueError):
            utils.rescale(500, 'unknown')


if __name__ == '__main__':
    unittest.main()
