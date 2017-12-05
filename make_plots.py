"""
Plotting script for the outputs of the simulations.

Author: Josh Borrow
Date created: 5th December 2017
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import numpy as np

import h5py


plt.rcParams["image.cmap"] = "cool"


class Grid(object):
    """
    Grid object that contains various axes, and the figure object.
    """
    def __init__(self, figargs=None):
        if figargs is not None:
            self.figure = plt.figure(**figargs)
        else:
            self.figure = plt.figure()

        self.grid = gs.GridSpec(5, 3)
        self.get_axes(self.figure, self.grid)

        return None


    def get_axes(self, figure, grid):
        """
        Get the axes from the grid and set them as attributes.
        """
        self.particle_ax = figure.add_subplot(grid[0, :])
        self.pressure_ax = figure.add_subplot(grid[1:, 0])
        self.density_ax = figure.add_subplot(grid[1:, 1])
        self.hsml_ax = figure.add_subplot(grid[1:3, 2])
        self.info_ax = figure.add_subplot(grid[3:, 2])

        return None


class Data(object):
    """
    Data object that loads in the hdf5 data and sets it as attributes.
    """
    def __init__(self, file="output_0001.hdf5"):
        self.filename = file
        self.handle = h5py.File(self.filename, "r")

        self.get_positions(self.handle)
        self.get_energies(self.handle)
        self.get_pressures(self.handle)
        self.get_densities(self.handle)
        self.get_hsmls(self.handle)
        self.get_info(self.handle)

        self.handle.close()

        return None
   

    def get_positions(self, handle):
        """
        Get the x-positions of the particles.
        """
        coordinates = handle["PartType0"]["Coordinates"][:, 0]
        self.positions = coordinates[...]

        return self.positions


    def get_energies(self, handle):
        """
        Get the internal energies of the particles.
        """
        energies = handle["PartType0"]["InternalEnergy"][:]
        self.energies = energies[...]

        return self.energies


    def get_pressures(self, handle):
        """
        Get the pressures of the particles.
        """
        pressures = handle["PartType0"]["Pressure"][:]
        self.pressures = pressures[...]

        return self.pressures
    
    
    def get_densities(self, handle):
        """
        Get the densities of the particles.
        """
        densities = handle["PartType0"]["Density"][:]
        self.densities = densities[...]

        return self.densities


    def get_hsmls(self, handle):
        """
        Get the smoothing lenghts of the particles.
        """
        hsmls = handle["PartType0"]["SmoothingLength"][:]
        self.hsmls = hsmls

        return self.hsmls


    def get_info(self, handle):
        """
        Get the code information from the file handle.
        """
        header = handle['Header']
        code = handle['Code']
        hydro = handle['HydroScheme']

        self.info = {
            "header" : dict(header.attrs),
            "code" : dict(code.attrs),
            "hydro" : dict(hydro.attrs)
        }

        return self.info


class Plotter(object):
    """
    Plotting class. Opens the data file, extracts the data using the Data
    class and then plots it on the Grid class.
    """
    def __init__(self, filename="output_0001.hdf5", limits=[45, 60], save=True, tl=True):
        self.filename = filename
        self.limits = limits

        self.grid = Grid()
        self.data = Data(filename)


        self.plot_positions()
        self.plot_density()
        self.plot_pressure()
        self.plot_hsml()


        if tl:
            self.grid.grid.tight_layout(self.grid.figure)

        if save:
            self.grid.figure.savefig(f"{filename[:-4]}png", dpi=300)

        return

   
    def set_plot_limits(self, ax):
        """
        Sets the x-limits to limits and names the x axis "$x$ position".
        """
        ax.set_xlim(*self.limits)
        ax.set_xlabel("$x$ position")

        return None


    def plot_positions(self):
        """
        Make the plot of positions, this essentially just shows the spacing
        between the particles.
        """

        self.grid.particle_ax.scatter(
            self.data.positions,
            [0] * len(self.data.positions),
            c=self.data.energies,
            s=3
        )

        self.set_plot_limits(self.grid.particle_ax)
        self.grid.particle_ax.yaxis.set_visible(False)

        return None


    def plot_pressure(self):
        """
        Make the pressure(x) plot.
        """
        
        self.grid.pressure_ax.scatter(
            self.data.positions,
            self.data.pressures,
            c=self.data.energies,
            s=3
        )

        self.set_plot_limits(self.grid.pressure_ax)
        self.grid.pressure_ax.set_ylabel("Pressure")

        return None


    def plot_density(self):
        """
        Make the density(x) plot.
        """
        
        self.grid.density_ax.scatter(
            self.data.positions,
            self.data.densities,
            c=self.data.energies,
            s=3
        )

        self.set_plot_limits(self.grid.density_ax)
        self.grid.density_ax.set_ylabel("Density")

        return None


    def plot_hsml(self):
        """
        Make the hsml(x) plot.
        """
        
        self.grid.hsml_ax.scatter(
            self.data.positions,
            self.data.hsmls,
            c=self.data.energies,
            s=3
        )

        self.set_plot_limits(self.grid.hsml_ax)
        self.grid.hsml_ax.set_ylabel("Smoothing Length")

        return None


if __name__ == "__main__":
    import sys

    try:
        number = int(sys.argv[1])
    except:
        number = 1

    FILENAME = "output_{:04d}.hdf5".format(number)
    print(f"Reading {FILENAME}")

    PLOTTER = Plotter(FILENAME)

