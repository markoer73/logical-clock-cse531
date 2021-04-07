# ASU CSE531 Second Assignment
Logical Clock project for the ASU CSE531 assignment of 2021.

The goal of this project is to build a distributed banking system that implements Lamport's logical clock algorithm, building on the project 1: gRPC.

This is an assignment from Arizona State University (ASU), March 2021.


![ASU Ira A. Fulton Schools of Engineering](images/112785808-29a17880-9055-11eb-8014-d637183ab0a0.png)

# How to run the project?

The project has been developed and tested on Ubuntu 20.04.2 LTS and Python 3.8.  It may work with other Python and Linux versions, but they have not been tested for this assignment. The operative system was a freshly installed VM running on VMware Workstation 16.1.0.

First of all, checkout the whole project from the "Main" Branch.  Then, there are two possible ways to proceed:

1. Linux command line.  Change to the directory "logical-clock" and execute ./run_exercise.sh - this should setup the virtualenv, reference the libraries already included in the  and install all eventually missing libraries.  It may fail if virtualenv is not installed in the system and the current users does not have permissions to install it.

2. Use Microsoft Visual Studio.  In this case, change to the same directory "logical-clock" and execute "code".  If you have Visual Studio installed, it should bring up the current environment and configuration.
