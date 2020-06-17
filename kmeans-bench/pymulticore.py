import click
import numba as numba
from scipy.sparse.linalg.eigen.arpack._arpack import timing
from flask import cli

@timing
@numba.jit(parallel=True)
def add_sum_threaded(rea):
    """Use all the cores"""
    x,_ = rea.shape
    total = 0
    for _ in numba.prange(x):
        total += rea.sum()
        print(total)

@timing
def add_sum(rea):
    """traditional for loop"""
    x,_ = rea.shape
    total = 0
    for _ in numba.prange(x):
        total += rea.sum()
        print(total)

@cli.command()
@click.option('--threads/--no-jit', default=False)
def thread_test(threads):
    rea = real_estate_array()
    if threads:
        click.echo(click.style('Running with multicore threads', fg='green'))
        add_sum_threaded(rea)
    else:
        click.echo(click.style('Running NO THREADS', fg='red'))
    add_sum(rea)


def real_estate_array():
    return "hello"
