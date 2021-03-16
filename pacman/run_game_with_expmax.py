import multiprocessing
import subprocess

from pathlib import Path
from time import time

from tabulate import tabulate

PACMAN_DIR = Path(__file__).parent / 'pacman'
Ghosts = ['DirectionalGhost', 'RandomGhost']


def main():
    results = multiprocessing.Pool().map(run, Ghosts)
    print(tabulate(results, headers=["Ghost type", "Win Rate", "Time", "Avg Score", "Scores"]))

# DirectionalGhost, RandomGhost


def run(ghost_type):
    time_start = time()

    output = subprocess.run(
        f'python {PACMAN_DIR}/pacman.py -p ExpectimaxAgent -g {ghost_type} -a depth=3 -n 30 -q --timeout 5 -c',
        cwd=PACMAN_DIR, stdout=subprocess.PIPE, shell=True).stdout.splitlines()

    time_delta = time() - time_start
    avg_score = output[-4].decode("utf-8").split("', ")[-1].replace(")", '').strip()
    scores = output[-3].decode("utf-8").split("', '")[-1].replace("')", '').strip()
    win_rate = output[-2].decode("utf-8").split(": ")[-1].strip()
    return ghost_type, win_rate, time_delta, avg_score, scores


if __name__ == '__main__':
    main()
