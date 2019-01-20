#!/usr/bin/env python

######################################################
#
# dsshell - Data Science Shell
# by Rodrigo Abt <rodrigo.abt@gmail.com>
#
######################################################

import subprocess
# import re
import os
from colorama import Fore, init
from datetime import datetime
import sqlite3
import uuid
import oyaml as yaml
import click
import shutil
import sys
import pendulum
from tabulate import tabulate
from glob import glob

init(autoreset=True)

# On Win 10 use pyreadline instead
try:
    import readline
except ImportError:
    import pyreadline as readline

EXPERIMENT_DIR = os.path.join(os.getcwd(), '__EXPERIMENT__')
LOG_FILEPATH = os.path.join(EXPERIMENT_DIR, 'log.db')
PROJECT_FILEPATH = os.path.join(EXPERIMENT_DIR, 'project.yml')
PROMPT_HEADER = '[ds-shell:{}]$ '
DS_COMMANDS = ['python', 'R', 'sed', 'grep', 'awk', 'sqlite3', 'nano']


def completer(text, state):
    """Gets all files and directories starting with pattern 'text'"""
    listing = glob('*')
    options = [i for i in listing if i.startswith(text)]
    return options[state] if state < len(options) else None


def log_command(command, start, end):
    """Logs allowed commands in __EXPERIMENT__/log.db"""
    elapsed = end - start
    conn = sqlite3.connect(LOG_FILEPATH)
    # today = datetime.today().strftime('%Y-%m-%d %H:%M')
    sql = 'INSERT INTO experiments (command, start, end, elapsed) \
            VALUES (?,?,?,?)'

    c = conn.cursor()
    c.execute(sql, [
        repr(command),
        start.to_datetime_string(),
        end.to_datetime_string(), elapsed.seconds
    ])
    conn.commit()
    conn.close()


def get_current_prompt(current_dir):
    """Returns colorized prompt according to current_dir"""
    return Fore.GREEN + PROMPT_HEADER.format(current_dir) + Fore.WHITE


def get_current_input(prompt):
    """Retrieves current line from input"""
    original_stdout = sys.stdout
    sys.stdout = sys.__stdout__
    current_input = input(prompt)
    sys.stdout = original_stdout
    return current_input


def parse_line(line):
    """Returns a list of tuples with allowed commands and their arguments"""
    command_group = line.split(" ", maxsplit=1)
    return [(command_group[0],
             '')] if len(command_group) == 1 else [tuple(command_group)]


def process_command(command_tuple):
    command, arguments = command_tuple
    if command == 'cd':
        if arguments:
            try:
                os.chdir(arguments)
            except Exception as e:
                print(e)
        else:
            os.chdir(os.path.expanduser('~'))
    elif command in DS_COMMANDS:
        start = pendulum.now()
        print(Fore.RED + '(DS-LOG: Used {})'.format(command) + Fore.WHITE)
        if 'arguments' not in locals():
            cmd = subprocess.Popen([command], shell=True)
        else:
            cmd = subprocess.Popen(" ".join([command, arguments]), shell=True)
        cmd.wait()
        end = pendulum.now()
        log_command(command, start, end)
    else:
        try:
            cmd = subprocess.Popen(
                " ".join([command, arguments]), stdout=subprocess.PIPE)
            cmd_out = cmd.communicate()[0]
            print(Fore.WHITE + cmd_out.decode("utf-8").strip('\x00')
                  .replace('\\n', '\n'))
        except Exception as e:
            print(e)
    return os.getcwd()


def run_shell():
    while True:
        if 'cwd' not in locals():
            cwd = os.getcwd()

        current_prompt = get_current_prompt(cwd)
        current_line = get_current_input(current_prompt)
        full_command = current_line.strip().lower()
        list_commands = parse_line(current_line)

        if full_command == 'exit':
            break

        if full_command == '':
            continue

        if full_command.startswith('dls'):
            if '-' in full_command:
                _, args = full_command.split("-", maxsplit=1)
            else:
                args = 'plain'
            show_history(args)
            continue

        for command_tuple in list_commands:
            cwd = process_command(command_tuple)


def check_project(name):
    if not os.path.exists(EXPERIMENT_DIR):
        os.mkdir(EXPERIMENT_DIR)
        try:
            name = input('Project name: ')
        except SyntaxError:
            name = None

        if not name:
            name = 'Unnamed project'
        today = datetime.today().strftime('%Y-%m-%d %H:%M')
        project_data = dict(
            uuid=str(uuid.uuid1()),
            project_name=name,
            description='(none)',
            creation_date=today,
        )

        with open(PROJECT_FILEPATH, 'w') as outfile:
            yaml.dump(project_data, outfile, default_flow_style=False)

        conn = sqlite3.connect(LOG_FILEPATH)
        sql = """
        CREATE TABLE IF NOT EXISTS experiments (
        command text,
        start date,
        end date,
        elapsed decimal
        )
        """
        conn.execute(sql)
        conn.close()


def show_history(fmt='plain'):
    conn = sqlite3.connect(LOG_FILEPATH)
    sql = 'SELECT * FROM experiments'
    c = conn.cursor()
    c.execute(sql)
    print(
        tabulate(
            c.fetchall(),
            headers=['Command', 'Start', 'End', 'Elapsed'],
            tablefmt=fmt))
    conn.close()


# Command line subcommands
@click.group()
def cli():
    pass


@click.command()
@click.option('--name', default='Unnamed Project')
def run(name):
    """Runs Data Science Shell from current directory"""
    check_project(name)
    run_shell()


@click.command()
def clean():
    """Deletes __EXPERIMENT__ directory recursively"""
    try:
        shutil.rmtree(EXPERIMENT_DIR)
    except Exception:
        pass


@click.command()
def ls():
    """Show all logged commands in current session"""
    show_history()


readline.parse_and_bind("tab: complete")
readline.set_completer(completer)
cli.add_command(run)
cli.add_command(clean)
cli.add_command(ls)

if __name__ == '__main__':
    cli()
