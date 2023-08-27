"""
This file is needed because C3 has execution time too big.
It contains the same configuration of C3, but it run different cases
"""

import numpy as np
from condition_C3 import modify_image as modify_image_C3


label      = 'C3'

cases = dict()
for n in range(20,39) :
    cases[f'shift{n}'] = n


def modify_image ( *args ) :
    return modify_image_C3 ( *args )
