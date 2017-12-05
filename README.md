SPH Tests in 1D
===============

A quick example of an SPH test in 1D. We use `swift` as a submodule to
actually run our test problems rather than  having to concern ourselves with
writing our own (slower) SPH code.

To run this, do the following:

+ Ensure the `swiftsim` submodule is loaded/cloned
+ `./run.sh` and wait.

`run.sh` sets all of the correct configuration parameters for SWIFT, generates
the initial conditions, makes and runs SWIFT, and then creates plots that it
saves in `./plots`. At the moment the plots are a bit 'rough and ready', but
seeing as the purpose of this is to test the convergence between PE and TSPH,
here are the plots from the initial conditions:

### GADGET ICs
![Gadget Initial Conditions Plot](static/gadget_0000.png)
### Pressure Entropy ICs
![PE Initial Conditions Plot](static/pe_0000.png)

and after convergence:

### GADGET After Convergence
![Gadget Converged Plot](static/gadget_0100.png)
### Pressure Entropy After Convergence
![PE Converged Plot](static/pe_0100.png)
