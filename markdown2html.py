#!/usr/bin/python3
"""This module defines a scrip that takes an argument 2 strings"""


if __name__ == "__main__":
    from sys import argv, stderr
    from os.path import exists

    markdownFile = "README.md"
    htmlFile = "README.html"

    if len(argv) <= 2:
        stderr.write("Usage: ./markdown2html.py README.md README.html \n")
        exit(1)

    if not exists(markdownFile):
        print("Missing {}".format(markdownFile), file=stderr)
        exit(1)

    with open(markdownFile, 'r',encoding='utf-8') as markdown:
        with open(htmlFile, 'w', encoding='utf-8') as html:
            count = 1
            for line in markdown:
                heading = line.strip().count('#')
                title = line.lstrip('# ').rstrip("\n")
                html.write("<h{}>{}</h{}>\n".format(heading, title, heading))
                count += 1
    exit(0)
