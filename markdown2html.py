#!/usr/bin/python3
"""This module defines a scrip that takes an argument 2 strings"""


if __name__ == "__main__":
    from sys import argv, stderr
    from os.path import exists

    filename = "README.md"

    if len(argv) <= 2:
        stderr.write("Usage: ./markdown2html.py README.md README.html \n")
        exit(1)

    if not exists(filename):
        print("Missing {}".format(filename), file=stderr)
        exit(1)
    else:
        exit(0)
