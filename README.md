# Readme

Many of the files in this repository are original to https://github.com/sfujim/TD3 - the code from the original authors of TD3, the learning algorithm we utilize in our notebooks here; including the contained readme below.  To dive in to our own content, the ModifyingRL.ipynb notebook is a great place to start and can be seen as a more comprehensive readme for the things we're demonstrating here.

----------------

## Introduction
The exercises (notebooks) in this repo comprise a short course for data scientists and other practitioners covering the practical considerations needed to effectively apply reinforcement learning to real-world problems.  The course uses a simulation environment (Robot Ant) that simplifies some aspects of implementation but addresses real, Physics-based learning tasks.

See the [docs]() for more.

## Run the notebooks on your computer

If you want to run the notebooks in this course, be sure to pull the repo and set up the conda environment. 
1. Install conda.  We like to use [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. Pull this repo using your favorite method, such as

    `git clone git@github.com:Quansight/Practical-RL.git`

3. Go to the Practial-RL directory

    `cd Practial-RL`

4. Build the environment (see the [conda user guide](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html))

    `conda env create -f environment.yml`