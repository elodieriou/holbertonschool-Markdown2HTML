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

            unorderedList = False
            orderedList = False

            for line in markdown:
                heading = line.strip().count('#')
                unordered = line.strip().count('-')
                ordered = line.strip().count('*')

                if heading > 0:
                    title = line.lstrip('# ').rstrip("\n")
                    html.write("<h{}>{}</h{}>\n".format(heading, title, heading))

                if unordered == 1:
                    title = line.lstrip('- ').rstrip("\n")
                    if not unorderedList:
                        html.write("<ul>\n")
                        unorderedList = True
                    html.write("\t<li>{}</li>\n".format(title))

                if ordered == 1:
                    title = line.lstrip('* ').rstrip("\n")
                    if not orderedList:
                        html.write("<ol>\n")
                        orderedList = True
                    html.write("\t<li>{}</li>\n".format(title))

                if (heading or unordered or ordered) == 0:
                    html.write("<p>{}</p>\n".format(line.rstrip("\n")))
    exit(0)
