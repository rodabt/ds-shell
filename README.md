# dsshell (Data Science Shell)

Since I'm a forgetful person who sometimes jumps straight into code I've built a helper terminal system which logs every activity related to Data Science tasks in the terminal, such as:

* Calling file manipulation functions: sed, awk, cat, head, cp, mv and so on
* Launching interactive shells: python, R, or sqlite (with or without arguments)
* Editing code
* Idle time

Every command is recorded to an sqlite database inside a directory called `__EXPERIMENT__` which is created on the first run along a configuration file in YAML called project.yml

This is a **WIP**. Very experimental.

## Basic Usage

```
Usage: main.py [OPTIONS] COMMAND [ARGS]...            
                                                      
Options:                                              
  --help  Show this message and exit.                 
                                                      
Commands:                                             
  clean  Deletes __EXPERIMENT__ directory recursively 
  ls     Show all logged commands in current session  
  run    Runs Data Science Shell from current directory
```

## TODO

- [x] Refactor the code according to best practices (PEP8, etc.)
- [x] Log command after execution to track its duration
- [ ] Create usage statistics (time spent on file manipulation, calling scripts, etc)
- [ ] Update project.yml with a list of recognized commands you wish to be logged
- [ ] Create a setup file and upload to PyPy

