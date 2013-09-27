# coding: utf-8

import unittest

from pycoat.core import Filter, Layer
from pycoat.hln import load


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


if __name__ == '__main__':
    unittest.main()
