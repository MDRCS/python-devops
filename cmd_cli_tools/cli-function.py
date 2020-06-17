#!/usr/bin/env python
"""
Simple fire example """
import fire


def greet(greeting='Hiya', name='Tammy'):
    print(f"{greeting} {name}")


if __name__ == '__main__':
    fire.Fire(greet)
