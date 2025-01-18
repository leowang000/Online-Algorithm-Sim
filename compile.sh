#!/bin/bash

# Shell script to compile the required .so files for the python code

cd src 
python3 setup.py build_ext --inplace 
cd scheduler
python3 setup.py build_ext --inplace 