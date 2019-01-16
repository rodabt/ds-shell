# ds-shell (Data Science Shell)

Since I'm a forgetful person who sometimes jumps straight into code I've built a helper terminal system which logs every activity related to Data Science tasks in the terminal, such as:

* Calling Bash functions: sed, awg, cat, head, and so on
* Launching python, R, or sqlite (with or without arguments)
* Using file functions: cp, mv

Every command is recorded to an sqlite database inside a directory called `__EXPERIMENT__` which is created on the first run along a configuration file in YAML called project.yml

This is a **WIP**

## Basic Usage

Call `python main.py` inside a working directory you wish to log commands in, and use it as a regular Bash terminal replacement

## TODO

- [ ] Update project.yml with a list of recognized commands you wish logged
- [ ] Refactor the code according to best practices
- [ ] Create a setup file and upload to PyPy
