"""
Initial conditions generation script for the 1D test shock problem.

Author: Josh Borrow
Date created: 5th December 2017
"""

import write_gadget as wg
import numpy as np


def gen_positions(sep_left=0.1, sep_right=1.0, delta=0.0, nparts=1000):
    """
    Generate the positions for the particles.
    """
    positions = np.empty(nparts)

    start_left = 0.
    end_left = start_left + (nparts/2) * sep_left
    positions_left = np.arange(start_left, end_left, sep_left)

    start_right = end_left + sep_right + delta - sep_left
    end_right = start_right + (nparts/2) * sep_right
    positions_right = np.arange(start_right, end_right, sep_right)

    positions[:int(nparts/2)] = positions_left
    positions[int(nparts/2):] = positions_right

    return positions

