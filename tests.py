# coding: utf-8

import unittest

from pycoat.core import Filter, Layer


class TestCore(unittest.TestCase):
    def test_filter_thickness(self):
        f = Filter(1.52, [Layer(1.35, 1), Layer(1.6, 1)])

        self.assertAlmostEqual(f.optical_thickness(500), 250)
        self.assertAlmostEqual(f.optical_thickness(500, 'micron'), 0.25)

        self.assertAlmostEqual(f.physical_thickness(500), 170.7175, 3)
        self.assertAlmostEqual(f.physical_thickness(500, 'micron'), 0.1707, 3)


if __name__ == '__main__':
    unittest.main()
