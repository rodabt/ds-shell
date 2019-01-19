# dsshell (Data Science Shell)

Since I'm a forgetful person who sometimes jumps straight into code I've built a helper terminal system which logs every activity related to Data Science tasks in the terminal, such as:

* Calling file manipulation functions: sed, awk, cat, head, cp, mv and so on
* Launching interactive shells: python, R, or sqlite (with or without arguments)
* Editing code
* Idle time

Every command is recorded to an sqlite database inside a directory called `__EXPERIMENT__` which is created on the first run along a configuration file in YAML called project.yml

This is a **WIP**. Very experimental.

## Basic Usage

Call `python main.py` inside a working directory you wish to log commands in, and use it as a regular Bash terminal replacement

## TODO

- [ ] Refactor the code according to best practices (PEP8, etc.)
- [ ] Log command after execution to track its duration
- [ ] Create usage statistics (time spent on file manipulation, calling scripts, etc)
- [ ] Update project.yml with a list of recognized commands you wish to be logged
- [ ] Create a setup file and upload to PyPy

