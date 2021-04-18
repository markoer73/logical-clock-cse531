# ASU CSE531 Second Assignment
Logical Clock project for the ASU CSE531 assignment of 2021.

The goal of this project is to build a distributed banking system that implements Lamport's logical clock algorithm, building on the project 1: gRPC.

This is an assignment from Arizona State University (ASU), April 2021.


![ASU Ira A. Fulton Schools of Engineering](images/112785808-29a17880-9055-11eb-8014-d637183ab0a0.png)

# How to run the project?

The project has been developed and tested on Ubuntu 20.04.2 LTS and Python 3.8.  It may work with other Python and Linux versions, but they have not been tested for this assignment. The operative system was a freshly installed VM running on VMware Workstation 16.1.0.

First of all, checkout the whole project from the "Master" Branch.  This can be done through git, or simply by downloading the project as a ZIP file. If you downloaded the ZIP, be sure you expand it into a directory of choice.

The directory of the project should be called "logical-clock".  There are three possible ways to execute the program:

1. <b>Linux command line - text file only.</b>  Change to the directory "logical-clock" and execute ./run_exercise.sh - this should setup the virtualenv, reference the libraries already included in the  and install all eventually missing libraries.  It may fail if virtualenv is not installed in the system and the current users does not have permissions to install it on the local directory.

2. <b>Linux command line - using your Window Manager to display graphical windows.</b>  Change to the directory "logical-clock" and execute ./run_exercise.sh - this should setup the virtualenv, reference the libraries already included in the  and install all eventually missing libraries.  It may fail if virtualenv is not installed in the system and the current users does not have permissions to install it.

3. <b>Using Microsoft Visual Studio.</b>  In this case, change to the same directory "logical-clock" and execute "code".  If you have Visual Studio installed, it should bring up the current environment and configuration.

## Advanced Uses of the Software

- If you open the batch file "run_exercise.sh" you may notice that there are several possible ways to execute the software - they are all commented out and only the default execution if uncommented.
It is possible to execute the previous assignment (gRPC) and the third assignment will also be executed in the same way.

- There are command-line switches that can be used to change the behaviour of the software.  They are reported below:

<i>-i / --Input   <input_file.json></i>     input file to process, in JSON format

<i>-o / --Output  <output_file.json></i>    output file for the customers (client), in JSON format

<i>-c / --Clock   <clock_file.json></i>     output file for the branches (servers), in JSON format.  When this is used, the software enables the Lampard's clock logic.  If absent, the clock logic is disabled (branches stay with local clock = 0).

<i>-w / --Windows <True|False></i>    Enables or disables usage of graphical windows and user interactivity.

<i>-p / --Pretty  <True|False></i>    Enables or disables pretty-printing of JSON output files.


## Important Notes

- Mode number 1 is the default, and it is the one intended to execure the application.  Using mode number 2 is useful for debugging and to obtain a graphical and user-interactiive representation of the application; however, since it relies on user input to execute the events, it "goes easier" on the branch/server objects and basically reduced the possibility of multiprocessing conflicts, which are one of the issue we want to test on distributed systems. The best way to test the software as it is intended, is not to run it interactively but automatically, which is what mode 1 performs.

- This software is backward compatible and can also execute the assignment from project 1 - it is only a matter of changing a command line argument passed to the Python Main procedure.