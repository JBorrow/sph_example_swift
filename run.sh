#! /bin/sh

# Generate Initial Conditions
python3 generate_ics.py

# The first run with GADGET
cd swiftsim
./autogen.sh

make clean
./configure --with-hydro-dimension=1 --disable-compiler-warnings
make -j 2

cd ..
mkdir output
cd output

mkdir gadget
cd gadget
../../swiftsim/examples/swift -s ../../parameter_file.yml

# Now do P-E
cd ../../swiftsim
make clean
./configure --with-hydro-dimension=1 --disable-compiler-warnings --with-hydro=hopkins
make -j 2

cd ../output
mkdir pressure_entropy
cd pressure_entropy
../../swiftsim/examples/swift -s ../../parameter_file.yml

