"""
Initial conditions generation script for the 1D test shock problem.

Author: Josh Borrow
Date created: 5th December 2017
"""

import write_gadget as wg
import numpy as np

import h5py


def gen_positions(sep_left=0.1, sep_right=1.0, delta=0.0, nparts=1000):
    """
    Generate the positions for the particles.
    """
    # Ensure that an even number of particles has been selected
    if nparts % 2:
        raise AttributeError("Please use an even number of particles")

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


def gen_internal_energies(energy_left=1., energy_right=10., nparts=1000):
    """
    Generate the internal energies for the particles.
    """
    # Ensure that an even number of particles has been selected
    if nparts % 2:
        raise AttributeError("Please use an even number of particles")

    energies = np.empty(nparts)

    energies[:int(nparts/2)] = energy_left
    energies[int(nparts/2):] = energy_right

    return energies
    

def write_data(positions, energies, boxsize, hsml, filename="initial_conditions.hdf5"):
    with h5py.File(filename, "w") as f:
        wg.write_header(
            f,
            boxsize=boxsize,
            flag_entropy=0,
            np_total=[len(positions), 0, 0, 0, 0, 0],
            np_total_hw=[0]*6,
            other={"Dimension" : 1}
        )    

        wg.write_runtime_pars(
            f,
            periodic_boundary=1
        )

        wg.write_units(
            f,
            current=1.,
            length=1.,
            mass=1.,
            temperature=1.,
            time=1.,
        )

        wg.write_block(
            f,
            part_type=0,
            pos=np.array([positions, np.zeros_like(positions), np.zeros_like(positions)]).T,
            vel=np.zeros_like(positions),
            ids=np.arange(len(positions)),
            mass=np.ones_like(positions),
            int_energy=energies,
            smoothing=np.array(hsml),
        )

    return 0  # Living the UNIX life

if __name__ == "__main__":
    import yaml

    with open("config.yml", "r") as stream:
        configuration_options = yaml.load(stream)
        initial_conditions = configuration_options["initial_conditions"]

        N_PARTS = initial_conditions["nparts"]
        SEP_LEFT = initial_conditions["separations"]["left"]
        SEP_RIGHT = initial_conditions["separations"]["right"]
        DELTA = initial_conditions["delta"]
        ENERGY_LEFT = initial_conditions["energies"]["left"]
        ENERGY_RIGHT = initial_conditions["energies"]["right"]
        FILENAME = initial_conditions["filename"]

        BOXSIZE = (N_PARTS + 1) * (SEP_LEFT + SEP_RIGHT) / 2

    POSITIONS = gen_positions(SEP_LEFT, SEP_RIGHT, DELTA, N_PARTS) + SEP_LEFT / 2
    ENERGIES = gen_internal_energies(ENERGY_LEFT, ENERGY_RIGHT, N_PARTS)
    SMOOTHING = [SEP_LEFT] * int(N_PARTS / 2) + [SEP_RIGHT] * int(N_PARTS / 2)

    EXIT_CODE = write_data(POSITIONS, ENERGIES, BOXSIZE, SMOOTHING, FILENAME)

    exit(EXIT_CODE)

