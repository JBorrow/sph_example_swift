"""
Tests for the initial conditions generator.

Author: Josh Borrow
Date created: 5th December 2017
"""

import generate_ics as gi
import numpy as np


def test_positions():
    """
    Unit tests for the positions generator.
    """

    generated = gi.gen_positions(
        sep_left=0.1,
        sep_right=1.0,
        delta=0.0,
        nparts=2,
    )
    
    expected = np.array([0.0, 1.0])

    assert all(generated == expected)

    generated = gi.gen_positions(
        sep_left=0.1,
        sep_right=1.0,
        delta=0.0,
        nparts=4,
    )
    
    expected = np.array([0.0, 0.1, 1.1, 2.1])

    assert all(np.isclose(generated, expected, 0.01))


def test_internal_energies():
    """
    Unit tests for the internal energies generator.
    """

    generated = gi.gen_internal_energies(
        energy_left=1.,
        energy_right=10.,
        nparts=2,
    )

    expected = np.array([1., 10.])

    assert all(np.isclose(generated, expected, 0.01))

    generated = gi.gen_internal_energies(
        energy_left=1.,
        energy_right=10.,
        nparts=100,
    )

    expected = np.array([1.]*50 + [10.]*50)

    assert all(np.isclose(generated, expected, 0.01))

