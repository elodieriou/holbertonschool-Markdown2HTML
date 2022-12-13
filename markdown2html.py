#!/usr/bin/python3
"""This module defines a scrip that takes an argument 2 strings"""
from sys import argv, stderr
from os.path import exists
from hashlib import md5
import re

if __name__ == "__main__":

    markdownFile = "README.md"
    htmlFile = "README.html"

    if len(argv) <= 2:
        stderr.write("Usage: ./markdown2html.py README.md README.html \n")
        exit(1)

    if not exists(markdownFile):
        print("Missing {}".format(markdownFile), file=stderr)
        exit(1)

    with open(markdownFile, 'r', encoding='utf-8') as markdown:
        with open(htmlFile, 'w', encoding='utf-8') as html:

            isUnorderedOpen, isOrderedOpen = False, False
            numberUnorderedList, numberOrderedList,  = 0, 0
            numberHeading, numberParagraph = 0, 0

            index = markdown.readlines()
            count = 0

            for line in index:
                count += 1

                # Parsing bold and emphasis text
                line = line.replace("**", "<b>", 1)
                line = line.replace("**", "</b>", 1)
                line = line.replace("__", "<em>", 1)
                line = line.replace("__", "</em>", 1)

                # Converting in MD5
                findRegex = re.findall(r'\[\[.+?\]\]', line)
                if findRegex:
                    line = line.replace(findRegex[0], md5(findRegex[0].encode()).hexdigest())

                # Removing '(', ')' 'C', 'c'
                findRegex2 = re.findall(r'\(\(.+?\)\)', line)
                if findRegex2:
                    line = line.translate({ord(i): None for i in '()Cc'})

                header = line.strip().count('#')
                unordered = line.strip().count('-')
                ordered = line.strip().count('*')

                # Translate Headings Markdown
                if header > 0:
                    if numberUnorderedList > 0 and numberHeading == 0:
                        html.write("</ul>\n")
                        numberUnorderedList = 0
                    if numberOrderedList > 0 and numberHeading == 0:
                        html.write("</ol>\n")
                        numberOrderedList = 0
                    if numberParagraph > 0 and numberHeading == 0:
                        html.write("</p>\n")
                        numberParagraph = 0
                    title = line.lstrip('# ').rstrip("\n")
                    html.write("<h{}>{}</h{}>\n".format(header, title, header))
                    numberHeading += 1

                # Translate Unordered List Markdown
                if unordered == 1:
                    if numberOrderedList > 0 and numberUnorderedList == 0:
                        html.write("</ol>\n")
                        numberOrderedList = 0
                    if numberParagraph > 0 and numberUnorderedList == 0:
                        html.write("</p>\n")
                        numberParagraph = 0
                    title = line.lstrip('- ').rstrip("\n")
                    if not isUnorderedOpen:
                        html.write("<ul>\n")
                        isUnorderedOpen = True
                    html.write("\t<li>{}</li>\n".format(title))
                    numberUnorderedList += 1
                    if count == len(index) and numberUnorderedList > 0:
                        html.write("</ul>\n")

                # Translate Ordered List Markdown
                if ordered == 1:
                    if numberUnorderedList > 0 and numberOrderedList == 0:
                        html.write("</ul>\n")
                        numberUnorderedList = 0
                    if numberParagraph > 0 and numberOrderedList == 0:
                        html.write("</p>\n")
                        numberParagraph = 0
                    title = line.lstrip('* ').rstrip("\n")
                    if not isOrderedOpen:
                        html.write("<ol>\n")
                        isOrderedOpen = True
                    html.write("\t<li>{}</li>\n".format(title))
                    numberOrderedList += 1
                    if count == len(index) and numberOrderedList > 0:
                        html.write("</ol>\n")

                # Translate Paragraph Markdown
                if header == 0 and unordered == 0 and ordered == 0:
                    numberParagraph += 1
                    if index[count - 1] == "\n":
                        html.write("</p>\n")
                        numberParagraph = 0
                    elif numberParagraph > 1:
                        html.write("<br/>{}".format(line.rstrip("\n")))
                    else:
                        html.write("<p>{}".format(line.rstrip("\n")))
                    if count == len(index):
                        html.write("</p>\n")
    exit(0)
