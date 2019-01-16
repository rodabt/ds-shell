import subprocess
import re
import os
from colorama import Fore, init
from datetime import datetime
import sqlite3
import uuid
import oyaml as yaml
import click
import shutil
import sys
from glob import glob

init(autoreset=True)


try:
    import readline
except ImportError:
    import pyreadline as readline


def completer(text, state):
    listing = glob('*')
    options = [i for i in listing if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None


readline.parse_and_bind("tab: complete")
readline.set_completer(completer)


# Global settings
EXPERIMENT_DIR = os.path.join(os.getcwd(), '__EXPERIMENT__')
LOG_FILEPATH = os.path.join(EXPERIMENT_DIR, 'log.db')
PROJECT_FILEPATH = os.path.join(EXPERIMENT_DIR, 'project.yml')


def run_shell():
    while True:
        CWD = os.getcwd()
        PROMPT = Fore.GREEN + '[ds-shell:{}]$ '.format(CWD) + Fore.WHITE

        original_stdout = sys.stdout
        sys.stdout = sys.__stdout__
        s = input(PROMPT)
        sys.stdout = original_stdout

        if ' ' in s:
            c, args = s.split(' ', maxsplit=1)
        else:
            c = s

        if c == 'exit':
            break
        if c == '':
            continue

        if c in ['python', 'R', 'sed', 'grep', 'awk', 'sqlite3']:
            print(Fore.RED + '(DS-LOG: Used {})'.format(c) + Fore.WHITE)

        if c == 'cd':
            if args:
                try:
                    os.chdir(args)
                    CWD = os.getcwd()
                except Exception as e:
                    print(e)
            else:
                os.chdir(os.path.expanduser('~'))
                CWD = os.getcwd()
            continue

        if c in ['python', 'R', 'ipython', 'nano', 'sqlite3']:
            if 'args' not in locals():
                args = ''
            cmd = subprocess.Popen([c, args], shell=True)
            cmd.wait()

        else:
            try:
                cmd = subprocess.Popen(re.split(r'\s+', s),
                                       stdout=subprocess.PIPE)
                cmd_out = cmd.communicate()[0]
                print(Fore.WHITE + cmd_out.decode("utf-8").strip('\x00')
                      .replace('\\n', '\n'))
            except Exception as e:
                print(e)
            if 'args' in locals():
                del(args)


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
        uuid text,
        parameters text,
        exp_date date
        )
        """
        conn.execute(sql)
        conn.close()


@click.command()
@click.option('--name', default='Unnamed Project')
def cli_setup_project(name):
    check_project(name)
    run_shell()


def cli_clean_project():
    """Deletes recursively all experiment's files and dirs"""
    try:
        shutil.rmtree(EXPERIMENT_DIR)
    except Exception as e:
        pass


if __name__ == '__main__':
    cli_setup_project()
