# -*- coding: utf-8 -*-
"""
Created on Sat May  6 17:36:46 2023

@author: He
"""

import unittest
from my_modules.raster import Raster


class TestRaster(unittest.TestCase):

    def setUp(self):
        self.environment = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.raster = Raster(self.environment, 'test_raster')

    def test_init(self):
        self.assertEqual(self.raster.environment, self.environment)
        self.assertEqual(self.raster.name, 'test_raster')
        self.assertEqual(self.raster.rows, 3)
        self.assertEqual(self.raster.cols, 3)

    def test_multiply(self):
        expected_result = [
            [2, 4, 6],
            [8, 10, 12],
            [14, 16, 18]
        ]
        new_raster = self.raster.multiply(2)
        self.assertEqual(new_raster.environment, expected_result)
        self.assertEqual(new_raster.name, 'multiply')

    def test_normalize(self):
        self.raster.normalize()
        expected_result = [
            [0, 31, 63],
            [95, 127, 159],
            [191, 223, 255]
        ]
        self.assertEqual(self.raster.environment, expected_result)
        
    def test_add_rasters(self):
        raster1 = Raster([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ], 'raster1')

        raster2 = Raster([
            [9, 8, 7],
            [6, 5, 4],
            [3, 2, 1]
        ], 'raster2')

        expected_result = [
            [10, 10, 10],
            [10, 10, 10],
            [10, 10, 10]
        ]

        sum_raster = Raster.add_rasters([raster1, raster2])
        self.assertEqual(sum_raster.environment, expected_result)
        self.assertEqual(sum_raster.name, 'Site suitability')
    
        


if __name__ == '__main__':
    unittest.main()
